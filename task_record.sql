DROP DATABASE IF EXISTS `task_record`;
CREATE DATABASE IF NOT EXISTS `task_record`;
USE `task_record`;

CREATE USER 'sampleUser'@'localhost' IDENTIFIED BY 'password_user';
GRANT ALL ON task_record.* TO 'sampleUser'@'localhost';

CREATE TABLE IF NOT EXISTS `category`(
    categoryNo INT(3) NOT NULL,
    categoryName VARCHAR(20) NOT NULL,
    categoryType VARCHAR(20) NOT NULL,
    CONSTRAINT category_cateogryNo_pk PRIMARY KEY(categoryNo),
    CONSTRAINT category_categoryName_uk UNIQUE(categoryName)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into category (categoryNo, categoryName, categoryType) values
	(1, 'Hygiene', 'Personal'),
	(2, 'CMSC 127', 'Professional');


CREATE TABLE IF NOT EXISTS `task`(
    taskNo INT(4) NOT NULL,
    categoryNo INT(3) NOT NULL,
    dueDate DATE NOT NULL,
    details varchar(50) NOT NULL,
    taskStatus varchar(15) NOT NULL DEFAULT 'NOT YET STARTED',
    CONSTRAINT task_taskNo_pk PRIMARY KEY(taskNo),
    CONSTRAINT task_categoryNo_fk FOREIGN KEY(categoryNo) REFERENCES
    category(categoryNo)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into task (taskNo, categoryNo, dueDate, details, taskStatus) values
	(1, 1, '2022-08-15', 'Long quiz #1', "Not yet started"),
	(2, 2, '2022-07-02', 'Exercise #4', "In-progress");