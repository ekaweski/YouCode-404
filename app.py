from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)

# Models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    location = db.Column(db.String(200))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    items = db.Column(db.String(100))
    contact = db.Column(db.String(150))

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    items = TextAreaField('Items', validators=[DataRequired()])
    contact = StringField('Contact Info', validators=[DataRequired()])
    submit = SubmitField('Post')

# Temporary in-memory user database
database = {
    'ella': {'password': '123', 'role': 'donor'},
    'madi': {'password': '123', 'role': 'recipient'},
    'yuzyki': {'password': '123', 'role': 'donor'}
}


@app.route('/')
def login_page():
    return render_template("login.html")

tempdata = {'title':'post', 'location':'ubc', 'date':'april second', 'time':'two pm', 
'fooditems':['carrots', 'peas', 'grapes']}

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
        return render_template('home_recipient.html', name=username1, post=tempdata)
    else:
        return render_template('home_donor.html',name=username1)
    

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

@app.route('/post_upload',methods=['POST','GET'])
def donor():
    form = dict(request.form)
    if form:
        print(form, file=sys.stderr)
        new_post = Post(
            title=form['posttitle'],
            location=form['location'],
            date=form['date'],
            time=form['time'],
            items=form['items'],
            contact=form['contact']
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('recipient'))
    return render_template('home_donor.html', form=form)

@app.route('/recipient/<int:post_id>')
def recipient(post_id):
    post = Post.query.get_or_404(post_id)

    # Get previous and next posts for navigation
    next_post = Post.query.filter(Post.id > post_id).order_by(Post.id.asc()).first()
    prev_post = Post.query.filter(Post.id < post_id).order_by(Post.id.desc()).first()

    return render_template('home_recipient.html', post=post, next_post=next_post, prev_post=prev_post)

@app.route('/recipient')
def recipient_redirect():
    first_post = Post.query.order_by(Post.id.asc()).first()
    if first_post:
        return redirect(url_for('recipient', post_id=first_post.id))
    return "No posts available."


if __name__ == '__main__':
    app.run(debug=True)