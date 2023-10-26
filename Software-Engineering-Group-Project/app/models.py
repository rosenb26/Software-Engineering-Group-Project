from app import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


@login.user_loader
def loadStaff(id:str):
    return Staff.query.get(int(id))

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(25))
    lastName = db.Column(db.String(25))
    phoneNumber = db.Column(db.String(25))

    def __repr__(self):
        return f"Visitor: {self.firstName} {self.lastName} [{self.phoneNumber}]"

class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    passwordHash = db.Column(db.String(64))

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)
    
    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)

    def __repr__(self):
        return f"Staff: {self.username}"
    