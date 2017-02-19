# export FLASK_APP=app.py
# export FLASK_DEBUG=1
# flask run
# flask initdb

# all the imports 
import os
import sqlite3
from flask import Flask             #for basic app
from flask import request           #for request methods
from flask import session           
from flask import g
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template   #for using html files, templates and layouts
from flask import flash

import logging
from logging.handlers import RotatingFileHandler
# create our little application :)
app = Flask(__name__)               #help it determine the root path
app.config.from_object(__name__)


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'robyrockk'
app.config['MYSQL_DATABASE_DB'] = 'hospitals'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# # Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',			# The SECRET_KEY is needed to keep the client-side sessions secure.
    USERNAME='roby',	
    PASSWORD='rockk'
))
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv

# # Because database connections encapsulate a transaction,
# # we also need to make sure that only one request at the time uses the connection. 

# # For instance, the request variable is the request object associated with the current request,
# # whereas g is a general purpose variable associated with the current application context.

# def get_db():
#     """Opens a new database connection if there is none yet for the current application context."""
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db


# # Functions marked with teardown_appcontext() are called every time the app context tears down. 
# @app.teardown_appcontext	# to properly disconnect
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()


# def init_db():
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()


# # The app.cli.command() decorator registers a new command with the flask script.
# # When the command executes, Flask will automatically create an application context
# # for us bound to the right application. 
# @app.cli.command('initdb')
# def initdb_command():
#     """Initializes the database."""
#     init_db()
#     print 'Initialized the database.'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/facilities')
def facilities():
    return render_template('facilities.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard_book')
def dashboard_book():
    return render_template('dashboard_book.html')

@app.route('/dashboard_reports')
def dashboard_reports():
    return render_template('dashboard_reports.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		# db = get_db()
		# cursor = mysql.connect().cursor()
		cursor = mysql.get_db().cursor()
		email = request.form['email']
		password = request.form['password']
		# cursor.execute("SELECT * from login_credentials where username = ?" ,[request.form['username']])
		cursor.execute("SELECT * from login_credentials where username='" + email + "'")
		# cursor.execute("SELECT * from login_credentials where username ='" + email "'")
		entry_user = cursor.fetchone()
		cursor.execute("SELECT * from login_credentials where username='" + email + "' and password='" + password + "'")
		# cursor.execute("SELECT * from login_credentials where username = ? and password = ?" ,[request.form['username'], request.form['password']])
		entry_pass = cursor.fetchone()
		if entry_user is None:
			error = 'Username is not registered'
			flash(error)
		elif entry_pass is None:
			error = 'Password is not correct'
			flash(error)
		else:
			session['logged_in'] = True
			flash("")
			return render_template('dashboard.html', user=email)
	# else:
	# return render_template('index.html', error=error)
	# render_template('index.html', error=error)
	return redirect(url_for('index'))
	# return render_template('user.html', user=user)



# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
# 		db = get_db()
# 		# user = db.execute('select username from login_credentials')
# 		# user_entries = user.fetchone()
# 		# password = db.execute('select password from login_credentials')
# 		# password_entries = password.fetchone()
# 		user = db.execute("SELECT * from login_credentials where username = ?" ,[request.form['username']])
# 		entry_user = user.fetchone()
# 		password = db.execute("SELECT * from login_credentials where username = ? and password = ?" ,[request.form['username'], request.form['password']])
# 		entry_pass = password.fetchone()
# 		# if request.form['username'] != user_entries:
# 		# 	error = 'Invalid username'
# 		# elif request.form['password'] != password_entries:
# 		# 	error = 'Invalid password'
# 		if entry_user is None:
# 			error = 'Username is not registered'
# 		elif entry_pass is None:
# 			error = 'Password is not correct'
#         # if request.form['username'] != app.config['USERNAME']:
#         #     error = 'Invalid username'
#         # elif request.form['password'] != app.config['PASSWORD']:
#         #     error = 'Invalid password'
# 		else:
# 			session['logged_in'] = True
# 			flash('You were logged in')
# 			return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	error = None
# 	if request.method == 'POST':
# 		email = request.form['email']
# 		password = request.form['password']

# 		return render_template('dashboard.html')
# 	else:
# 		return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		retype_password = request.form['retype_password']
		conn = mysql.get_db()
		cursor = conn.cursor()
		cursor.execute("SELECT * from login_credentials where username='" + email + "'")
		entry_user = cursor.fetchone()
		if entry_user is None:
			if password != retype_password:
				error = "Password do not match"
				flash(error)
			else:
				cursor.execute("insert into login_credentials (username, password) values ('" + email + "', '" + password + "')")
				conn.commit()
				flash("")
		else:
			error = "Email is already registered"
			flash(error)
	return redirect(url_for('index'))
	# else:
	# 	return redirect(url_for('index'))

# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                  [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))

# # @app.route('/checkDetails',methods=['POST','GET'])
# # def checkDetails():

# # 	# read the posted values from the UI
# # 	username = request.form['inputEmail']
# # 	password = request.form['inputPassword']

# # 	cursor = mysql.connect().cursor()
# # 	cursor.execute("SELECT * from tbl_user where user_username='" + username + "' and user_password='" + password + "'")
# # 	data = cursor.fetchone()
# # 	if data is None:
# # 		return "Username or Password is wrong"
# # 	else:
# # 		return str(data);

# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))

