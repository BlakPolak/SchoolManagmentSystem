BEGIN TRANSACTION;
CREATE TABLE "User" (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Name`	TEXT,
	`Surname`	TEXT,
	`Gender`	TEXT,
	`Birth_date`	TEXT,
	`Email`	TEXT,
	`Login`	TEXT,
	`Password`	TEXT,
	`User_type`	TEXT
);
INSERT INTO `User` (ID,Name,Surname,Gender,Birth_date,Email,Login,Password,User_type) VALUES (1,'Jerzy','Mardaus','male','1986-12-12','jerzy.mardaus@codecool.com','jerzy.mardaus@codecool.com','password','manager'),
 (2,'Miriam','Codecool','female','1986-12-12','miriam@codecool.com','miriam@codecool.com','password','employee'),
 (3,'Kati','Codecool','female','1986-12-12','kati@codecool.com','kati@codecool.com','password','employee'),
 (4,'Pawel','Polakiewicz','male','1986-12-12','pawelp@codecool.com','pawelp@codecool.com','password','student'),
 (5,'Ika','Grabon','female','1986-12-12','ika@codecool.com','ika@codecool.com','password','student'),
 (6,'Marta','Sajdak ','female','1986-12-12','marta@codecool.com','marta@codecool.com','password','student'),
 (7,'Joanna','Gargas','female','1986-12-12','joanna@codecool.co"joanna@codecool.com"','joanna@codecool.co"joanna@codecool.com"','password','student'),
 (8,'Pawel','Lasota','male','1986-12-12','pawell@codecool.com','pawell@codecool.com','password','student'),
 (9,'Maria','Steinmec','female','1986-12-12','marias@codecool.com','marias@codecool.com','password','student'),
 (10,'Anna','Matras','female','1986-12-12','annam@codecool.com','annam@codecool.com','password','student'),
 (11,'Rafal','Stepien','male','1986-12-12','rafals@codecool.com','rafals@codecool.com','password','mentor'),
 (12,'Mateusz','Ostafil','male','1986-12-12','mateuszo@codecool.com','mati','pass','mentor'),
 (13,'Marcin','Izworski','male','1986-12-12','marcini@codecool.com','marcini@codecool.com','password','mentor'),
 (14,'Przemek','Ciacka','male','1986-12-12','przemekc@codecool.com','przemekc@codecool.com','password','mentor');

CREATE TABLE "Teams" (
	`ID`	INTEGER,
	`Team Name`	TEXT,
	`ID_Student`	INTEGER,
	PRIMARY KEY(`ID`)
);
INSERT INTO `Teams` (ID,Team Name,ID_Student) VALUES (1,'jakkolwike',''),
 (2,'jakkolwiek',''),
 (3,'oops',''),
 (4,'oops',NULL),
 (5,NULL,NULL),
 (6,NULL,NULL),
 (7,NULL,NULL);
CREATE TABLE `Submission` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`ID_Student`	INTEGER,
	`ID_Assignment`	INTEGER,
	`Result`	TEXT,
	`Grade`	INTEGER,
	`Submittion_date`	NUMERIC
);
CREATE TABLE "Checkpoint_submittion" (
	`ID`	INTEGER,
	`ID_Student`	INTEGER,
	`Date`	TEXT,
	`Card`	TEXT,
	`ID_Mentor`	INTEGER,
	`ID_Assignment`	INTEGER,
	PRIMARY KEY(`ID`)
);
CREATE TABLE "Checkpoint_assignment" (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Name`	TEXT,
	`Assignment`	TEXT
);
CREATE TABLE "Attendance" (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`ID_Student`	INTEGER,
	`Date`	NUMERIC,
	`Presence`	INTEGER
);
INSERT INTO `Attendance` (ID,ID_Student,Date,Presence) VALUES (1,2,NULL,NULL),
 (2,2,NULL,NULL),
 (3,NULL,NULL,NULL);
CREATE TABLE `Assignment` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Name`	TEXT,
	`Type`	TEXT,
	`Max_points`	INTEGER,
	`Delivery_date`	NUMERIC,
	`Content`	TEXT
);
COMMIT;
