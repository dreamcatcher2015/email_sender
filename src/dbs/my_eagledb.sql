/*
Navicat MySQL Data Transfer

Source Server         : 192.168.138.93
Source Server Version : 50529
Source Host           : 192.168.138.93:3306
Source Database       : eagledb

Target Server Type    : MYSQL
Target Server Version : 50529
File Encoding         : 65001

Date: 2014-02-11 03:07:28
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `node_tasks`
-- ----------------------------
DROP TABLE IF EXISTS `node_tasks`;
CREATE TABLE `node_tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskid` varchar(50) DEFAULT NULL,
  `taskinfo` text,
  `node` varchar(50) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT '0',
  `times` int(11) DEFAULT '0',
  `atime` datetime DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  `stime` datetime DEFAULT NULL,
  `ftime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taskid` (`taskid`),
  KEY `taskid_idx` (`taskid`),
  KEY `state_idx` (`state`),
  KEY `level_idx` (`level`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of node_tasks
-- ----------------------------

-- ----------------------------
-- Table structure for `node_tasks0`
-- ----------------------------
DROP TABLE IF EXISTS `node_tasks0`;
CREATE TABLE `node_tasks0` (
  `id` int(11) NOT NULL,
  `taskid` varchar(50) DEFAULT NULL,
  `taskinfo` text,
  `node` varchar(50) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT '0',
  `times` int(11) DEFAULT '0',
  `atime` datetime DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  `stime` datetime DEFAULT NULL,
  `ftime` datetime DEFAULT NULL,
  KEY `taskid_idx` (`taskid`),
  KEY `state_idx` (`state`),
  KEY `level_idx` (`level`),
  KEY `taskid` (`taskid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of node_tasks0
-- ----------------------------

-- ----------------------------
-- Table structure for `task_logs`
-- ----------------------------
DROP TABLE IF EXISTS `task_logs`;
CREATE TABLE `task_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskid` varchar(50) DEFAULT NULL,
  `output` text,
  `errput` text,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taskid` (`taskid`),
  KEY `taskid_idx` (`taskid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of task_logs
-- ----------------------------
DROP TRIGGER IF EXISTS `backup_node_tasks`;
DELIMITER ;;
CREATE TRIGGER `backup_node_tasks` BEFORE DELETE ON `node_tasks` FOR EACH ROW begin
  insert into node_tasks0 select * from node_tasks where id = OLD.id ;
end
;;
DELIMITER ;
