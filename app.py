from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, login_user

from models import db, login, User
from account import createAccount, loginAccount
from werkzeug.utils import redirect

app = Flask(__name__)

ENV = "dev"

if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jha@localhost/filesystem'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cdawzcdbskcdpd:750487e3896466ef4bf5a34f02f730301d1e861377118ee0cd55e86935200a9b@ec2-54-196-33-23.compute-1.amazonaws.com:5432/d7rf7uhpqn1ite'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = 'login'
 
@app.before_first_request
def create_all():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("login"):
            return render_template("loginPage.html")
        elif request.form.get("create"):
            return render_template("createPage.html")
    return render_template("index.html")

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/myfiles')
     
    if request.method == 'POST':
        uname = request.form['username']
        user = User.query.filter_by(username = uname).first()
        if user is not None and user.loginAccount(request.form['password']):
            login_user(user)
            return redirect('/myfiles')
        else:
            return render_template('loginPage.html', message="Invalid username or password")
    return render_template('loginPage.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/myfiles')
     
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(User.query.filter_by(username = username))
        if User.query.filter_by(username = username).first():
            print("test")
            return render_template("createPage.html", message="Username already exists. Try again")
             
        user = User(username=username)
        user.createAccount(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('createPage.html')     

@app.route("/myfiles", methods=["GET","POST"])
@login_required
def home():
    return render_template("myfiles.html")

@app.route("/writeFile", methods=["GET","POST"])
def write():
    return render_template("createFile.html")

# @app.route("/logout")

if __name__ == '__main__':
    app.run()