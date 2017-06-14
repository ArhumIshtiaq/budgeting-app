#!/usr/bin/python
# Accounting.py - A simple command line based budgeting software with the
# ability to have data saved for, virtually, inifite amount of users.
#
# TO-DO:
# 1. Convert data storage to CSV
# 2. Add interface with Tkinter
# 3. Convert data storage to SQL

import os
import time
import shelve


def main():
    printGreeting()
    global appData
    name, password = getNameAndPass()
    user, appData = checkOrCreateData(name, password)

    printWait("Your current balance is Rs." + str(appData['total']))

    while True:
        cc, main, cclen = getCommand()

        if (main == "deposit"):
            user.deposit(int(cc[1]))
        elif (main == "withdraw"):
            user.withdraw(int(cc[1]))
        elif (cclen == 2):
            funcName(main, askAmount())
        elif (cclen == 3):
            try:
                amount = int(cc[2])
                funcName(main, amount)
            except:
                funcName(main, askAmount())
        elif (main == "summary"):
            printWait("Fetching summary...")
            progresBar()
            printTable(createTable())
        elif (main == "exit" or main == "quit"):
            if (confirm("Are you sure? ") == True):
                printWait("\nThank you for using this budgeting software. See you next time, " + name[0].upper() + name[1:] + ". Bye!")
                lastUser = name
                time.sleep(1)
                appData.close()
                quit()
        else:
            printWait("Sorry, I don't understand this command. Please try again.")


# Asking for name and password to check against database
def getNameAndPass():
    name = input('Hi! What is your name?\nName:  ').lower()
    password = input(
        '\nHi ' + name[0].upper() + name[1:] + "! May I have you password as well?\nPassword:  ")
    return name, password


def checkOrCreateData(name, password):
    # Create shelve object while keeping nomenclature to the 
    # specific user for easier access
    appData = shelve.open(('fad' + name))

    printWait("\nInitializing your account...")
    printWait("Retrieving any previous data, if any...")

    # Checking username against existing shelve data
    if (name in appData):
        progresBar(endText = "Data found. Checking password...")

        # If username exists, then check password against user-defined existing
        # shelve data
        while (password != appData['password']):
            password = str(input("Wrong password. Try again!\nPassword: "))

        printWait("Password is correct! Logging in...")
        progresBar(endText = "Success!")

        # Save the specific shelve object to a variable for permanent data
        # accessibility for the user session
        user = appData[name]

    else:
        progresBar(endText = "No previous record found.")

        if (confirm("\nWould you like to create a new account?") == True):

            # Creating new user object using data provided by user at script
            # initialization
            user = Budget(name, password)

            # Saving customized class object to shelve object
            appData[user.user_name] = user

            printWait("Creating account...")
            progresBar(endText = "Account created.")

        else:
            printWait("I will not create an account. Exiting program...")

            # Deleting data that this script may have unintentionally created while
            # checking for username against shelve data
            try:
                os.unlink(os.path.abspath(os.curdir) + r"\fad" + name + ".dat")
                os.unlink(os.path.abspath(os.curdir) + r"\fad" + name + ".dir")
                os.unlink(os.path.abspath(os.curdir) + r"\fad" + name + ".bak")
            except FileNotFoundError:
                pass

            quit()

    return user, appData


#A greeting to be printed at every initialization of the program
def printGreeting(width = 80):
    print("*"*width)
    print("\n\n" + "Welcome to Arhum's Python Budgeting Script!".center(width) + "\n\n")
    print("*"*width)


# Getting action to commit from user
def getCommand():
    command = str(input("\nWhat else would you like to do?\nCommand: ")).lower()
    cc = command.split(' ')
    main = cc[0]
    cclen = len(cc)

    return cc, main, cclen


#A visual representation of progress to help provide a better UX
def progresBar(marker = "#", length = 15, endText = "Done!"):
    bar = "[]"
    progress = ""

    for i in range(length):
        progress += marker
        print(bar[0] + progress + " "*(length-1-i) + bar[1], flush = True, end= "\r")
        time.sleep(0.1)

    printWait(endText.center(length+2), end = "\n", flush = True)



# Name of the user specified action (when cclen > 1)
def funcName(main, amount):
    if (main == "create"):
        user.create(cc[1], amount)
    elif (main == "add"):
        user.add(cc[1], amount)
    elif (main == "remove"):
        user.remove(cc[1], amount)


#Asks for user to define amount, if not already done
def askAmount():
    amount = input("Amount?")

    while int(amount) <= 0 and amount.isnum():
        amount = int(
            input("Sorry, please enter an integer value greater than 0."))
    return int(amount)


# A prompt-and-wait function to reduce repetition of same lines of code
def printWait(string, timer = 0.8, flush = True, end = "\n"):
    print(string, flush = flush, end = end)
    time.sleep(timer)


# Function to double-check user selection
def confirm(string):
    ans = input(string + "(y/n)\n").lower()

    if (ans == "y"):
        return True
    elif (ans == "n"):
        return False


# Createing table data to pass through printTable()
def createTable():
    tp = [["TOTAL", ":", str(appData['total'])]]
    types = appData['types'].split('/')

    # Loop for creating a data stucture (list of lists) to provide
    # printTable() fucntion with an argument
    for i in types:
        ts = []
        ts.append(i.upper())
        ts.append(":")
        ts.append(str(appData[i]))
        tp.append(ts)

    return list(zip(*tp))


# Function to prompt the user data in a presentable format
def printTable(table):
    colWidths = [0] * len(table)
    mainListLen = len(table)
    listOfListLen = len(table[0])

    for i in range(mainListLen):
        for x in table[i]:
            if (colWidths[i] < len(x)):
                colWidths[i] = len(x)

    for i in range(listOfListLen):
        for x in range(mainListLen):
            print(table[x][i].rjust(colWidths[x]), end=" ")
        print()


class Budget():

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
        self.types = []
        appData['user_name'] = user_name
        appData['password'] = password
        appData['total'] = 0

        """
        The following line of code is a workaround of the fact that shelve objects can not store dictionaries.
        I have programmed it so that all the types will be in a single string, seperated by the fron-slash(/).
        When the need arises, this program will split the string and use the resulting data accordingly.
        """

        appData['types'] = "/".join(self.types)


    def deposit(self, amount):
        if amount > 0:
            appData['total'] += amount
            print("Depositing...")
            progresBar(endText = "Deposit Succesful!")
            printWait("Your total balance now is Rs." + str(appData['total']))


    def withdraw(self, amount):
        if (amount > appData['total']):
            print("Sorry, you do not have enough money!")

        else:
            appData['total'] -= amount
            print("Withdrawing...")
            progresBar(endText = "Withdrawal Succesful!")
            printWait("Your total balance now is Rs." + str(appData['total']))


    def create(self, name, amount):
        types = appData['types'].split('/')
        types.append(name)
        appData['types'] = "/".join(types)

        if (amount > appData['total']):
            print("Sorry, you do not have enough money to spend on this thing!")

        else:
            appData['total'] -= amount
            appData[name] = amount
            printWait("Your total balance now is Rs." + str(appData['total']))


    def add(self, type_, amount):
        appData['total'] -= amount

        if appData[type_] > 0:
            appData[type_] += amount

        else:
            appData[type_] = 0
            appData[type_] += amount

        printWait("Your total balance now is Rs." + str(appData['total']))


    def remove(self, type_, amount):
        if (amount > appData[type_]):
            print("Sorry, that's not possible!")

        elif (amount == appData[type_]):
            types.remove(type_)
            appData['types'] = "/".join(types)

        else:
            appData['total'] += amount
            appData[type_] -= amount
            print("Tranferring Rs." + str(amount) +
                      " back to your Total Balance...")
            progresBar(endText = "Transfer Complete!")
            printWait("Your total balance now is Rs." + str(appData['total']))


if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        printWait("Sorry, an error occured: " + str(error) + ".")
        printWait(" I am saving your work and quitting the program...")
        appData.close()
        quit()
