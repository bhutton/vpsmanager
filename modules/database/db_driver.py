import os
import configparser

from flask import Flask
from flaskext.mysql import MySQL
import sqlite3 as sqlite

dir_path = os.path.dirname(os.path.realpath(__file__))

mysql = MySQL()

app = Flask(__name__)
app.config.from_object(__name__)

# Get MySQL configurations from configuration.cfg
Config = configparser.ConfigParser()
Config.read("{}/../../configuration.cfg".format(dir_path))
app.config['MYSQL_DATABASE_USER'] = Config.get('Database','database_username')
app.config['MYSQL_DATABASE_PASSWORD'] = Config.get('Database','database_password')
app.config['MYSQL_DATABASE_DB'] = Config.get('Database','database_name')
app.config['MYSQL_DATABASE_HOST'] = Config.get('Database','database_host')
app.config['MYSQL_DATABASE_DRIVER'] = Config.get('Database','database_driver')
mysql.init_app(app)

class DatabaseConnectivity:

    def __init__(self):
        try:
            self.database_driver = os.environ['DB_DRIVER']
        except:
            self.database_driver = Config.get('Database', 'database_driver')

        self.db_connect()

    def __exit__(self):
        try:
            self.cnx.close()
        except:
            print('failed to close database')

    @property
    def db_connect(self):
        if self.database_driver == 'mysql':
            return self.db_connect_mysql
        elif self.database_driver == 'sqlite':
            return self.db_connect_sqlite

    def db_connect_sqlite(self):
        try:
            self.cnx = sqlite.connect(":memory:")
            self.cursor = self.cnx.cursor()
            self.initialise_sqlite_database()
            self.database_connected = True
        except:
            self.database_connected = False
            return 'an error occured'

    def db_connect_mysql(self):
        try:
            db_connector = MySQL()
            db_connector.init_app(app)
            self.cnx = db_connector.connect()
            self.cursor = self.cnx.cursor()
            self.database_connected = True
        except:
            self.database_connected = False
            return "error connecting to database"

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
            "INSERT INTO users VALUES(21,'ben@benhutton.com.au','fred bloggs1','abc1234')"
        )



    def db_return_cursor(self):
        return self.cursor

    def db_execute_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cnx.commit()
        except:
            return "error running query"

    def db_get_row(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def db_get_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

