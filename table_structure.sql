-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        5.6.29-log - Source distribution
-- 服务器操作系统:                      Linux
-- HeidiSQL 版本:                  9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 god_metric_meta 的数据库结构
CREATE DATABASE IF NOT EXISTS `god_metric_meta` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `god_metric_meta`;

-- 导出  表 god_metric_meta.t_chart_datasource 结构
CREATE TABLE IF NOT EXISTS `t_chart_datasource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '名称',
  `types` tinyint(4) NOT NULL COMMENT '数据源类型，0:mysql,1:计算型mysql,2.fakecube,3:hive',
  `conf` blob COMMENT '数据源配置信息',
  `user` varchar(50) NOT NULL COMMENT '用户名',
  `uptime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '状态，0无效1有效',
  PRIMARY KEY (`id`),
  KEY `name_status` (`name`,`status`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COMMENT='数据源表';

-- 数据导出被取消选择。
-- 导出  表 god_metric_meta.t_chart_menu 结构
CREATE TABLE IF NOT EXISTS `t_chart_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '菜单名称',
  `url` varchar(100) NOT NULL COMMENT '对应url',
  `level` tinyint(4) NOT NULL DEFAULT '0' COMMENT '菜单等级',
  `parent_id` int(11) NOT NULL DEFAULT '0' COMMENT '父菜单id',
  `sort` int(11) NOT NULL DEFAULT '100' COMMENT '顺序',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态：0无效1显式菜单2隐式菜单',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COMMENT='菜单表';

-- 数据导出被取消选择。
-- 导出  表 god_metric_meta.t_chart_modules 结构
CREATE TABLE IF NOT EXISTS `t_chart_modules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '模块名称',
  `module_types` varchar(50) NOT NULL COMMENT '父模块名',
  `types` tinyint(4) NOT NULL COMMENT '模块类型',
  `template` varchar(50) NOT NULL COMMENT '模板',
  `status` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `module_types_types` (`module_types`,`types`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='模块表指定文件关系';

-- 数据导出被取消选择。
-- 导出  表 god_metric_meta.t_chart_reports 结构
CREATE TABLE IF NOT EXISTS `t_chart_reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '报表名称',
  `conf` blob NOT NULL COMMENT '图表配置信息',
  `code` text COMMENT '自定义代码',
  `customs` blob COMMENT '自定义信息',
  `user` varchar(100) NOT NULL DEFAULT '' COMMENT '最后管理者',
  `uptime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '状态：0为删除，1为有效',
  PRIMARY KEY (`id`),
  KEY `name` (`name`,`status`),
  KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COMMENT='报表配置';

-- 数据导出被取消选择。
-- 导出  表 god_metric_meta.t_chart_task 结构
CREATE TABLE IF NOT EXISTS `t_chart_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '任务名称',
  `types` tinyint(4) NOT NULL COMMENT '计划任务类型（为了和数据源统一），0:mysql,1:计算型mysql,fakecube,3:hive',
  `conf` blob COMMENT '计划任务配置信息',
  `st` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '任务有效期开始时间',
  `et` timestamp NULL DEFAULT NULL COMMENT '任务有效期结束时间',
  `cron` varchar(50) NOT NULL COMMENT '运行时间',
  `pri` int(11) NOT NULL DEFAULT '0' COMMENT '优先级',
  `user` int(11) NOT NULL DEFAULT '0' COMMENT '用户名',
  `uptime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '状态，0无效 1有效,2删除',
  `task_status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0 待加入cron 1已加入cron 2 已从cron删除',
  PRIMARY KEY (`id`),
  KEY `name_status` (`name`,`status`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='任务表';

-- 数据导出被取消选择。
-- 导出  表 god_metric_meta.t_chart_task_log 结构
CREATE TABLE IF NOT EXISTS `t_chart_task_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tid` int(11) NOT NULL COMMENT '任务id',
  `types` tinyint(4) NOT NULL COMMENT '任务类型，1为自动2为手动',
  `run_time` timestamp NULL DEFAULT NULL COMMENT '传送任务的时间',
  `st` timestamp NULL DEFAULT NULL COMMENT '任务开始时间',
  `et` timestamp NULL DEFAULT NULL COMMENT '任务结束时间',
  `msg` varchar(500) NOT NULL DEFAULT '' COMMENT '错误信息',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '任务状态：0初始化，1任务失败，2任务成功，3取消任务',
  PRIMARY KEY (`id`),
  KEY `status` (`status`,`tid`),
  KEY `tid` (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8 COMMENT='任务运行表';

-- 数据导出被取消选择。
-- 导出  表 god_metric_meta.t_chart_task_relation 结构
CREATE TABLE IF NOT EXISTS `t_chart_task_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tid` int(11) NOT NULL COMMENT '任务id',
  `tables` varchar(100) NOT NULL COMMENT '表名',
  `table_tag` varchar(100) DEFAULT NULL COMMENT '标签名称，根据标签名称找表',
  `date` date NOT NULL COMMENT '日期',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tid_table` (`tid`,`tables`),
  KEY `tid` (`tid`,`date`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8 COMMENT='任务与创建表的关系';

DELETE FROM `t_chart_menu`;
/*!40000 ALTER TABLE `t_chart_menu` DISABLE KEYS */;
INSERT INTO `t_chart_menu` (`id`, `name`, `url`, `level`, `parent_id`, `sort`, `status`) VALUES
  (1, '数据源管理', '/datasource/', 1, 0, 100, 1),
  (2, '查看数据源', '/datasource/index', 2, 1, 100, 1),
  (3, '添加数据源', '/datasource/edit?types', 2, 1, 100, 1),
  (4, 'mysql', '/datasource/edit?types=0', 3, 3, 100, 1),
  (5, '计算型mysql', '/datasource/edit?types=1', 3, 3, 100, 1),
  (6, 'fakecube', '/datasource/edit?types=2', 3, 3, 100, 1),
  (7, '报表管理', '/chart/', 1, 0, 100, 1),
  (8, '查看报表', '/chart/index', 2, 7, 100, 1),
  (9, '添加报表', '/chart/edit', 2, 7, 100, 1),
  (10, '任务管理', '/task/', 1, 0, 90, 1),
  (11, '任务查看', '/task/index', 2, 10, 100, 1),
  (12, '添加任务', '/task/edit?types', 2, 10, 100, 1),
  (13, '任务日志', '/task/run_index', 2, 10, 100, 1),
  (14, '计算型mysql', '/task/edit?types=1', 3, 12, 100, 1),
  (15, 'fakecube', '/task/edit?types=2', 3, 12, 100, 1),
  (16, '数据源操作', '/datasource/edit?id', 2, 1, 100, 2),
  (17, '报表操作', '/chart/edit?id', 2, 7, 100, 2),
  (18, '报表查看', '/chart/get_chart', 2, 7, 100, 2),
  (19, '任务操作', '/task/edit?id', 2, 10, 100, 2),
  (20, 'hive', '/datasource/edit?types=3', 3, 3, 100, 1),
  (21, 'hive', '/task/edit?types=3', 3, 12, 100, 1);
/*!40000 ALTER TABLE `t_chart_menu` ENABLE KEYS */;

-- 正在导出表  god_metric_meta.t_chart_modules 的数据：~7 rows (大约)
DELETE FROM `t_chart_modules`;
/*!40000 ALTER TABLE `t_chart_modules` DISABLE KEYS */;
INSERT INTO `t_chart_modules` (`id`, `name`, `module_types`, `types`, `template`, `status`) VALUES
  (1, 'fakecube', 'datasource', 2, 'datasource/fakecube_edit.tpl', 1),
  (2, 'hive', 'datasource', 3, 'datasource/hive_edit.tpl', 1),
  (3, 'mysql', 'datasource', 0, 'datasource/mysql_edit.tpl', 1),
  (4, 'mysql_caculate', 'datasource', 1, 'datasource/mysql_caculate_edit.tpl', 1),
  (5, 'mysql_caculate', 'task', 1, 'task/mysql_caculate_edit.tpl', 1),
  (6, 'fakecube', 'task', 2, 'task/fakecube_edit.tpl', 1),
  (7, 'hive', 'task', 3, 'task/hive_edit.tpl', 1);