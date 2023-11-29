from flask import render_template, request, url_for, flash, redirect
from app.forms import VisitorRegistrationForm
from app import app
import sqlite3
import app.queries as q


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username, password = request.form.get("username"), request.form.get("password")
        if not q.checkStaffCredentials(username, password):
            flash("Invalid credentials.")
        else:
            return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstName, lastName, residentName, date, phone, email = (
            request.form.get("firstname"),
            request.form.get("lastname"),
            request.form.get("residentname"),
            request.form.get("date"),
            request.form.get("phonenumber"),
            request.form.get("email"),
        )
        if not q.visitorInDatabase(firstName, lastName, email):
            q.addVisitor(firstName, lastName, residentName, date, phone, email)
            flash("You have been registered!")
            return redirect(url_for("index"))
        else:
            flash("Visitor already registered.")
    return render_template("visitor-registration.html")


@app.route("/visitors")
def visitors():
    visitors = q.allVisitors()
    columnNames = ["First Name", "Last Name", "Resident Visited"]
    return render_template("table.html", items=visitors, header="Visitors", columnNames=columnNames)

@app.route("/residents")
def residents():
    residents = q.allResidents()
    columnNames = ["First Name", "Last Name", "Room Number"]
    return render_template("table.html", items=residents, header="Residents", columnNames=columnNames)

# @app.route("/requests")
# def requests():
#     requests = q.allRequests()
#     columnNames = ["Description", "First Name", "Last Name", "Room Number"]
#     return render_template("table.html", items=requests, header="Requests", columnNames=columnNames)

@app.route("/add-resident", methods=["GET", "POST"])
def addResident():
    if request.method == "POST":
        firstName, lastName, roomNumber = request.form.get("firstname"), request.form.get("lastname"), request.form.get("room-number")
        q.addResident(firstName, lastName, roomNumber)
        flash("Resident successfully added.")
    return render_template("add-resident.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

@app.route("/add-requests")
def requests():
    return render_template("requests.html")
