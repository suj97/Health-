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
app.config['MYSQL_DATABASE_DB'] = 'hospitals'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# # Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',			# The SECRET_KEY is needed to keep the client-side sessions secure.
    USERNAME='root',
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
	# email = 'anonymous_user'
	cursor.execute("SELECT * from login_credentials where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		return render_template('index.html')
	return render_template('index.html', user=email)

@app.route('/facilities')
def facilities():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from login_credentials where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		return render_template('facilities.html')
	return render_template('facilities.html', user=email)

@app.route('/about')
def about():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from login_credentials where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		return render_template('about.html')
	return render_template('about.html', user=email)



@app.route('/contact')
def contact():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from login_credentials where username='" + email + "'")
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
	if email == 'reception':
		cursor.execute("SELECT count(*) from appointments where status='false'")
		appt_number = cursor.fetchone()[0]
		return render_template('dashboard_reception.html', user=email, appt_number= appt_number)
	return render_template('dashboard.html', user=email, record=record)

@app.route('/dashboard_view')
def dashboard_view():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from details where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		render_template('index.html')
	if email == 'reception':
		cursor.execute("SELECT username,patient_name,patient_contact from details ")
		patient = cursor.fetchall()
		return render_template('reception_view.html', user=email, patient= patient)

@app.route('/dashboard_settings')
def dashboard_settings():
	email = request.cookies.get('userID')
	if email == 'reception':
		return render_template('reception_settings.html', user=email)	
	return render_template('dashboard_settings.html', user=email)

@app.route('/dashboard_book')
def dashboard_book():
	email = request.cookies.get('userID')
	return render_template('dashboard_book.html', user=email)

@app.route('/book_appointment',methods=['GET', 'POST'])
def book_appointment():
	message = None
	email = request.cookies.get('userID')
	if request.method == 'POST':
		book_name = request.form['book_name']
		book_email = request.form['book_email']
		book_date = request.form['book_date']
		book_type = request.form.get('book_type')
		conn = mysql.get_db()
		cursor = conn.cursor()
		cursor.execute("SELECT * from login_credentials where username='" + book_email + "'")
		entry_user = cursor.fetchone()
		cursor.execute("SELECT * from appointments where username='" + book_email + "' and booking_date='" + book_date + "'")
		key = cursor.fetchone()
		if entry_user is None:
			message = "Username/Email is not registered"
			flash(message, 'error') 
			if email == 'anonymous_user':
				return render_template('index.html')	
			return render_template('dashboard_book.html', user=email)
		elif key is None:
			cursor.execute("insert into appointments (username, name, email, booking_date, department) values ('" + book_email + "', '" + book_name + "', '" + book_email + "', '" + book_date + "', '" + book_type + "')")
			message = "Appointment of " + book_email +" for date : " + book_date + " has been booked successfully in " + book_type + " section"
			conn.commit()
			flash(message, 'success')
			if email == 'anonymous_user':
				return render_template('index.html')	
			return render_template('dashboard_book.html', user=email)			
		else:
			message = book_email + " has previously booked an appointment on the same date"
			flash(message, 'error')
			if email == 'anonymous_user':
				return render_template('index.html')	
			return render_template('dashboard_book.html', user=email)			
	if email == 'anonymous_user':
		return render_template('index.html')	
	return render_template('dashboard_book.html', user=email)

@app.route('/dashboard_reports')
def dashboard_reports():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from details where username='" + email + "'")
	record = cursor.fetchone()
	if record is None:
		render_template('index.html')
	cursor.execute("SELECT * from records where username='" + email + "' ORDER BY STR_TO_DATE(visit_date, '%m/%d/%Y')")
	record = cursor.fetchall()
	cursor.execute("SELECT * from appointments where username='" + email + "' and status='false' ORDER BY STR_TO_DATE(booking_date, '%m/%d/%Y')")
	appts = cursor.fetchall()
	return render_template('dashboard_reports.html',user=email, record=record, appts=appts)


@app.route('/login', methods=['GET', 'POST'])
def login():
	message = None
	if request.method == 'POST':
		cursor = mysql.get_db().cursor()
		email = request.form['email']
		password = request.form['password']
		cursor.execute("SELECT * from login_credentials where username='" + email + "'")
		entry_user = cursor.fetchone()
		cursor.execute("SELECT * from login_credentials where username='" + email + "' and password='" + password + "'")
		entry_pass = cursor.fetchone()
		if entry_user is None:
			message = 'Username is not registered'
			flash(message, 'login_error')
			return render_template('index.html')
		elif entry_pass is None:
			message = 'Password is not correct'
			flash(message, 'login_error')
			return render_template('index.html')
		elif email == 'reception':
			session['logged_in'] = True
			message = email + 'successfully logged in'
			cursor.execute("SELECT count(*) from appointments where status='false'")
			appt_number = cursor.fetchone()[0]
			resp = make_response(render_template('dashboard_reception.html', user=email, appt_number=appt_number))
			resp.set_cookie('userID', email)
			return resp
		else:
			session['logged_in'] = True
			cursor.execute("SELECT * from details where username='" + email + "'")
			record = cursor.fetchone()
			message = 'Successfully logged in'
			resp = make_response(render_template('dashboard.html', user=email, record=record))
			resp.set_cookie('userID', email)
			return resp
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	message = None
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
				message = "Password do not match" 
				flash(message, 'register_error')
				return render_template('index.html')
			else:
				cursor.execute("insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('" + email + "', '" + patient_name + "', '" + patient_age + "', '" + patient_sex + "', '" + patient_blood_group + "', '" + patient_weight + "', '" + patient_contact + "')")
				cursor.execute("insert into login_credentials (username, password) values ('" + email + "', '" + password + "')")
				conn.commit()
				message = "Username " + email + " successfully registered"
				flash(message, 'register_success')
				return render_template('index.html')
		else:
			message = "Email is already registered"
			flash(message, 'register_error')
			return render_template('index.html')
	return redirect(url_for('index'))

@app.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
	error = None
	email = request.cookies.get('userID')
	if request.method == 'POST':
		old_pass = request.form['old_pass']
		new_pass = request.form['new_pass']
		conn = mysql.get_db()
		cursor = conn.cursor()
		cursor.execute("SELECT * from login_credentials where username='" + email + "' and password='" + old_pass + "'")
		entry_pass = cursor.fetchone()
		if entry_pass is None:
			message = 'Password is not correct'
			flash(message, 'change_pass_error')
			if email == 'reception':
				return render_template('reception_settings.html', user=email)	
			return render_template('dashboard_settings.html', user=email)
		else:
			cursor.execute("UPDATE login_credentials SET password='" + new_pass + "' where username='" + email + "'")
			conn.commit()
			message = 'Password updated successfully'
			flash(message, 'change_pass_success')
			if email == 'reception':
				return render_template('reception_settings.html', user=email)			
			return render_template('dashboard_settings.html', user=email)
	return render_template('dashboard_settings.html', user=email)


@app.route('/change_number', methods=['GET', 'POST'])
def change_number():
	error = None
	email = request.cookies.get('userID')
	if request.method == 'POST':
		new_contact = request.form['new_contact']
		conn = mysql.get_db()
		cursor = conn.cursor()
		cursor.execute("UPDATE details SET patient_contact='" + new_contact + "' where username='" + email + "'")
		message = 'Contact no. updated successfully'
		conn.commit()
		flash(message, 'change_contact')
		return render_template('dashboard_settings.html', user=email)
	return render_template('dashboard_settings.html', user=email)

@app.route('/reception_appt')
def reception_appt():
	email = request.cookies.get('userID')
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * from appointments where status='true' ORDER BY STR_TO_DATE(booking_date, '%m/%d/%Y')")
	record_true = cursor.fetchall()
	cursor.execute("SELECT * from appointments where status='false' ORDER BY STR_TO_DATE(booking_date, '%m/%d/%Y')")
	record_false = cursor.fetchall()
	return render_template('reception_appointments.html', user=email, record_true=record_true, record_false= record_false)

@app.route('/reception_add')
def reception_add():
	email = request.cookies.get('userID')
	return render_template('reception_add.html', user=email)


@app.route('/add_record',methods=['GET', 'POST'])
def add_record():
	message = None
	email = request.cookies.get('userID')
	if request.method == 'POST':
		username = request.form['username']
		visit_date = request.form['visit_date']
		prescription = request.form['prescription']
		conn = mysql.get_db()
		cursor = conn.cursor()
		cursor.execute("SELECT * from login_credentials where username='" + username + "'")
		entry_user = cursor.fetchone()
		cursor.execute("SELECT * from appointments where username='" + username + "' and booking_date='" + visit_date + "'")
		key = cursor.fetchone()
		cursor.execute("SELECT * from records where username='" + username + "' and visit_date='" + visit_date + "'")
		entry = cursor.fetchone()
		if entry_user is None:
			message = "Username/Email is not registered" 
			flash(message, 'error')
			return render_template('reception_add.html', user=email)
		elif key is None:
			message = "No such appointment is there"
			flash(message, 'error')
			return render_template('reception_add.html', user=email)
		elif entry is None:
			cursor.execute("insert into records (username, visit_date, prescription) values ('" + username + "', '" + visit_date + "', '" + prescription + "')")
			message = "You have added record for " + username + " who visited on " + visit_date
			cursor.execute("update appointments SET status='true' where username='"+ username +"' and booking_date='"+visit_date+"'")
			conn.commit()
			flash(message, 'success')
			return render_template('reception_add.html', user=email)
		else:
			message = "This record of " + username + " has been added previously"
			flash(message, 'error')
			return render_template('reception_add.html', user=email)
	return render_template('reception_add.html', user=email)







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
	resp.set_cookie('userID', 'anonymous_user')
	return resp
    # return redirect(url_for('index'))