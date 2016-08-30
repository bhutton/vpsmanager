from flask import Flask, render_template, json, request, redirect, session, g
from flaskext.mysql import MySQL
import socket
import sys
import os

app = Flask(__name__)


app.config.from_object(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER']       = 'ah_vps'
app.config['MYSQL_DATABASE_PASSWORD']   = 'Mnie7865sh'
app.config['MYSQL_DATABASE_DB']         = 'ah_vps'
app.config['MYSQL_DATABASE_HOST']       = 'mysql'
mysql.init_app(app)

min_console = 100
min_device = 100
HOST, PORT = "10.128.2.1", 9999

class VPS:

    def __init__(self):
        self.conn = mysql.connect()
        self.cursor = self.conn.cursor()

    def getVPS(self):
        try:
            self.cursor.execute("select * from vps")
            VPS.row = self.cursor.fetchall();
        finally:
            return VPS.row 

    def getIndVPS(self,id):
        self.id = id

        get_ind_vps = ("select * from vps where id=%s")

        try:
            self.cursor.execute(get_ind_vps,(self.id,))
            self.row = self.cursor.fetchall();
        finally:
            return self.row

    def getBridge(self):
        get_bridge  = ("select id,device from bridge")

        try:
            self.cursor.execute(get_bridge)
            VPS.bridge = self.cursor.fetchall()
        finally:    
            return VPS.bridge

    def getBridgeID(self,device):
        VPS.device = device

        get_bridge  = ("select id from bridge where device=%s")

        try:
            self.cursor.execute(get_bridge,(VPS.device,))
            VPS.bridge = self.cursor.fetchone()
        finally:
            return VPS.bridge[0]

    def getMaxConsole(self):
        self.get_console = ("select max(console) from vps")

        try:
            self.cursor.execute(self.get_console)
            self.console = self.cursor.fetchone()

            if (self.console[0] == None):
                self.console = min_console
            else:
                self.console = int(self.console[0]) + 1
        finally:
            return self.console


    def getInt(self):
        get_int = ("select max(device) from interface")

        try:
            self.cursor.execute(get_int)
            self.int = self.cursor.fetchone()

            if (self.int[0] == None):
                self.int = min_device
            else:
                self.int = int(self.int[0]) + 1
        finally:
            return self.int

    def addDevice(self,device,vps_id,bridge_id):
        VPS.device      = int(device)
        VPS.vps_id      = int(vps_id)
        VPS.bridge_id   = int(bridge_id)

        add_device  = ("insert into interface (device,vps_id,bridge_id) values (%s,%s,%s)")

        try:
            self.cursor.execute(add_device,(VPS.device,VPS.vps_id,VPS.bridge_id))
            self.data = self.cursor.fetchone()
            self.conn.commit()
        finally:
            return self.data

    def delNetwork(self,id):
        VPS.id = id

        del_network = ("delete from interface where id=%s")

        try:
            self.cursor.execute(del_network,(VPS.id,))
            self.data = self.cursor.fetchone()
            self.conn.commit()
        finally:
            return self.data

    def getStatus(self,vps_id):
        try:
            self.data = str(vps_id)

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(self.data + ",status\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)

            if (len(received) > 0):
                status = "Running"
            else:
                status = "Stopped"
        finally:
            sock.close()
            return received

        

    def addDisk(self,name,size,order,vps_id):
        self.name    = name
        self.size    = size
        self.order   = order
        self.vps_id  = vps_id

        add_disk = ("insert into disk (name,size,ord,vps_id) values (%s,%s,%s,%s)")

        try:
            self.cursor.execute(add_disk,(self.name,self.size,self.order,self.vps_id))
            self.data = self.cursor.fetchone()
            self.conn.commit()

            #HOST, PORT = "10.128.2.1", 9999
            self.data = str(self.vps_id)

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(self.data + ",create\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
        
        return self.data

    def delDisk(self,id):
        self.id = int(id)

        del_disk = ("delete from disk where id=%s")
        self.cursor.execute(del_disk,(self.id,))
        self.data = self.cursor.fetchone()
        self.conn.commit()
        
        return self.data

    def getDisks(self,id):
        self.id = id

        get_disks = ("select * from disk where vps_id=%s")
        self.cursor.execute(get_disks,(self.id,))
        self.row = self.cursor.fetchall()

        return self.row

    def getIntVPS(self,id):
        self.id = id

        get_int_vps = ("select interface.id,interface.device,interface.vps_id,bridge.device from interface,bridge where vps_id=%s and interface.bridge_id = bridge.id")
        self.cursor.execute(get_int_vps,(self.id,))
        self.row = self.cursor.fetchall()

        return self.row

    def updateVPS(self,name,description,ram,id):
        self.name           = name
        self.description    = description
        self.ram            = ram
        self.id             = id

        update_vps  = ("update vps set name=%s,description=%s,ram=%s where id=%s")
        self.cursor.execute(update_vps,(self.name,self.description,self.ram,self.id))
        self.row = self.cursor.fetchall()

        self.conn.commit()

        return self.row

        
    def createVPS(self,name,description,ram,con):
        self.name           = name
        self.description    = description
        self.ram            = ram
        self.con            = con

        #create_vps = "insert into vps (name,description,ram,console) values (%s,%s,%s,190)"
        #self.cursor.execute(create_vps,(self.name,self.description,self.ram,self.con))
        

        self.cursor.callproc('sp_createVPS',(self.name,self.description,self.ram,self.con))
        self.conn.commit()

        self.cursor.execute('SELECT last_insert_id()')
        self.vps_id = self.cursor.fetchone()

        return self.vps_id[0]

    def createDisk(self,name,order,disk,vps_id):
        self.name   = name
        self.order  = order
        self.disk   = disk
        self.vps_id = vps_id

        try:
            self.cursor.callproc('sp_createDisks',(self.name,self.order,self.disk,self.vps_id))
        
            self.conn.commit()

        
            self.data = str(self.vps_id)

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(self.data + ",create\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
        
        return "created"

    def delVPS(self,id):
        self.id = id

        del_vps     = ("delete from vps where id=%s")

        try:
            self.cursor.execute(del_vps,(self.id,))
            #self.row = self.cursor.fetchall()
            self.conn.commit()

            data = str(id)

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(data + ",delete\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()

        return "success"

    def restartConsole(self,id):
        self.id = id

        try:
            data = str(id)

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(data + ",restartConsole\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()

        return "success"

    def ctrlVPS(self,id,command):
        data = str(id)
        command = command

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(data + "," + command + "\n")
        
            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
            return received
    