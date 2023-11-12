from flask import Flask, render_template

app = Flask(__name__)

ADMIN = [
  {
    'id': 1,
    'name': 'John Doe',
    'email': 'tugrp@example.com',
    'username': 'adminusername',
    'password': 'adminpassword'

  }
]

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login")
def login():
  return render_template('login.html')


@app.route("/register")
def register():
  return render_template('register.html')


@app.route("/check")
def check():
  return render_template('check.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
