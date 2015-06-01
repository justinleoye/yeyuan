/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50128
Source Host           : localhost:3306
Source Database       : alex

Target Server Type    : MYSQL
Target Server Version : 50128
File Encoding         : 65001

Date: 2013-02-27 22:50:52
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `user`
-- ----------------------------

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `userpass` varchar(100) NOT NULL,
  `salt` varchar(100) NOT NULL,
  `email` varchar(100),
  `qq` varchar(13),
  PRIMARY KEY (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for `wordsbook`
-- ----------------------------

DROP TABLE IF EXISTS `wordsbook`;
CREATE TABLE `wordsbook` (
  `userwordid` int(13) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `word` varchar(60) NOT NULL,
  `count` int(4) NOT NULL DEFAULT 0,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userwordid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------


















