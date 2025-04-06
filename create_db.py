from datetime import datetime

from app import app, db, User, Post, Comment

with app.app_context():
    db.create_all()
    
    axiu = User(username='Axiu', email='axiu@yehaw.com', age=19)
    patrick = User(username='Patrick', email='patrick@jmail,com', age=20)
    codrin = User(username='Codrin', email='corvin@uvt.cum', age=20)

    db.session.add(axiu)
    db.session.add(patrick)
    db.session.add(codrin)
    
    db.session.commit()