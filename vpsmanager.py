from functools import wraps

from flask import Flask, render_template, json, request, redirect, session, g
from werkzeug import generate_password_hash, check_password_hash
import modules.vps
import modules.user
import modules.graph
import configparser
import os
import json

from sqlite3 import dbapi2 as sqlite3


dir_path = os.path.dirname(os.path.realpath(__file__))
vps_configuration = configparser.ConfigParser()
vps_configuration.read("{}/configuration.cfg".format(dir_path))

host_address = vps_configuration.get('Global', 'host')
debug_status = vps_configuration.get('Global', 'debug')
server_port = int(vps_configuration.get('Global', 'port'))

app = Flask(__name__)

app.config.from_object(__name__)

app.secret_key = 'why would I tell you my secret key?'

menu = ([['/','Home'],
         ['/UserManagement','User Management'],
         ['/Logout','Profile']])

menuProfile = ([['/modifyUser?id=','Account'],
                ['/Logout','Logout']])

# Get VPS configurations from configuration.cfg
Config = configparser.ConfigParser()
Config.read("{}/configuration.cfg".format(dir_path))
PassString = Config.get('Global','PassString')
ShellInABoxPref = Config.get('Global','shell_in_a_box_pref')
RootPath = Config.get('Global','RootPath')
app.config['MYSQL_DATABASE_USER'] = Config.get('Database','database_username')

os.environ['LD_LIBRARY_PATH'] = Config.get('Global','gccpath')
hostAddress = Config.get('VPS','host')




## Unit Test Functions
##########################################################

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

## End of Unit Test Functions
##########################################################


##
## Authentication Decorator
##
def check_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user'):
            return f(*args, **kwargs)
        else:
            return redirect('/Login')
    return decorated_function


@app.route("/",methods=['POST','GET'])
@check_auth
def main():
    if (request.args.get('vpsadded')): vpsadded = request.args.get('vpsadded')
    else: vpsadded = "no"

    vps = modules.vps.VPS()
    row = vps.getVPS()

    active = '/'

    return render_template('index.html', menu=menu, user=session.get('user'), menuProfile=menuProfile, active=active, row=row, vpsadded=vpsadded)


@app.route('/Logout')
def logout():
    session.pop('user',None)
    return redirect('/Login')


@app.route('/validateLogin',methods=['POST','GET'])
def validate_login():
    _username = request.form['username']
    _password = request.form['password']

    users = modules.user.User()
    data = users.checkUsername(_username)

    if len(data) > 0:
        if check_password_hash(str(data[0][3]),_password):
            session['user'] = data[0][0]
            return redirect('/')
    return render_template('error.html',error = 'Wrong Email address or Password.')


@app.route("/UserManagement")
@check_auth
def user_management():
    if (request.args.get('useradded')): status = "added"
    elif (request.args.get('userupdated')): status = "updated"
    else: status = "no"

    users = modules.user.User()

    row = users.getUsers()

    active = '/UserManagement'
    title = 'User Management'

    return render_template('usermanagement.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), active=active, row=row, status=status, title=title)


@app.route("/addUser")
@check_auth
def add_user():
    active = "/UserManagement"
    title = "Add User"

    return render_template('createUser.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), title=title, active=active)


@app.route("/createUser",methods=['POST'])
@check_auth
def create_user():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:

        users = modules.user.User()
        data = users.createUser(_name,_email,_password)

        return json.dumps(data)
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


@app.route("/deleteUser")
@check_auth
def delete_user():
    id = int(request.args.get('id'))

    users 	= modules.user.User()
    data 	= users.deleteUser(id)
    row 	= users.getUsers()

    if len(data) is 0:
        userdeleted = "yes"
    else:
        userdeleted = "no"

    active = "/UserManagement"
    title = "Add User"

    return render_template('usermanagement.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), active=active, row=row, userdeleted=userdeleted)


@app.route("/modifyUser")
@check_auth
def modify_user():
    id = int(request.args.get('id'))
    error = request.args.get('error')

    user = modules.user.User()

    row = user.getUser(id)

    active = "/UserManagement"
    title = "Modify User"

    return render_template('modifyuser.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), active=active, row=row, title=title, error=error)


@app.route("/updateUser",methods=['POST','GET'])
@check_auth
def update_user():
    id = int(request.form['id'])
    email = request.form['inputEmail']
    name = request.form['inputName']
    newPassword	= request.form['newPassword']
    repPassword	= request.form['repPassword']

    user = modules.user.User()

    validate = user.checkPassword(newPassword,repPassword)

    if (validate == "match"):
        user.updateUser(id,name,email,newPassword)
        return str(id) + ',User Updated'
    elif (validate == "missmatch"):
        return str(id) + ',Passwords must Match'
    else:
        user.updateUser(id,name,email)
        return str(id) + ',User Updated'


@app.route("/startVPS")
@check_auth
def start_instance():
    id = request.args.get('id')

    vps = modules.vps.VPS()
    vps.startVPS(id)

    return redirect('/viewVPS?id=' + id)


@app.route("/stopVPS")
@check_auth
def stop_instance():
    id = request.args.get('id')

    vps = modules.vps.VPS()
    vps.stopVPS(id)

    return redirect('/viewVPS?id=' + id)


@app.route("/startInterface")
@check_auth
def start_interface():
    id = request.args.get('id')
    vps_id = request.args.get('vps_id')

    vps = modules.vps.VPS()
    vps.ctrlVPS(id,'netStart')

    return redirect('/viewVPS?id=' + vps_id)


@app.route("/stopInterface")
@check_auth
def stop_interface():
    id = request.args.get('id')
    vps_id = request.args.get('vps_id')

    vps = modules.vps.VPS()
    vps.ctrlVPS(id,'netStop')

    return redirect('/viewVPS?id=' + vps_id)


@app.route("/AddVPS")
@check_auth
def add_instance():
    vps = modules.vps.VPS()
    bridge = vps.getBridge()

    active = '/AddVPS'
    title = 'Add VPS'

    return render_template('addvps.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), title=title, active=active, bridge=bridge)


@app.route("/addDisk")
@check_auth
def add_disk():
    id = request.args.get('id')

    active = ""
    title = "Add Disk"

    return render_template('adddisk.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), title=title, active=active, id=id)


@app.route("/editDisk")
@check_auth
def edit_disk():
    id = request.args.get('id')
    disk_id = request.args.get('disk')

    vps = modules.vps.VPS()
    disk = vps.getDisk(disk_id)

    active = ""
    title = "Edit Disk"

    return render_template('editdisk.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), title=title, active=active, id=id, disk=disk)


@app.route("/updateDisk",methods=['POST','GET'])
@check_auth
def update_disk():
    id = request.form['id']
    name = request.form['name']
    disk_id = request.form['disk_id']

    vps = modules.vps.VPS()
    vps.updateDisk(disk_id,name)

    return id


@app.route("/addNetwork")
@check_auth
def add_network():
    id = request.args.get('id')
    request.args.get('updated')

    network = modules.vps.VPS()
    network.getInt()
    bridge = network.getBridge()

    title = "Add Network Interface"

    return render_template('addnetwork.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), title=title, bridge=bridge, id=id)


@app.route("/createNetwork",methods=['POST'])
@check_auth
def create_network():
    id = request.form['id']
    bridge = request.form['bridge']

    network = modules.vps.VPS()
    new_device = network.getInt()
    bridge_id = network.getBridgeID(bridge)

    network.addDeviceUpdate(new_device,id,bridge_id)

    return id


#
# Delete interface from Database and redirect to modifyVPS page
#
@app.route("/delNetwork")
@check_auth
def del_network():
    id = request.args.get('id')
    vps_id = request.args.get('vps_id')

    network = modules.vps.VPS()
    network.delete_network_interface(id, vps_id)

    location = "/modifyVPS?id=" + vps_id + "&updated=yes"

    return redirect(location, code=302)


@app.route("/createDisk",methods=['POST','GET'])
@check_auth
def create_disk():
    id = request.form['id']
    name = request.form['name']
    disk = request.form['disk']

    try:
        createDisk  = request.form['createDisk']
    except:
        createDisk = "off"

    if (disk == "20GB"): disk = 20
    elif (disk == "30GB"): disk = 30
    elif (disk == "40GB"): disk = 40

    order = 0

    network = modules.vps.VPS()
    network.addDisk(name,disk,order,id,createDisk)

    return id


@app.route("/deleteDisk")
@check_auth
def delete_disk():
    id = request.args.get('id')
    vps_id = request.args.get('vps_id')
    request.args.get('updated')

    network = modules.vps.VPS()
    network.delDisk(id)

    location = "/modifyVPS?id=" + vps_id + "&updated=yes"

    return redirect(location, code=302)


@app.route("/modifyVPS")
@check_auth
def modify_instance():
    id = request.args.get('id')

    updated = request.args.get('updated')

    vps = modules.vps.VPS()
    row = vps.getIndVPS(id)
    disks = vps.getDisks(id)
    device = vps.getIntVPS(id)
    status = vps.getStatus(id).json()
    graph = modules.graph.GraphTraffic()
    file = graph.genGraph(device)

    active = '/'
    title = 'Modify VPS'

    return render_template('modifyvps.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), title=title, active=active, row=row, disks=disks, updated=updated, device=device, status=status['status'], file=file)


@app.route("/viewVPS")
@check_auth
def view_instance():
    id = request.args.get('id')

    vps = modules.vps.VPS()
    row = vps.getIndVPS(id)
    disks = vps.getDisks(id)
    device = vps.getIntVPS(id)
    status = vps.getStatus(id).json()

    graph = modules.graph.GraphTraffic()
    file = graph.genGraph(device)

    rootPath = RootPath

    active  = '/'
    title   = 'View VPS'

    return render_template('viewvps.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), title=title, active=active, row=row, disks=disks, device=device, status=status['status'], prefport=ShellInABoxPref, file=file, rootPath=rootPath)


@app.route("/snapShot")
@check_auth
def snapshot():
    id = request.args.get('id')
    status = request.args.get('status')

    vps = modules.vps.VPS()
    row = vps.getIndVPS(id)
    snapshots = vps.listSnapShot(id)

    active = '/'
    title = 'Snapshot Manager'

    return render_template('snapshotmanager.html', menu=menu, menuProfile=menuProfile, user=session.get('user'), title=title, active=active, row=row, status=status, snapshots=snapshots)


@app.route("/takeSnapShot",methods=['POST','GET'])
@check_auth
def take_snapshot():
    id = request.args.get('id')
    snapshotName = request.args.get('snapshotName')

    vps = modules.vps.VPS()
    vps.takeSnapShot(id,snapshotName)

    status = 'Snapshot Taken'
    return redirect('/snapShot?id=' + id + '&status=' + status)


@app.route("/restoreSnapShot")
@check_auth
def restore_snapshot():
    id = request.args.get('id')
    snapshot = request.args.get('snapshot')

    vps = modules.vps.VPS()
    status = 'Snapshot \"' + snapshot + '\"' \
             + vps.restoreSnapShot(id, snapshot)

    return redirect('/snapShot?id=' + id + '&status=' + status)


@app.route("/removeSnapShot")
@check_auth
def remove_snapshot():
    id = request.args.get('id')
    snapshot = request.args.get('snapshot')

    vps = modules.vps.VPS()
    vps.removeSnapShot(id, snapshot)
    status = 'Snapshot \"' + snapshot + '\" Removed'

    return redirect('/snapShot?id=' + id + '&status=' + status)


@app.route('/restartConsole')
@check_auth
def restart_console():
    id = request.args.get('id')

    vps = modules.vps.VPS()
    vps.restartConsole(id)

    return redirect('/viewVPS?id=' + id)


@app.route("/updateVPS",methods=['POST'])
@check_auth
def update_instance():
    id = request.form['id']
    name = request.form['name']
    description = request.form['description']
    ram = request.form['ram']
    path = request.form['path']
    startScript = request.form['startscript']
    stopScript = request.form['stopscript']
    image = request.form['image']

    vps = modules.vps.VPS()
    ram = vps.convertRAM(ram)
    vps.updateVPS(name,description,ram,id,path,startScript,stopScript,image)

    return id


@app.route('/createVPS',methods=['POST','GET'])
@check_auth
def create_instance():
    # read the posted values from the UI
    name = request.form['name']
    description = request.form['description']
    ram = request.form['ram']
    disk = request.form['disk']
    bridge = request.form['bridge']
    image = request.form['image']
    disk_name = ""

    try:
        createDisk = request.form['createDisk']
    except:
        createDisk = "off"

    try:
        createPath = request.form['createPath']
    except:
        createPath = "off"

    if (name and description and ram):

        order = 0

        # Create a VPS using options selected by user
        #
        # Note:
        # new_device = is the Tunnel Interface device on the server i.e. tun2
        # device = the actual device returned after the server is created
        # console = is the port the user uses to connect to the terminal console
        # data is the returned payload from the server connector

        vps = modules.vps.VPS()
        ram = vps.convertRAM(ram)
        disk = vps.convertDisk(disk)
        console = vps.getMaxConsole()
        vps_id = vps.createVPS(name,description,ram,console,image)
        new_device = vps.getInt()
        bridge_id = vps.getBridgeID(bridge)
        vps.addDevice(new_device,vps_id,bridge_id)
        vps.createDisk(disk_name,order,disk,vps_id,createDisk,createPath)

        # Send ID of create VPS to ajax script which gets picked up by Unit/Function tests
        # Currently returns to main page but this allows the option of bringing
        # up the newly created server
        return json.dumps(vps_id)
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


@app.route("/deleteVPS")
@check_auth
def delete_instance():
    active = '/'
    title = 'VPS Manager'

    id = request.args.get('id')
    vps = modules.vps.VPS()
    delstatus, message = vps.delVPS(id)
    row = vps.getVPS()

    return render_template('index.html', menu=menu, title=title, active=active, row=row, delstatus=delstatus, message=message)

@app.route("/Login", methods=['POST','GET'])
def login():
    active 	= '/Login'
    title 	= 'Login'
    return render_template('login.html', menu=menu, menuProfile=menuProfile, title=title, active=active)


if __name__ == "__main__":
    app.run(host=host_address, port=server_port)