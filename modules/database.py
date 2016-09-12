from flask import Flask
from flaskext.mysql import MySQL
import ConfigParser
import os 

app = Flask(__name__)
app.config.from_object(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))

mysql = MySQL()

# Get MySQL configurations from configuration.cfg
Config = ConfigParser.ConfigParser()
Config.read("{}/../configuration.cfg".format(dir_path))
app.config['MYSQL_DATABASE_USER']       = Config.get('Database','mysql_username')
app.config['MYSQL_DATABASE_PASSWORD']   = Config.get('Database','mysql_password')
app.config['MYSQL_DATABASE_DB']         = Config.get('Database','mysql_dbname')
app.config['MYSQL_DATABASE_HOST']       = Config.get('Database','mysql_dbhost')
mysql.init_app(app)


class DB_Users:

	def __init__(self):
		self.conn = mysql.connect()
		self.cursor = self.conn.cursor()

	def getUsers(self):
		self.cursor.execute("select id,name,email,password from users")
		return self.cursor.fetchall()

	def getUser(self,id):
		self.cursor.execute("select id,name,email,password from users where id = %s",(id,))
		return self.cursor.fetchone()

	def createUser(self,name,email,password):
		self.cursor.callproc('sp_createUser',(name,email,password))
		self.conn.commit()

		self.cursor.execute('SELECT last_insert_id()')
		self.vps_id = self.cursor.fetchone()
		return self.vps_id[0]

	def deleteUser(self,id):
		self.cursor.execute("delete from users where id = %s",(id,))
		self.data = self.cursor.fetchall()
		self.conn.commit()
		return self.data

	def checkUser(email):
		get_user = "select password from users where email=%s"
		self.cursor.execute(get_user,(email,))
		return self.cursor.fetchone()

	def checkUsername(self,name):
		self.cursor.callproc('sp_validateLogin',(name,))
		return self.cursor.fetchall()

	def updateUserandPassword(self,name,email,password,id):
		update_user = "update users set name=%s,email=%s,password=%s where id=%s"
		self.cursor.execute(update_user,(name,email,password,id))
		self.data = self.cursor.fetchall()
		self.conn.commit()
		return self.data

	def updateUser(self,name,email,id):
		update_user = "update users set name=%s,email=%s where id=%s"
		self.cursor.execute(update_user,(name,email,id))
		self.data = self.cursor.fetchall()
		self.conn.commit()
		return self.data


class DB_VPS:

	def __init__(self):
		self.conn = mysql.connect()
		self.cursor = self.conn.cursor()

	def getVPS(self):
		self.cursor.execute("select id,name,description,image from vps")
		return self.cursor.fetchall();

	def getIndVPS(self,id):
		get_ind_vps = ("select * from vps where id=%s")
		self.cursor.execute(get_ind_vps,(id,))
		return self.cursor.fetchall();

	def getBridge(self):
		self.cursor.execute("select id,device from bridge")
		return self.cursor.fetchall()

	def getBridgeID(self,device):
		self.cursor.execute("select id from bridge where device=%s",(device,))
		self.data =  self.cursor.fetchone()
		return self.data[0]

	def getMaxConsole(self):
		self.cursor.execute("select max(console) from vps")
		self.data = self.cursor.fetchone()
		return self.data[0]

	def getInt(self):
		self.cursor.execute("select max(device) from interface")
		self.int = self.cursor.fetchone()
		return self.int[0]

	def addDevice(self,device,vps_id,bridge_id):
		add_device  = ("insert into interface (device,vps_id,bridge_id) values (%s,%s,%s)")
		self.cursor.execute(add_device,(device,vps_id,bridge_id))
		self.data = self.cursor.fetchone()
		self.conn.commit()
		return self.data

	def delNetwork(self,id):
		self.cursor.execute("delete from interface where id=%s",(id,))
		self.data = self.cursor.fetchone()
		self.conn.commit()
		return self.data

	def addDisk(self,name,size,order,vps_id):
		add_disk = ("insert into disk (name,size,ord,vps_id) values (%s,%s,%s,%s)")

		self.cursor.callproc('sp_createDisks',(name,order,size,vps_id))

		self.conn.commit()

		
		self.cursor.execute('SELECT last_insert_id()')
		self.vps_id = self.cursor.fetchone()

		return self.vps_id[0]

	def delDisk(self,id):
		self.id = int(id)

		self.cursor.execute("delete from disk where id=%s",(self.id,))
		self.data = self.cursor.fetchone()
		self.conn.commit()

		return self.data

	def getDisks(self,id):
		self.cursor.execute("select * from disk where vps_id=%s",(id,))
		return self.cursor.fetchall()

	def getIntVPS(self,id):
		get_int_vps = ("select interface.id,interface.device,interface.vps_id,bridge.device from interface,bridge where vps_id=%s and interface.bridge_id = bridge.id")
		self.cursor.execute(get_int_vps,(id,))
		return self.cursor.fetchall()

	def updateVPS(self,name,description,ram,id):
		self.cursor.execute("update vps set name=%s,description=%s,ram=%s where id=%s",(name,description,ram,id))
		self.row = self.cursor.fetchall()

		self.conn.commit()

		return self.row

	def createVPS(self,name,description,ram,con,image):
		#self.cursor.callproc('sp_createVPS',(name,description,ram,con,image))
		self.cursor.execute("insert into vps (name,description,ram,console,image) values (%s,%s,%s,%s,%s)",(name,description,ram,con,image))
		self.conn.commit()

		self.cursor.execute('SELECT last_insert_id()')
		self.vps_id = self.cursor.fetchone()

		return self.vps_id[0]

	def createDisk(self,name,order,disk,vps_id):
		self.cursor.callproc('sp_createDisks',(name,order,disk,vps_id))

		self.conn.commit()

		return str(self.vps_id[0])

	def delVPS(self,id):
		self.cursor.execute("delete from vps where id=%s",(id,))
		self.data = self.cursor.fetchone()
		self.conn.commit()

		return self.data

