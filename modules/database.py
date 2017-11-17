from flask import Flask
from flaskext.mysql import MySQL
import configparser
# import sqlite3 as sqlite
import os

app = Flask(__name__)
app.config.from_object(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))

mysql = MySQL()

# Get MySQL configurations from configuration.cfg
Config = configparser.ConfigParser()
Config.read("{}/../configuration.cfg".format(dir_path))
app.config['MYSQL_DATABASE_USER'] = Config.get('Database','database_username')
app.config['MYSQL_DATABASE_PASSWORD'] = Config.get('Database','database_password')
app.config['MYSQL_DATABASE_DB'] = Config.get('Database','database_name')
app.config['MYSQL_DATABASE_HOST'] = Config.get('Database','database_host')
app.config['MYSQL_DATABASE_DRIVER'] = Config.get('Database','database_driver')
mysql.init_app(app)

class DatabaseConnectivity:

    def __init__(self):
        self.configuration = configparser.ConfigParser()
        self.configuration.read(
            "{}/../configuration.cfg".format(dir_path)
        )
        try:
            self.database_driver = os.environ['DB_DRIVER']
        except:
            self.database_driver = self.configuration.get(
                'Database', 'database_driver'
            )

        self.db_connection

    def __exit__(self):
        try:
            self.cnx.close()
        except:
            print('failed to close database')

    @property
    def db_connection(self):
        if self.database_driver == 'mysql':
            return self.db_connect_mysql
        elif self.database_driver == 'sqlite':
            return self.db_connect_sqlite

    @property
    def db_connect_sqlite(self):
        try:
            self.cnx = sqlite.connect(":memory:")
            self.cursor = self.cnx.cursor()
            self.initialise_sqlite_database()
            return 'connection successful'
        except:
            return 'an error occured'

    def initialise_sqlite_database(self):

        self.cursor.execute(
            "CREATE TABLE disk"
            "(id int, name text, ord int, "
            "size int, vps_id int)")
        self.cursor.execute(
            "CREATE TABLE vps "
            "(id int,name text,description text,"
            "ram int,console int,image int,path text,"
            "startscript text,stopscript text)")
        self.cursor.execute(
            "CREATE TABLE interface"
            "(bridge_id int,device int,id int,vps_id int)")
        self.cursor.execute(
            "CREATE TABLE bridge(device int,id int)")
        self.cursor.execute(
            "CREATE TABLE console(device int, id int)")

        self.cursor.execute(
            "CREATE TABLE users(id int, email text, name text, password text)"
        )

        self.cursor.execute(
            "INSERT INTO vps VALUES(878,'test','mytest'"
            ",512,1,1,'/tmp/','start','stop')"
        )

        self.cursor.execute(
            "INSERT INTO disk VALUES(878,'test',1,20,878)"
        )

        self.cursor.execute(
            "INSERT INTO interface VALUES(0,0,0,878)"
        )

        self.cursor.execute(
            "INSERT INTO users VALUES(21,'fred bloggs1','test1@email.com','abc1234'"
        )




    def db_connect_mysql(self):
        try:
            # self.database_user = self.configuration.get('Database', 'database_user')
            # self.database_password = self.configuration.get('Database', 'database_password')
            # self.database_host = self.configuration.get('Database', 'database_host')
            # self.database_name = self.configuration.get('Database', 'database_name')
            # self.raise_on_warnings = self.configuration.get('Database', 'raise_on_warnings')
            #
            # app.config['MYSQL_DATABASE_USER'] = self.database_user
            # app.config['MYSQL_DATABASE_PASSWORD'] = self.database_password
            # app.config['MYSQL_DATABASE_DB'] = self.database_name
            # app.config['MYSQL_DATABASE_HOST'] = self.database_host

            db_connector = MySQL()
            db_connector.init_app(app)
            self.cnx = db_connector.connect()
            self.cursor = self.cnx.cursor()
            self.database_connected = True
        except:
            self.database_connected = False
            return "error connecting to database"

    def db_return_cursor(self):
        return self.cursor

    def db_execute_query(self, query):
        try:
            self.cursor.execute(query)
            return self.conn.commit()
        except:
            return "error running query"

    def db_get_row(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def db_get_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()


class DB_Users(DatabaseConnectivity):
    def __init__(self):
        super().__init__()
        # self.conn = mysql.connect()
        # self.cursor = self.conn.cursor()
        self.db_connection()

    def __exit__(self):
        try:
            self.cnx.close()
        except:
            print("Error closing database")

    def getUsers(self):
        self.cursor.execute("select id,name,email,password from users")
        return self.cursor.fetchall()

    def getUser(self, id):
        self.cursor.execute("select id,name,email,password from users where id = %s", (id,))
        return self.cursor.fetchone()

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

    def checkUser(email):
        get_user = "select password from users where email=%s"
        self.cursor.execute(get_user, (email,))
        return self.cursor.fetchone()

    def checkUsername(self, name):
        self.cursor.callproc('sp_validateLogin', (name,))
        return self.cursor.fetchall()

    def updateUserandPassword(self, name, email, password, id):
        update_user = 'update users set name="{}",email="{}",password="{}" where id={}'.format(name,email,password,id)
        # update_user = 'update users set name="' + name + '",email="' + email + '",password="' + password + '" where id=' + id

        try:
            self.db_execute_query(update_user)
            # self.cursor.execute(update_user, (name, email, password, id))
            # self.data = self.cursor.fetchall()
            # self.conn.commit()
            return "update successful"
        except:
            return "update failed"

    def updateUser(self, name, email, id):
        update_user = "update users set name=%s,email=%s where id=%s"
        return self.db_execute_query(update_user)
        # self.cursor.execute(update_user, (name, email, id))
        # self.data = self.cursor.fetchall()
        # self.conn.commit()
        # return self.data


class DB_VPS(DatabaseConnectivity):
    def __init__(self):
        super().__init__()
        # self.conn = mysql.connect()
        # self.cursor = self.conn.cursor()
        self.db_connection()

    def __exit__(self):
        try:
            self.conn.close()
        except:
            print("Error closing database")

    def getVPS(self):
        #self.cursor.execute("select id,name,description,image from vps")
        #return self.cursor.fetchall();
        return self.db_get_all("select id,name,description,image from vps")

    def getIndVPS(self, id):
        get_ind_vps = ("select * from vps where id=%s")
        self.cursor.execute(get_ind_vps, (id,))
        return self.cursor.fetchall();

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
        self.data = self.db_execute_query(add_device)
        return self.data

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
