from werkzeug import generate_password_hash, check_password_hash

import modules.database

class User:

    def __init__(self):
        self.db = modules.database.database.DB_Users()

    def getUsers(self):
        return self.db.getUsers()

    def getUserByEmail(self, email):
        return self.db.getUserByEmail(email)

    def getUser(self,id):
        return self.db.getUser(id)
    
    def createUser(self,name,email,password):
        self.hashed_password = generate_password_hash(password)
        return self.db.createUser(name,email,self.hashed_password)

    def deleteUser(self,id):
        return self.db.deleteUser(id)
        
    def checkUsername(self,name):
        return self.db.checkUsername(name)

    # def checkPassword(self,newPassword,repPassword):
    #     if (len(newPassword) > 0):
    #         if (newPassword == repPassword):
    #             return "match"
    #         else:
    #             return "missmatch"
    #     else:
    #         return "invalid"

    def updateUser(self,id,name,email,password=''):
        if (len(password) > 0):
            self.hashed_password = generate_password_hash(password)
            return self.db.updateUserandPassword(name,email,self.hashed_password,id)
        else:
            return self.db.updateUser(name,email,id)
