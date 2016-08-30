from flask import Flask, render_template, json, request, redirect, session, g
from flaskext.mysql import MySQL

app = Flask(__name__)


app.config.from_object(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER']       = 'ah_vps'
app.config['MYSQL_DATABASE_PASSWORD']   = 'Mnie7865sh'
app.config['MYSQL_DATABASE_DB']         = 'ah_vps'
app.config['MYSQL_DATABASE_HOST']       = 'mysql'
mysql.init_app(app)

class User:

    def __init__(self):
        self.conn = mysql.connect()
        self.cursor = self.conn.cursor()

    def getUsers(self):
    	
        self.cursor.execute("select id,name,email,password from users")    
        User.row = self.cursor.fetchall()
        return User.row

    def getUser(self,id):
        User.id = id

        self.cursor.execute("select id,name,email,password from users where id = %s",(User.id,))
        User.row = self.cursor.fetchone()
        return User.row
    
    def createUser(self,name,email,password):
        User.name = name
        User.email = email
        User.password = password
        
        User.hashed_password = generate_password_hash(User.password)

        self.cursor.callproc('sp_createUser',(User.name,User.email,User.hashed_password))
        self.data = self.cursor.fetchall()
        self.conn.commit()

        return self.data

    def deleteUser(self,id):
        User.id = id

        self.cursor.execute("delete from users where id = %s",(User.id,))
        self.data = self.cursor.fetchall()
        self.conn.commit()

        return self.data

    def checkUser(self,email,password):
        User.email = email
        User.password = password

        get_user = "select password from users where email=%s"
        self.cursor.execute(get_user,(User.email,))
        data = self.cursor.fetchone()

        if (check_password_hash(str(data[0]),User.password)):
    	    return "valid"
        else: 
            return "invalid"

    def checkUsername(self,name):
        User.name = name

        self.cursor.callproc('sp_validateLogin',(User.name,))
        data = self.cursor.fetchall()

        return data

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
        User.id = id
        User.name = name
        User.email = email
        User.password = password

        if (len(User.password) > 0):
            User.hashed_password = generate_password_hash(User.password)
            update_user = "update users set name=%s,email=%s,password=%s where id=%s"
            self.cursor.execute(update_user,(User.name,User.email,User.hashed_password,User.id))
        else:
            update_user = "update users set name=%s,email=%s where id=%s"
            self.cursor.execute(update_user,(User.name,User.email,User.id))

        data = self.cursor.fetchone()
        self.conn.commit()
        return "User Updated"