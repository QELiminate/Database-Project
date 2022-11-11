import database_operations

def registerCustomer(name, email, passWord):
    # hash the password and then store
    connectionObj = database_operations.connectToDatabase()
    database_operations.addCustomer(connectionObj, name, email, passWord)

def placeOrderCustomer():
    # to be done by Megan

def checkStatusOrder():

if __name__ == '__main__':
    print("\n Hello, Welcome to QElim. \n PLease Sign In/Sign Up to place an order \n")
    isUserRegisteredInput = input("\n If you're already a registered user? Y/N \n")

    if isUserRegisteredInput == "Y":
        # ask user to enter username /password

        # check if the user is registered

        # if the user is registered then sign in
        input("\n What operation would you like to perform? \n 1. Place an order \n 2. Check status of your order \n ")
    else:
        # sign up the user
        name = input(" \n Please enter your Name: \n ")
        email = input(" \n Please enter the email: \n ")
        passWord = input("\n Please enter the password: \n ")

        # we'll have to see how to create functions for payments


        registerCustomer(name, email, passWord)


        # Jose
        # once signed up/ signed in -> will show all the restaurants name
        # customer should select a restaurant
        # once the restaurant is selected show all the item names for the restaurant
        # customer will select a set of items and their quantity

        # Megan
        # payment and place order



