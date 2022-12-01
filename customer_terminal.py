import database_operations

cnx=database_operations.connectToDatabase()

def checkCustomer(username, password):
    result=database_operations.isValidUser(cnx, username, password)
    #if result = 1, then username/password is valid
    #if result = -1, no such user
    #if result = -2, user exists, but pass does not match
    return result

def registerCustomer(name, email, passWord):
    # hash the password and then store
    connectionObj = database_operations.connectToDatabase()
    database_operations.addCustomer(connectionObj, name, email, passWord)
    cnx.commit();

def insertToMenu():
    cursor = cnx.cursor()
    query_add_order = ("INSERT INTO Menu "
                         "(ItemID, RestaurantID, ItemName, Price) "
                         "VALUES (%d, %d, %s, %d)")
    order = (ItemID, RestaurantID, ItemName, Price)
    cursor.execute(query_add_order, order)
    cnx.commit();


def insertRestaurant():
    cursor = cnx.cursor()
    restaurant = (RestaurantID, restaurantName)
    query_add_restaurant = ("INSERT INTO Restaurant "
                            "(RestaurantID, restaurantName) "
                         "VALUES (%d, %s)")
    cursor.execute(query_add_restaurant, restaurant)
    cnx.commit();


def placeOrderCustomer(restaurantId, itemId, quantity):
    database_operations.addOrderNew(cnx, restaurantId, itemId, quantity)


#def placeOrderCustomer(rID, itemID):
#    cursor = cnx.cursor()
#    restaurantsID = ('SELECT RestaurantID FROM Restaurant')
#    cursor.execute(restaurantsID, rID)
#    rID=cursor.fetchall()
#    itemsID = ("SELECT ItemID FROM Menu")
#    iID = (ItemID)
#    placingOrder = ("UPDATE Orders SET RestaurantID = restaurantsID WHERE ItemID = itemsID")
#    cursor.execute(placingOrder, rID)
#    #cursor.execute(itemsID, iID)#here
#    cnx.commit();

def checkStatusOrder():
    cursor = cnx.cursor()#test
    status = ("SELECT isOrderPickedUp FROM Orders")
    pickedup = (isOrderPickedUp)
    cursor.execute(status, pickedup)
    if cursor.fetchone() == 0:
        return -1
    return 1
    cnx.commit();

def payment():
    cursor = cnx.cursor()
    payment = ("SELECT (Account.balance-Orders.totalprice) AS balance FROM table Orders CROSS JOIN table Account WHERE Orders.totalprice = Item.cost")
    cost = (balance)
    cursor.execute(payment, cost);
    cnx.commit();

if __name__ == '__main__':
    
    cursorMain=cnx.cursor(buffered=True)
    print("\n Hello, Welcome to QElim. \n PLease Sign In/Sign Up to place an order \n")
    isUserRegisteredInput = input("\n If you're already a registered user? Y/N \n")

    if isUserRegisteredInput == "Y" or isUserRegisteredInput == "y":
        # ask user to enter username /password
        username = input(" \n Please enter your username (email address): \n ")
        passWord = input("\n Please enter your password: \n")
        # check if the user is registered
        if checkCustomer(username,passWord) == 1:
     #   if username == ("SELECT (email) FROM Customer") and passWord == ("SELECT (pass) FROM Customer"):
            choice = input("\n What operation would you like to perform? \n 1. Place an order \n 2. Check status of your order \n ")
            choice=int(choice)
            if choice == 1:
                listoforders = ("SELECT ItemId, RestaurantID, ItemName FROM menu")
                cursorMain.execute(listoforders)
                menuItemList=cursorMain.fetchall()
                for item in menuItemList:
                    itemId=item[1]
                    restaurantID=item[2]
                    itemName=item[3]
                    print(itemId, RestaurantID, ItemName)
                
                itemId=input("\nEnter Item Id\n")
                restaurantID=input("\nEnter Restaurant Id\n")
                quantity=input("\nquantity\n")
                placeOrderCustomer(RestaurantId, itemId, quantity)
            if choice == 2:
                checkStatusOrder()
    else:
        # sign up the user
        n = input(" \n Please enter your Name: \n ")
        e = input(" \n Please enter the email: \n ")
        p = input("\n Please enter the password: \n ")
        emailexists = ("SELECT count(*) FROM customer WHERE email = %s")
        executeemail = (e)
        cursorMain.execute(emailexists, (executeemail,))
        #print(emailexists)
 #       quit()
        if emailexists == 1:
            print("Your email already has an account.")
            n = input(" \n Please enter your Name: \n ")
            e = input(" \n Please enter the email: \n ")
            p = input("\n Please enter the password: \n ")
        
        accountcreation = ("INSERT INTO account (balance) VALUES %d")
        starterValue = 0.00
        cursorMain.execute(accountcreation,(starterValue))
        accountNum = cursorMain.execute("SELECT accountNo FROM account WHERE balance = %d")
        print(accountNum)
        signedup = ("INSERT INTO customer (accountNo, customerName, email, pass) VALUES (%d, %s, %s, %s)")
        signupinfo = (accountNum, n, e, p)
        cursorMain.execute(signedup, (signupinfo))
        # we'll have to see how to create functions for payments

        registerCustomer(n, e, p)


        # Jose
        # once signed up/ signed in -> will show all the restaurants name
        # customer should select a restaurant
        # once the restaurant is selected show all the item names for the restaurant
        # customer will select a set of items and their quantity

        # Megan
        # payment and place order

cnx.close()

