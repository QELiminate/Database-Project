from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

import utility_functions


def connectToDatabase():
    cnx = mysql.connector.connect(user='your_username', password='your_password',
                                  host='127.0.0.1', port='3306',
                                  database='app_schema')
    return cnx


def getRestaurantNameFromID(cnx, restaurantID):
    cursor = cnx.cursor()
    cursor.execute("SELECT restaurantName from restaurant where RestaurantID=" + str(restaurantID))
    restaurantNameTuple = cursor.fetchone()
    cursor.close()
    return restaurantNameTuple


def getLastOrderInfo(cnx):
    lastOrderId = getLastOrderId(cnx)
    cursor = cnx.cursor()
    # select all rows with orderId = lastOrderId
    cursor.execute('SELECT * from orders where orderID =' + str(lastOrderId))
    fetcAll = cursor.fetchall()
    cursor.close()
    return fetcAll


def getLastOrderId(cnx):
    cursor = cnx.cursor()
    cursor.execute('SELECT orderID FROM orders ORDER BY orderID DESC LIMIT 1')
    lastOrderInfo = cursor.fetchone()
    if lastOrderInfo is None:
        return 0
    else:
        return lastOrderInfo[0]


def getCustomerNameFromID(cnx, customerId):
    cursor = cnx.cursor()
    query = 'SELECT customerName FROM customer where customerID = ' + str(customerId)
    cursor.execute(query)
    customerName = cursor.fetchone()
    return customerName


def isValidUser(cnx, email, passoword):
    cursor = cnx.cursor()

    cursor.execute('SELECT * FROM customer where email ="' + email + '"')
    customerInfo = cursor.fetchone()
    if customerInfo is None:
        return (-1, None, None)
    else:
        passwordInDB = customerInfo[4]
        # compare entered password with passwordInDB
        isPasswordCorrect = utility_functions.checkPassword(passoword, passwordInDB)
        if not isPasswordCorrect:
            return (-2, None, None)
        else:
            return (1, customerInfo[0], customerInfo[1])
    cursor.close()


def showRestaurants(cnx):
    # written by Jose
    cursor = cnx.cursor()
    showRestQuery = ('SELECT * FROM Restaurant')
    cursor.execute(showRestQuery)
    result = cursor.fetchall()
    print('Restaurant ID       Restaurants:\n')
    for r in result:
        print(str(r[0]) + '              ' + r[1] + '\n')
    cursor.close()


def isValidRestaurant(cnx, restaurantId):
    cursor = cnx.cursor()
    getRestaurant = 'SELECT * from Restaurant R where R.RestaurantID = ' + str(restaurantId)
    cursor.execute(getRestaurant)
    if cursor.fetchone() is None:
        return -1
    else:
        return 1


def getCustomerIDForOrder(cnx, orderID, restaurantId):
    cursor = cnx.cursor(buffered=True)
    query = "SELECT customerID from orders where orderID=" + str(orderID) + " and restaurantId=" + str(restaurantId)
    cursor.execute(query)
    customerIDTuple = cursor.fetchone()
    cursor.close()
    return customerIDTuple


def orderReady(cnx, orderId, restaurantId):
    cursor = cnx.cursor()
    updateisReady = "UPDATE orderinfo SET isReady = 1 WHERE orderID=%s AND RestaurantID=%s"
    values = (orderId, restaurantId)
    cursor.execute(updateisReady, values)
    cnx.commit()
    cursor.close()


def isValidItem(cnx, itemId, restaurantID):
    cursor = cnx.cursor(buffered=True)
    cursor.execute('SELECT * from Menu M where M.ItemID = ' + str(itemId) + ' and M.RestaurantID= ' + str(restaurantID))
    fetchedItem = cursor.fetchone()
    if fetchedItem is None:
        return (-1, None)
    else:
        # return the price of the item
        return (1, fetchedItem[3])


def getItemNameFromItemID(cnx, itemId, restaurantId):
    cursor = cnx.cursor()
    query = ('SELECT ItemName FROM Menu M, Restaurant R WHERE M.RestaurantID=R.RestaurantID AND R.RestaurantID=' + str(
        restaurantId) + ' AND M.ItemID=' + str(itemId))
    cursor.execute(query)
    resultItemName = cursor.fetchone()
    cursor.close()
    return resultItemName


def showRItems(cnx, RSelect):
    # written by Jose
    cursor = cnx.cursor()
    showRItemQuery = (
                'SELECT ItemID, ItemName, Price FROM Menu M, Restaurant R WHERE M.RestaurantID=R.RestaurantID AND R.RestaurantID=' + RSelect)
    cursor.execute(showRItemQuery)
    result = cursor.fetchall()
    print('Menu for ' + RSelect + '\n')
    print('Item ID:          Item Name:             Price: \n')
    for r in result:
        print(str(r[0]) + '           ' + str(r[1]) + '           ' + str(r[2]) + '\n')
    cursor.close()


def addOrder(cnx, orderId, restaurantId, itemId, quantity, custId):
    # written by Tarun
    cursor = cnx.cursor()
    query_add_orders = ("INSERT INTO orders "
                        "(orderID, ItemID, RestaurantID, customerID, Quantity) "
                        "VALUES (%s, %s, %s, %s, %s)")
    values = (orderId, itemId, restaurantId, custId, quantity)
    cursor.execute(query_add_orders, values)
    cnx.commit()

    cursor.close()


def getOrdersForCustomer(cnx, customerID):
    cursor = cnx.cursor()
    query = 'SELECT orderID, ItemID, RestaurantID, Quantity FROM orders WHERE customerID=' + str(customerID)
    cursor.execute(query)
    allResultsList = cursor.fetchall()
    cursor.close()
    return allResultsList


def getOrdersForRestaurant(cnx, restuarntId):
    cursor = cnx.cursor()
    query = ("SELECT * FROM orders where RestaurantID = " + restuarntId)
    cursor.execute(query)
    allResultsList = cursor.fetchall()
    cursor.close()
    return allResultsList


def getLastNRowsFromOrdersTable(cnx, numRows):
    cursor = cnx.cursor()
    query = "SELECT * FROM orders ORDER BY orderID DESC LIMIT " + str(numRows)
    cursor.execute(query)
    allResultsList = cursor.fetchall()
    cursor.close()
    return allResultsList


def addOrderInfo(cnx, totalPrice, readyTime, orderId, restaurantId):
    # written by Tarun
    cursor = cnx.cursor()
    query_add_orderInfo = ("INSERT INTO orderinfo "
                           "(orderID, isReady, readyTime, totalPrice, isOrderPickedUp, RestaurantID) "
                           "VALUES (%s, %s, %s, %s, %s, %s)")
    # orderExpirationDateTime = readyTime + 1 hr
    # we'll not implement expirationDateTime, instead we'll have a script/cronjob that runs at 3:00 am everyday and deletes all orders
    values = (orderId, 0, readyTime, totalPrice, 0, restaurantId)
    cursor.execute(query_add_orderInfo, values)
    cnx.commit()

    cursor.close()


def getReadyTimeForOrder(cnx, orderId, RestaurantID):
    cursor = cnx.cursor(buffered=True)
    query = 'SELECT readyTime from orderinfo where orderID=' + str(orderId) + ' AND RestaurantID=' + str(RestaurantID)
    cursor.execute(query)
    readyTimeTuple = cursor.fetchone()
    cursor.close()
    return readyTimeTuple


def addAccount(cnx, balance):
    # written by Tarun
    cursor = cnx.cursor()
    query_add_account = ("INSERT INTO account "
                         "(balance) "
                         "VALUES (%s)")
    values = (balance,)
    cursor.execute(query_add_account, values)
    cnx.commit()

    cursor.close()

    cursor = cnx.cursor()
    count_number_of_accounts_query = "SELECT COUNT(*) FROM account"
    cursor.execute(count_number_of_accounts_query)
    numberofRows = cursor.fetchone()[0]

    # numberofRows is equal to the account number recently created
    account_number = numberofRows

    cursor.close()

    return account_number


def addCustomer(cnx, name, email, passWord):
    # written by Tarun
    cursor = cnx.cursor()
    # first create an account

    # first check if the email already exists

    # we'll need a function to ask how much money they want to put in their account, maybe implement payments -> currently giving a hardcoded value
    account_number = addAccount(cnx, 0)

    query_add_customer = ("INSERT INTO customer "
                          "(customerName, accountNo, email, pass) "
                          "VALUES (%s, %s, %s, %s)")

    # add email validation -> https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    data_customer = (name, account_number, email, passWord)
    cursor.execute(query_add_customer, data_customer)
    cnx.commit()

    cursor.close()


def cancelOrder(cnx, orderID,
                restaurantID):  # cancel order (delete order and notify about cancellation) - written by Jose
    # refund order
    cursor = cnx.cursor(buffered=True)

    getTotalPriceQuery = (
                'SELECT O.totalPrice FROM orderinfo O WHERE O.orderID=' + str(orderID) + ' AND O.RestaurantID=' + str(
            restaurantID))
    cursor.execute(getTotalPriceQuery)
    try:
        totalp = cursor.fetchone()[0]
    except:
        print("Order Not Found. Please ensure Restaurant and Order IDs are both valid.")
        return 0

    getBalanceQuery = ('SELECT A.balance FROM account A, orders O, customer C WHERE O.orderID=' + str(
        orderID) + ' AND O.customerID=C.customerID AND C.accountNo=A.accountNo' + ' AND O.RestaurantID=' + str(
        restaurantID))
    cursor.execute(getBalanceQuery)
    balan = cursor.fetchone()[0]

    getAccountQuery = ('SELECT A.accountNo FROM account A, orders O, customer C WHERE O.orderID=' + str(
        orderID) + ' AND O.customerID=C.customerID AND C.accountNo=A.accountNo' + ' AND O.RestaurantID=' + str(
        restaurantID))
    cursor.execute(getAccountQuery)
    AccountNo = cursor.fetchone()[0]

    totalp = float(totalp)
    balan = float(balan)
    balan = balan + totalp
    updateBalanceQuery = ('UPDATE account SET balance=' + str(balan) + ' WHERE accountNo=' + str(AccountNo))
    cursor.execute(updateBalanceQuery)

    deleteOrderQuery = ('DELETE FROM orders WHERE orderID=' + str(orderID) + ' AND RestaurantID=' + str(restaurantID))
    cursor.execute(deleteOrderQuery)
    cnx.commit()
    orderDeleteParityCheck(cnx)

    cursor.close()
    print('Order ' + str(orderID) + ' from restaurant ' + str(restaurantID) + ' has been canceled and refunded.\n')


# written by Jose
def setOrderPickedup(cnx, orderId):
    # Let restaurant change bool pickedup to 1 (true) Check if picked up is true, if so then delete order from order info and orders tables
    cursor = cnx.cursor()
    setPickedUpQuery = ('UPDATE orderinfo SET isOrderPickedUp=1 WHERE orderID=' + str(orderId))
    cursor.execute(setPickedUpQuery)
    cnx.commit()
    cursor.close()
    print('Order ' + str(orderId) + ' has been picked up.\n')


# written by Jose
def clearPickedOrders(cnx):
    cursor = cnx.cursor()
    clearPickedQuery = ('DELETE FROM orderinfo WHERE isOrderPickedUp=1')
    cursor.execute(clearPickedQuery)
    cnx.commit()
    orderDeleteParityCheck(cnx)
    cursor.close()
    print('Cleared\n')


# written by Jose, ensures that there are no orphaned Order or orderinfo tables when a row in either is deleted.
def orderDeleteParityCheck(cnx):
    cursor = cnx.cursor()
    selectOrdersQuery = ('SELECT orderID FROM orders')
    cursor.execute(selectOrdersQuery)
    ord1 = cursor.fetchall()
    selectOrderInfosQuery = ('SELECT orderID FROM orderinfo')
    cursor.execute(selectOrderInfosQuery)
    ord2 = cursor.fetchall()

    match = 0
    for x in ord1:
        for y in ord2:
            if x[0] == y[0]:
                match = 1
        if match == 0:
            deleteOrderQuery = ('DELETE FROM orders WHERE orderID=' + str(x[0]))
            cursor.execute(deleteOrderQuery)
            cnx.commit()

    match = 0
    for x in ord2:
        for y in ord1:
            if x[0] == y[0]:
                match = 1
        if match == 0:
            deleteOrderInfoQuery = ('DELETE FROM orderinfo WHERE orderID=' + str(x[0]))
            cursor.execute(deleteOrderInfoQuery)
            cnx.commit()
    cursor.close()


# pay for order - written by Jose
def payOrder(cnx, total, customerID):
    cursor = cnx.cursor()
    # access account balance
    getAccountNoQuery = ('SELECT A.accountNo FROM account A, customer C WHERE A.accountNo=C.accountNo AND C.customerID='+ str(customerID))
    cursor.execute(getAccountNoQuery)
    AccountNo = cursor.fetchone()[0]
    cursor.execute('SELECT balance FROM account A WHERE A.accountNo=' + str(AccountNo))
    balance = cursor.fetchone()[0]
    balance = float(balance)
    total = float(total)
    # if, order total is greater than account balance, then decline order
    if total > balance:
        print('Insufficient funds in account, order cancelled.\n')
        cursor.close()
        return False
    # else, decrease balance by order total
    else:
        balance -= total
        updateBalanceQuery = ('UPDATE Account SET balance=' + str(balance) + ' WHERE AccountNo=' + str(AccountNo))
        cursor.execute(updateBalanceQuery)
        cnx.commit()
        # notify that payment went through
        print('Payment processed.')
        cursor.close()
        return True

#view and add money to account balance - written by Jose
def balanceFunc(cnx, customerID):
    cursor = cnx.cursor()
    #access account balance
    getAccountNoQuery = ('SELECT A.accountNo FROM Account A, Customer C WHERE A.accountNo=C.accountNo AND C.customerID=' + str(customerID))
    cursor.execute(getAccountNoQuery)
    AccountNo = cursor.fetchone()[0]
    getBalanceQuery = ('SELECT balance FROM Account A WHERE A.accountNo=' + str(AccountNo))
    cursor.execute(getBalanceQuery)
    balance = cursor.fetchone()[0]
    balance = float(balance)
    print("Current account balance: $" + str(balance) + "\n")
    command = input("Would you like to change your account balance? Y/N: \n")
    if command == 'Y':
        newbalance = input("Enter amount to be added \n")
        newbalance=float(newbalance)
        if newbalance<0:
            print("Please enter an amount > 0")
            return
        balance+=newbalance
        updateBalanceQuery = ('UPDATE Account SET balance=' + str(balance) + ' WHERE accountNo=' + str(AccountNo))
        cursor.execute(updateBalanceQuery)
        cnx.commit()
        print("$"+str(newbalance)+" added to your account.")
        print("New balance is: $"+str(balance))


