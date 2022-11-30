# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import database_operations



# when the customer is registering, we'll ask the customer to create an payment account and add balance to it, after the payment account is added
name = input(" \n Please enter your Name: \n ")
email = input(" \n Please enter the email: \n ")
passWord = input("\n Please enter the password: \n ")

emailexists = ("SELECT count(*) FROM customer WHERE email = e")
execute(emailexists)
if (emailexists == 1) {
    print("Your email already has an account.")
    n = input(" \n Please enter your Name: \n ")
    e = input(" \n Please enter the email: \n ")
    p = input("\n Please enter the password: \n ")
    }

execute("INSERT INTO customer values(n, e, p)")
payment = input("\n Please enter your balance: \n ")
execute("INSERT INTO account ()")

# the entity which is created first, that doesn't include the foreign key



