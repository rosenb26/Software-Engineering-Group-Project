CREATE TABLE Residents (
	residentID INTEGER PRIMARY KEY AUTOINCREMENT,
	residentFirstName CHAR(20) NOT NULL,
	residentLastName CHAR(20) NOT NULL,
	enterDate DATE NOT NULL,
	roomNumber INTEGER NOT NULL,
	birthdate DATE NOT NULL,
	insurance TEXT NOT NULL,
	emergencyContactFirstName CHAR(20) NOT NULL,
	emergencyContactLastName CHAR(20) NOT NULL,
	emergencyContactPhoneNumber CHAR(10) NOT NULL
);

CREATE TABLE Visitors (
	visitorID INTEGER PRIMARY KEY AUTOINCREMENT,
	email CHAR(20) NOT NULL,
	dateRegistered DATE NOT NULL,
	visitorFirstName CHAR(20) NOT NULL,
	visitorLastName CHAR(20) NOT NULL,
	residentFirstName CHAR(20) NOT NULL,
	residentLastName CHAR(20) NOT NULL,
	residentID INTEGER NOT NULL,
	FOREIGN KEY(residentID) REFERENCES Residents(residentID)
);

CREATE TABLE VisitorList (
    visitorID INTEGER PRIMARY KEY NOT NULL,
    dateVisit DATE NOT NULL,
	visitorFirstName CHAR(20) NOT NULL,
	visitorLastName CHAR(20) NOT NULL,
	checkInTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	residentFirstName CHAR(20) NOT NULL,
	residentLastName CHAR(20) NOT NULL,
	residentID INTEGER NOT NULL,
	checkOutTime CHAR(10),
	FOREIGN KEY(residentID) REFERENCES Residents(residentID)
);

CREATE TABLE StaffLogin (
	staffID INTEGER NOT NULL PRIMARY KEY,
	username CHAR(20) NOT NULL,
	password CHAR(20) NOT NULL
);

CREATE TABLE Travel_Request (
	travelRequestID INTEGER PRIMARY KEY AUTOINCREMENT,
	residentFirstName CHAR(20) NOT NULL,
	residentLastName CHAR(20) NOT NULL,
	submissionDate DATE NOT NULL,
	dateRequested DATE NOT NULL,
	locationRequested TEXT NOT NULL,
	status CHAR(20) NOT NULL
);

CREATE TABLE Maintenance_Request (
	workID INTEGER PRIMARY KEY AUTOINCREMENT,
	residentFirstName CHAR(20) NOT NULL,
	residentLastName CHAR(20) NOT NULL,
	submissionDate DATE NOT NULL,
	roomNumber INTEGER NOT NULL,
	workType CHAR(20) NOT NULL,
	residentID INTEGER NOT NULL,
	dateCompleted DATE,
	FOREIGN KEY(residentID) REFERENCES Residents(residentID)
);

CREATE TABLE Doctor_Request (
	doctorRequestID INTEGER PRIMARY KEY AUTOINCREMENT,
	residentFirstName CHAR(20) NOT NULL,
	residentLastName CHAR(20) NOT NULL,
	submissionDate DATE NOT NULL,
	roomNumber INTEGER NOT NULL,
	visitType CHAR(20) NOT NULL,
	residentID INTEGER NOT NULL,
	dateSeen DATE
);









	