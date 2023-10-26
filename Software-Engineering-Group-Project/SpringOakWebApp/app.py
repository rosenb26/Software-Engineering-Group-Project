import sqlite3
import time
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


# Dummy staff username and password (replace this with a secure authentication mechanism)
STAFF_USERNAME = "admin"
STAFF_PASSWORD = "password"


# In-memory list to store registered visitors
registered_visitors = []


# In-memory list to store checked-in visitors
checked_in_visitors = []


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == STAFF_USERNAME and password == STAFF_PASSWORD:
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password. Please try again."
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    checked_in_count = len(checked_in_visitors)
    checked_out_count = len(registered_visitors) - checked_in_count
    registered_count = len(registered_visitors)
    return render_template('dashboard.html', checked_in_count=checked_in_count, checked_out_count=checked_out_count, registered_count=registered_count)


@app.route('/visitors')
def visitors():
    visitor_type = request.args.get('type', 'registered')
    return render_template('visitors.html', visitors=registered_visitors, checked_in_visitors=checked_in_visitors, type=visitor_type)




@app.route('/registration-success')
def registration_success():
    return render_template('registration_success.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        residentname = request.form['residentname']
        date = request.form['date']
        phonenumber = request.form['phonenumber']
        email = request.form['email']


        # Create a dictionary to represent the visitor
        visitor = {
            'name': f'{firstname} {lastname}',
            'resident_name': residentname,
            'date': date,
            'phone': phonenumber,
            'email': email
        }


        # Add the visitor to the list of registered visitors
        registered_visitors.append(visitor)
        return redirect(url_for('registration_success'))


    return render_template('index.html')


@app.route('/visitor-dashboard', methods=['GET', 'POST'])
def visitor_dashboard():
    if request.method == 'POST':
        if 'register' in request.form:
            return redirect(url_for('register'))
        elif 'checkin' in request.form:
            visitor_email = request.form['visitor_email']
            for visitor in registered_visitors:
                if visitor['email'] == visitor_email and visitor not in checked_in_visitors:
                    checked_in_visitors.append(visitor)
                    return "Check-in successful!"
            return "Visitor not found or already checked in."
        elif 'checkout' in request.form:
            visitor_email = request.form['visitor_email']
            for visitor in checked_in_visitors:
                if visitor['email'] == visitor_email:
                    checked_in_visitors.remove(visitor)
                    return "Check-out successful!"
            return "Visitor not found or not checked in."


    return render_template('visitor_dashboard.html')


@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))
if __name__ == '__main__':


    app.run(debug=True)

