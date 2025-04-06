from flask import Flask,request,render_template, url_for

app = Flask(__name__)

database={
    'ella' : {'password': '123', 'role': 'donor'},
    'madi': {'password': '123', 'role': 'recipient'},
    'yuzyki' : {'password': '123', 'role': 'donor'}
}

@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route('/form_login',methods=['POST','GET'])
def login():
    username1 = request.form['username']
    password1 = request.form['password']

    if username1 not in database:
        return render_template('register.html',info='Invalid User')
    
    if database[username1]['password'] != password1:
        return render_template('login.html')
    
    user_role = database[username1]['role']
    if user_role == 'recipient':
        return render_template('home_recipient.html', name=username1)
    else:
        return render_template('home_donor.html',name=username1)
    
# @app.route('/register')
# def register():
#     return render_template("register.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
        
    full_name = request.form['full_name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    database[username] = {'password': password, 'role': role}

    return redirect(url_for('hello_world'))


if __name__ == '__main__':
    app.run(debug=True)