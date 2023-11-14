CREATE TABLE Residents (
	residentID INTEGER PRIMARY KEY AUTOINCREMENT,
	residentFirstName CHAR(20) NOT NULL,
	residentLastName CHAR(20) NOT NULL,
	enterDate DATE NOT NULL,
	roomNumber INTEGER NOT NULL,
	birthdate DATE NOT NULL,
	insurance TEXT NOT NULL,
	emergencyContactFullName CHAR(50) NOT NULL,
	emergencyContactPhoneNumber CHAR(10) NOT NULL
);

CREATE TABLE Visitors (
	visitorID INTEGER PRIMARY KEY AUTOINCREMENT,
	email CHAR(20) NOT NULL,
	phoneNumber CHAR(20),
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
    email CHAR(20),
    phoneNumber CHAR(20),
	visitorFirstName CHAR(20) NOT NULL,
	visitorLastName CHAR(20) NOT NULL,
	checkInTime CHAR(10) NOT NULL,
	residentFirstName CHAR(20) NOT NULL,
	residentLastName CHAR(20) NOT NULL,
	residentID INTEGER NOT NULL,
	checkOutTime CHAR(10),
	FOREIGN KEY(residentID) REFERENCES Residents(residentID)
);

CREATE TABLE Staff_Login (
	staffID INTEGER NOT NULL PRIMARY KEY,
	username CHAR(20) NOT NULL,
	password CHAR(20) NOT NULL
);

CREATE TABLE Travel_Request (
	travelRequestID INTEGER PRIMARY KEY AUTOINCREMENT,
	residentFirstName CHAR(20) NOT NULL,
	residentLastName CHAR(20) NOT NULL,
	residentID INTEGER NOT NULL,
	submissionDate DATE NOT NULL,
	dateRequested DATE NOT NULL,
	dateTraveled DATE,
	locationRequested TEXT NOT NULL,
	notes TEXT,
	status CHAR(20) NOT NULL,
	FOREIGN KEY(residentID) REFERENCES Residents(residentID)
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
	status CHAR(20) NOT NULL,
	notes TEXT,
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
	status CHAR(20) NOT NULL,
	notes TEXT,
	dateSeen DATE,
	FOREIGN KEY(residentID) REFERENCES Residents(residentID)
);









	