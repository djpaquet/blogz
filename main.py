from flask import Flask, redirect, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import traceback 
import re

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'p4458[peik)&yylls'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(400))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, author):

        self.name = name
        self.body = body
        self.author = author

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='author')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/signup')

@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            #TODO "remember" that the user has logged in
            session['logged_in'] = True
            session['username'] = username
            print(session)
            flash('Logged in')
            
            return render_template('blog.html', user=user)
        
        else:
            #TODO explain why login failed
            flash('User password incorrect, or user does not exist', 'error')
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        #verify = request.form['verify']
        #user_id = request.args.get('id')
        #TODO - validate user data

        username_error = ''
        if len(username) >= 3 and len(username) <= 20:
            for character in username:
                if character == ' ':
                    username_error = 'Please enter a valid Username that has no spaces'
                    username = ''
        elif len(username) < 3 or len(username) > 20:
            username_error = 'Username must be between 3-20 characters'
            username = ''
    
    #validate password to meet criteria
        
        password_error = ''
        if len(password) >=3 and len(password) <=20:
            for character in password:
                if character == ' ':
                    password_error = 'Please enter a valid Password that has no spaces'
                    password = ''
        elif len(password) < 3 or len(password) > 20:
            password_error = 'Password must be at least 6 characters'
            password = ''
        
    #double check verify password that it matches passwordS
        verify = request.form['verify']
        verify_password_error = ''
        if password != verify:
            verify_password_error = 'Passwords do not match'
            password = ''
    
    #use regular expression to validate email
        if not re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.])', email):
            email_error = 'Please enter a valid email'
            email = ''


        existing_user = User.query.filter_by(email=email).first()
        #existing_username = User.query.filter_by(username=username).first()
        if not email_error and not password_error:
            if not verify_password_error:
                if not existing_user:
                    new_user = User(username, password, email)
                    db.session.add(new_user)
                    db.session.commit()
                    session['username'] = username
                    return redirect ('/')
            

            
        
                else:
                    #TODO user better response messaging
                    return '<h1>Username already exists</h1>'
                    return redirect('/login')
            
    return render_template ('signup.html', username_error= username_error, password_error=password_error,
                            email_error=email_error, verify_password_error=verify_password_error)

@app.route('/')
def index():
    
    users = User.query.all()
    return render_template('index.html', users=users)
    
    
    #blogs = Blog.query.all()
    #return render_template('blog.html', blogs=blogs)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    username = request.args.get('username')
    
    if not blog_id:
        blogs = Blog.query.filter_by(username=username).all()

        return render_template('blog.html', title='Blogz', blogs=blogs, username=username)
    else:
        blogs = Blog.query.filter_by(id=blog_id).all()

        return render_template('blog.html', title='Blogz', blogs=blogs, username=username)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error = ""
    body_error = ""

    if request.method == 'POST':
        name = request.form['name']
        body = request.form['body']
        author = User.query.filter_by(username=session['username']).first()
        blog = Blog(name, body, author)


        if not name and not body:
            title_error = "Please enter a title for your blog entry"
            body_error = "Please enter a blog to post"
            return render_template('newpost.html', title_error=title_error, body_error=body_error)
        if not name:
            title_error = "Please enter a title for your blog entry"
            return render_template('newpost.html', title_error=title_error)
        if not body:
            body_error = "Please enter a blog to post"
            return render_template('newpost.html', body_error=body_error)
        else:
             
            db.session.add(blog)
            db.session.commit()
            
            return render_template('display_blog.html', name=name, body=body, blog=blog)
                
    return render_template('newpost.html',body_error=body_error, title_error=title_error )

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

    
if __name__ == '__main__':
    app.run()