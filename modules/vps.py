import socket, modules.database, time, ConfigParser
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

# Get VPS configurations from configuration.cfg
Config = ConfigParser.ConfigParser()
Config.read("{}/../configuration.cfg".format(dir_path))
min_console = Config.get('VPS','minconsole')
min_device = Config.get('VPS','mindevice')
HOST = str(Config.get('VPS','host'))
PORT = int(Config.get('VPS','port'))

class VPS:

    def __init__(self):
        self.db = modules.database.DB_VPS()

    def getVPS(self):
        row = self.db.getVPS()

        if (len(row) > 0):

            row2 = [[]]

            count = 0
            num_items = len(row)

            for line in row:

                # Get running status of machine
                status = self.getStatus(line[0])

                row2[count].append(line[0])
                row2[count].append(line[1])
                row2[count].append(line[2])
                row2[count].append(status)
                row2[count].append(line[3])

                if (count < num_items-1): row2.append([])

                count+=1

            return row2
        
    def getIndVPS(self,id):
        return self.db.getIndVPS(id)

    def getBridge(self):
        return self.db.getBridge()

    def getBridgeID(self,device):
        return self.db.getBridgeID(device)
        
    def getMaxConsole(self):
        self.console = self.db.getMaxConsole()

        if (self.console == None):
            self.console = min_console
            #self.console = "test"
        else:
            self.console = int(self.console) + 1

        return self.console


    def getInt(self):
        
        self.int = self.db.getInt()

        if (self.int == None):
            self.int = min_device
        else:
            self.int = int(self.int) + 1

        return self.int


    def addDevice(self,device,vps_id,bridge_id):
        
        self.db.addDevice(device,vps_id,bridge_id)

        """try:
            
            self.data = str(vps_id)
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(self.data + ",updatevps\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)

            if (len(received) > 0):
                status = "Running"
            else:
                status = "Stopped"
        finally:
            sock.close()
            return received"""

    def addDeviceUpdate(self,device,vps_id,bridge_id):
        self.db.addDevice(device,vps_id,bridge_id)

        try:
            
            self.data = str(vps_id)
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(self.data + ",updatevps\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)

            if (len(received) > 0):
                status = "Running"
            else:
                status = "Stopped"
        finally:
            sock.close()
            return received

    def delNetwork(self,id,vps_id):
        self.db.delNetwork(id)

        try:
            
            self.data = str(vps_id)
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(self.data + ",updatevps\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)

        finally:
            sock.close()
            return received

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
        
        try:
            self.data = self.db.addDisk(name,size,order,vps_id)
            
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(str(self.data) + ",createdisk\n")

            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
            return self.data



    def delDisk(self,id):

        try:
            #self.data = self.db.delDisk(id)

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(str(id) + ",deletedisk\n")

            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
            #self.data = self.db.delDisk(id)
            return "deleted"

    def getDisks(self,id):
        return self.db.getDisks(id)


    def getIntVPS(self,id):
        return self.db.getIntVPS(id)

    def updateVPS(self,name,description,ram,id):
        return self.db.updateVPS(name,description,ram,id)

        
    def createVPS(self,name,description,ram,con,image):
        return self.db.createVPS(name,description,ram,con,image)

    def createDisk(self,name,order,disk,vps_id):
        
        try:
        
            self.db.createDisk(name,order,disk,vps_id)

            self.data = str(vps_id)

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(self.data + ",createvps\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
        
        return "created"

    #def deleteDisk(self,vps_id,disk_id):


    def delVPS(self,id):
        status = self.getStatus(id)

        if (status == "Stopped"):

            try:
                self.db.delVPS(id)

                data = str(id)

                # Create a socket (SOCK_STREAM means a TCP socket)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            
                # Connect to server and send data
                sock.connect((HOST, PORT))
                sock.sendall(data + ",delete\n")
        
                # Receive data from the server and shut down
                received = sock.recv(1024)
            except:
                return ("error","An unknown error has occurred")
            finally:
                sock.close()
                return ("success","VPS Successfully Deleted")
        else:
            return ("error","Error, VPS must be stopped before Deleting it!")



        return "success"

    def restartConsole(self,id):

        data = str(id)

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
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

            if (command == "start"): time.sleep(1)
            return received

    def convertRAM(self,ram):
        if (ram == "512MB"): ram = 512
        elif (ram == "1GB"): ram = 1024
        elif (ram == "2GB"): ram = 2048

        return ram

    def convertDisk(self,disk):
        if (disk == "20GB"):   disk = 20
        elif (disk == "30GB"): disk = 30
        elif (disk == "40GB"): disk = 40

        return disk


    