from flask import Flask, redirect, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'p4458[peik)&yylls'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(400))

    def __init__(self, title, body):

        self.title = title
        self.body = body

    

@app.route('/')
def index():
    return render_template('newpost.html')


@app.route('/blog', methods=['POST'])
def blog():

    
@app.route('/newpost', methods=['POST'])
def new_post():

    title = request.form['title']
    body = request.form['body']
    if body.
    new_post = Blog(title,body)
    db.session.add(new_post)
    db.session.commit()



if __name__ == '__main__':
    app.run()