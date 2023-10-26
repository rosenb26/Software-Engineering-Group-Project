
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length, Regexp
from app.models import Staff


class VisitorRegistrationForm(FlaskForm):
    firstName = StringField("First Name", validators=[InputRequired()])
    lastName = StringField("Last Name", validators=[InputRequired()])
    phoneNumber = StringField("Phone Number", validators=[InputRequired(), Length(min=10, max=10), Regexp(regex="[0-9]{10}")])
    submit = SubmitField("Register")

class StaffLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    #remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

    # def validate_username(self, username):
    #     s = Staff.query.filter_by(username=username.data).first()
    #     if s is None:
    #         raise ValidationError("No such staff member.")
        

    