from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from dotenv import load_dotenv
import os

from models import db, login, User, File
from keyGenerators import getMyPrivateKey, getSharedKey

app = Flask(__name__)
app.secret_key = os.urandom(16)

load_dotenv()

ENV = "prod"
print(os.environ.get("DATABASE_URL"))
if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = 'login'
 
@app.before_first_request
def reset():
    # db.drop_all()
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect('/myfiles')

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

        if User.query.filter_by(username = username).first():
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
    files = File.query.filter_by(owner=current_user.username).order_by((File.lastModified.desc())).all()
    return render_template("myfiles.html", files=files)

@app.route("/sharedfiles", methods=["GET","POST"])
def homeShared():
    files = File.query.filter_by(sharedwith=current_user.username).order_by((File.lastModified.desc())).all()
    return render_template("sharedfiles.html", files=files)


@app.route("/writeFile", methods=["GET","POST"])
def write():
    if request.form.get("cancel"):
        return redirect("/myfiles")
    users = [user.username for user in User.query.all() if user.username != current_user.username]
    # if request.method == "POST":
    filename = request.form.get("filename")
    sharewith = request.form.get("user")
    content = request.form.get("contents")
    if filename is not None and sharewith is not None and content is not None:
        if File.query.filter_by(name=filename).first():
            return render_template("createFile.html", message1="File already exists.", users=users, content= content)
        if filename != '' and sharewith != '':
            myfile = File(name=filename, sharedwith=sharewith, owner=current_user.username)
            otherpublickey = User.query.filter_by(username = sharewith).first().publickey
            myprivatekey = getMyPrivateKey(current_user.passkey, current_user.secret)
            myfile.create(content, getSharedKey(otherpublickey, myprivatekey))
            if request.form.get("save"):
                db.session.add(myfile)
                db.session.commit()            
                return redirect("/myfiles")
            return render_template("createFile.html", users = users, filename = filename, content = content)
    return render_template("createFile.html", users=users)



@app.route("/viewFile/<string:filename>", methods=["GET","POST"])
def read(filename):
    if request.form.get('back'):
        return redirect("/myfiles")
    myfile = File.query.filter_by(name=filename).first()
    myprivatekey = getMyPrivateKey(current_user.passkey, current_user.secret)
    if myfile.owner == current_user.username:
        otherpublickey = User.query.filter_by(username=myfile.sharedwith).first().publickey
    else:
        otherpublickey = User.query.filter_by(username=myfile.owner).first().publickey
    content = myfile.view(getSharedKey(otherpublickey, myprivatekey))
    if myfile.owner == current_user.username:
        return render_template("viewFile.html", owner=True, filename=filename, user=myfile.sharedwith, content=content)
    if request.form.get("update"):
        return redirect(url_for("update", filename=filename))
    return render_template("viewFile.html", filename=filename, user=myfile.owner, content=content)

@app.route("/writeFile/<filename>", methods=["GET","POST"])
def update(filename):
    if request.form.get('cancel'):
        return redirect("/myfiles")
    users = [user.username for user in User.query.all() if user.username != current_user.username]
    myfile = File.query.filter_by(name=filename).first()
    otherpublickey = User.query.filter_by(username=myfile.sharedwith).first().publickey
    myprivatekey = getMyPrivateKey(current_user.passkey, current_user.secret)
    content = myfile.view(getSharedKey(otherpublickey, myprivatekey))
    if request.form.get("save"):
        sharewith = request.form.get("user")
        content = request.form.get("contents")
        if sharewith != myfile.sharedwith:
            otherpublickey = User.query.filter_by(username = sharewith).first().publickey
        myfile.create(content, getSharedKey(otherpublickey, myprivatekey))
        db.session.delete(myfile)
        db.session.add(myfile)
        db.session.commit()
        return redirect("/myfiles")
            
    return render_template("createFile.html", update=True, users=users, filename=filename, uname=myfile.sharedwith, content=content)

@app.route('/logout', methods=["GET","POST"])
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run()