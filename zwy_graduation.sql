-- MySQL dump 10.13  Distrib 8.1.0, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: zwy_graduation
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications` (
  `applications_id` int NOT NULL,
  `applications_petName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `applications_petImage` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `applications_applicantName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `applications_applicantPhone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `applications_applicantEmail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `applications_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `applications_applyDate` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `applications_reviewDate` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `applications_shelter` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`applications_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications`
--

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `articles` (
  `articles_id` int unsigned NOT NULL,
  `articles_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `articles_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `articles_category` enum('knowledge','story','news','guide') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `articles_author` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `articles_status` enum('published','draft','review') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `articles_views` int unsigned DEFAULT NULL,
  `articles_likes` int unsigned DEFAULT NULL,
  `articles_comments` int unsigned DEFAULT NULL,
  `articles_createdAt` date NOT NULL,
  `articles_publishedAt` date DEFAULT NULL,
  PRIMARY KEY (`articles_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donation_project`
--

DROP TABLE IF EXISTS `donation_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donation_project` (
  `donationProjects_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `donationProjects_title` int unsigned NOT NULL,
  `donationProjects_image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `donationProjects_current` decimal(15,2) NOT NULL,
  `donationProjects_target` decimal(15,2) NOT NULL,
  `donationProjects_progress` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `donationProjects_donors` int unsigned NOT NULL,
  `donationProjects_daysLeft` smallint NOT NULL,
  `donationProjects_status` enum('draft','active','completed','paused') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `donationProjects_createdAt` date DEFAULT NULL,
  `donationProjects_endDate` date DEFAULT NULL,
  PRIMARY KEY (`donationProjects_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donation_project`
--

LOCK TABLES `donation_project` WRITE;
/*!40000 ALTER TABLE `donation_project` DISABLE KEYS */;
/*!40000 ALTER TABLE `donation_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donation_records`
--

DROP TABLE IF EXISTS `donation_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donation_records` (
  `donationRecords_id` int NOT NULL,
  `donationRecords_projectId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `donationRecords_projectTitle` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `donationRecords_donorName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `donationRecords_donorPhone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `donationRecords_amount` decimal(10,2) NOT NULL,
  `donationRecords_type` enum('direct','indirect','anonymous') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `donationRecords_status` enum('pending','completed','refunded','failed') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `donationRecords_createdAt` datetime NOT NULL,
  PRIMARY KEY (`donationRecords_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donation_records`
--

LOCK TABLES `donation_records` WRITE;
/*!40000 ALTER TABLE `donation_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `donation_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `events_id` int unsigned NOT NULL,
  `events_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `events_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `events_date` date NOT NULL,
  `events_time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `events_location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `events_status` enum('upcoming','ongoing','ended','canceled') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `events_participants` int unsigned DEFAULT NULL,
  `events_maxParticipants` int unsigned NOT NULL,
  `events_organizer` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `events_createdAt` date NOT NULL,
  PRIMARY KEY (`events_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pets`
--

DROP TABLE IF EXISTS `pets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pets` (
  `pets_id` int NOT NULL,
  `pets_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_breed` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_age` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_ageUnit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_neutered` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_vaccinated` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_createdAt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pets_shelter` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`pets_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pets`
--

LOCK TABLES `pets` WRITE;
/*!40000 ALTER TABLE `pets` DISABLE KEYS */;
/*!40000 ALTER TABLE `pets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `users_id` varchar(20) NOT NULL,
  `users_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `users_email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `users_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `users_role` enum('admin','users') NOT NULL DEFAULT 'users',
  `users_status` enum('active','inactive') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'active',
  `users_registeredAt` date NOT NULL,
  `users_lastLogin` date NOT NULL,
  `users_pwd` varchar(255) NOT NULL,
  `users_avatar` longblob,
  `users_gender` varchar(255) DEFAULT '其他',
  `users_exp` varchar(255) NOT NULL DEFAULT '有养宠经验',
  `users_job` varchar(255) NOT NULL DEFAULT '暂无' COMMENT '职业',
  `users_intro` varchar(100) NOT NULL DEFAULT '暂无' COMMENT '个人简介',
  `users_birthday` date NOT NULL DEFAULT '2025-01-01',
  PRIMARY KEY (`users_id`) USING BTREE,
  UNIQUE KEY `uniq_email` (`users_email`) USING BTREE,
  KEY `idx_status` (`users_status`) USING BTREE,
  KEY `idx_registered` (`users_registeredAt`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('1406b5d4-096','用户8','user8@example.com','178****7234','users','active','2024-02-17','2024-03-27','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('1917546e-575','用户10','user10@example.com','198****9234','users','inactive','2024-01-19','2024-03-29','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('20613844-bb2','YoloVme50','2013358073@qq.com','15095274931','admin','active','2025-04-13','2025-04-13','li040214',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('23c5d276-eb3','用户4','user4@example.com','138****3234','users','inactive','2024-01-12','2024-03-23','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('24b89a85-72f','用户6','user6@example.com','158****5234','users','active','2024-03-15','2024-03-25','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('2bb14d0f-d81','用户9','user9@example.com','188****8234','users','active','2024-03-18','2024-03-28','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('3ed0d766-fca','用户7','user7@example.com','168****6234','users','inactive','2024-01-16','2024-03-26','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('6c7c20be-a4b','用户3','user3@example.com','128****2234','users','active','2024-03-12','2024-03-22','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('8b8d10a1-aeb','用户5','user5@example.com','148****4234','users','active','2024-02-14','2024-03-24','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('aad5752c-6b1','你好','20133580170@qq.com','1509115274935','admin','active','2025-04-16','2025-04-16','li0410214',NULL,'其他',' ',' ',' ','2025-01-01'),('acfcd291-ccb','你好','201335810170@qq.com','150915274935','admin','active','2025-04-16','2025-04-16','li0410214',NULL,'其他','暂无养宠经验','暂无',' ','2025-01-01'),('cec400e4-a73','用户2','user2@example.com','118****1234','users','active','2024-02-11','2024-03-21','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('cf0f9bb5-03f','用户1','user1@example.com','108****0234','admin','inactive','2024-01-10','2024-03-20','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('da1a580f-4cd','用户11','user11@example.com','191****9234','users','inactive','2024-01-19','2024-03-29','1',_binary '﻿','其他','有养宠经验','暂无','暂无','2025-01-01'),('e9cc7c68-963','YoloVme52','2013358070@qq.com','15095274935','admin','active','2025-04-15','2025-04-15','li040214',NULL,'其他','','','','2025-01-01');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-16 20:34:57
