from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from account import createAccount

app = Flask(__name__)

ENV = "prob"

if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jha@localhost/filesystem-data'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://faczclvhitvdwh:ae3089dce8da2eadfc810e426aa0d464be78d7fdb44a8d3792c94fbd5bfadd0a@ec2-54-224-120-186.compute-1.amazonaws.com:5432/d5rg047ldjvf8m'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
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