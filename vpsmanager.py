from flask import Flask, render_template, json, request, redirect, session, g
from werkzeug import generate_password_hash, check_password_hash
import modules.vps
import modules.user
import ConfigParser
import os 

from sqlite3 import dbapi2 as sqlite3


dir_path = os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__)


app.config.from_object(__name__)

app.secret_key = 'why would I tell you my secret key?'

menu = ([['/','Home'],
         ['/UserManagement','User Management'],
         ['/Logout','Logout']])

# Get VPS configurations from configuration.cfg
Config = ConfigParser.ConfigParser()
Config.read("{}/configuration.cfg".format(dir_path))
ShellInABoxPref = Config.get('Global','ShellInABoxPref')


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

    
        
  

@app.route("/",methods=['POST','GET'])
def main():
    if session.get('user'):
        if (request.args.get('vpsadded')): vpsadded = request.args.get('vpsadded')
        else: vpsadded = "no"

        vps = modules.vps.VPS()
        row = vps.getVPS()

        active = '/'

        return render_template('index.html', menu=menu, active=active, row=row, vpsadded=vpsadded)
    else:
        return redirect('/Login')

@app.route('/Logout')
def logout():
    session.pop('user',None)
    return redirect('/Login')

@app.route('/validateLogin',methods=['POST','GET'])
def validateLogin():
    _username = request.form['username']
    _password = request.form['password']

    # connect to mysql

    users = modules.user.User()

    data = users.checkUsername(_username)

    if len(data) > 0:
        if check_password_hash(str(data[0][3]),_password):
            session['user'] = data[0][0]
            return redirect('/')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
    else:
        return render_template('error.html',error = 'Wrong Email address or Password.')
  

@app.route("/UserManagement")
def userManagement():
    if session.get('user'):
        if (request.args.get('useradded')): status = "added"
        elif (request.args.get('userupdated')): status = "updated"
        else: status = "no"

        users = modules.user.User()

        row = users.getUsers()

        active = '/UserManagement'

        return render_template('usermanagement.html', menu=menu, active=active, row=row, status=status)
    else:
        return redirect('/Login')


    

@app.route("/addUser")
def addUser():
    if session.get('user'):
    	active = "/UserManagement"
    	title = "Add User"

    	return render_template('createUser.html', menu=menu, title=title, active=active)
    else:
        return redirect('/Login')

@app.route("/createUser",methods=['POST'])
def createUser():
    if session.get('user'):
        _name 		= request.form['inputName']
        _email 		= request.form['inputEmail']
        _password 	= request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
        
            users = modules.user.User()
            data = users.createUser(_name,_email,_password)

            #return data
            return json.dumps(data)

            """if len(data) is 0:
                return json.dumps({'message':'User created successfully !'})
                
            else:
                return json.dumps({'error':str(data[0])})"""
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    else:
        return redirect('/Login')

@app.route("/deleteUser")
def deleteUser():
    if session.get('user'):	
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

        return render_template('usermanagement.html', menu=menu, active=active, row=row, userdeleted=userdeleted)

    else:
        return redirect('/Login')


@app.route("/modifyUser")
def modifyUser():
    if session.get('user'):
        id = int(request.args.get('id'))
        error = request.args.get('error')
        
        user = modules.user.User()

        row = user.getUser(id)

        active = "/UserManagement"
        title = "Modify User"

        return render_template('modifyuser.html', menu=menu, active=active, row=row, title=title, error=error)
    else:
        return redirect('/Login')

@app.route("/updateUser",methods=['POST','GET'])
def updateUser():
    if session.get('user'):
        id 				= int(request.form['id'])
        email 			= request.form['inputEmail']
        name 			= request.form['inputName']
        newPassword		= request.form['newPassword']
        repPassword		= request.form['repPassword']

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

    else:
        return redirect('/Login')


@app.route("/startVPS")
def startVPS():
    if session.get('user'):
        id = request.args.get('id')

        active 	= '/'
        title 	= 'Modify VPS'

        vps         = modules.vps.VPS()
        received    = vps.ctrlVPS(id,'start')
        row         = vps.getIndVPS(id)
        disks       = vps.getDisks(id)
        device      = vps.getIntVPS(id)
        status      = vps.getStatus(id)

        active  = '/'
        title   = 'View VPS'

        return render_template('viewvps.html', menu=menu, title=title, active=active, row=row, disks=disks, device=device, status=status, prefport=ShellInABoxPref)
    else:
        return redirect('/Login')

@app.route("/stopVPS")
def stopVPS():
    if session.get('user'):
        id = request.args.get('id')

        vps         = modules.vps.VPS()
        received    = vps.ctrlVPS(id,'stop')
        row         = vps.getIndVPS(id)
        disks       = vps.getDisks(id)
        device      = vps.getIntVPS(id)
        status      = vps.getStatus(id)

        active  = '/'
        title   = 'View VPS'

        return render_template('viewvps.html', menu=menu, title=title, active=active, row=row, disks=disks, device=device, status=status, prefport=ShellInABoxPref)

    else:
        return redirect('/Login')

@app.route("/AddVPS")
def AddVPS():
    if session.get('user'):
        vps = modules.vps.VPS()
        bridge = vps.getBridge()

        active 	= '/AddVPS'
        title 	= 'Add VPS'
        return render_template('addvps.html', menu=menu, title=title, active=active, bridge=bridge)
    else:
        return redirect('/Login')

@app.route("/addDisk")
def addDisk():
    if session.get('user'):
        id = request.args.get('id')

        active = ""
        title = "Add Disk"

        return render_template('adddisk.html', menu=menu, title=title, active=active, id=id)
    else:
        return redirect('/Login')

@app.route("/addNetwork")
def addNetwork():
    if session.get('user'):
        id = request.args.get('id')
        updated = request.args.get('updated')

        network     = modules.vps.VPS()
        max_device  = network.getInt()
        bridge      = network.getBridge()

        active = ""
        title = "Add Network Interface"

        return render_template('addnetwork.html', menu=menu, title=title, bridge=bridge, id=id)
    else:
        return redirect('/Login')

@app.route("/createNetwork",methods=['POST'])
def createNetwork():
    if session.get('user'):
        id 		= request.form['id']
        bridge 	= request.form['bridge']

        network     = modules.vps.VPS()
        new_device  = network.getInt()

        bridge_id = network.getBridgeID(bridge)
        
        data = network.addDeviceUpdate(new_device,id,bridge_id)
    
        active = ""
        title = "Add Network Interface"

        return id
    else:
        return redirect('/Login')

#
# Delete interface from Database and redirect to modifyVPS page
#
@app.route("/delNetwork")
def delNetwork():
    if session.get('user'):
        id = request.args.get('id')
        vps_id = request.args.get('vps_id')

        del_network = ("delete from interface where id=%s")

        network = modules.vps.VPS()
        data = network.delNetwork(id,vps_id)

        location = "/modifyVPS?id=" + vps_id + "&updated=yes"

        return redirect(location, code=302)
    else:
        return redirect('/Login')

@app.route("/createDisk",methods=['POST','GET'])
def createDisk():
    if session.get('user'):
        id 		= request.form['id']
        name 	= request.form['name']
        disk	= request.form['disk']

        if (disk == "20GB"): disk = 20
        elif (disk == "30GB"): disk = 30
        elif (disk == "40GB"): disk = 40

        order = 0

        network = modules.vps.VPS()
        data = network.addDisk(name,disk,order,id)
    
        active = ""
        title = "Add Disk"

        return id
    else:
        return redirect('/Login')

@app.route("/deleteDisk")
def deleteDisk():
    if session.get('user'):
        id = request.args.get('id')
        vps_id = request.args.get('vps_id')
        updated = request.args.get('updated')

        network = modules.vps.VPS()
        data = network.delDisk(id)

        location = "/modifyVPS?id=" + vps_id + "&updated=yes"

        return redirect(location, code=302)
    else:
        return redirect('/Login')


@app.route("/modifyVPS")
def modifyVPS():
    if session.get('user'):
        id = request.args.get('id')

        updated = request.args.get('updated')
       
        vps     = modules.vps.VPS()
        row     = vps.getIndVPS(id)
        disks   = vps.getDisks(id)
        device  = vps.getIntVPS(id)
        status  = vps.getStatus(id)
       
        active 	= '/'
        title 	= 'Modify VPS'

        return render_template('modifyvps.html', menu=menu, title=title, active=active, row=row, disks=disks, updated=updated, device=device, status=status)
    else:
        return redirect('/Login')

@app.route("/viewVPS")
def viewVPS():
    if session.get('user'):
        id = request.args.get('id')

        vps     = modules.vps.VPS()
        row     = vps.getIndVPS(id)
        disks   = vps.getDisks(id)
        device  = vps.getIntVPS(id)
        status  = vps.getStatus(id)

        prefport = ShellInABoxPref


        active  = '/'
        title   = 'View VPS'

        return render_template('viewvps.html', menu=menu, title=title, active=active, row=row, disks=disks, device=device, status=status, prefport=ShellInABoxPref)
    else:
        return redirect('/Login')

@app.route('/restartConsole')
def restartConsole():
    if session.get('user'):
        id = request.args.get('id')

        vps     = modules.vps.VPS()
        row     = vps.getIndVPS(id)
        disks   = vps.getDisks(id)
        device  = vps.getIntVPS(id)
        status  = vps.getStatus(id)
        
        console = vps.restartConsole(id)

        active  = '/'
        title   = 'View VPS'

        return render_template('viewvps.html', menu=menu, title=title, active=active, row=row, disks=disks, device=device, status=status, prefport=ShellInABoxPref)
    else:
        return redirect('/Login')


@app.route("/updateVPS",methods=['POST'])
def updateVPS():    
    if session.get('user'):
        id 				= request.form['id']
        name 			= request.form['name']
        description 	= request.form['description']
        ram 			= request.form['ram']

        if (ram == "512MB"): ram = 512
        elif (ram == "1GB"): ram = 1024
        elif (ram == "2GB"): ram = 2048
    
        vps = modules.vps.VPS()
        row = vps.updateVPS(name,description,ram,id)
        
        return id
    else:
        return redirect('/Login')

@app.route('/createVPS',methods=['POST','GET'])
def createVPS():
    if session.get('user'):
        # read the posted values from the UI
        name 		= request.form['name']
        description = request.form['description']
        ram 		= request.form['ram']
        disk 		= request.form['disk']
        bridge 		= request.form['bridge']
        image       = request.form['image']

        if (name and description and ram):
            if (ram == "512MB"): ram = 512
            elif (ram == "1GB"): ram = 1024
            elif (ram == "2GB"): ram = 2048

            if (disk == "20GB"):   disk = 20
            elif (disk == "30GB"): disk = 30
            elif (disk == "40GB"): disk = 40

            order = 0

            vps         = modules.vps.VPS()
            console     = vps.getMaxConsole()
            vps_id      = vps.createVPS(name,description,ram,console,image)
            new_device  = vps.getInt()
            bridge_id   = vps.getBridgeID(bridge)
            device      = vps.addDevice(new_device,vps_id,bridge_id)
            data        = vps.createDisk(name,order,disk,vps_id)
                        
            row         = vps.getVPS()

            active 	= '/'
            title 	= 'VPS Manager'

            return json.dumps(vps_id)
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    else:
        return redirect('/Login')

@app.route("/deleteVPS")
def deleteVPS():
    if session.get('user'):
        active  = '/'
        title   = 'VPS Manager'

        id = request.args.get('id')

        vps = modules.vps.VPS()
        delstatus,message = vps.delVPS(id)

        row = vps.getVPS()

        return render_template('index.html', menu=menu, title=title, active=active, row=row, delstatus=delstatus, message=message)
    else:
        return redirect('/Login')

@app.route("/Login",methods=['POST','GET'])
def Login():
    active 	= '/Login'
    title 	= 'Login'
    return render_template('login.html', menu=menu, title=title, active=active)


if __name__ == "__main__":
    app.run()