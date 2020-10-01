import os
from flask import Flask
from   flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('DATABASE_URL')#'sqlite:///test.db' #
db =SQLAlchemy(app)

class  info(db.Model):
    __tablename__='info'
    id = db.Column('id', db.Integer, primary_key=True)
    username=db.Column(db.String(80))
    password = db.Column(db.String(120))
    
