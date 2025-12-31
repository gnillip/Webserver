# Imports
from flask import Flask, render_template, redirect, jsonify, abort, request, session
import os, hashlib, json

# Variables
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Functions
def read(file:str) -> dict:
    if not os.path.exists(f"./{file}"):
        open(file, "w").write("{}")
        return {}
    
    with open(file, "r") as data:
        return json.load(data)
    
def write(file:str, contents:dict) -> None:
    with open(file, "w") as data:
        json.dump(contents, data, indent=4)

def security(username:str, admin:bool=False) -> None:
    SAM:dict = read("SAM.json")

    if username not in SAM:
        abort(403, "This user does not exist?")
    
    if SAM[username]["locked"]:
        abort(403, "This Account is currently locked!")
    
    if admin:
        if "admins" not in SAM[username]["groups"]:
            abprt(403, "You need admin-status to do that.")

def load_dateien(username:str):
    temp = []
    for entry in os.listdir(f"./static/dateien/{username}"):
        temp.append(entry)
    return temp

# Flask build
@app.route('/')
def startseite():
    return render_template("startseite.html")

@app.route('/login', methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    SAM:dict = read("SAM.json")

    if username not in SAM:
        return redirect('/')
    
    if SAM[username]["password"] == hashlib.sha512(password.encode()).hexdigest():

        if SAM[username]["locked"]:
            abort(401, "Your Account is Locked!")
        
        session["username"] = username
        return redirect('/selection')
    return redirect('/')

@app.route('/registration', methods=["POST"])
def registration():
    username = request.form["username"]
    password = request.form["password"]
    SAM:dict = read("SAM.json")

    if username in SAM:
        abort(403, "This user is already in use!")
    
    SAM[username] = {
        "password": hashlib.sha512(password.encode()).hexdigest(),
        "locked": False,
        "groups": ["users"]
    }
    write("SAM.json", SAM)
    os.mkdir(f"./static/dateien/{username}")
    return redirect('/selection')

@app.route('/selection')
def selection():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)

    SAM:dict = read("SAM.json")
    return render_template("selection.html", username=username, SAM=SAM)

@app.route('/PC')
def pc():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)

    return render_template("pc.html")

@app.route('/PC/dach', methods=["GET", "POST"])
def pc_dach():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)

    PC = read("PC.json")

    if request.method == "POST":
        method = request.form["method"]

        if method == "change":
            name = request.form["name"]
            motherboard = request.form["motherboard"]
            cpu = request.form["cpu"]
            gpu = request.form["gpu"]
            ram = request.form["ram"]
            storage = request.form["storage"]
            os = request.form["os"]

            PC["dach"][name] = {
                "motherboard": motherboard,
                "cpu": cpu,
                "gpu": gpu,
                "ram": ram,
                "storage": storage,
                "os": os
            }

        elif method == "add":
            name = request.form["name"]
            motherboard = request.form["motherboard"]
            cpu = request.form["cpu"]
            gpu = request.form["gpu"]
            ram = request.form["ram"]
            storage = request.form["storage"]
            os = request.form["os"]

            PC["dach"][name] = {
                "motherboard": motherboard,
                "cpu": cpu,
                "gpu": gpu,
                "ram": ram,
                "storage": storage,
                "os": os
            }

        elif method == "delete":
            name = request.form["name"]
            PC["dach"].pop(name)

        write("PC.json", PC)

    return render_template("pc_dach.html", PC=PC)

@app.route('/PC/mitte', methods=["GET", "POST"])
def pc_mitte():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)

    PC = read("PC.json")

    if request.method == "POST":
        method = request.form["method"]

        if method == "change":
            name = request.form["name"]
            motherboard = request.form["motherboard"]
            cpu = request.form["cpu"]
            gpu = request.form["gpu"]
            ram = request.form["ram"]
            storage = request.form["storage"]
            os = request.form["os"]

            PC["mitte"][name] = {
                "motherboard": motherboard,
                "cpu": cpu,
                "gpu": gpu,
                "ram": ram,
                "storage": storage,
                "os": os
            }

        elif method == "add":
            name = request.form["name"]
            motherboard = request.form["motherboard"]
            cpu = request.form["cpu"]
            gpu = request.form["gpu"]
            ram = request.form["ram"]
            storage = request.form["storage"]
            os = request.form["os"]

            PC["mitte"][name] = {
                "motherboard": motherboard,
                "cpu": cpu,
                "gpu": gpu,
                "ram": ram,
                "storage": storage,
                "os": os
            }

        elif method == "delete":
            name = request.form["name"]
            PC["mitte"].pop(name)

        write("PC.json", PC)

    return render_template("pc_mitte.html", PC=PC)

@app.route('/PC/keller', methods=["GET", "POST"])
def pc_keller():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)

    PC = read("PC.json")

    if request.method == "POST":
        method = request.form["method"]

        if method == "change":
            name = request.form["name"]
            motherboard = request.form["motherboard"]
            cpu = request.form["cpu"]
            gpu = request.form["gpu"]
            ram = request.form["ram"]
            storage = request.form["storage"]
            os = request.form["os"]

            PC["keller"][name] = {
                "motherboard": motherboard,
                "cpu": cpu,
                "gpu": gpu,
                "ram": ram,
                "storage": storage,
                "os": os
            }

        elif method == "add":
            name = request.form["name"]
            motherboard = request.form["motherboard"]
            cpu = request.form["cpu"]
            gpu = request.form["gpu"]
            ram = request.form["ram"]
            storage = request.form["storage"]
            os = request.form["os"]

            PC["keller"][name] = {
                "motherboard": motherboard,
                "cpu": cpu,
                "gpu": gpu,
                "ram": ram,
                "storage": storage,
                "os": os
            }

        elif method == "delete":
            name = request.form["name"]
            PC["keller"].pop(name)

        write("PC.json", PC)

    return render_template("pc_keller.html", PC=PC)

@app.route('/user')
def user_page():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)
    dateien = load_dateien(username)

    return render_template("user.html", username=username, dateien=dateien)

@app.route('/user/change_pw', methods=["POST"])
def user_change_pw():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)

    SAM = read("SAM.json")
    password = request.form["password"]

    SAM[username]["password"] = hashlib.sha512(password.encode()).hexdigest()
    write("SAM.json", SAM)
    session.clear()
    return redirect('/')

@app.route('/user/upload', methods=["POST"])
def user_upload():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)

    file = request.files["file"]
    file.save(f"./static/dateien/{username}/{file.filename}")
    return redirect('/user')

@app.route('/user/send', methods={"POST"})
def user_send():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)

    file = request.form["file"]
    sendto = request.form["sendto"]

    os.system(f"cp ./static/dateien/{username}/{file} ./static/dateien/{sendto}/{file}")
    return redirect('/user')

@app.route('/user/delete', methods=["POST"])
def user_delete():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)

    file = request.form["file"]
    os.remove(f"./static/dateien/{username}/{file}")
    return redirect('/user')

@app.route('/get_hash')
def get_hash_js():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username, True)

    value = request.args.get('value')

    if not value:
        return jsonify({'error': 'no value was given'}), 400
    
    hash_result = hashlib.sha512(value.encode()).hexdigest()
    return jsonify({'hash': hash_result})

@app.route('/admin')
def admin():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username, True)

    SAM:dict = read("SAM.json")
    return render_template("admin.html", SAM=SAM, username=username)

@app.route('/admin/change', methods=["POST"])
def admin_change():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username, True)

    SAM:dict = read("SAM.json")
    user = request.form["username"]
    locked = request.form["locked"]
    groups = request.form["groups"]
    password = request.form["password"]

    if locked.lower() == "false":
        locked = False
    else:
        locked = True
    
    if "," in groups:
        groups = groups.split(",")
    else:
        groups = [groups.split(",")[0]]
    
    SAM[user] = {
        "password": password,
        "locked": locked,
        "groups": groups
    }
    write("SAM.json", SAM)
    return redirect('/admin')

@app.route('/admin/add', methods=["POST"])
def admin_add():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username, True)

    SAM:dict = read("SAM.json")
    user = request.form["username"]
    locked = request.form["locked"]
    groups = request.form["groups"]
    password = request.form["password"]

    if locked.lower() == "false":
        locked = False
    else:
        locked = True
    
    if "," in groups:
        groups = groups.split(",")
    else:
        groups = [groups.split(",")[0]]
    
    if user in SAM:
        abort(401, "This user already exists!")
    
    SAM[user] = {
        "password": password,
        "locked": locked,
        "groups": groups
    }
    write("SAM.json", SAM)
    os.mkdir(f"./static/dateien/{user}")
    return redirect('/admin')

@app.route('/admin/delete', methods=["POST"])
def admin_delete():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username, True)

    user = request.form["user"]
    SAM = read("SAM.json")

    if user not in SAM:
        abort(401, "This user doen't exist. Maybe you mistyped?")
    
    SAM.pop(user)
    write("SAM.json", SAM)
    os.rmdir(f"./static/dateien/{user}")
    return redirect('/admin')

# Starting sequence
if __name__ == "__main__":

    SAM = read("SAM.json")
    for key, value in SAM.items():
        if not os.path.exists(f"./static/dateien/{key}"):
            os.mkdir(f"./static/dateien/{key}")

    if not os.path.exists("./PC.json"):
        with open("PC.json", "w") as data:
            json.dump({
                "dach": {},
                "mitte": {},
                "keller": {}
            }, data, indent=4)

    app.run("0.0.0.0", 5000, False)