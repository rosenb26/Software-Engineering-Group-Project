from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pytz
from sqlalchemy import String, func  # This is the correct import for datetime.strptime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qxfdouabbyiwxc:839dace584e6853abff16bbd21bd31126cf6bdfdd5fa0b6193f439ed41e20f19@ec2-3-212-29-93.compute-1.amazonaws.com:5432/d2sbv72ptga2jm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: to suppress a warning

# Initialize extensions
db = SQLAlchemy(app)

# Define models
class Resident(db.Model):
    __tablename__ = 'residents'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    enter_date = db.Column(db.DateTime, nullable=False)
    room_number = db.Column(db.String(), nullable=False)
    insurance = db.Column(db.String(), nullable=True)
    emergency_contact = db.Column(db.String(), nullable=True)

# Initialize the database (This will create the tables based on your models at the first run)
with app.app_context():
    db.create_all()

# Replace with database or secure authentication mechanism
STAFF_USERNAME = "admin"
STAFF_PASSWORD = "password"  

# Use session to store the information which is more secure
residents = []
registered_visitors = []
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

@app.route('/resident-database', methods=['GET', 'POST'])
def resident_database():
    if request.method == 'POST':
        # Create a new instance of Resident
        new_resident = Resident(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            birthdate=datetime.strptime(request.form['birthdate'], '%Y-%m-%d'),
            enter_date=datetime.strptime(request.form['enter_date'], '%Y-%m-%d'),
            room_number=request.form['room_number'],
            insurance=request.form.get('insurance', ''),  # Optional field
            emergency_contact=request.form.get('emergency_contact', '')  # Optional field
        )
        # Add to the session and commit
        db.session.add(new_resident)
        try:
            db.session.commit()
            flash('Resident added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred: {}'.format(e), 'error')
    else:
        # GET request - retrieve and display residents
        residents = Resident.query.all()
        return render_template('resident_database.html', residents=residents)

    # After POST redirect to the same page to see the list of residents
    return redirect(url_for('resident_database'))

@app.route('/resident-database', methods=['POST'])
def add_resident():
    new_resident = Resident(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').strftime('%m-%d-%Y'),
        enter_date = datetime.strptime(request.form['enter_date'], '%Y-%m-%d').strftime('%m-%d-%Y'),
        room_number=request.form['room_number'],
        insurance=request.form.get('insurance', ''),  # Optional field
        emergency_contact=request.form.get('emergency_contact', '')  # Optional field
    )
    db.session.add(new_resident)
    try:
        db.session.commit()
        flash('Resident added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred: {}'.format(e), 'error')
    return redirect(url_for('resident_database'))

@app.route('/search-residents', methods=['GET'])
def search_residents():
    query = request.args.get('query', '')
    search = "%{}%".format(query)
    residents = Resident.query.filter(
        (Resident.first_name.like(search)) |
        (Resident.last_name.like(search)) |
        (func.cast(Resident.birthdate, String).like(search))
    ).all()
    return render_template('resident_database.html', residents=residents)

@app.route('/resident-login', methods=['POST'])
def resident_login():
    room_number = request.form['room_number']
    last_name = request.form['last_name']

    # Query the database to find a resident with the given room number and last name
    resident = Resident.query.filter_by(room_number=room_number, last_name=last_name).first()
    
    # Check if the resident exists
    if resident:
        # If resident is found, store the resident's ID in the session for future requests
        session['resident_id'] = resident.id
        # Render the requests page with the resident's information
        return render_template('resident_requests.html', resident=resident)
    else:
        # If resident is not found, flash an error message and redirect to the resident_database page
        flash('Invalid room number or last name. Please try again.', 'danger')
        return redirect(url_for('resident_database'))

@app.route('/resident-logout', methods=['POST'])
def resident_logout():
    # Remove the resident_id from the session if it's there
    session.pop('resident_id', None)
    # Redirect to the resident_database which contains the login form
    flash('You have been logged out.', 'success')
    return redirect(url_for('resident_database'))

@app.route('/dashboard')
def dashboard():
    checked_in_count = len(checked_in_visitors)
    checked_out_count = len(registered_visitors) - checked_in_count
    registered_count = len(registered_visitors)
    return render_template('dashboard.html', checked_in_count=checked_in_count, checked_out_count=checked_out_count, registered_count=registered_count)

class Visitor(db.Model):
    __tablename__ = 'visitors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    resident_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    checked_in = db.Column(db.Boolean, default=False, nullable=False)
    checkin_time = db.Column(db.DateTime, nullable=True)
    checkout_time = db.Column(db.DateTime, nullable=True)

# In your Flask route
from datetime import timedelta

@app.route('/visitors')
def visitors():
    # Retrieve the filter type from the query parameter
    visitor_type = request.args.get('type', 'all')

    # Filter the visitors based on the visitor_type
    if visitor_type == 'checked_in':
        visitors = Visitor.query.filter_by(checked_in=True).all()
    elif visitor_type == 'checked_out':
        visitors = Visitor.query.filter(Visitor.checked_in == False, Visitor.checkout_time.isnot(None)).all()
    else:
        visitors = Visitor.query.all()

    for visitor in visitors:
        # Apply manual adjustment for check-in time
        if visitor.checkin_time:
            adjusted_checkin_time = visitor.checkin_time - timedelta(hours=5)
            visitor.local_checkin_time = adjusted_checkin_time.strftime('%I:%M %p')
        else:
            visitor.local_checkin_time = 'N/A'

        # Apply manual adjustment for check-out time
        if visitor.checkout_time:
            adjusted_checkout_time = visitor.checkout_time - timedelta(hours=5)
            visitor.local_checkout_time = adjusted_checkout_time.strftime('%I:%M %p')
        else:
            visitor.local_checkout_time = 'N/A'

    return render_template('visitors.html', visitors=visitors)

@app.route('/registration-success')
def registration_success():
    return render_template('registration_success.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            new_visitor = Visitor(
                name=f"{request.form.get('firstname')} {request.form.get('lastname')}",
                resident_name=request.form.get('residentname'),
                date=datetime.strptime(request.form.get('date'), '%Y-%m-%d'),
                phone=request.form.get('phonenumber'),
                email=request.form.get('email'),
                checked_in=False
            )
            db.session.add(new_visitor)
            db.session.commit()
            return redirect(url_for('registration_success'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred: ' + str(e), 'error')
            return redirect(url_for('register'))
    return render_template('index.html')

@app.route('/visitor-dashboard', methods=['GET', 'POST'])
def visitor_dashboard():
    print("Visitor dashboard route accessed")
    if request.method == 'POST':
        visitor_email = request.form['visitor_email']
        local_time_str = request.form['local_time']

        # Parse the ISO format date
        utc_time = datetime.fromisoformat(local_time_str.rstrip("Z"))  # Remove the 'Z' before parsing
        print("Original UTC Time:", utc_time)

        # Manually adjust the time five hours back
        adjusted_time = utc_time - timedelta(hours=5)
        print("Adjusted Time:", adjusted_time)

        # Check-in logic
        if 'checkin' in request.form:
            visitor = Visitor.query.filter_by(email=visitor_email).first()
            if visitor:
                if not visitor.checked_in:
                    visitor.checked_in = True
                    visitor.checkin_time = utc_time  # Store the UTC time
                    db.session.commit()
                    return render_template('checkin_success.html', visitor=visitor)
                else:
                    return "Visitor is already checked in."
            else:
                return "Visitor not found."

        # Check-out logic
        elif 'checkout' in request.form:
            visitor = Visitor.query.filter_by(email=visitor_email).first()
            if visitor:
                if visitor.checked_in:
                    visitor.checked_in = False
                    visitor.checkout_time = utc_time  # Store the UTC time
                    db.session.commit()
                    return render_template('checkout_success.html', visitor=visitor)
                else:
                    return "Visitor is not checked in. Cannot check out."
            else:
                return "Visitor not found or not checked in."

    return render_template('visitor_dashboard.html')

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)