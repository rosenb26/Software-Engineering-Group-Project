import sqlite3
import time
import datetime
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, redirect, url_for, flash, session
import re

app = Flask(__name__)

app.config['STATIC_FOLDER'] = 'static'
bootstrap = Bootstrap5(app)

#secret key
app.config['SECRET_KEY'] = 'keyfob'

# Set app context
def db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Dummy staff username and password (replace this with a secure authentication mechanism)
# STAFF_USERNAME = "admin"
# STAFF_PASSWORD = "password"

# In-memory list to store registered visitors
registered_visitors = []

# In-memory list to store checked-in visitors
checked_in_visitors = []


@app.route('/', methods=['GET', 'POST'])
def login():
    cursor = db_connection()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials
        data = cursor.execute('SELECT * from StaffLogin WHERE username = ? AND password = ?', (username, password)).fetchone()
        if data:
            session['loggedin'] = True
            session['id'] = data['staffID']
            session['username'] = data['username']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password. Please try again."
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    cursor = db_connection()

    # Retrieve counts from the VisitorList table
    checked_in_count = cursor.execute('SELECT COUNT(*) FROM VisitorList WHERE checkOutTime IS NULL').fetchone()[0]
    checked_out_count = cursor.execute('SELECT COUNT(*) FROM VisitorList WHERE checkOutTime IS NOT NULL').fetchone()[0]
    registered_count = cursor.execute('SELECT COUNT(*) FROM Visitors').fetchone()[0]

    return render_template('dashboard.html', checked_in_count=checked_in_count, checked_out_count=checked_out_count,
                           registered_count=registered_count)

@app.route('/visitors')
def visitors():
    visitor_type = request.args.get('type', 'registered')
    cursor = db_connection()

    # Retrieve data from the VisitorList table
    visitors_data = cursor.execute('SELECT * FROM VisitorList').fetchall()

    checked_in_count = sum(1 for visitor in visitors_data if visitor['checkOutTime'] is None)
    checked_out_count = len(visitors_data) - checked_in_count

    if visitor_type == 'checked_in':
        filtered_visitors = [visitor for visitor in visitors_data if visitor['checkOutTime'] is None]
    elif visitor_type == 'checked_out':
        filtered_visitors = [visitor for visitor in visitors_data if visitor['checkOutTime'] is not None]
    else:
        filtered_visitors = visitors_data

    return render_template('visitors.html', visitors=filtered_visitors, checked_in_visitors=checked_in_visitors,
                           type=visitor_type, checked_in_count=checked_in_count, checked_out_count=checked_out_count)


@app.route('/registration-success')
def registration_success():
    return render_template('registration_success.html')


# Modify the register route to include the 'checked_in' field
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("Register route received a POST request")
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        residentname = request.form.get('residentname')
        date = request.form.get('date')
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')

        # Parse resident first and last name
        firstlast = residentname.split()
        rfirstname = firstlast[0]
        rlastname = firstlast[1]

        # Retrieve resident ID based on resident name
        with db_connection() as connection:
            cursor = connection.cursor()
            data = cursor.execute(
                "SELECT residentID FROM Residents WHERE residentFirstName = ? AND residentLastName = ?", (rfirstname, rlastname)).fetchone()

            if data:
                resid = data['residentID']
            else:
                # Handle the case where the resident is not found
                flash('Error: Resident not found.')
                return redirect(url_for('register'))

        # Add some code her to check if visitor already exists

        # Commit user entries to the database
        with db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Visitors (dateRegistered, email, visitorFirstName, visitorLastName, residentFirstName, residentLastName, residentID)"
                "VALUES (?,?,?,?,?,?,?)",
                (date, f'{email}', f'{firstname}', f'{lastname}', f'{residentname}', f'{residentname}', resid))

            connection.commit()

        return redirect(url_for('registration_success'))

    return render_template('index.html')


@app.route('/visitor-dashboard', methods=['GET', 'POST'])
def visitor_dashboard():
    cursor = db_connection()
    if request.method == 'POST':
        # User needs to register
        if 'register' in request.form:
            return redirect(url_for('register'))

        # User is checking in as returning user
        elif 'checkin' in request.form:
            visitor_email = request.form['visitor_email']
            print(f"Check-in request for email: {visitor_email}")

            # Retrieve visitor information from the Visitors table
            visitor_data = cursor.execute("SELECT * FROM Visitors WHERE email = ?", (visitor_email,)).fetchone()

            # Check if the visitor exists
            if not visitor_data or visitor_data['checkOutTime']:
                print("Visitor not found or already checked in.")
                return "Visitor not found or already checked in."

            # Insert new entry into Visitor List table
            with db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO VisitorList (dateRegistered, visitorFirstName, visitorLastName, residentFirstName, residentLastName, residentID, checkInTime) VALUES (DATE('now'),?,?,?,?,?, CURRENT_TIMESTAMP)",
                               (visitor_data['visitorFirstName'], visitor_data['visitorLastName'], visitor_data['residentFirstName'], visitor_data['residentLastName'], visitor_data['residentID']))
                connection.commit()

            print("Check-in successful!")
            return render_template('checkin_success.html')

        # User is checking out
        elif 'checkout' in request.form:
            visitor_email = request.form['visitor_email']
            print(f"Check-out request for email: {visitor_email}")

            # Retrieve visitor information from the Visitors table
            visitor_data = cursor.execute("SELECT * FROM Visitors WHERE email = ?", (visitor_email,)).fetchone()

            # Check if the visitor exists
            if not visitor_data or visitor_data['checkInTime']:
                print("Visitor not found or not checked in.")
                return "Visitor not found or not checked in."

            # Execute the update query to set the checkOutTime
            data = cursor.execute("UPDATE Visitors SET checkOutTime = CURRENT_TIMESTAMP WHERE email = ? AND checkOutTime IS NULL",(visitor_email,))
            cursor.commit()

            # Check that a valid entry was found
            if data:
                print("Check-out successful!")
                return render_template('checkout_success.html')
            else:
                print("Visitor not found or not checked in.")
                return "Visitor not found or not checked in."

    return render_template('visitor_dashboard.html')


@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)