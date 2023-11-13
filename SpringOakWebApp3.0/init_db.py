import sqlite3

connection = sqlite3.connect('database.db')

with open('springoaks.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO Staff_Login (staffID, username, password) VALUES (?, ?, ?)", (1234, 'admin', 'password'))

cur.execute("INSERT INTO Staff_Login (staffID, username, password) VALUES (?, ?, ?)", (4321, 'marsh103', 'password'))

cur.execute("INSERT INTO Residents (residentID, residentFirstName, residentLastName, enterDate, roomNumber, "
            "birthdate, insurance, emergencyContactFullName, emergencyContactPhoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (111, "Alyssia", "Marshall", 11/11/2023, 101, 3/1/2001, "Horizon", "Mom", "6091234567"))

connection.commit()
connection.close()