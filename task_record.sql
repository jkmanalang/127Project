DROP DATABASE IF EXISTS `task_record`;
CREATE DATABASE IF NOT EXISTS `task_record`;
USE `task_record`;

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
	(1, 1, str_to_date('15-OCT-2022','%d-%M-%Y'), 'Long quiz #1', "NOT YET STARTED"),
	(2, 2, str_to_date('02-JUN-2022','%d-%M-%Y'), 'Exercise #4', "IN-PROGRESS");