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
 
    

@app.route('/blog')
def blog():
    title = request.args.get('title')
    body = request.args.get('body')

    blog = Blog(title, body)

    blog_id = Blog.query.get('id')
    
    blogs = Blog.query.filter_by().all()
    
    return render_template ('blog.html', blogs=blogs) 

    
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        blog = Blog(title, body) 
        

        if (not title):
            flash ("Please enter a title", 'title_error')
            return redirect('/newpost')
        elif not body:
            flash ("Please make a entry", 'body_error' )
            return redirect ('/newpost')
        else:
            db.session.add(blog)
            db.session.commit()
            return redirect ('/display_blog')
                
    

    return render_template('newpost.html')

@app.route('/display_blog')
def display():
    title = request.args.get('title')
    body = request.args.get('body')
    blog = Blog(title, body)
    return render_template('display_blog.html', title=title, body=body, blog=blog)


if __name__ == '__main__':
    app.run()