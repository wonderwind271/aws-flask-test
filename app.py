from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from form import *
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '7592a32b23cd57c86c45'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    def __repr__(self):
        return f'User({self.username}, {self.email})'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f'Post({self.title}, {self.date_posted})'

posts = [
    {'author': 'Shuyu',
     'title': 'First Post',
     'content': 'First Content',
     'date_posted': '2-22-2023'},
    {'author': 'Tim',
     'title': 'Post 2',
     'content': 'Content 2',
     'date_posted': '2-23-2023'}
]

@app.route('/')
@app.route('/home')
def home():  # put application's code here
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title="about page")

@app.route('/register', methods=['GET', 'POST'])
def register():  # put application's code here
    form = RegistrationForm()
    username = request.form.get('username')
    if form.validate_on_submit():
        flash('successfully create account', 'success')
        return redirect(url_for('home'))


    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)

if __name__ == '__main__':
    app.run(debug=True)
