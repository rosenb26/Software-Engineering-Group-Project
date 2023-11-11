import sqlite3

connection = sqlite3.connect('database.db')

with open('springoaks.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO StaffLogin (staffID, username, password) VALUES (?, ?, ?)", (1234, 'admin', 'password'))

cur.execute("INSERT INTO StaffLogin (staffID, username, password) VALUES (?, ?, ?)", (4321, 'marsh103', 'password'))

connection.commit()
connection.close()