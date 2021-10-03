from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from account import createAccount

app = Flask(__name__)

ENV = "prod"

if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jha@localhost/filesystem-data'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cdawzcdbskcdpd:750487e3896466ef4bf5a34f02f730301d1e861377118ee0cd55e86935200a9b@ec2-54-196-33-23.compute-1.amazonaws.com:5432/d7rf7uhpqn1ite'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(50), primary_key=True)
    passkey = db.Column(db.String(500))
    publickey = db.Column(db.String(500))
    secret = db.Column(db.String(500))

    def __init__(self, username, passkey, publickey, secret):
        self.username = username
        self.passkey = passkey
        self.publickey = publickey
        self.secret = secret

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/loginAccount", methods=["GET", "POST"])
def login():
    return render_template("loginPage.html")

@app.route("/createAccount", methods=["GET", "POST"])
def create():
    return render_template("createPage.html")

@app.route("/accountStatus", methods=["GET", "POST"])
def getStatus():
    uname = request.form['username']
    pwd = request.form['password']
    if db.session.query(User).filter(User.username == uname).count() == 0:
        acInfo = createAccount(uname, pwd)
        data = User(acInfo[0], acInfo[1], acInfo[2], acInfo[3])
        db.session.add(data)
        db.session.commit()
        return render_template("loginPage.html", message="You can login now")
    else:
        return render_template("createPage.html", message="Username already exists. Try again")


# @app.route("/dashboard", methods=["GET","POST"])
# def dashboard():
#     return render_template("dashboard.html", uname=uname, pwd=pwd, res=res)

if __name__ == '__main__':
    app.run()