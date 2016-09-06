import socket, modules.database

min_console = 100
min_device = 100
HOST, PORT = "10.128.2.1", 9999

class VPS:

    def __init__(self):
        self.db = modules.database.DB_VPS()

    def getVPS(self):
        return self.db.getVPS()
        
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
        return self.db.addDevice(device,vps_id,bridge_id)

    def delNetwork(self,id):
        return self.db.delNetwork(id)

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
            self.data = self.db.delDisk(id)
            return self.data

    def getDisks(self,id):
        return self.db.getDisks(id)


    def getIntVPS(self,id):
        return self.db.getIntVPS(id)

    def updateVPS(self,name,description,ram,id):
        return self.db.updateVPS(name,description,ram,id)

        
    def createVPS(self,name,description,ram,con):
        return self.db.createVPS(name,description,ram,con)

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
        finally:
            sock.close()

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
            return received
    