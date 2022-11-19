import database_operations

if __name__ == '__main__':
    #after order is placed, entry done in orders table
    cursor = cnx.cursor()
    item = ("SELECT ItemID FROM Orders")
    if checkStatusOrder is 1:
	   printf("Your order has been placed!")
    # restaurant will see the order ->
    orderid = ("SELECT OrderID FROM Orders WHERE ItemID = item")
    order = OrderID
    execute(orderid, order)
    # restaurant will enter the preparation time for the order - for now
    preparationtime = ("SELECT readyTime FROM OrderInfo WHERE orderID = Orders.orderID AND Orders.ItemID = item")
    preptime = (readyTime)
    execute(preparationtime, preptime)

