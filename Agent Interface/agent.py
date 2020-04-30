from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'thiru123'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'realestate'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
     # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form:
        id = request.form['id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM agent WHERE id = %s AND password = %s', (id, password,))
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['ID'] = account['ID']
            session['NAME'] = account['NAME']
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg='')

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('ID', None)
   session.pop('NAME', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form and 'mobile' in request.form:
        # Create variables for easy access
        id = request.form['id']
        name = request.form['name']
        password = request.form['password']
        mobile = request.form['mobile']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM agent WHERE id = %s', (id,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', id):
            msg = 'Username must contain only characters and numbers,(use MDU at the begining)!'
        elif not id or not password or not mobile:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO AGENT VALUES ( %s,%s, %s,%s,0,0)', (id,name,mobile,password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', ID =session['ID'])
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM AGENT WHERE id = %s', (session['ID'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@app.route("/Update_sales",methods=['GET','POST'])
def Update_sales():
    msg = ''
    if request.method=='POST':
        DEAL_NO = request.form['DEAL_NO']
        PID = request.form['PID']
        BUYER_NAME = request.form['BUYER_NAME']
        BUYER_MOBILE = request.form['BUYER_MOBILE']
        DEAL_DATE = request.form['DEAL_DATE']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM sales WHERE PID = %s', (PID,))
        property = cursor.fetchone()
        if property:
            return 'Property deal over already!'
        else:
            cursor.execute('INSERT INTO sales VALUES ( %s, %s, %s, %s, %s)', (DEAL_NO,PID,BUYER_NAME,BUYER_MOBILE,DEAL_DATE,))
            cursor.execute('UPDATE PROPERTY SET STATUS ="CLOSED" WHERE PID = %s',(PID,))
        mysql.connection.commit()
        msg ="sales updated"
    return render_template('Update_sales.html', msg=msg)



if(__name__=='__main__'):
    app.secret_key="abc123"
    app.run(debug=True)
