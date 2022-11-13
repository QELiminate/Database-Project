import sys

import database_operations
import utility_functions


def registerCustomer(name, email, passWord):
    # hash the password and then store
    validEmail = utility_functions.isValidEmail(email)
    if not validEmail:
        return -1
    connectionObj = database_operations.connectToDatabase()
    hashedPass = utility_functions.hashPassword(passWord)
    database_operations.addCustomer(connectionObj, name, email, hashedPass)
    return 1


def isRegisteredCustomer(email,password):
    connectionObj = database_operations.connectToDatabase()
    return_value = database_operations.isValidUser(connectionObj, email, password)
    if return_value == -1:
        return "Email doesn't exist"
    elif return_value == -2:
        return "Invalid password"
    elif return_value == 1:
        return "Registered User"

# def placeOrderCustomer():

# def checkStatusOrder():

if __name__ == '__main__':
    while True:
        print("\n Hello, Welcome to QElim. \n PLease Sign In/Sign Up to place an order \n")
        isUserRegisteredInput = input("\n If you're already a registered user? Y/N \n")

        if isUserRegisteredInput == "Y":
            # ask user to enter username /password
            email = input("Please enter your email address")
            password = input("Please enter your password")

            # check if the user is registered
            stringVal = isRegisteredCustomer(email, password)
            if stringVal == "Registered User":

            # if the user is registered then sign in
                choice = input("\n What operation would you like to perform? \n 1. Place an order \n 2. Check status of your order 3. Exit\n ")

                if choice == '3':
                    sys.exit()
            else:
                continue
        else:
            # sign up the user
            name = input(" \n Please enter your Name: \n ")
            email = input(" \n Please enter the email: \n ")
            passWord = input("\n Please enter the password: \n ")

            # check if the user is registered
            strVal = isRegisteredCustomer(email, passWord)
            if strVal == "Registered User" or strVal=="Invalid password":

                print("The user is already registered please sign in to continue")
                continue

            # we'll have to see how to create functions for payments

            else:
                return_value = registerCustomer(name, email, passWord)
                if return_value == -1:
                    print("The email address you entered is not a valid email")
                    continue
                else:
                    print("Registration successful, please Sign In to continue")




        # Jose
        # once signed up/ signed in -> will show all the restaurants name
        # customer should select a restaurant
        # once the restaurant is selected show all the item names for the restaurant
        # customer will select a set of items and their quantity




