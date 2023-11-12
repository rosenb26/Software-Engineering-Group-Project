from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from pytz import timezone
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from flask_sqlalchemy import SQLAlchemy

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
    # Add any other columns you need

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
        try:
            new_resident = Resident(
                first_name=request.form['ResidentFirstName'],
                last_name=request.form['ResidentLastName'],
                enter_date=datetime.datetime.strptime(request.form['EnterDate'], '%Y-%m-%d'),
                room_number=request.form['RoomNumber'],
                birthdate=datetime.datetime.strptime(request.form['Birthdate'], '%Y-%m-%d'),
                insurance=request.form['Insurance'],
                emergency_contact=request.form['EmergencyContact'],
            )
            db.session.add(new_resident)
            db.session.commit()
            flash('Resident added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred: ' + str(e), 'error')
        
        return redirect(url_for('resident_database'))

    else:
        residents = Resident.query.all()
        return render_template('resident_database.html', residents=residents)
    
@app.route('/resident-database', methods=['POST'])
def add_resident():
    new_resident = Resident(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        birthdate=datetime.strptime(request.form['birthdate'], '%Y-%m-%d'),
        enter_date=datetime.strptime(request.form['enter_date'], '%Y-%m-%d'),
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


@app.route('/dashboard')
def dashboard():
    checked_in_count = len(checked_in_visitors)
    checked_out_count = len(registered_visitors) - checked_in_count
    registered_count = len(registered_visitors)
    return render_template('dashboard.html', checked_in_count=checked_in_count, checked_out_count=checked_out_count, registered_count=registered_count)
@app.route('/visitors')
def visitors():
    visitor_type = request.args.get('type', 'registered')
    if visitor_type == 'checked_in':
        visitors = Visitor.query.filter_by(checked_in=True).all()
    elif visitor_type == 'checked_out':
        visitors = Visitor.query.filter(Visitor.checked_in == False, Visitor.checkout_time.isnot(None)).all()
    else:
        visitors = Visitor.query.all()
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
                date=datetime.datetime.strptime(request.form.get('date'), '%Y-%m-%d'),
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

from pytz import timezone
import datetime
from flask import request, render_template

@app.route('/visitor-dashboard', methods=['GET', 'POST'])
def visitor_dashboard():
    print("Visitor dashboard route accessed")
    if request.method == 'POST':
        visitor_email = request.form['visitor_email']
        local_time_str = request.form['local_time']

        # Print statements for debugging
        print("Local Time String:", local_time_str)

        # Since the local_time_str is already in UTC, we can use it directly
        utc_time = datetime.datetime.fromisoformat(local_time_str)
        print("UTC Time:", utc_time)

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