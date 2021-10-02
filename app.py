from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createAccount', methods=['POST'])
def create():
    if request.method == 'POST':
        return render_template('createAccount.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        return render_template('success.html')

@app.route('/create', methods=['POST'])
def created():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return render_template('success.html')

if __name__ == '__main__':
    app.debug = True
    app.run()