import bcrypt
import re

def hashPassword(password):
    password = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed

def checkPassword(userEnteredPasswordStr, storedHash):
    userEnteredPasswordBytes = bytes(userEnteredPasswordStr, 'utf-8')
    storedHashBytes = bytes(storedHash, 'utf-8')
    #print("userEnteredPasswordBytes , ", userEnteredPasswordBytes)
    #print("storedHashBytes: ", storedHashBytes)
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(storedHashBytes, salt)
    #isPasswordSame = bcrypt.checkpw(userEnteredPasswordBytes, storedHashBytes)
    isPasswordSame = bcrypt.checkpw(userEnteredPasswordBytes, hash)
    #print(isPasswordSame)
    return isPasswordSame


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def isValidEmail(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False

# if __name__ == '__main__':
#     hashVal = hashPassword("hello")
#     print("type -> ", type(hashVal))

    # print(checkPassword('jkfjrf', "$2b$12$c9Zw1KnTQOkjXB0tYFjvmOq3F/mvCgLjnEi1UuLQ33Y3V6Q4bq.aa"))