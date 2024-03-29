import socket, modules.database.database, time, configparser
import os 
import base64
import requests
from flask import jsonify, make_response, json

dir_path = os.path.dirname(os.path.realpath(__file__))

# Get VPS configurations from configuration.cfg
Config = configparser.ConfigParser()
Config.read("{}/../configuration.cfg".format(dir_path))
env = Config.get('Global','env')
min_console = Config.get('VPS','minconsole')
min_device = Config.get('VPS','mindevice')
HOST = str(Config.get('VPS','host'))
PORT = int(Config.get('VPS','port'))
PassString = Config.get('Global','PassString')
vps_server = Config.get('vps_server','address')
vps_username = Config.get('vps_server','username')
vps_password = Config.get('vps_server','password')
vps_get_status = Config.get('rest_calls','status')
vps_update_vps = Config.get('rest_calls','update_vps')
vps_take_snapshot = Config.get('rest_calls','take_snapshot')
vps_restore_snapshot = Config.get('rest_calls','restore_snapshot')
vps_remove_snapshot = Config.get('rest_calls','remove_snapshot')
vps_add_device = Config.get('rest_calls','add_device')
vps_del_device = Config.get('rest_calls','del_device')
vps_add_disk = Config.get('rest_calls','add_disk')
vps_del_disk = Config.get('rest_calls','del_disk')
vps_del_vps = Config.get('rest_calls','del_vps')
vps_get_net_status = Config.get('rest_calls','net_status')
vps_start_vps = Config.get('rest_calls','start_vps')
vps_stop_vps = Config.get('rest_calls','stop_vps')
vps_console_restart = Config.get('rest_calls','restart_console')


class VPS:

    def __init__(self):
        self.return_values = {}
        self.db = modules.database.database.DB_VPS()

    def getVPS(self):
        vpsList = self.db.getVPS()

        if (len(vpsList) > 0):
            vpsListWithStatus = [[]]

            count = 0
            num_items = len(vpsList)

            for line in vpsList:
                status = self.getStatus(line[0]).json()

                vpsListWithStatus[count].append(line[0])
                vpsListWithStatus[count].append(line[1])
                vpsListWithStatus[count].append(line[2])
                vpsListWithStatus[count].append(status['status'])
                vpsListWithStatus[count].append(line[3])

                if (count < num_items-1): vpsListWithStatus.append([])

                count+=1

            return vpsListWithStatus
        
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
        self.db.addDevice(device,vps_id,bridge_id)
        return self.make_call_to_vpssvr(vps_update_vps + str(vps_id))

    def addDeviceUpdate(self,device,vps_id,bridge_id):
        self.db.addDevice(device,vps_id,bridge_id)

        try:
            
            self.data = str(vps_id)
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(PassString + "," + self.data + ",updatevps\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)

            if (len(received) > 0):
                status = "Running"
            else:
                status = "Stopped"
        finally:
            sock.close()
            return received

    def delete_network_interface(self, id, vps_id):
        self.db.delNetwork(id)

        return self.make_call_to_vpssvr(vps_update_vps + str(vps_id))

    def getStatus(self,vps_id):
        return self.make_call_to_vpssvr(vps_get_status + str(vps_id))

    def startVPS(self,vps_id):
        return self.make_call_to_vpssvr(vps_start_vps + str(vps_id))

    def stopVPS(self,vps_id):
        return self.make_call_to_vpssvr(vps_stop_vps + str(vps_id))

    def getNetworkInterfaceStatus(self,vps_id):
        self.make_call_to_vpssvr(vps_get_net_status + str(vps_id))

    def takeSnapShot(self,vps_id,snapshotName):
        return self.make_call_to_vpssvr(
            vps_take_snapshot + str(vps_id) + '/' + snapshotName
        )

    def restoreSnapShot(self,vps_id,snapshotName):
        try:
            self.make_call_to_vpssvr(
                vps_restore_snapshot + str(vps_id) + '/' + snapshotName
            )
            return "Restored"
        except:
            return "An error occured"

    def removeSnapShot(self,vps_id,snapshot):
        self.make_call_to_vpssvr(vps_remove_snapshot + str(vps_id))
        '''try:
            self.data = str(vps_id)
            self.snapshot = str(snapshot)

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(PassString + "," + self.data + ",removeSnapshot," + self.snapshot + "\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)

        finally:
            sock.close()
            return received'''


    def listSnapShot(self,vps_id):
        try:
            # Connect to server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            sock.sendall(PassString + "," + str(vps_id) + ",listSnapshot\n")
            received = sock.recv(1024)
        except:
            return None
        finally:
            sock.close()
            item = [[]]

            try:
                received = received.split('\n')
                count = 0

                for line in received:
                    items = line.split()

                    if (len(items) > 0):
                        item[count].append(items)

                    item.append([])
                    count += 1
            except:
                print('an error occured')

            return item

    def addDisk(self,name,size,order,vps_id,createDisk):
        try:
            self.data = self.db.addDisk(name,size,order,vps_id)

            if (createDisk == "on"):
            
                # Create a socket (SOCK_STREAM means a TCP socket)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect to server and send data
                sock.connect((HOST, PORT))
                sock.sendall(PassString + "," + str(self.data) + ",createdisk\n")

                # Receive data from the server and shut down
                received = sock.recv(1024)
        finally:
            if (createDisk == "on"):
                sock.close()

            return self.data



    def delDisk(self,id):

        try:
            #self.data = self.db.delDisk(id)

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(PassString + "," + str(id) + ",deletedisk\n")

            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
            #self.data = self.db.delDisk(id)
            return "deleted"

    def getDisks(self,id):
        return self.db.getDisks(id)

    def getDisk(self,id):
        return self.db.getDisk(id)

    def updateDisk(self,id,name):
        return self.db.updateDisk(id,name)

    def getIntVPS(self,id):
        row = self.db.getIntVPS(id)
        
        row2 = [[]]

        index = 0
        #num_items = len(row)

        for line in row:

            tap = line[1]
            bridge = line[3]

            row2[index].append(line[0])
            row2[index].append(tap)     # interfaces

            row2[index].append(line[2])
            row2[index].append(bridge)

            row2[index].append(self.getNetworkInterfaceStatus(tap))

            row2.append([])

            index+=1

        row2.pop()

        return row2

    def updateVPS(self,name,description,ram,id,path,startScript,stopScript,image):
        output = self.db.updateVPS(name, description, ram, id, path, startScript, stopScript, image)
        return self.make_call_to_vpssvr(vps_update_vps + str(id))
        
    def createVPS(self,name,description,ram,con,image,path):
        return self.db.createVPS(name,description,ram,con,image,path)


    def createDisk(self,name,order,disk,vps_id,createDisk,createPath):
        return self.make_call_to_vpssvr(vps_add_disk + str(id))

    def delVPS(self,id):
        # self.db.delVPS(id)
        return self.make_call_to_vpssvr(vps_del_vps + id)

    def restartConsole(self,id):

        data = str(id)

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(PassString + "," + data + ",restartConsole\n")
    
            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
            return "success"


    def ctrlVPS(self,id,command):
        return self.make_call_to_vpssvr(vps_start_vps + id)
        # data = str(id)
        # command = command
        #
        # # Create a socket (SOCK_STREAM means a TCP socket)
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #
        # try:
        #     # Connect to server and send data
        #     sock.connect((HOST, PORT))
        #     sock.sendall(PassString + "," + data + "," + command + "\n")
        #
        #     # Receive data from the server and shut down
        #     received = sock.recv(1024)
        # finally:
        #     sock.close()
        #
        #     if (command == "start"): time.sleep(1)
        #     return received


    def convertRAM(self,ram):
        if (ram == "512MB"): ram = 512
        elif (ram == "1GB"): ram = 1024
        elif (ram == "2GB"): ram = 2048
        elif (ram == "3GB"): ram = 3072

        return ram


    def convertDisk(self,disk):
        if (disk == "20GB"):   disk = 20
        elif (disk == "30GB"): disk = 30
        elif (disk == "40GB"): disk = 40

        return disk

    def rest_api_call(self):
        pass

    def open_with_auth(self, url, method, username, password):
        headers = {
            'Authorization': 'Basic %s' % base64.b64encode(b"miguel:python").decode("ascii")
        }
        return requests.get(url, headers=headers)

    def set_dev_return_values(self):
        self.return_values = {
            'status': 'VPS 878 Updated\n'
        }

    def get_dev_return_value(self, key_name):
            return self.return_values(key_name)

    def make_call_to_vpssvr(self, path):
        connection_string = vps_server + path
        try:
              return self.open_with_auth(connection_string,
                              'GET', vps_username, vps_password)
        except:
            return "Error: was not able to connect"

