from flask import Flask,request,render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("login.html")
database={'ella':'123','madi':'123','yuzuki':'123'}

@app.route('/form_login',methods=['POST','GET'])
def login():
    username1 = request.form['username']
    password1 = request.form['password']

    if username1 not in database:
        return render_template('login.html',info='Invalid User')
    else:

        if database[username1]!=password1:
            return render_template('login.html',info='Invalid Password')
        
        else:
             return render_template('home_donor.html',name=username1)

if __name__ == '__main__':
    app.run(debug=True)