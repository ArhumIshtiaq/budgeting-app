#!/usr/bin/python
#Accounting.py - A simple command line based budgeting software with the ability to have data saved for, virtually, inifite amount of users.

import os
import os.path
import time 
import shelve

# A print-and-wait function to reduce repetition of same lines of code
def pw(str):
  print(str)
  time.sleep(0.8)

#Function to double-check user selection
def sure():
  yn = input("Are you sure?\n ").lower()
  
  if (yn[0][0] == "y"):
    return False
  
  elif (yn[0][0] == "n"):
    return True

#Function to print the user data in a presentable format
def printTable(table):
  colWidths = [0] * len(table)
  ll = len(table)
  lol = len(table[0])

  for i in range(ll):
    for x in table[i]:
      if (colWidths[i] < len(x)):
  colWidths[i] = len(x)

  for i in range(lol):
    for x in range(ll):
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
    I have programmed it so that all the budget category 'types' will be in a single string, seperated by the front-slash(/).
    When the need arises, this program will split the string and use the resulting data accordingly.
    """
    appData['types'] = "/".join(self.types)

  def deposit(self, amount):
    if amount > 0:
      appData['total'] += amount
      pw("Depositing...")
      pw("Deposit Succesful!")
      pw("Your total balance now is Rs." + str(appData['total']))

  def withdraw(self, amount):
    if (amount > appData['total']):
      print("Sorry, you do not have enough money!")
    
    else:
      appData['total'] -= amount
      pw("Withdrawing...")
      pw("Withdrawal Succesful!")
      pw("Your total balance now is Rs." + str(appData['total']))

  def create_type(self, name, amount):
    types = appData['types'].split('/')
    types.append(name)
    appData['types'] = "/".join(types)
    
    if (amount > appData['total']):
      print("Sorry, you do not have enough money to spend on this thing!")
    
    else:
      appData['total'] -= amount
      appData[name] = amount
      pw("Your total balance now is Rs." + str(appData['total']))

  def add_amount(self, type_, amount):
    appData['total'] -= amount
    
    if appData[type_] > 0:
      appData[type_] += amount
    
    else:
      appData[type_] = 0
      appData[type_] += amount
    
    pw("Your total balance now is Rs." + str(appData['total']))

  def rm_amount(self, type_, amount):
    if (amount > appData[type_]):
      print("Sorry, that's not possible!")
    
    else:
      appData['total'] += amount
      appData[type_] = 0
      appData[type_] -= amount
      pw("Tranferring Rs.", amount, "back to your Total Balance...")
      pw("Transfer complete!")
      pw("Your total balance now is Rs." + str(appData['total']))

#Acquire initial login data from user
name = input('Hi! What is your name?\n  ').lower()
password = input('\nHi ' + name + "! May I have you password as well?\n  ")

#Create shelve object while keeping nomenclature to the specific user for easier access
appData = shelve.open(('fad' + name))

pw("\nInitializing your account...")
pw("Retrieving any previous data, if any...")

#Checking username against existing shelve data
if (name in appData):
  pw("Data found. Loading...")
  pw("Checking password...")

  #If username exists, then check password against user-defined existing shelve data
  while (password != appData['password']):
    password = str(input("Wrong password. Try again!\n "))

  pw("Password is correct! Logging in...")
  pw("Success!")

  #Save the specific shelve object to a variable for permanent data accessibility for the user session
  user = appData[name]

else:
  pw("No previous record found.")

  if (input("\nWould you like to create a new account?\n ")[0] == "y"):
    
    #Creating new user object using data provided by user at script initialization
    user = Budget(name, password)

    #Saving customized class object to shelve object
    appData[user.user_name] = user
    
    pw("Creating account...")
    pw("Account created.")

  else: 
    pw("I will not create an account. Exiting program...")

    #Deleting data that this script may have unintentionally created while checking for username against shelve data
    try:
    os.unlink(os.path.abspath(os.curdir)+r"\fad"+name+".dat")
    os.unlink(os.path.abspath(os.curdir)+r"\fad"+name+".dir")
    os.unlink(os.path.abspath(os.curdir)+r"\fad"+name+".bak")
    except FileNotFoundError:
    pass
    
    quit()

pw("Your current balance is Rs." + str(appData['total']))

"""
Testing portion of code, needed when-if:
user.deposit(2500)
user.create_type("pleasure", 500)
user.create_type("bills", 100)
user.create_type("travel", 80)
user.create_type("food", 200)
user.add_amount("pleasure", 500)
user.create_type("friends", 200)
"""

try:
  while True:
    command = str(input("\nWhat else would you like to do?\n ")).lower()
    cc = command.split(' ')
    main = cc[0]

    if (main == "deposit"):
      user.deposit(int(cc[1]))

    elif (main == "withdraw"):
      user.withdraw(int(cc[1]))

    elif (main == "summary"):
    tp = [["TOTAL", ":", str(appData['total'])]]
    types = appData['types'].split('/')

    #Loop for creating data stucture (list of lists) to provide printTable() fucntion with an argument
    for i in types:
      ts = []
      ts.append(i.upper())
      ts.append(":")
      ts.append(str(appData[i]))
      tp.append(ts)
    printTable(list(zip(*tp)))

    elif (main == "exit" or main == "quit"):
      s = sure()

      if (s == False):
  pw("Thank you for using this budgeting software. See you next time, " + name + ". Bye!")
  time.sleep(1)
  appData.close()
  quit()

except Exception as error:
  pw("Sorry, a" + error + "error occured. I am saving your work and quitting the program...")
  appData.close()
  quit()
