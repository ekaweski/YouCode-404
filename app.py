from flask import Flask, render_template, request, redirect, url_for, session
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
    items = db.Column(db.Text(00))
    contact = db.Column(db.String(150))

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    items = TextAreaField('Items', validators=[DataRequired()])
    contact = StringField('Contact Info', validators=[DataRequired()])
    submit = SubmitField('Post')

with app.app_context():
    db.create_all()
    
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

@app.route('/form_login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username1 = request.form.get('username')
        password1 = request.form.get('password')

        if username1 not in database:
            return render_template('register.html', info='Invalid User')

        if database[username1]['password'] != password1:
            return render_template('login.html', info='Incorrect Password')

        session['username'] = username1
        session['role'] = database[username1]['role']

        if session['role'] == 'recipient':
            return redirect(url_for('recipient_redirect'))
        else:
            return render_template("home_donor.html")

    return render_template('login.html')

    

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

    if role == 'recipient':
        return redirect(url_for('recipient_redirect'))
    
    else:
        return render_template("home_donor.html")


@app.route('/post_upload',methods=['POST','GET'])
def donor():
    form = PostForm()
    if form:
        print(form, file=sys.stderr)
        new_post = Post(
            title=form.title.data,
            location=form.location.data,
            date=form.date.data,
            time=form.time.data,
            items=form.items.data,
            contact=form.contact.data
        )
        db.session.add(new_post)
        db.session.commit()
        return render_template('home_donor.html')
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

@app.route('/liked_posts')
def likes():
    return render_template('liked.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
