from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

def connectToDatabase():
    cnx = mysql.connector.connect(user='root', password='zip85;ski',
                                  host='127.0.0.1', port='3306',
                                  database='app_schema')
    return cnx


# def addMenu()

def addAccount(cnx, balance):
    cursor = cnx.cursor()
    query_add_account = ("INSERT INTO account "
                          "(balance)"
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
    addCustomer(cnx, "Jose", "hello1@gmail.com", "hello1")
    cnx.close()