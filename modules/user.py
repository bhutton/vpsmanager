from flask import Flask, render_template, json, request, redirect, session, g
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

import modules.database

app = Flask(__name__)


app.config.from_object(__name__)

#mysql = MySQL()

# MySQL configurations
"""app.config['MYSQL_DATABASE_USER']       = 'ah_vps'
app.config['MYSQL_DATABASE_PASSWORD']   = 'Mnie7865sh'
app.config['MYSQL_DATABASE_DB']         = 'ah_vps'
app.config['MYSQL_DATABASE_HOST']       = 'mysql'
mysql.init_app(app)"""

class User:

    def __init__(self):
        #self.conn = mysql.connect()
        #self.cursor = self.conn.cursor()
        self.db = modules.database.DB_Users()

    def getUsers(self):
        return self.db.getUsers()

    def getUser(self,id):
        """User.id = id

        self.cursor.execute("select id,name,email,password from users where id = %s",(User.id,))
        User.row = self.cursor.fetchone()
        return User.row"""

        #db = modules.database.MySQL()
        return self.db.getUser(id)
    
    def createUser(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password
        
        self.hashed_password = generate_password_hash(self.password)

        """self.cursor.callproc('sp_createUser',(User.name,User.email,User.hashed_password))
        self.data = self.cursor.fetchall()
        self.conn.commit()

        return self.data"""

        return self.db.createUser(self.name,self.email,self.hashed_password)

    def deleteUser(self,id):
        return self.db.deleteUser(id)
        """User.id = id

        self.cursor.execute("delete from users where id = %s",(User.id,))
        self.data = self.cursor.fetchall()
        self.conn.commit()

        return self.data"""

    def checkUser(self,email,password):
        User.email = email
        User.password = password

        """get_user = "select password from users where email=%s"
        self.cursor.execute(get_user,(User.email,))
        data = self.cursor.fetchone()"""

        data = self.db.checkUser(self.email)

        if (check_password_hash(str(data[0]),User.password)):
    	    return "valid"
        else: 
            return "invalid"

    def checkUsername(self,name):
        """User.name = name

        self.cursor.callproc('sp_validateLogin',(User.name,))
        data = self.cursor.fetchall()"""

        #return data

        return self.db.checkUsername(name)


    def checkPassword(self,newPassword,repPassword):
        User.newPassword = newPassword
        User.repPassword = repPassword

        if (len(User.newPassword) > 0):
            if (User.newPassword == User.repPassword):
                return "match"
            else:
                return "missmatch"
        else:
            return "invalid"

    def updateUser(self,id,name,email,password=''):
        if (len(password) > 0):
            self.hashed_password = generate_password_hash(password)
            return self.db.updateUserandPassword(name,email,self.hashed_password,id)
        else:
            return self.db.updateUser(name,email,id)
