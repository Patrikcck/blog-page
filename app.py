from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

BACKGROUND_IMAGES = ['fundalb.jpg', 'fundalb2.jpg', 'fundalb3.jpg']

@app.context_processor
def inject_background_image():
    return {'background_image': random.choice(BACKGROUND_IMAGES)}



#Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    posted_by = db.relationship('User')
    comments = db.relationship('Comment')
    posted = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    reads = db.Column(db.Integer, nullable=False, default=0)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))
    post = db.relationship('Post')
    body = db.Column(db.String(500), nullable = False)

#Routes

@app.route('/')
def display_posts():
    posts = Post.query.all()
    return render_template('posts.html', posts = posts)


@app.route('/user/profile/<int:user_id>')
def display_user_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template('user_profile.html', user=user)


@app.route('/users')
def display_all_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/post/<int:post_id>')
def display_post(post_id):
    found_post = Post.query.filter_by(id=post_id).first()
    found_post.reads += 1
    db.session.commit()
    return render_template('post.html', post=found_post)

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post = Post.query.get_or_404(post_id)
    body = request.form['body']
    comment = Comment(post_id=post_id, body=body)
    db.session.add(comment)
    post.reads -= 1 
    db.session.commit()
    return redirect(url_for('display_post', post_id=post_id))

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    users = User.query.all()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user_id = request.form['user_id']
        posted = datetime.now()

        post = Post(title=title, body=body, user_id=user_id, posted=posted)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('display_posts'))
    
    return render_template('create_post.html', users=users)


if __name__ == "__main__":
    app.run()