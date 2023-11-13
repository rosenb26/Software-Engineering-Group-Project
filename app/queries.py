import sqlite3
from werkzeug.security import check_password_hash

def addResident(firstName, lastName, roomNumber):
    connection = sqlite3.connect("springoak.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO resident (FirstName, LastName, RoomNumber) VALUES (?, ?, ?)", (firstName, lastName, roomNumber)
    )

    connection.commit()
    connection.close()

def allRequests():
    connection = sqlite3.connect("springoak.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT Description, Category, FirstName, LastName, RoomNumber FROM request JOIN resident ON request.resident = resident.ID;"
    )
    results = cursor.fetchall()
    connection.close()
    return results

def allResidents():
    connection = sqlite3.connect("springoak.db")
    #connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT FirstName, LastName, RoomNumber FROM resident")
    results = cursor.fetchall()
    connection.close()
    return results


def allVisitors(checkedIn=True):
    connection = sqlite3.connect("springoak.db")
    cursor = connection.cursor()

    cursor.execute("SELECT FirstName, LastName, Resident FROM visitor")
    results = cursor.fetchall()
    connection.close()
    return results


def visitorInDatabase(firstName, lastName, email):
    connection = sqlite3.connect("springoak.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM visitor WHERE FirstName = ? AND LastName = ? AND Email = ?",
        (firstName, lastName, email),
    )
    result = cursor.fetchall()
    return len(result) != 0
    connection = sqlite3.connect("springoak.db")


def checkStaffCredentials(username, password):
    connection = sqlite3.connect("springoak.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT Username, PasswordHash from STAFF WHERE username = ?", (username,)
    )
    result = cursor.fetchone()

    validCredentials = True
    if result is None:
        validCredentials = False
    else:
        if not check_password_hash(result["PasswordHash"], password):
            validCredentials = False
    return validCredentials


def addVisitor(firstName, lastName, residentName, date, phone, email):
    connection = sqlite3.connect("springoak.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO visitor (firstName, lastName, resident, date, phone, email) VALUES(?,?,?,?,?,?)",
        (firstName, lastName, residentName, date, phone, email)
    )
    connection.commit()
    connection.close()


def removeVisitor(firstName, lastName, email):
    connection = sqlite3.connect("springoak.db")
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM visitor WHERE FirstName = ? AND LastName = ? AND Email = ?",
        (firstName, lastName, email),
    )
    connection.commit()
    connection.close()
