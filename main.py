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

    def __init__(self, title, body, owner):

        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, user, password):
        self.user = user
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    user = request.form['user']
    password = request.form['password']
    users = User.query.filter_by(user=user).first()
    
    
    if request.method == 'POST':
        
        if user and user.password == password:
            #TODO "remember" that the user has logged in
            session['user'] = user
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
        user = request.form['user']
        password = request.form['password']
        verify = request.form['verify']
        user_id = request.args.get('id')
        #TODO - validate user data

        existing_user = User.query.filter_by(user_id=user_id).first()
        if not existing_user:
            new_user = User(user, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = user
            #TODO remember the data

            return redirect('/')
        
        else:
            #TODO user better response messaging
            return '<h1>Duplicate use</h1>'
        
            
    return render_template ('register.html')
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
        error = request.args.get('error')
        
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
                
    return render_template('newpost.html')

    
if __name__ == '__main__':
    app.run()