from flask import Flask, redirect, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import re 

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'p4458[peik)&yylls'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(400))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):

        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            #TODO "remember" that the user has logged in
            session['email'] = email
            flash('Logged in')
            print(session)
            return redirect('/newpost')
        
        else:
            #TODO explain why login failed
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
    

        #validate user data
        #validate email
        if not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.])",email ):
            email_error = 'Please enter a valid email'
            email = ''

        #validate password and verify password 
        password_error = ''
        if len(password) >=3 and len(password) <=20:
            for character in password:
                if character == ' ':
                    password_error = 'Please enter a valid Password that has no spaces'
                    password = ''
        elif len(password) < 3 or len(password) > 20:
            password_error = 'Password must be at least 6 characters'
            password = ''
        
        verify_password_error = ''
        if verify != password:
            verify_password_error = 'Passwords do not match'
            password = ''
        return render_template ('signup.html', password=password, 
                            password_error=password_error,
                            verify=verify,
                            verify_password_error=verify_password_error,
                            email=email, email_error=email_error)

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            #TODO remember the data

            return redirect('/newpost')
        
        #else:
            #TODO user better response messaging
            #return '<h1>Duplicate use</h1>'
        
            
    return render_template ('signup.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    id = request.args.get('id')

    if not id:
        blogs = Blog.query.filter_by().all()

        return render_template('blog.html', title='Build a Blog', blogs=blogs)
    else:
        blogs = Blog.query.filter_by(id=id).all()

        return render_template('blog.html', title='Build a Blog', blogs=blogs)




    
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error = ""
    body_error = ""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        blog = Blog(title, body) 
        #error = request.args.get('error')
        
        if not title and not body:
            title_error = "Please enter a title for your blog entry"
            body_error = "Please enter a blog to post"
            return render_template('newpost.html', title_error=title_error, body_error=body_error)
        if not title:
            title_error = "Please enter a title for your blog entry"
            return render_template('newpost.html', title_error=title_error)
        if not body:
            body_error = "Please enter a blog to post"
            return render_template('newpost.html', body_error=body_error)
        else:
            db.session.add(blog)
            db.session.commit()
            return render_template('display_blog.html', title=title, body=body, blog=blog)
                
    

    return render_template('newpost.html', body_error=body_error, title_error=title_error)


if __name__ == '__main__':
    app.run()