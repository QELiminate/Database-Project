import sys

import database_operations
import utility_functions
import time
import restaurant_terminal


def registerCustomer(name, email, passWord):
    # hash the password and then store
    validEmail = utility_functions.isValidEmail(email)
    if not validEmail:
        return -1
    connectionObj = database_operations.connectToDatabase()
    hashedPass = utility_functions.hashPassword(passWord)
    database_operations.addCustomer(connectionObj, name, email, hashedPass)
    return 1

def registerOrder(orderId, itemId, restaurantId, qty):
    connectionObj = database_operations.connectToDatabase()
    database_operations.addOrder(connectionObj, orderId, restaurantId, itemId, qty)
    connectionObj.close()

def isRegisteredRestaurant(restId):
    connectionObj = database_operations.connectToDatabase()
    return_val = database_operations.isValidRestaurant(connectionObj, restId)
    connectionObj.close()
    return return_val

def lastOrderId():
    connectionObj = database_operations.connectToDatabase()
    lastOrderNumber = database_operations.getLastOrderId(connectionObj)
    return lastOrderNumber
def isRegisteredItem(itemId, restuarantId):
    connectionObj = database_operations.connectToDatabase()
    return_val = database_operations.isValidItem(connectionObj, itemId, restuarantId)
    connectionObj.close()
    return return_val

def displayRestaurants():
    connectionObj = database_operations.connectToDatabase()
    database_operations.showRestaurants(connectionObj)
    connectionObj.close()

def showItems(restaurantId):
    connectionObj = database_operations.connectToDatabase()
    database_operations.showRItems(connectionObj, restaurantId)
    connectionObj.close()

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
            # show restaurants
                while True:
                    choice = input("\n What operation would you like to perform? \n 1. Show Restaurants \n 2. Place an order \n 3.Check status of your order \n 4. Exit \n ")

                    if choice == '1':
                        displayRestaurants()
                        continue
                    elif choice == '2':
                        restaurantId = input("Enter the restaurant id in which you would like to place the order in")
                        # check if it is a valid restaurantId
                        returnValRegisteredRestaurant = isRegisteredRestaurant(restaurantId)
                        if returnValRegisteredRestaurant == -1:
                            print("The restaurant ID is invalid, please enter a valid restaurant id")
                            continue
                        elif returnValRegisteredRestaurant == 1:
                            # show the items in the restaurant
                            showItems(restaurantId)
                            itemsList = []

                            lastOrderNumber = lastOrderId()
                            currOrderNumber = lastOrderNumber + 1
                            totalPriceOfOrder = 0
                            while True:
                                itemIdAndQty = input("Enter the item id and its corresponding quantity separated by a space, onc you're done please enter 2")
                                if itemIdAndQty == '2':
                                    break
                                itemQtyArr = itemIdAndQty.split(' ')
                                # qty should be an integer
                                # item id should be valid
                                itemAlreadyPresent = isRegisteredItem(itemQtyArr[0],restaurantId)
                                if itemAlreadyPresent[0] == -1:
                                    print("The item ID is invalid, please enter a valid item ID")
                                    continue
                                elif itemAlreadyPresent[0] == 1:
                                    registerOrder(currOrderNumber, itemQtyArr[0], restaurantId, itemQtyArr[1])
                                    totalPriceOfOrder += itemAlreadyPresent[1] * int(itemQtyArr[1])

                            tax = 0.1 * totalPriceOfOrder
                            print("The total amount is ", totalPriceOfOrder + tax)
                            print("Please choose a method of payment")
                            # implement payment methods
                            print("Order successfully placed, we'll shortly send you the estimated time for your order pickup")

                            input("Please wait while the restaurant sends you the order pickup time")

                            # after every 5 sec check if order id is there in ordersInfo, if it is then get the ready time
                            # if the ready time is returned exit the terminal



                    if choice == '4':
                        sys.exit()
            else:
                print(stringVal)
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







