from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')

# Get the database URL from the environment variable
database_url = os.environ.get('DATABASE_URL')

# If it's present and starts with 'postgres://', replace with 'postgresql://'
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)

# Define models
class Resident(db.Model):
    __tablename__ = 'residents'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    enter_date = db.Column(db.DateTime, nullable=False)
    room_number = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    insurance = db.Column(db.String(100), nullable=True)
    emergency_contact = db.Column(db.String(100), nullable=True)
    # Add any other columns you need

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

@app.route('/add-resident', methods=['POST'])
def add_resident():
    try:
        # Retrieve form data
        resident_id = request.form['ResidentID']
        first_name = request.form['ResidentFirstName']
        last_name = request.form['ResidentLastName']
        # ... get other form fields ...

        # Here, you would normally insert the data into a database
        # For now, let's simulate by adding to the session (as a placeholder)
        new_resident = {
            'ResidentID': resident_id,
            'ResidentFirstName': first_name,
            'ResidentLastName': last_name,
            # ... include other data fields ...
        }
        residents = session.get('residents', [])
        residents.append(new_resident)
        session['residents'] = residents

        # Redirect back to the resident database page with success message
        flash('New resident added successfully!', 'success')
        return redirect(url_for('resident_database'))

    except Exception as e:
        # If an error occurs, flash an error message and redirect to the form
        flash('An error occurred: ' + str(e), 'error')
        return redirect(url_for('resident_database'))

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
    checked_in_count = len([visitor for visitor in registered_visitors if visitor['checked_in']])
    checked_out_count = len(registered_visitors) - checked_in_count

    if visitor_type == 'checked_in':
        filtered_visitors = [visitor for visitor in registered_visitors if visitor['checked_in']]
    elif visitor_type == 'checked_out':
        filtered_visitors = [visitor for visitor in registered_visitors if not visitor['checked_in']]
    else:
        filtered_visitors = registered_visitors

    return render_template('visitors.html', visitors=filtered_visitors, checked_in_visitors=checked_in_visitors, type=visitor_type, checked_in_count=checked_in_count, checked_out_count=checked_out_count)

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

        # Create a dictionary to represent the visitor
        visitor = {
            'name': f'{firstname} {lastname}',
            'resident_name': residentname,
            'date': date,
            'phone': phonenumber,
            'email': email,
            'checked_in': False  # Initialize 'checked_in' to False when registering
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
            print(f"Check-in request for email: {visitor_email}")
            for visitor in registered_visitors:
                if visitor['email'] == visitor_email:
                    if not visitor['checked_in']:
                        visitor['checked_in'] = True
                        visitor['checkin_time'] = datetime.datetime.now()  # Capture check-in time
                        checked_in_visitors.append(visitor)
                        print("Check-in successful!")
                        return render_template('checkin_success.html')  # Render checkin_success.html on success
                    else:
                        print("Visitor is already checked in.")
                        return "Visitor is already checked in."
            print("Visitor not found.")
            return "Visitor not found."
        elif 'checkout' in request.form:
            visitor_email = request.form['visitor_email']
            print(f"Check-out request for email: {visitor_email}")
            for visitor in checked_in_visitors:
                if visitor['email'] == visitor_email:
                    if visitor['checked_in']:
                        visitor['checked_in'] = False
                        visitor['checkout_time'] = datetime.datetime.now()  # Capture check-out time
                        checked_in_visitors.remove(visitor)
                        print("Check-out successful!")
                        return render_template('checkout_success.html')  # Render checkout_success.html on success
                    else:
                        print("Visitor is not checked in. Cannot check out.")
                        return "Visitor is not checked in. Cannot check out."
            print("Visitor not found or not checked in.")
            return "Visitor not found or not checked in."

    return render_template('visitor_dashboard.html')

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
