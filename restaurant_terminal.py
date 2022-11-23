import sys

import database_operations
from datetime import datetime, timedelta
from classes import Store

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

    totalPrice = 0
    # [(3, 1, 1000, 102, 5), (3, 2, 1000, 102, 4)]
    print("Order ID       ItemName          Quantity")
    for itemTuple in orderInfoList:
        itemName = database_operations.getItemNameFromItemId(connObj, itemTuple[1])
        validAndItemPrice = database_operations.isValidItem(connObj, itemTuple[1], itemTuple[2])
        totalPrice += validAndItemPrice[1] * itemTuple[4]
        print(str(itemTuple[0])+'            '+str(itemName) + '          '+str(itemTuple[4]))
    totalPayment = 0.1 * totalPrice + totalPrice
    print("Total payment: ", totalPayment)
    connObj.close()
    return (orderInfoList[0][0], orderInfoList[0][2], totalPayment)


def getAllOrdersForRestaurant(restaurantId):
    storeObj = Store()
    connObj = database_operations.connectToDatabase()
    allOrders = database_operations.getOrdersForRestaurant(connObj, restaurantId)


    # get the customer name and item names to display in the order

    customerId = 0
    i = 0

    while i < len(allOrders):


        customerId = allOrders[i][3]

        customerNameTuple = database_operations.getCustomerNameFromID(connObj, customerId)
        print("\n \n Order for " + customerNameTuple[0] + "\n")
        # get the order(s) for the customer

        while i < len(allOrders) and allOrders[i][3] == customerId:
            # if the orderid change/first row then only get the ready time for that order

            if i == 0:
                readyDateTimeTuple = database_operations.getReadyTimeForOrder(connObj, allOrders[i][0])
                print("\n\nOrder ID: ", allOrders[i][0])

                print("\nReady Date and Time: ", readyDateTimeTuple[0])
            elif i-1 >= 0 and allOrders[i-1][0] != allOrders[i][0]:
                # get the ready time
                orderId = allOrders[i][0]
                readyDateTimeTuple = database_operations.getReadyTimeForOrder(connObj, orderId)
                print("Order ID: ", orderId)
                print("Ready Date and Time: ", readyDateTimeTuple[0])


            itemId = allOrders[i][1]
            restaurantID = allOrders[i][2]
            qty = allOrders[i][4]
            itemName = ''

            # if (itemId, restaurantID) is already in the hashtable then get its name else make a query to fetch it from database and store it in hashtable
            if (itemId, restaurantID) not in storeObj.itemIDRestaurantIdToItemNameHashTable:
                itemNameTuple = database_operations.getItemNameFromItemID(connObj, itemId, restaurantID)
                storeObj.itemIDRestaurantIdToItemNameHashTable[(itemId, restaurantID)] = itemNameTuple[0]
                itemName = itemNameTuple[0]
            else:
                itemName = storeObj.itemIDRestaurantIdToItemNameHashTable[(itemId, restaurantID)]

            print(itemName + "            " + str(qty))
            i += 1
    del storeObj
def checkForValidRestaurantID(restaurantId):
    storeObj = Store()

    if restaurantId in storeObj.restaurantIDSet:
        return 1

    connObj = database_operations.connectToDatabase()

    return_value = database_operations.isValidRestaurant(connObj, restaurantId)

    if return_value == 1 and restaurantId not in storeObj.restaurantIDSet:
            storeObj.restaurantIDSet.add(restaurantId)

    return return_value

def notifyCustomerOrderReady(orderId, restaurantId):

    # set isReady to 1 in orderinfo table
    conObj = database_operations.connectToDatabase()
    database_operations.orderReady(conObj, orderId, restaurantId)
    cusotmerIDTuple = database_operations.getCustomerIDForOrder(conObj, orderId, restaurantId)
    print("cusotmerIDTuple: ", cusotmerIDTuple)

    # get the name of the customer
    customerNameTuple = database_operations.getCustomerNameFromID(conObj, customerId=cusotmerIDTuple[0])
    restaurantNameTuple = database_operations.getRestaurantNameFromID(conObj, restaurantId)
    # notify the customer
    print("\nCustomer View\n")
    print("\n Hello " + customerNameTuple[0] + " your order number " + str(orderId) + " with the restaurant " + restaurantNameTuple[0] + " is ready \n")
if __name__ == "__main__" :


    while True:
        print("\nRestaurant View\n")
        restaurantId = input("\nEnter your restaurant ID\n")
        returnValue = checkForValidRestaurantID(restaurantId)
        if returnValue == 1:
            choice = input("What operation would you like to perform: \n 1. View all orders  \n2. Notify the customer that order is ready \n 3. Update the ready time for an order \n4. Cancel an order \n5. Update the order pickup status \n6. Exit")

            if choice == '1':
                # get all the orders for the restaurant
                getAllOrdersForRestaurant(restaurantId)
            elif choice == '2':
                orderID = input("\n Enter the order ID for the order which is ready \n")
                notifyCustomerOrderReady(orderID, restaurantId)

            elif choice == '5':
                sys.exit()
        else:
            print("Invalid Restaurant ID")



#
#     lastOrderInfo()
    # print("New Order\n")
    # newOrderCameIn.has_been_called = False\
    # while True:
    #     # if newOrderCameIn() is called then print here something
    #
    #     if newOrderCameIn:
    #         print("hello")
        # newOrderCameIn.has_been_called = False
    # after the order is placed -> entry is done in the Orders table
    # restaurant will see the order ->
    # restaurant will enter the preparation time for the order - for now
    #
        # print("New Order\n")
        # orderId, restaurantId, totalPayment = lastOrderInfo()

        #
        # # we also need the name of the customer who made the order
        #
        # # insert into orderinfo values (1, 0, '2022-01-01 22:23:24', 34, 0, '2022-01-01 22:23:24', 1000)
        # # readyDateTimeObj = datetime.strptime(readyDateTime, '%Y-%m-%d %H:%M:%S')
        # registerOrderInfo(orderId, restaurantId, totalPayment, readyDateTime)
    # communicateDateTime(readyDateTime)
    # insert the order into Orders Info with ready Time, order Id, restaurant id

