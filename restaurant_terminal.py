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


# if __name__ == "__main__" :
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

