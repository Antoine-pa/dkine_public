DROP DATABASE IF EXISTS `dk_users`;
DROP DATABASE IF EXISTS `dk_maps`;
DROP DATABASE IF EXISTS `dk_dkine`;
DROP DATABASE IF EXISTS `dkinedata`;

CREATE DATABASE `dk_users`;
CREATE DATABASE `dk_maps`;
CREATE DATABASE `dk_dkine`;

USE `dk_users`;
CREATE TABLE IF NOT EXISTS `t-d-users` (
	`user-id` BIGINT(20) PRIMARY KEY,
	`user-date-creation` DATETIME,
	`user-lang` CHAR(2) DEFAULT 'en'
);

CREATE TABLE IF NOT EXISTS `t-d-profile` (
	`p-id` BIGINT(20) PRIMARY KEY,
	`p-premium` BOOLEAN DEFAULT FALSE,
	`p-population` INT NOT NULL DEFAULT 300,
	`p-mood` TINYINT NOT NULL DEFAULT 40,
	`p-gold` INT NOT NULL DEFAULT 0,
	`p-iron` INT NOT NULL DEFAULT 0,
	`p-coal` INT NOT NULL DEFAULT 0,
	`p-stone` INT NOT NULL DEFAULT 0,
	`p-wood` INT NOT NULL DEFAULT 0,
	`p-leather` INT NOT NULL DEFAULT 0, /*cuire*/
	`p-food` INT NOT NULL DEFAULT 0,
	`p-soldat` BIGINT(20) DEFAULT 10, /*nb de soldat*/
	`p-archer` BIGINT(20) DEFAULT 10, /*nb d'archer*/
	`p-mage` BIGINT(20) DEFAULT 10, /*nb de mage*/
	`p-machine` BIGINT(20) DEFAULT 10, /*nb de siege*/
	`p-boat` SMALLINT NOT NULL DEFAULT 0,
	`p-energy` SMALLINT NOT NULL DEFAULT 0,
	`p-lvl-mine` SMALLINT NOT NULL DEFAULT 1,
	`p-lvl-town` SMALLINT NOT NULL DEFAULT 1,
	`p-lvl-lava-mine` SMALLINT NOT NULL DEFAULT 1,
	`p-lvl-workshop` TINYINT NOT NULL DEFAULT 1,
	`p-lvl-caserne` TINYINT NOT NULL DEFAULT 1,
	`p-rep` SMALLINT DEFAULT 0,
	`p-xp` BIGINT DEFAULT 0,
	`p-lvl` BIGINT DEFAULT 1,
	`p-meteor` INT NOT NULL DEFAULT 0,
	`p-rune` INT NOT NULL DEFAULT 0,
	`p-lava` INT NOT NULL DEFAULT 0,
	`p-timestamp-town` BIGINT(11) NOT NULL DEFAULT 0,
	`p-timestamp-mine` BIGINT(11) NOT NULL DEFAULT 0,
	`p-timestamp-lava-mine` BIGINT(11) NOT NULL DEFAULT 0,
	
	CONSTRAINT `p-id_fk1` FOREIGN KEY(`p-id`) REFERENCES `t-d-users`(`user-id`)
);

CREATE TABLE IF NOT EXISTS `ban-game` (
	`id` BIGINT(20) PRIMARY KEY,
	`ban` BOOLEAN DEFAULT FALSE,
	`raise` TEXT(50000),
	`timestamp` BIGINT(11), /*if ban and timestamp == 0: infinite, if not ban, timestamp == 0*/
	`number-ban` INT(3)
);



CREATE TABLE IF NOT EXISTS `t-d-timestamp` (
	`t-user-id` BIGINT(20),
	`t-tax` BIGINT(11) DEFAULT 0,
	`t-daily` BIGINT(11) DEFAULT 0,
	`t-weekly` BIGINT(11) DEFAULT 0,
	`t-rep` BIGINT(11) DEFAULT 0,
	`t-recrut-cac` BIGINT(11) DEFAULT 0,
	`t-recrut-dist` BIGINT(11) DEFAULT 0,
	`t-build-boat` BIGINT(11) DEFAULT 0,
	`t-up-workshop` BIGINT(11) DEFAULT 0,
	`t-regen-enery` BIGINT(11) DEFAULT 0,
	`t-premium` BIGINT(11) DEFAULT 0,

	CONSTRAINT `t-user-id_fk1` FOREIGN KEY(`t-user-id`) REFERENCES `t-d-users`(`user-id`)
);

CREATE TABLE IF NOT EXISTS `construction` (
	`index` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`user-id` BIGINT(20),
	`channel` BIGINT(20),
	`zone` CHAR(3), /*p for profile or a zone*/
	`build` CHAR(10),
	`lvl` INT(1),
	`timestamp` BIGINT(11),
	`people` BIGINT(7), /*for the 'remboursement' xD*/
	PRIMARY KEY (`index`)
);


INSERT INTO `t-d-users`(`user-id`, `user-date-creation`) VALUES(728263853820870767, NOW());
INSERT INTO `t-d-profile`(`p-id`) VALUES(728263853820870767);
INSERT INTO `ban-game`(`id`, `ban`, `raise`, `timestamp`, `number-ban`) VALUES(728263853820870767, 0, "", 0, 0);

INSERT INTO `t-d-users`(`user-id`, `user-date-creation`,`user-lang`) VALUES(627191994699087873, NOW(), "fr");
INSERT INTO `t-d-profile`(`p-id`) VALUES(627191994699087873);
INSERT INTO `ban-game`(`id`, `ban`, `raise`, `timestamp`, `number-ban`) VALUES(627191994699087873, 0, "", 0, 0);

DESCRIBE `t-d-users`;
DESCRIBE `t-d-profile`;
DESCRIBE `t-d-timestamp`;


USE `dk_maps`;
CREATE TABLE `t-d-maps`(
	`m-map` CHAR(3),
	`m-user` BIGINT(20),
	`m-soldat` BIGINT(20) DEFAULT 10, /*nb de soldat*/
	`m-archer` BIGINT(20) DEFAULT 10, /*nb d'archer*/
	`m-mage` BIGINT(20) DEFAULT 10, /*nb de mage*/
	`m-machine` BIGINT(20) DEFAULT 10, /*nb de siege*/
	`m-town` CHAR(8), /*nombre de ferme niv1/2/3*/
	`m-mine` CHAR(8), /*nombre de mine niv1/2/3*/
	`m-lava-mine` CHAR(8), /*nombre de mine spécials niv1/2/3 (only map C)*/
	`m-timestamp-town` BIGINT(11) NOT NULL DEFAULT 0,
	`m-timestamp-mine` BIGINT(11) NOT NULL DEFAULT 0,
	`m-timestamp-lava-mine` BIGINT(11) NOT NULL DEFAULT 0
);


CREATE TABLE IF NOT EXISTS `moove`(
	`index` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`user-id` BIGINT(20),
	`value` CHAR(10), /* nom du type de mouvement et si c'est atk, mettre sous ce formt : atk/[bonus d'attack en pourcentage] */
	`timestamp` BIGINT(11),
	`channel` BIGINT(20),
	`zone1` CHAR(3),
	`zone2` CHAR(3),
	`soldat` BIGINT(20) DEFAULT 0, /*nb de soldat*/
	`archer` BIGINT(20) DEFAULT 0, /*nb d'archer*/
	`mage` BIGINT(20) DEFAULT 0, /*nb de mage*/
	`machine` BIGINT(20) DEFAULT 0, /*nb de siege*/
	PRIMARY KEY (`index`)
);




INSERT INTO `t-d-maps`(`m-map`, `m-user`, `m-town`, `m-mine`, `m-lava-mine`) VALUES('A1', 627191994699087873, '0/2/0', '1/0/0', '0/0/0'), ('A2', 521983736485511178, '0/2/0', '1/0/0', '0/0/0'), ('A3', 627191994699087873, '0/2/0', '1/0/0', '0/0/0'), ('A4', 0, '0/2/0', '1/0/0', '0/0/0'), ('A5', 0, '0/2/0', '1/0/0', '0/0/0'), ('A6', 0, '0/2/0', '1/0/0', '0/0/0'), ('A7', 0, '0/2/0', '1/0/0', '0/0/0'), ('A8', 0, '0/2/0', '1/0/0', '0/0/0'), ('A9', 0, '0/2/0', '1/0/0', '0/0/0'), ('A10', 0, '0/2/0', '1/0/0', '0/0/0'), 
('A11', 0, '0/2/0', '1/0/0', '0/0/0'), ('A12', 0, '0/2/0', '1/0/0', '0/0/0'), ('A13', 0, '0/2/0', '1/0/0', '0/0/0'), ('A14', 0, '0/2/0', '1/0/0', '0/0/0'), ('A15', 0, '0/2/0', '1/0/0', '0/0/0'), ('A16', 0, '0/2/0', '1/0/0', '0/0/0'), ('A17', 0, '0/2/0', '1/0/0', '0/0/0'), ('A18', 0, '0/2/0', '1/0/0', '0/0/0'), ('A19', 0, '0/2/0', '1/0/0', '0/0/0'), ('A20', 0, '0/2/0', '1/0/0', '0/0/0'), 
('A21', 0, '0/2/0', '1/0/0', '0/0/0'), ('A22', 0, '0/2/0', '1/0/0', '0/0/0'), ('A23', 0, '0/2/0', '1/0/0', '0/0/0'), ('A24', 0, '0/2/0', '1/0/0', '0/0/0'), ('A25', 0, '0/2/0', '1/0/0', '0/0/0'), ('A26', 0, '0/2/0', '1/0/0', '0/0/0'), ('A27', 0, '0/2/0', '1/0/0', '0/0/0'), ('A28', 0, '0/2/0', '1/0/0', '0/0/0'), ('A29', 0, '0/2/0', '1/0/0', '0/0/0'), ('A30', 0, '0/2/0', '1/0/0', '0/0/0'), 
('B1', 0, '1/0/0', '0/2/0', '0/0/0'), ('B2', 0, '1/0/0', '0/2/0', '0/0/0'), ('B3', 0, '1/0/0', '0/2/0', '0/0/0'), ('B4', 0, '1/0/0', '0/2/0', '0/0/0'), ('B5', 0, '1/0/0', '0/2/0', '0/0/0'), ('B6', 0, '1/0/0', '0/2/0', '0/0/0'), ('B7', 0, '1/0/0', '0/2/0', '0/0/0'), ('B8', 0, '1/0/0', '0/2/0', '0/0/0'), ('B9', 0, '1/0/0', '0/2/0', '0/0/0'), ('B10', 0, '1/0/0', '0/2/0', '0/0/0'), 
('B11', 0, '1/0/0', '0/2/0', '0/0/0'), ('B12', 0, '1/0/0', '0/2/0', '0/0/0'), ('B13', 0, '1/0/0', '0/2/0', '0/0/0'), ('B14', 0, '1/0/0', '0/2/0', '0/0/0'), ('B15', 0, '1/0/0', '0/2/0', '0/0/0'), ('B16', 0, '1/0/0', '0/2/0', '0/0/0'), ('B17', 0, '1/0/0', '0/2/0', '0/0/0'), ('B18', 0, '1/0/0', '0/2/0', '0/0/0'), ('B19', 0, '1/0/0', '0/2/0', '0/0/0'), ('B20', 0, '1/0/0', '0/2/0', '0/0/0'), 
('B21', 0, '1/0/0', '0/2/0', '0/0/0'), ('B22', 0, '1/0/0', '0/2/0', '0/0/0'), ('B23', 0, '1/0/0', '0/2/0', '0/0/0'), ('B24', 0, '1/0/0', '0/2/0', '0/0/0'), ('B25', 0, '1/0/0', '0/2/0', '0/0/0'), ('B26', 0, '1/0/0', '0/2/0', '0/0/0'), ('B27', 0, '1/0/0', '0/2/0', '0/0/0'), ('B28', 0, '1/0/0', '0/2/0', '0/0/0'), ('B29', 0, '1/0/0', '0/2/0', '0/0/0'), ('B30', 0, '1/0/0', '0/2/0', '0/0/0'), 
('C1', 0, '0/0/0', '1/0/0', '1/0/0'), ('C2', 0, '0/0/0', '1/0/0', '1/0/0'), ('C3', 0, '0/0/0', '1/0/0', '1/0/0'), ('C4', 0, '0/0/0', '1/0/0', '1/0/0'), ('C5', 0, '0/0/0', '1/0/0', '1/0/0'), ('C6', 0, '0/0/0', '1/0/0', '1/0/0'), ('C7', 0, '0/0/0', '1/0/0', '1/0/0'), ('C8', 0, '0/0/0', '1/0/0', '1/0/0'), ('C9', 0, '0/0/0', '1/0/0', '1/0/0'), ('C10', 0, '0/0/0', '1/0/0', '1/0/0'), 
('C11', 0, '0/0/0', '1/0/0', '1/0/0'), ('C12', 0, '0/0/0', '1/0/0', '1/0/0'), ('C13', 0, '0/0/0', '1/0/0', '1/0/0'), ('C14', 0, '0/0/0', '1/0/0', '1/0/0'), ('C15', 0, '0/0/0', '1/0/0', '1/0/0'), ('C16', 0, '0/0/0', '1/0/0', '1/0/0'), ('C17', 0, '0/0/0', '1/0/0', '1/0/0'), ('C18', 0, '0/0/0', '1/0/0', '1/0/0'), ('C19', 0, '0/0/0', '1/0/0', '1/0/0'), ('C20', 0, '0/0/0', '1/0/0', '1/0/0'), 
('C21', 0, '0/0/0', '1/0/0', '1/0/0'), ('C22', 0, '0/0/0', '1/0/0', '1/0/0'), ('C23', 0, '0/0/0', '1/0/0', '1/0/0'), ('C24', 0, '0/0/0', '1/0/0', '1/0/0'), ('C25', 0, '0/0/0', '1/0/0', '1/0/0'), ('C26', 0, '0/0/0', '1/0/0', '1/0/0'), ('C27', 0, '0/0/0', '1/0/0', '1/0/0'), ('C28', 0, '0/0/0', '1/0/0', '1/0/0'), ('C29', 0, '0/0/0', '1/0/0', '1/0/0'), ('C30', 0, '0/0/0', '1/0/0', '1/0/0');
UPDATE `t-d-maps` SET `m-mage` = 50 WHERE `m-map` = 'A1';

DESCRIBE `t-d-maps`;


USE `dk_dkine`;
CREATE TABLE IF NOT EXISTS `t-d-meteor` (
	`m-meteorshower-start` BIGINT(11),
	`m-meteorshower-end` BIGINT(11),
	`m-arrive-meteor` BIGINT(11),
	`m-leave-meteor` BIGINT(11)
);

CREATE TABLE IF NOT EXISTS `t-d-convois` (
	`c-convois` BIGINT(11) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `t-d-serv` (
	`s-server-id` BIGINT(20) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `t-d-interserver-tchat` (
	`it-id` BIGINT(20) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `chan-lock-command` (
	`id` BIGINT(20) PRIMARY KEY
);


DESCRIBE `t-d-convois`;
DESCRIBE `t-d-serv`;
DESCRIBE `t-d-interserver-tchat`;
DESCRIBE `chan-lock-command`;