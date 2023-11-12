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

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
