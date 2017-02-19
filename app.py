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
# from werkzeug import generate_password_hash, check_password_hash
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template   #for using html files, templates and layouts
from flask import flash
from flask import make_response

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
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from details where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		return render_template('index.html')
	return render_template('index.html', user=email)

@app.route('/facilities')
def facilities():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from details where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		return render_template('facilities.html')
	return render_template('facilities.html', user=email)

@app.route('/dashboard_settings')
def dashboard_settings():
    return render_template('dashboard_settings.html')

@app.route('/about')
def about():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from details where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		return render_template('about.html')
	return render_template('about.html', user=email)


@app.route('/services')
def services():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from details where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		return render_template('services.html')
	return render_template('services.html', user=email)


@app.route('/contact')
def contact():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from details where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		return render_template('contact.html')
	return render_template('contact.html', user=email)

@app.route('/dashboard')
def dashboard():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from details where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		render_template('index.html')
	return render_template('dashboard.html', user=email, record=record)

@app.route('/dashboard_book')
def dashboard_book():
    return render_template('dashboard_book.html')

@app.route('/dashboard_reports')
def dashboard_reports():
    return render_template('dashboard_reports.html')

@app.route('/book_appointment',methods=['GET', 'POST'])
def book_appointment():
	if request.method == 'POST':
		book_name = request.form['book_name']
		book_email = request.form['book_email']
		book_date = request.form['book_date']
		book_type = request.form.get('book_type')
		return render_template('book_appointment.html', book_name=book_name, book_email=book_email, book_date=book_date, book_type=book_type)
	else:
		return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error=None
	if request.method == 'POST':
		cursor = mysql.get_db().cursor()
		email = request.form['email']
		password = request.form['password']
		cursor.execute("SELECT * from login_credentials where username='" + email + "'")
		entry_user = cursor.fetchone()
		cursor.execute("SELECT * from login_credentials where username='" + email + "' and password='" + password + "'")
		entry_pass = cursor.fetchone()
		if entry_user is None:
			error = 'Username is not registered'
			flash(error)
		elif entry_pass is None:
			error = 'Password is not correct'
			flash(error)
		else:
			session['logged_in'] = True
			flash('')
			cursor.execute("SELECT * from details where username='" + email + "'")
			record = cursor.fetchone()
			resp = make_response(render_template('dashboard.html', user=email, record=record))
			resp.set_cookie('userID', email)
			return resp
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		retype_password = request.form['retype_password']
		patient_name = request.form['patient_name']
		patient_age = request.form['patient_age']
		patient_sex = request.form['patient_sex']
		patient_blood_group = request.form['patient_blood_group']
		patient_weight = request.form['patient_weight']
		patient_contact = request.form['patient_contact']
		conn = mysql.get_db()
		cursor = conn.cursor()
		cursor.execute("SELECT * from login_credentials where username='" + email + "'")
		entry_user = cursor.fetchone()
		if entry_user is None:
			if password != retype_password:
				error = ["Password do not match", "register"] 
				flash(error)
			else:
				cursor.execute("insert into login_credentials (username, password) values ('" + email + "', '" + password + "')")
				conn.commit()
				cursor.execute("insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('" + email + "', '" + patient_name + "', '" + patient_age + "', '" + patient_sex + "', '" + patient_blood_group + "', '" + patient_weight + "', '" + patient_contact + "')")
				cursor.commit()
		else:
			error = ["Email is already registered","register"]
			flash(error)
	return redirect(url_for('index'))

@app.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
	error = None
	if request.method == 'POST':
		old_pass = request.form['old_pass']
		new_pass = request.form['new_pass']
		conn = mysql.get_db()
		cursor = conn.cursor()
		email = request.cookies.get('userID')
		cursor.execute("SELECT * from login_credentials where username='" + email + "' and password='" + old_pass + "'")
		entry_pass = cursor.fetchone()
		if entry_pass is None:
			error = 'Password is not correct'
			# flash(error)
		else:
			# cursor.execute("SELECT * from login_credentials where username='" + email + "' and password='" + password + "'")
			cursor.execute("UPDATE login_credentials SET password='" + new_pass + "' where username='" + email + "'")
			# flash("Password Updated")
			conn.commit()
			return redirect(url_for('dashboard'))
	return render_template('dashboard_settings.html')


@app.route('/change_number', methods=['GET', 'POST'])
def change_number():
	error = None
	if request.method == 'POST':
		new_contact = request.form['new_contact']
		conn = mysql.get_db()
		cursor = conn.cursor()
		email = request.cookies.get('userID')
		cursor.execute("UPDATE details SET patient_contact='" + new_contact + "' where username='" + email + "'")
		# flash("Contact Updated")
		conn.commit()
		return redirect(url_for('dashboard'))
	return render_template('dashboard_settings.html')



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


@app.route('/logout')
def logout():
    # session.pop('logged_in', None)
    # flash('You were logged out')
	resp = make_response(render_template('index.html'))
	resp.set_cookie('userID', 'logout')
	return resp
    # return redirect(url_for('index'))