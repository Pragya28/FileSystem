from pwinput import pwinput
import json

from login import createAccount, loginAccount
from keys import getMyPrivateKey, getSharedKey
from fileFunctions import createFile, updateFile, viewFile
from gitCommands import gitPush

def homePage():
    print('''
WHAT DO YOU WANT TO DO?
1. Login My Account
2. Create New Account
Press q to Quit 
    ''')
    option = input("Your option: ")
    if not option.isdigit():
        print("Exiting Application...")
        return False, None
    else:
        option = int(option)
        if option == 1:
            uname = input("Enter your username: ")
            pwd = pwinput("Enter your password: ", mask="*")
            with open('users.json', 'r') as f:
                data = json.load(f)
            names = [x['username'] for x in data]
            if uname not in names:
                print('''
Invalid credentials
Going back to home page                
                ''')
                homePage()
            else:
                idx = names.index(uname)
                status, info = loginAccount(data[idx], pwd)
                if not status:
                    print('''
Invalid credentials
Going back to home page                
                    ''')
                    homePage()
                else:
                    print("Logged In")
                    return True, info
        elif option == 2:
            status, info = createAccount()
            if not status:
                print('''
Account creation failed
Going back to home page                
                ''')
                homePage()
            else:
                print("Account created")
                return True, info
        else:
            print('''
Invalid option
Exiting Application...
            ''')
            return False, None

def optionsPage(myData):
    print('''
WHAT DO YOU WANT TO DO WITH YOUR FILES?
1. Create
2. View
3. Update    
Press q to Quit 
    ''')
    option = input("Your option: ")
    if not option.isdigit():
        print("Exiting Application...")
        return False, None
    else:
        option = int(option)
        if option not in [1, 2, 3]:
            print('''
Invalid option
Try Again...
            ''')
            optionsPage(myData)
        else:
            with open('users.json', 'r') as f:
                userData = json.load(f)
            usernames = [x['username'] for x in userData]
            otherUser = None
            while otherUser not in usernames:
                otherUser = input("Enter username of receipent: ")
            idx = usernames.index(otherUser)
            publicKey = userData[idx]['publickey']
            privateKey = getMyPrivateKey(myData['passkey'], myData['secret'])
            sharedKey = getSharedKey(publicKey, privateKey)
        if option == 1:
            try:
                createFile(myData['username'], otherUser, sharedKey)
                print("Your file is created")
                print("#"*100)
                gitPush()
            except Exception as e:
                print(str(e))
        elif option == 2:
            try:
                viewFile(sharedKey)
            except Exception as e:
                print(str(e))
        elif option == 3:
            try:
                updateFile(myData['username'], otherUser, sharedKey)
                print("Your file is updated")
                print("#"*100)
                gitPush()
            except Exception as e:
                print(str(e))
        optionsPage(myData)
        
