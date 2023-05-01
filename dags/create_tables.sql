create database if not exists newsDb;
use newsDb;

create table if not exists `newsDb`.`sources`
(
sourceID varchar(128)  primary key,
sourceName varchar(500) NOT null
);

create table if not exists `newsDb`.`authors`
(
authorID varchar(128) primary key,
authorName varchar(500) NOT null
);

create table if not exists `newsDb`.`articles`
(
articleID INT NOT NULL AUTO_INCREMENT primary key,
authorID varchar(128) NOT NULL,
sourceID varchar(128) NOT NULL,
title varchar(500) NOT null,
url VARCHAR(500) NOT NULL,
publishedDate VARCHAR(500) NOT NULL,
FOREIGN KEY (authorID) REFERENCES authors(authorID),
FOREIGN KEY (sourceID) REFERENCES sources(sourceID)
);