#
import functools
import os
from   flask_sqlalchemy import SQLAlchemy

from flask import ( Blueprint, flash, g, redirect, render_template, request, session, url_for,Flask )
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
bp = Blueprint('auth', __name__, url_prefix='/auth')

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db' #'postgres://yyilkblbrykehy:84cf0c8052645f4de0c2d7c64dce1ae3c781581f3358eae5f0efddd7c0de00c1@ec2-35-174-127-63.compute-1.amazonaws.com:5432/d8n77erpfco80f'#os.environ.get('DATABASE_URL')#
db =SQLAlchemy(app)

class  info(db.Model):
    __tablename__='info'
    id = db.Column('id', db.Integer, primary_key=True)
    username=db.Column(db.String(80))
    password = db.Column(db.String(120))


#mine
@bp.route('/getcred', methods=('GET', 'POST'))
def getcred():
    if request.method == 'POST':
        username1 = request.form['username']
        password1 = request.form['password']
        data = info(username=username1, password=password1)
        db.session.add(data)
        db.session.commit()
    return render_template('auth/getcred.html')

@bp.route('/register', methods=('GET', 'POST'))
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
        flash(error)
    return render_template('auth/register.html')


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
