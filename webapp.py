# Imports
from flask import Flask, render_template, redirect, abort, request, session
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
    return redirect('/selection')

@app.route('/selection')
def selection():
    username = session.get("username")
    if not username:
        return redirect('/')
    security(username)

    SAM:dict = read("SAM.json")
    return render_template("selection.html", username=username, SAM=SAM)


# Starting sequence
if __name__ == "__main__":
    app.run("0.0.0.0", 8080, False)