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
INSERT INTO `User` (ID,Name,Surname,Gender,Birth_date,Email,Login,Password,User_type) VALUES (1,'Jerzy','Mardaus','male','1986-12-12','jerzy.mardaus@codecool.com','jurek','password','manager'),
 (2,'Miriam','Codecool','female','1986-12-12','miriam@codecool.com','miriam','password','employee'),
 (3,'Kati','Codecool','female','1986-12-12','kati@codecool.com','kati','password','employee'),
 (5,'Ika','Grabon','female','1986-12-12','ika@codecool.com','ika','password','student'),
 (6,'Marta','Sajdak ','female','1986-12-12','marta@codecool.com','marta','password','student'),
 (11,'Rafal','Stepien','male','1986-12-12','rafals@codecool.com','rafals','haslo','mentor'),
 (12,'Mateusz','Ostafil','male','1990-01-01','mati@wp.pl','mateo','pass','mentor'),
 (13,'Marcin','Izworski','male','1986-12-12','marcini@codecool.com','marcin','password','mentor'),
 (17,'Zbyszek','Wodecki','male','1990-01-01','zbych@wp.pl','zbychu','pass','mentor'),
 (18,'Roman','Polanski','male','1990-01-01','romek@wp.pl','roman','pass','student');
CREATE TABLE "Team" (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT,
	`ID_Student`	INTEGER
);
INSERT INTO `Team` (ID,name,ID_Student) VALUES (40,'team2','<empty>');
CREATE TABLE "Submission" (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`ID_Student`	INTEGER,
	`ID_Assignment`	INTEGER,
	`Result`	TEXT,
	`Grade`	INTEGER,
	`date`	TEXT,
	`ID_Mentor`	INTEGER
);
INSERT INTO `Submission` (ID,ID_Student,ID_Assignment,Result,Grade,date,ID_Mentor) VALUES (21,5,1,'Beautifull dojo app',NULL,'2017-03-10',NULL),
 (22,6,2,'Program in python',4,'2017-03-10',NULL),
 (23,18,3,'Javascript functions ',4,'2017-03-10',NULL),
 (24,5,2,'submitted assignment',4,'2017-03-10',NULL),
 (25,5,6,'result for nowy',NULL,'2017-03-10',NULL);
CREATE TABLE "Checkpoint_submission" (
	`ID`	INTEGER,
	`ID_Student`	INTEGER,
	`Date`	TEXT,
	`Card`	TEXT,
	`ID_Mentor`	INTEGER,
	`ID_Assignment`	INTEGER,
	PRIMARY KEY(`ID`)
);
INSERT INTO `Checkpoint_submission` (ID,ID_Student,Date,Card,ID_Mentor,ID_Assignment) VALUES (1,5,'2017-03-10','yellow',12,1),
 (2,5,NULL,NULL,NULL,2),
 (3,5,'2017-03-10','red',12,3),
 (4,6,'2017-03-10','red',12,1),
 (5,6,NULL,NULL,NULL,2),
 (6,6,'2017-03-10','green',12,3),
 (7,18,'2017-03-10','green',12,1),
 (8,18,NULL,NULL,NULL,2),
 (9,18,'2017-03-10','green',12,3);
CREATE TABLE "Checkpoint_assignment" (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Name`	TEXT,
	`Assignment`	TEXT
);
INSERT INTO `Checkpoint_assignment` (ID,Name,Assignment) VALUES (1,'Checkpoint1','todo'),
 (2,'Checkpoint2','python basic'),
 (3,'Checkpoint3','java');
CREATE TABLE "Attendance" (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`ID_Student`	INTEGER,
	`Date`	TEXT,
	`Presence`	INTEGER
);
INSERT INTO `Attendance` (ID,ID_Student,Date,Presence) VALUES (1,4,'2007-10-02',1),
 (2,5,'2007-10-02',0),
 (3,6,'2007-10-02',0),
 (4,4,'2007-10-03',0),
 (5,5,'2007-10-03',1),
 (6,6,'2007-10-03',0),
 (7,4,'2007-10-04',1),
 (8,5,'2007-10-04',1),
 (9,6,'2007-10-04',0),
 (10,4,'2007-10-04',1),
 (11,5,'2007-10-04',0),
 (12,6,'2007-10-04',0),
 (13,4,'2017-02-10',0),
 (14,5,'2017-02-10',1),
 (15,6,'2017-02-10',1),
 (65,18,'2017-03-09',1),
 (66,6,'2017-03-09',1),
 (67,5,'2017-03-09',1),
 (71,18,'2017-03-10',1),
 (72,5,'2017-03-10',0),
 (73,6,'2017-03-10',2);
CREATE TABLE "Assignment" (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Name`	TEXT,
	`Type`	TEXT,
	`Max_points`	INTEGER,
	`Delivery_date`	TEXT,
	`Content`	TEXT
);
INSERT INTO `Assignment` (ID,Name,Type,Max_points,Delivery_date,Content) VALUES (2,'Python','individual',42,'2017-04-01','Basic content for Python'),
 (3,'Javascript','individual',48,'2017-03-21','Content Javascript'),
 (4,'Python','individual',48,'2017-04-23','Python content'),
 (6,'nowy','individual',23,'2017-03-24','content assignment');
COMMIT;
