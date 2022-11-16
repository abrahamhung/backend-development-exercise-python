import unittest
from datetime import datetime


class logger:
    def log(self, s):
        print(s)

class storage:
    def __init__(self):
        self.accounts = {}
    
    def storeaccount(self, username, password):
        if self.accounts.get(username) is not None: 
            return "UAE"
        self.accounts[username] = password
        return True
    
    def verifyaccount(self, username, password):
        if self.accounts.get(username) is None:
            return "NaN"
        return self.accounts[username] == password


class usermanager:
    def __init__(self, store, log):
        self.store = store
        self.logger = log
        self.loginstat = [0,0]

    def adduser(self, username):

        password = "securepassword" # presumably there will be some password generation logic

        if not self.store.storeaccount(username, password): return False

        self.logger.log("new user " + username + "added")
        return password

    def verifyuser(self, username, password):
        self.loginstat[0] += 1
        if datetime.now().weekday() == 6: 
            return "Not open on Sunday"
        
        result = self.store.verifyaccount(username, password)
        if result == True: 
            self.loginstat[1] += 1
            return None
        elif result == False:
            return "verification failed"
        elif result == "NaN":
            return "user does not exist"
        
    def getauthenticationstats(self):
        return self.loginstat

class TestUsermanager(unittest.TestCase):
    def test_createandverifyuser(self):
        data = storage()
        log = logger()
        manager = usermanager(data, log)

        # add account
        password = manager.adduser("user1")
        self.assertFalse(password == None)  #password does exist

        #login success
        verification = manager.verifyuser("user1", password)
        self.assertTrue(verification == None)

        #login fail
        verification = manager.verifyuser("user1", "notpword")
        self.assertTrue(verification == "verification failed")

    
    def test_statistics(self):
        data = storage()
        log = logger()
        manager = usermanager(data, log)

        # add account
        password = manager.adduser("user1")

        manager.verifyuser("user1", password)
        self.assertTrue([1,1] == manager.getauthenticationstats())

        manager.verifyuser("user1", "notpword")
        self.assertTrue([2,1] == manager.getauthenticationstats())

if __name__ == '__main__':
    unittest.main()



