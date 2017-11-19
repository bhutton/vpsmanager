from flask import Flask

import modules.database.db_driver as db_driver

# import sqlite3 as sqlite

app = Flask(__name__)
app.config.from_object(__name__)


class DB_Users(db_driver.DatabaseConnectivity):
    def __init__(self):
        super().__init__()
        self.db_connection()

    def __exit__(self):
        super().__exit__()

    def getUsers(self):
        return self.db_get_all("select id,name,email,password from users")

    def getUser(self, id):
        return self.db_get_row("select id,name,email,password from users where id = {}". format(id))

    def getUserByEmail(self, email):
        return self.db_get_row("select id,name,email,password from users where email='{}'".format(email))

    def createUser(self, name, email, password):
        self.cursor.callproc('sp_createUser', (name, email, password))
        self.conn.commit()

        self.cursor.execute('SELECT last_insert_id()')
        self.vps_id = self.cursor.fetchone()
        return self.vps_id[0]

    def deleteUser(self, id):
        self.cursor.execute("delete from users where id = %s", (id,))
        self.data = self.cursor.fetchall()
        self.conn.commit()
        return self.data

    # def checkUser(email):
    #     get_user = "select password from users where email=%s"
    #     self.cursor.execute(get_user, (email,))
    #     return self.cursor.fetchone()

    def checkUsername(self, name):
        self.cursor.callproc('sp_validateLogin', (name,))
        return self.cursor.fetchall()

    def updateUserandPassword(self, name, email, password, id):
        try:
            self.db_execute_query(
                'update users set name="{}",email="{}",password="{}" where id={}'
                .format(name,email,password,id)
            )
        except:
            return "update failed"

        return "update successful"

    def updateUser(self, name, email, id):
        update_user = "update users set name=%s,email=%s where id=%s"
        return self.db_execute_query(update_user)


class DB_VPS(db_driver.DatabaseConnectivity):
    def __init__(self):
        super().__init__()
        self.db_connection()

    def __exit__(self):
        try:
            self.conn.close()
        except:
            print("Error closing database")

    def getVPS(self):
        return self.db_get_all("select id,name,description,image from vps")

    def getIndVPS(self, id):
        return self.db_execute_query("select * from vps where id={}".format(id))

    def getBridge(self):
        self.cursor.execute("select id,device from bridge")
        return self.cursor.fetchall()

    def getBridgeID(self, device):
        self.cursor.execute("select id from bridge where device=%s", (device,))
        self.data = self.cursor.fetchone()
        return self.data[0]

    def getMaxConsole(self):
        self.cursor.execute("select max(console) from vps")
        self.data = self.cursor.fetchone()
        return self.data[0]

    def getInt(self):
        self.cursor.execute("select max(device) from interface")
        self.int = self.cursor.fetchone()
        return self.int[0]

    def addDevice(self, device, vps_id, bridge_id):
        add_device = 'insert into interface (device,vps_id,bridge_id) values ({},{},{})'.format(device,vps_id,bridge_id)
        return self.db_execute_query(add_device)

    def delNetwork(self, id):
        #self.cursor.execute("delete from interface where id=" + str(id))
        self.db_execute_query("delete from interface where id=" + str(id))
        # self.data = self.cursor.fetchone()
        #self.conn.commit()
        return "deleted"

    def addDisk(self, name, size, order, vps_id):
        add_disk = ("insert into disk (name,size,ord,vps_id) values (%s,%s,%s,%s)")

        self.cursor.callproc('sp_createDisks', (name, order, size, vps_id))

        self.conn.commit()

        self.cursor.execute('SELECT last_insert_id()')
        self.vps_id = self.cursor.fetchone()

        return self.vps_id[0]

    def delDisk(self, id):
        self.id = int(id)

        self.cursor.execute("delete from disk where id=%s", (self.id,))
        self.data = self.cursor.fetchone()
        self.conn.commit()

        return self.data

    def getDisks(self, id):
        self.cursor.execute("select * from disk where vps_id=%s", (id,))
        return self.cursor.fetchall()

    def getDisk(self, id):
        self.cursor.execute("select * from disk where id=%s", (id,))
        return self.cursor.fetchone()

    def updateDisk(self, id, name):
        self.cursor.execute("update disk set name=%s where id=%s", (name, id))

        self.data = self.cursor.fetchone()
        self.conn.commit()

        return self.data

    def getIntVPS(self, id):
        get_int_vps = (
        "select interface.id,interface.device,interface.vps_id,bridge.device from interface,bridge where vps_id=%s and interface.bridge_id = bridge.id")
        self.cursor.execute(get_int_vps, (id,))
        return self.cursor.fetchall()

    def updateVPS(self, name, description, ram, id, path, start_script, stop_script, image):
        self.cursor.execute(
            "update vps set name=%s,description=%s,ram=%s,path=%s,startscript=%s,stopscript=%s,image=%s where id=%s",
            (name, description, ram, path, start_script, stop_script, image, id))
        self.row = self.cursor.fetchall()

        self.conn.commit()

        return self.row

    def createVPS(self, name, description, ram, con, image):
        self.cursor.execute("insert into vps (name,description,ram,console,image) values (%s,%s,%s,%s,%s)",
                            (name, description, ram, con, image))
        self.conn.commit()

        self.cursor.execute('SELECT last_insert_id()')
        self.vps_id = self.cursor.fetchone()

        return self.vps_id[0]

    def createDisk(self, name, order, disk, vps_id):
        self.cursor.callproc('sp_createDisks', (name, order, disk, vps_id))

        self.conn.commit()

        return str(self.vps_id[0])

    def delVPS(self, id):
        self.cursor.execute("delete from vps where id=%s", (id,))
        self.data = self.cursor.fetchone()
        self.conn.commit()

        return self.data

    def getTrafficData(self, interface):
        self.cursor.execute(
            "(SELECT `LastIpkts`,`LastOpkts`,`timestamp`,`index` FROM `traffic` where `interface`=%s ORDER BY `index` DESC LIMIT 289) ORDER BY `index` ASC",
            (interface,))
        return self.cursor.fetchall()
