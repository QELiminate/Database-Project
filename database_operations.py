from __future__ import print_function
import mysql.connector

import utility_functions


def connectToDatabase():
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1', port='3306',
                                  database='app_schema'
    return cnx

def getLastOrderId(cnx):
    cursor = cnx.cursor()
    cursor.execute('SELECT orderID FROM orders ORDER BY orderID DESC LIMIT 1')
    lastOrderInfo = cursor.fetchone()
    if lastOrderInfo is None:
        return 0
    else:
        return lastOrderInfo[0]

def isValidUser(cnx, email, passoword):
    cursor = cnx.cursor()

    cursor.execute('SELECT * FROM customer where email ="' + email +'"')
    customerInfo = cursor.fetchone()
    if customerInfo is None:
        return -1
    else:
        passwordInDB = customerInfo[4]
        # compare entered password with passwordInDB
        isPasswordCorrect = utility_functions.checkPassword(passoword, passwordInDB)
        if not isPasswordCorrect:
            return -2
        else:
            return 1
    cursor.close()
def showRestaurants(cnx):
    # written by Jose
    cursor = cnx.cursor()
    showRestQuery = ('SELECT * FROM Restaurant')
    cursor.execute(showRestQuery)
    result = cursor.fetchall()
    print ('Restaurant ID       Restaurants:\n')
    for r in result:
        print(str(r[0]) +'      '+ r[1] +'\n')
    cursor.close()

def isValidRestaurant(cnx, restaurantId):
    cursor = cnx.cursor()
    getRestaurant = 'SELECT * from Restaurant R where R.RestaurantID = '+ str(restaurantId)
    cursor.execute(getRestaurant)
    if cursor.fetchone() is None:
        return -1
    else:
        return 1

def isValidItem(cnx, itemId, restaurantID):
    cursor = cnx.cursor()
    cursor.execute('SELECT * from Menu M where M.ItemID = '+ str(itemId) + ' and M.RestaurantID= ' + str(restaurantID))
    if cursor.fetchone() is None:
        return -1
    else:
        return 1
def showRItems(cnx, RSelect):
    # written by Jose
    cursor = cnx.cursor()
    showRItemQuery = ('SELECT ItemID, ItemName, Price FROM Menu M, Restaurant R WHERE M.RestaurantID=R.RestaurantID AND R.RestaurantID=' + RSelect)
    cursor.execute(showRItemQuery)
    result = cursor.fetchall()
    print('Menu for ' + RSelect + '\n')
    print('Item ID:           Price: \n')
    for r in result:
        print(str(r[0]) + '           ' + str(r[1]) + '\n')
    cursor.close()

def addOrder(cnx, orderId, restaurantId, itemId, quantity):
    # written by Tarun
    cursor = cnx.cursor()
    query_add_orders = ("INSERT INTO orders "
                         "(orderID, ItemID, RestaurantID, Quantity) "
                         "VALUES (%s, %s, %s, %s)")
    values = (orderId, itemId, restaurantId, quantity)
    cursor.execute(query_add_orders, values)
    cnx.commit()

    cursor.close()



def addOrderInfo(cnx, totalPrice, readyTime, orderId, restaurantId):
    # written by Tarun
    cursor = cnx.cursor()
    query_add_account = ("INSERT INTO orderinfo "
                         "(orderID, isReady, readyTime, totalPrice, isOrderPickedUp, orderExpirationDateTime, RestaurantID) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    # orderExpirationDateTime = readyTime + 1 hr
    values = (orderId, False, readyTime, totalPrice, False, readyTime, restaurantId)
    cursor.execute(query_add_account, values)
    cnx.commit()

    cursor.close()


def addAccount(cnx, balance):
    # written by Tarun
    cursor = cnx.cursor()
    query_add_account = ("INSERT INTO account "
                          "(balance) "
                          "VALUES (%s)")
    values = (balance, )
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


if __name__ == '__main__':
    cnx = connectToDatabase()
    # addCustomer(cnx, "Jose", "hello1@gmail.com", "hello1")
    # showRestaurants(cnx)
    # showRItems(cnx, "McDonalds")
    # isValidUser(cnx, "hello@gmail.com", "hello")
    cnx.close()

