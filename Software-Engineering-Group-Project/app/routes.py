from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import VisitorRegistrationForm, StaffLoginForm
from app.models import Visitor, Staff
from flask_login import login_required

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    registrationForm = VisitorRegistrationForm()
    if registrationForm.validate_on_submit():
        visitor = Visitor(firstName=registrationForm.firstName.data, lastName=registrationForm.lastName.data, phoneNumber=registrationForm.phoneNumber.data)
        db.session.add(visitor)
        db.session.commit()
        flash("You've been registered.")
        return redirect(url_for("index"))
    return render_template("register.html", form=registrationForm)


@app.route("/staff-login", methods=["GET", "POST"])
def staff():
    staffLoginForm = StaffLoginForm()
    if staffLoginForm.validate_on_submit():
        staff = Staff.query.filter_by(username=staffLoginForm.username.data).first()
        if staff is None or not staff.checkPassword(staffLoginForm.password.data):
            flash("Invalid credentials.")   
            return redirect(url_for("staff"))
        return redirect(url_for("dashboard"))
    return render_template("dashboard.html", form=staffLoginForm)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")