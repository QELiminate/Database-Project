import sys

import database_operations
from datetime import datetime, timedelta

'''
The following function gets the datetime from the restaurant and sends it to the customer
'''
# def communicateDateTime(dateTimeFromRestaurant):
#     return dateTimeFromRestaurant

# def example():
#     example.has_been_called = True
#     pass




def registerOrderInfo(orderId, restaurantId, totalPayment, readyDateTime):
    connObj = database_operations.connectToDatabase()
    database_operations.addOrderInfo(connObj, totalPayment, readyDateTime, orderId, restaurantId)
    connObj.close()

def lastOrderInfo():
    connObj = database_operations.connectToDatabase()
    orderInfoList = database_operations.getLastOrderInfo(connObj)

    if len(orderInfoList) == 0:
        print("No orders")
        sys.exit()

    totalPrice = 0
    # [(3, 1, 1000, 102, 5), (3, 2, 1000, 102, 4)]
    print("Order ID       ItemName          Quantity")
    for itemTuple in orderInfoList:
        itemName = database_operations.getItemNameFromItemID(connObj, itemTuple[1], itemTuple[2])
        validAndItemPrice = database_operations.isValidItem(connObj, itemTuple[1], itemTuple[2])
        totalPrice += validAndItemPrice[1] * itemTuple[4]
        print(str(itemTuple[0])+'            '+str(itemName[0]) + '          '+str(itemTuple[4]))
    totalPayment = 0.1 * totalPrice + totalPrice
    print("Total payment: ", totalPayment)
    connObj.close()
    return (orderInfoList[0][0], orderInfoList[0][2], totalPayment)

def clearPickedOrders():
    connObj = database_operations.connectToDatabase()
    database_operations.clearPickedOrders(connObj)
    connObj.close()
def getAllOrdersForRestaurant(restaurantId):
    connObj = database_operations.connectToDatabase()
    allOrders = database_operations.getOrdersForRestaurant(connObj, restaurantId)


    # get the customer name and item names to display in the order

    customerId = 0
    i = 0

    while i < len(allOrders):


        customerId = allOrders[i][3]

        customerNameTuple = database_operations.getCustomerNameFromID(connObj, customerId)
        print("\n \nOrder for " + customerNameTuple[0] + "\n")
        # get the order(s) for the customer

        while i < len(allOrders) and allOrders[i][3] == customerId:
            # if the orderid change/first row then only get the ready time for that order

            if i == 0:
                readyDateTimeTuple = database_operations.getReadyTimeForOrder(connObj, allOrders[i][0], restaurantId)
                if readyDateTimeTuple is None:
                    readyDateTimeTuple = ('Not yet added by the restaurant')
                print("\nOrder ID: ", allOrders[i][0])

                print("\nReady Date and Time: ", readyDateTimeTuple[0])
            elif i-1 >= 0 and allOrders[i-1][0] != allOrders[i][0]:
                # get the ready time
                orderId = allOrders[i][0]
                readyDateTimeTuple = database_operations.getReadyTimeForOrder(connObj, orderId, restaurantId)
                if readyDateTimeTuple is None:
                    readyDateTimeTuple = ('Not yet added by the restaurant')
                print("\n Order ID: ", orderId)
                print(" \n Ready Date and Time: ", readyDateTimeTuple[0])


            itemId = allOrders[i][1]
            restaurantID = allOrders[i][2]
            qty = allOrders[i][4]

            # if (itemId, restaurantID) is already in the hashtable then get its name else make a query to fetch it from database and store it in hashtable
            itemNameTuple = database_operations.getItemNameFromItemID(connObj, itemId, restaurantID)
            itemName = itemNameTuple[0]

            print(itemName + "            " + str(qty))
            i += 1

def checkForValidRestaurantID(restaurantId):
    connObj = database_operations.connectToDatabase()
    return_value = database_operations.isValidRestaurant(connObj, restaurantId)
    connObj.close()
    return return_value

def setOrderPickedup(orderId):
    connObj = database_operations.connectToDatabase()
    database_operations.setOrderPickedup(connObj, orderId)
    connObj.close()
def cancelOrder(orderId, restaurantId):
    connObj = database_operations.connectToDatabase()
    database_operations.cancelOrder(connObj, orderId, restaurantId)
    connObj.close()

def notifyCustomerOrderReady(orderId, restaurantId):

    # set isReady to 1 in orderinfo table
    conObj = database_operations.connectToDatabase()
    database_operations.orderReady(conObj, orderId, restaurantId)
    cusotmerIDTuple = database_operations.getCustomerIDForOrder(conObj, orderId, restaurantId)
    if cusotmerIDTuple is None:
        # there is no order for the customer
        return None
    # get the name of the customer
    customerNameTuple = database_operations.getCustomerNameFromID(conObj, customerId=cusotmerIDTuple[0])
    restaurantNameTuple = database_operations.getRestaurantNameFromID(conObj, restaurantId)
    # notify the customer
    print("\nCustomer View\n")
    print("\n Hello " + customerNameTuple[0] + " your order number " + str(orderId) + " with the restaurant " + restaurantNameTuple[0] + " is ready \n")
    return 1
if __name__ == "__main__" :
    while True:
        print("\nRestaurant View\n")
        restaurantId = input("\nEnter your restaurant ID\n")
        if restaurantId == "":
            print("Invalid Restaurant ID")
            continue
        returnValue = checkForValidRestaurantID(restaurantId)
        if returnValue == 1:
            choice = input("What operation would you like to perform: \n 1. View all orders  \n 2. Notify the customer that order is ready \n 3. Cancel an order \n 4. Update the order pickup status \n 5. Clear picked up orders \n 6. Exit \n")

            if choice == '1':
                # get all the orders for the restaurant
                getAllOrdersForRestaurant(restaurantId)
            elif choice == '2':
                orderID = input("\n Enter the order ID for the order which is ready \n")
                returnValue = notifyCustomerOrderReady(orderID, restaurantId)
                if returnValue is None:
                    print("Order ID doesn't exist")
                    continue

            elif choice == '3':
                #cancel order - written by Jose
                ordertocancel = input("Type order ID of order to be cancelled: \n")
                cancelOrder(ordertocancel, restaurantId)
                continue
            elif choice == '4':
                #mark order as picked up - written by Jose
                orderId = input("Enter the order number to mark as picked up: \n")
                setOrderPickedup(orderId)
                continue
            elif choice == '5':
                #clear all orders marked as picked up - written by Jose
                clearPickedOrders()
                continue
            elif choice == '6':
                sys.exit()
        else:
            print("Invalid Restaurant ID")


