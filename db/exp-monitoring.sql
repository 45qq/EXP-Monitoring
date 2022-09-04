-- MySQL dump 10.13  Distrib 5.6.10, for Win64 (x86_64)
--
-- Host: localhost    Database: exp-monitoring
-- ------------------------------------------------------
-- Server version	5.6.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `github_info`
--

DROP TABLE IF EXISTS `github_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `github_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `star` int(11) NOT NULL,
  `name_key` varchar(15) DEFAULT NULL,
  `full_name` varchar(100) NOT NULL,
  `add_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `github_info_url_uindex` (`full_name`)
) ENGINE=InnoDB AUTO_INCREMENT=177202 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `github_info_inseart` AFTER INSERT ON `github_info` FOR EACH ROW begin
        if new.name_key is not null then
            insert into github_name_key_list(name_key, count, total_star, add_time, update_time)
                values(new.name_key, 1, new.star, new.add_time, new.add_time)
                on duplicate key update count=count+1, total_star=total_star+new.star, update_time=new.add_time;
        end if;
    end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `github_info_push_list`
--

DROP TABLE IF EXISTS `github_info_push_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `github_info_push_list` (
  `id` int(11) NOT NULL,
  `is_push` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  CONSTRAINT `github_info_push_github_info_id_fk` FOREIGN KEY (`id`) REFERENCES `github_info` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `github_monitor_list_view`
--

DROP TABLE IF EXISTS `github_monitor_list_view`;
/*!50001 DROP VIEW IF EXISTS `github_monitor_list_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `github_monitor_list_view` (
  `id` tinyint NOT NULL,
  `full_name` tinyint NOT NULL,
  `latest_star` tinyint NOT NULL,
  `update_time` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `github_name_key_change`
--

DROP TABLE IF EXISTS `github_name_key_change`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `github_name_key_change` (
  `name_key` varchar(80) NOT NULL,
  `count` int(11) DEFAULT NULL,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `github_name_key_change_name_key_update_time_uindex` (`name_key`,`update_time`),
  CONSTRAINT `github_name_key_change_github_name_key_list_name_key_fk` FOREIGN KEY (`name_key`) REFERENCES `github_name_key_list` (`name_key`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `github_name_key_list`
--

DROP TABLE IF EXISTS `github_name_key_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `github_name_key_list` (
  `name_key` varchar(80) NOT NULL,
  `count` int(11) NOT NULL,
  `total_star` int(11) DEFAULT NULL,
  `add_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`name_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `github_name_update` AFTER UPDATE ON `github_name_key_list` FOR EACH ROW begin
        insert into github_name_key_change(name_key, count, update_time)
        values(old.name_key, old.count, old.update_time) on duplicate key update count=new.count;
    end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary table structure for view `github_name_key_list_view`
--

DROP TABLE IF EXISTS `github_name_key_list_view`;
/*!50001 DROP VIEW IF EXISTS `github_name_key_list_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `github_name_key_list_view` (
  `name_key` tinyint NOT NULL,
  `count` tinyint NOT NULL,
  `add_time_today` tinyint NOT NULL,
  `update_time_today` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `github_name_key_push_list`
--

DROP TABLE IF EXISTS `github_name_key_push_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `github_name_key_push_list` (
  `name_key` varchar(80) NOT NULL,
  `count` int(11) NOT NULL,
  `push_grade` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`name_key`),
  CONSTRAINT `github_name_key_push_list_github_name_key_list_name_key_fk` FOREIGN KEY (`name_key`) REFERENCES `github_name_key_list` (`name_key`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `github_star_change`
--

DROP TABLE IF EXISTS `github_star_change`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `github_star_change` (
  `id` int(11) NOT NULL,
  `star` int(11) NOT NULL,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `github_star_change_id_star_uindex` (`id`,`star`),
  KEY `github_star_change_github_star_list_id_fk` (`id`),
  CONSTRAINT `github_star_change_github_star_list_id_fk` FOREIGN KEY (`id`) REFERENCES `github_star_list` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `github_star_change_push_list`
--

DROP TABLE IF EXISTS `github_star_change_push_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `github_star_change_push_list` (
  `id` int(11) NOT NULL,
  `growth_star` int(11) NOT NULL,
  `push_grade` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  CONSTRAINT `github_star_change_push_list_github_star_change_info_id_fk` FOREIGN KEY (`id`) REFERENCES `github_star_list` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `github_star_change_view`
--

DROP TABLE IF EXISTS `github_star_change_view`;
/*!50001 DROP VIEW IF EXISTS `github_star_change_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `github_star_change_view` (
  `id` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `init_star` tinyint NOT NULL,
  `latest_star` tinyint NOT NULL,
  `add_time_today` tinyint NOT NULL,
  `update_time_today` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `github_star_list`
--

DROP TABLE IF EXISTS `github_star_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `github_star_list` (
  `id` int(11) NOT NULL,
  `star` int(11) NOT NULL,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT `github_star_change_github_info_id_fk` FOREIGN KEY (`id`) REFERENCES `github_info` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `github_star_update` AFTER UPDATE ON `github_star_list` FOR EACH ROW begin
        insert ignore into github_star_change(id, star, update_time) values(old.id, old.star, old.update_time);
    end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `monitoring_config`
--

DROP TABLE IF EXISTS `monitoring_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitoring_config` (
  `option` varchar(35) NOT NULL DEFAULT '',
  `value` int(11) DEFAULT NULL,
  PRIMARY KEY (`option`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'exp-monitoring'
--
/*!50003 DROP FUNCTION IF EXISTS `get_config` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `get_config`(opt varchar(35)) RETURNS int(11)
begin
    return (select value from monitoring_config where `option`=opt);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `github_monitor_list_view`
--

/*!50001 DROP TABLE IF EXISTS `github_monitor_list_view`*/;
/*!50001 DROP VIEW IF EXISTS `github_monitor_list_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `github_monitor_list_view` AS select `github_info`.`id` AS `id`,`github_info`.`full_name` AS `full_name`,if(isnull(`gsl`.`star`),`github_info`.`star`,`gsl`.`star`) AS `latest_star`,if(isnull(`gsl`.`update_time`),`github_info`.`add_time`,`gsl`.`update_time`) AS `update_time` from (`github_info` left join `github_star_list` `gsl` on((`github_info`.`id` = `gsl`.`id`))) where ((to_days(now()) - to_days(`github_info`.`add_time`)) <= `get_config`('github_monitoring_duration')) order by if(isnull(`gsl`.`update_time`),`github_info`.`add_time`,`gsl`.`update_time`) desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `github_name_key_list_view`
--

/*!50001 DROP TABLE IF EXISTS `github_name_key_list_view`*/;
/*!50001 DROP VIEW IF EXISTS `github_name_key_list_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `github_name_key_list_view` AS select `github_name_key_list`.`name_key` AS `name_key`,`github_name_key_list`.`count` AS `count`,(to_days(now()) - to_days(`github_name_key_list`.`add_time`)) AS `add_time_today`,(to_days(now()) - to_days(`github_name_key_list`.`update_time`)) AS `update_time_today` from `github_name_key_list` where ((to_days(now()) - to_days(`github_name_key_list`.`update_time`)) <= `get_config`('github_monitoring_duration')) order by (to_days(now()) - to_days(`github_name_key_list`.`update_time`)),`github_name_key_list`.`count` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `github_star_change_view`
--

/*!50001 DROP TABLE IF EXISTS `github_star_change_view`*/;
/*!50001 DROP VIEW IF EXISTS `github_star_change_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `github_star_change_view` AS select `gi`.`id` AS `id`,`gi`.`name` AS `name`,`gi`.`star` AS `init_star`,`gmlv`.`latest_star` AS `latest_star`,(to_days(now()) - to_days(`gi`.`add_time`)) AS `add_time_today`,(to_days(now()) - to_days(`gmlv`.`update_time`)) AS `update_time_today` from (`github_info` `gi` join `github_monitor_list_view` `gmlv` on((`gi`.`id` = `gmlv`.`id`))) order by (to_days(now()) - to_days(`gmlv`.`update_time`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-04 20:52:51
