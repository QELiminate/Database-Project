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

def registerOrder(orderId, itemId, restaurantId, qty,custId):
    connectionObj = database_operations.connectToDatabase()
    database_operations.addOrder(connectionObj, orderId, restaurantId, itemId, qty, custId)
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
    if return_value[0] == -1:
        return ("Email doesn't exist", None, None)
    elif return_value[0] == -2:
        return ("Invalid password", None, None)
    elif return_value[0] == 1:
        return ("Registered User", return_value[1], return_value[2])


# def checkStatusOrder():

if __name__ == '__main__':
    while True:
        print("Customer View")
        print("\n Hello, Welcome to QElim. \n PLease Sign In/Sign Up to place an order \n")
        isUserRegisteredInput = input("\n Are you already a registered user? Y/N \n")

        if isUserRegisteredInput == "Y":
            # ask user to enter username /password
            email = input("Please enter your email address")
            password = input("Please enter your password")

            # check if the user is registered
            stringValAndCustId = isRegisteredCustomer(email, password)
            if stringValAndCustId[0] == "Registered User":
                customerId = stringValAndCustId[1]
                customerName = stringValAndCustId[2]
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
                            numberOfRowsInsertedInOrdersTable = 0
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
                                    registerOrder(currOrderNumber, itemQtyArr[0], restaurantId, itemQtyArr[1], customerId)
                                    totalPriceOfOrder += itemAlreadyPresent[1] * int(itemQtyArr[1])
                                    numberOfRowsInsertedInOrdersTable += 1

                            tax = 0.1 * totalPriceOfOrder
                            print("The total amount is ", totalPriceOfOrder + tax)
                            #Jose code start
                            payment = input("\n type pay to process payment or cancel to cancel order: \n")
                            if payment = 'pay':
                                # implement payment methods
                                total = totalPriceOrder+tax
                                paid = database_operations.payOrder(total,customerId)
                                if paid==False:
                                    database_operations.cancelOrder(currOrderNumber)
                                    return
                            elif payment = 'cancel':
                                database_operations.cancelOrder(currOrderNumber)
                                return
                            #Jose code end

                            print("\n Order successfully placed, we'll shortly send you the estimated time for your order pickup \n")

                            # create a trigger here for restaurant to get information of the order
                            # select the last numberOfRowsInsertedInOrdersTable from orders table
                            print("\n Restaurant View \n")
                            print("\n New Order for "+ customerName + "\n")
                            orderId, restaurantId, totalPayment = restaurant_terminal.lastOrderInfo()
                            readyDateTime = input("\nPlease enter the ready date(YYYY-MM-DD) and time(hh:mm:ss) for the order separated by space\n")
                            restaurant_terminal.registerOrderInfo(orderId, restaurantId, totalPayment, readyDateTime)
                            #Jose code start
                            restcommand = input("Type cancel to cancel an order or type proceed to continue: \n")
                            if restcommand='cancel':
                                ordertocancel = input("Type order ID of order to be cancelled: \n")
                                database_operations.cancelOrder(ordertocancel)
                            elif restcommand='proceed':
                                print("Proceeding...\n")
                            #Jose code end
                            print("\n Customer View\n ")
                            print("Your order's estimated time for pickup is: \n")
                            dateTimeObj = utility_functions.parseStrToDateTimeObj(readyDateTime)
                            print("\n Date: " + str(dateTimeObj.month) + "-" + str(dateTimeObj.day) + "-" + str(dateTimeObj.year))
                            print("\n Time in 24 hour format: \n")
                            print(str(dateTimeObj.hour) + ":" + str(dateTimeObj.minute))
                            
                            #Jose code start
                            #Let restaurant change bool pickedup to 1 (true) Check if picked up is true, if so then delete order from order info and orders tables
                            comm = input("To mark an order as picked up, type pickup\n")
                            if comm == 'pickup':
                                ord = input("Enter the order number to mark as picked up: \n")
                                database_operations.setOrderPickedup(ord)
                            #Jose code end


                            # input("Please wait while the restaurant sends you the order pickup time")

                            # after every 5 sec check if order id is there in ordersInfo, if it is then get the ready time
                            # if the ready time is returned exit the terminal



                    if choice == '4':
                        sys.exit()
            else:
                print(stringValAndCustId[0])
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







