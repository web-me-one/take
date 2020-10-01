import os
from flask import Flask
from   flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://yyilkblbrykehy:84cf0c8052645f4de0c2d7c64dce1ae3c781581f3358eae5f0efddd7c0de00c1@ec2-35-174-127-63.compute-1.amazonaws.com:5432/d8n77erpfco80f'#os.environ.get('DATABASE_URL')#'sqlite:///test.db' #
db =SQLAlchemy(app)

class  info(db.Model):
    __tablename__='info'
    id = db.Column('id', db.Integer, primary_key=True)
    username=db.Column(db.String(80))
    password = db.Column(db.String(120))
    
