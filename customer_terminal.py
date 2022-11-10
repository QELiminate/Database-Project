import database_operations

def registerCustomer(name, email, passWord):
    # hash the password and then store
    connectionObj = database_operations.connectToDatabase()
    database_operations.addCustomer(connectionObj, name, email, passWord)

if __name__ == '__main__':
    print("\n Hello, Welcome to QElim. \n PLease Sign In/Sign Up to place an order \n")
    isUserRegisteredInput = input("\n If you're already a registered user? Y/N \n")

    if isUserRegisteredInput == "Y":
        # ask user to enter username /password

        # check if the user is registered

        # if the user is registered
    else:
        # sign up the user
        name = input(" \n Please enter your Name: \n ")
        email = input(" \n Please enter the email: \n ")
        passWord = input("\n Please enter the password: \n ")

        # we'll have to see how to create functions for payments


        registerCustomer(name, email, passWord)



