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


def payOrder(totalPrice, customerId):
    connectionObj = database_operations.connectToDatabase()
    return_val = database_operations.payOrder(connectionObj, totalPrice, customerId)
    connectionObj.close()
    return return_val

def balanceFunc(customerId):
    connectionObj = database_operations.connectToDatabase()
    database_operations.balanceFunc(connectionObj, customerId)
    connectionObj.close()

def cancelOrder(orderId, restaurantId):
    connectionObj = database_operations.connectToDatabase()
    database_operations.cancelOrder(connectionObj, orderId, restaurantId)
    connectionObj.close()


def registerOrder(orderId, itemId, restaurantId, qty, custId):
    connectionObj = database_operations.connectToDatabase()
    database_operations.addOrder(connectionObj, orderId, restaurantId, itemId, qty, custId)
    connectionObj.close()


def isRegisteredRestaurant(restId):
    connectionObj = database_operations.connectToDatabase()
    return_val = database_operations.isValidRestaurant(connectionObj, restId)
    connectionObj.close()
    return return_val


def fetchOrdersForCustomer(customerId):
    connObj = database_operations.connectToDatabase()
    allOrdersList = database_operations.getOrdersForCustomer(connObj, customerId)

    print("\n Order ID          Restaurant Name         Item Name           Quantity            Ready Time \n")
    prevRestaurantId = 0
    prevOrderId = 0
    readyTimeTuple = None
    restaurantNameTuple = None
    for orderTuple in allOrdersList:
        # if order id or restaurantID change then only get the readyTime
        if prevOrderId != orderTuple[0] or prevRestaurantId != orderTuple[2]:
            readyTimeTuple = database_operations.getReadyTimeForOrder(connObj, orderTuple[0], orderTuple[2])
            if prevOrderId != orderTuple[0]:
                prevOrderId = orderTuple[0]
            if prevRestaurantId != orderTuple[2]:
                prevRestaurantId = orderTuple[2]
                # if the restaurant has changed then only get the restaurantName
                restaurantNameTuple = database_operations.getRestaurantNameFromID(connObj, orderTuple[2])
        itemNameTuple = database_operations.getItemNameFromItemID(connObj, orderTuple[1], orderTuple[2])

        if readyTimeTuple[0] is None:
            readyTimeTuple = ('Not yet added by restaurant')

        print("\n " + str(orderTuple[0]) + "        " + str(restaurantNameTuple[0]) + "         " + str(
            itemNameTuple[0]) + "           " + str(orderTuple[3]) + "          " + str(readyTimeTuple[0]) + "\n")


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


def isRegisteredCustomer(email, password):
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
                    choice = input("\n What operation would you like to perform? \n 1. Show Restaurants \n 2. Place an order \n 3. View your orders \n 4. Cancel an Order \n 5. Access your Account \n 6. Exit \n ")

                    if choice == '1':
                        displayRestaurants()
                        continue
                    elif choice == '2' :
                        restaurantId = input("Enter the restaurant id in which you would like to place the order in\n")
                        # check if it is a valid restaurantId
                        returnValRegisteredRestaurant = isRegisteredRestaurant(restaurantId)
                        if returnValRegisteredRestaurant == -1:
                            print("The restaurant ID is invalid, please enter a valid restaurant id\n")
                            continue
                        elif returnValRegisteredRestaurant == 1:
                            # show the items in the restaurant
                            showItems(restaurantId)
                            itemsList = []

                            lastOrderNumber = lastOrderId()
                            currOrderNumber = lastOrderNumber + 1
                            totalPriceOfOrder = 0
                            numberOfRowsInsertedInOrdersTable = 0
                            orderNumberAndItemIdsAndQtyList = []
                            while True:
                                itemIdAndQty = input(
                                    "Enter the item id and its corresponding quantity separated by a space, once you're done please enter 2\n")
                                if itemIdAndQty == '':
                                    print("Please enter a valid value")
                                    continue
                                if itemIdAndQty == '2':
                                    break

                                itemQtyArr = itemIdAndQty.split(' ')
                                if len(itemQtyArr) != 2:
                                    print("Invalid input")
                                    continue
                                # qty should be an integer
                                # item id should be valid
                                itemAlreadyPresent = isRegisteredItem(itemQtyArr[0], restaurantId)
                                if itemAlreadyPresent[0] == -1:
                                    print("The item ID is invalid, please enter a valid item ID\n")
                                    continue
                                elif itemAlreadyPresent[0] == 1:
                                    orderNumberAndItemIdsAndQtyList.append((currOrderNumber, itemQtyArr[0], itemQtyArr[1]))
                                    totalPriceOfOrder += itemAlreadyPresent[1] * int(itemQtyArr[1])
                                    numberOfRowsInsertedInOrdersTable += 1

                            tax = 0.1 * totalPriceOfOrder
                            print("The total amount is ", totalPriceOfOrder + tax)
                            # Jose code start
                            payment = input("\ntype pay to process payment or cancel to cancel order: \n")
                            if payment == 'pay':
                                # implement payment methods
                                total = totalPriceOfOrder + tax
                                paid = payOrder(total, customerId)
                                if paid:
                                    for i in range(len(orderNumberAndItemIdsAndQtyList)):
                                        orderId = orderNumberAndItemIdsAndQtyList[i][0]
                                        itemId = orderNumberAndItemIdsAndQtyList[i][1]
                                        quantity = orderNumberAndItemIdsAndQtyList[i][2]
                                        registerOrder(orderId, itemId, restaurantId, quantity,
                                                      customerId)
                                else:
                                    continue
                            elif payment == 'cancel':
                                continue
                            # Jose code end

                            print("\n Order successfully placed, we'll shortly send you the estimated time for your order pickup \n")

                            print("\n Restaurant View \n")
                            print("\n New Order for " + customerName + "\n")
                            orderId, restaurantId, totalPayment = restaurant_terminal.lastOrderInfo()
                            readyDateTime = input(
                                "\nPlease enter the ready date(YYYY-MM-DD) and time(hh:mm:ss) for the order separated by space\n")
                            restaurant_terminal.registerOrderInfo(orderId, restaurantId, totalPayment, readyDateTime)

                            print("\n Customer View\n ")
                            print("Your order's estimated time for pickup is: \n")
                            dateTimeObj = utility_functions.parseStrToDateTimeObj(readyDateTime)
                            print("\n Date: " + str(dateTimeObj.month) + "-" + str(dateTimeObj.day) + "-" + str(
                                dateTimeObj.year))
                            print("\n Time in 24 hour format: \n")
                            print(str(dateTimeObj.hour) + ":" + str(dateTimeObj.minute))

                    elif choice == '3':
                        fetchOrdersForCustomer(customerId)

                    elif choice == '4':
                        # cancel order - written by Jose
                        restcancel = input("Type restaurant ID of the order to be cancelled: \n")
                        ordertocancel = input("Type order ID of order to be cancelled: \n")
                        cancelOrder(ordertocancel, restcancel)
                        continue

                    elif choice == '5':
                        balanceFunc(customerId)
                    elif choice == '6':
                        sys.exit()
                    else:
                        print("\n Invalid value entered \n")
                        continue
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
            if strVal == "Registered User" or strVal == "Invalid password":

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
