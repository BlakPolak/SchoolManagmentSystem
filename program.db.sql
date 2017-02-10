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
 (11,'Rafal','Stepien','male','1986-12-12','rafals@codecool.com','rafals@codecool.com','password','mentor'),
 (12,'Mateusz','Ostafil','male','1986-12-12','mateuszo@codecool.com','mati','pass','mentor'),
 (13,'Marcin','Izworski','male','1986-12-12','marcini@codecool.com','marcini@codecool.com','password','mentor'),
 (14,'Przemek','Ciacka','male','1986-12-12','przemekc@codecool.com','przemekc@codecool.com','password','mentor'),
 (15,'dfs','sdfds','male','1898-12-12','qwewqe@wp.pl','dsaa','asdsad','student'),
 (18,'aaaaa','aaaaa','male','1234-34-43','dsad','asdsa','dsada','student');
CREATE TABLE "Teams" (
	`ID`	INTEGER,
	`Team_name`	TEXT,
	`ID_Student`	INTEGER,
	PRIMARY KEY(ID)
);
INSERT INTO `Teams` (ID,Team_name,ID_Student) VALUES (2,'rozmaryn',8),
 (6,'xxx',6),
 (7,'Jakkolwiek',15),
 (10,'oops',4),
 (11,'ZZZ',18),
 (12,'Fistaszki',5);
CREATE TABLE "Submission" (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`ID_Student`	INTEGER,
	`ID_Assignment`	INTEGER,
	`Result`	TEXT,
	`Grade`	INTEGER,
	`Submittion_date`	TEXT,
	`ID_mentor`	INTEGER
);
INSERT INTO `Submission` (ID,ID_Student,ID_Assignment,Result,Grade,Submittion_date,ID_mentor) VALUES (1,5,1,'result',4,'2016-12-12',12);
CREATE TABLE "Checkpoint_submittion" (
	`ID`	INTEGER,
	`ID_Student`	INTEGER,
	`Date`	TEXT,
	`Card`	TEXT,
	`ID_Mentor`	INTEGER,
	`ID_Assignment`	INTEGER,
	PRIMARY KEY(`ID`)
);
INSERT INTO `Checkpoint_submittion` (ID,ID_Student,Date,Card,ID_Mentor,ID_Assignment) VALUES (1,4,'2017-02-10','red',12,5),
 (2,4,'2017-02-10','yellow',12,2),
 (3,5,'2017-02-10','red',12,2);
CREATE TABLE "Checkpoint_assignment" (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Name`	TEXT,
	`Assignment`	TEXT
);
INSERT INTO `Checkpoint_assignment` (ID,Name,Assignment) VALUES (2,'Procedural programming','main(), procedures'),
 (5,'OOP','classes, init');
CREATE TABLE "Attendance" (
	`ID`	INTEGER,
	`ID_Student`	INTEGER,
	`Date`	TEXT,
	`Presence`	INTEGER,
	PRIMARY KEY(ID)
);
INSERT INTO `Attendance` (ID,ID_Student,Date,Presence) VALUES (1,4,'2017-02-09',1),
 (2,5,'2017-02-09',0),
 (3,6,'2017-02-09',1),
 (4,15,'2017-02-09',1),
 (5,18,'2017-02-09',1),
 (6,4,'2017-02-11',1),
 (7,5,'2017-02-11',0),
 (8,6,'2017-02-11',1),
 (9,15,'2017-02-11',0),
 (10,18,'2017-02-11',1),
 (11,4,'2017-02-10',1),
 (12,5,'2017-02-10',1),
 (13,6,'2017-02-10',1),
 (14,15,'2017-02-10',1),
 (15,18,'2017-02-10',1),
 (16,4,'2017-02-10',1),
 (17,5,'2017-02-10',1),
 (18,6,'2017-02-10',2),
 (19,15,'2017-02-10',1),
 (20,18,'2017-02-10',1);
CREATE TABLE `Assignment` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Name`	TEXT,
	`Type`	TEXT,
	`Max_points`	INTEGER,
	`Delivery_date`	NUMERIC,
	`Content`	TEXT
);
INSERT INTO `Assignment` (ID,Name,Type,Max_points,Delivery_date,Content) VALUES (1,'new ass','individual',48,'2017-01-02','Content for assignment'),
 (2,'Python','group',24,'2017-12-12','Content about python'),
 (3,'Java','group',48,'2017-01-01','Java content'),
 (4,'Javascript','individual',48,'2017-03-05','Content Javascript');
COMMIT;
