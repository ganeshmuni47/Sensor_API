-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 27, 2023 at 12:47 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sensors_database`
--

-- --------------------------------------------------------

--
-- Table structure for table `sensors_d`
--

CREATE TABLE `sensors_d` (
  `sensor_id` int(11) NOT NULL COMMENT 'Index Column Auto Incremented',
  `create_ts` datetime NOT NULL DEFAULT current_timestamp(),
  `sensor_name` varchar(100) DEFAULT NULL,
  `sensor_type` varchar(100) DEFAULT NULL,
  `sensor_details` varchar(1000) DEFAULT NULL,
  `sensor_applications` varchar(1000) DEFAULT NULL,
  `price` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sensors_d`
--

INSERT INTO `sensors_d` (`sensor_id`, `create_ts`, `sensor_name`, `sensor_type`, `sensor_details`, `sensor_applications`, `price`) VALUES
(0, '2023-12-26 17:21:04', ' Test Sensor - Water Pressure', 'Test Sensor', 'Manually Entered Data', NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `sensors_read_f`
--

CREATE TABLE `sensors_read_f` (
  `row_wid` int(11) NOT NULL COMMENT 'Index Column Auto Incremented',
  `sensor_id` int(11) NOT NULL,
  `read_ts` datetime NOT NULL DEFAULT current_timestamp(),
  `read_value` double NOT NULL,
  `read_value_1` double DEFAULT NULL,
  `read_value_2` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sensors_read_f`
--

INSERT INTO `sensors_read_f` (`row_wid`, `sensor_id`, `read_ts`, `read_value`, `read_value_1`, `read_value_2`) VALUES
(1, 0, '2023-12-27 11:55:28', 62, NULL, NULL),
(2, 0, '2023-12-27 11:55:38', 86, NULL, NULL),
(3, 0, '2023-12-27 11:55:48', 36, NULL, NULL),
(4, 0, '2023-12-27 12:02:12', 79, NULL, NULL),
(5, 0, '2023-12-27 12:02:23', 90, NULL, NULL),
(6, 0, '2023-12-27 12:02:33', 95, NULL, NULL),
(7, 0, '2023-12-27 12:02:43', 56, NULL, NULL),
(8, 0, '2023-12-27 12:02:53', 33, NULL, NULL),
(9, 0, '2023-12-27 12:03:03', 30, NULL, NULL),
(10, 0, '2023-12-26 12:03:13', 89, NULL, NULL),
(11, 0, '2023-12-27 12:03:23', 58, NULL, NULL),
(12, 0, '2023-12-27 12:03:33', 91, NULL, NULL),
(13, 0, '2023-12-27 12:03:43', 44, NULL, NULL),
(14, 0, '2023-12-27 12:03:53', 49, NULL, NULL),
(15, 0, '2023-12-27 12:04:03', 35, NULL, NULL),
(16, 0, '2023-12-27 12:04:13', 27, NULL, NULL),
(17, 0, '2023-12-27 12:04:23', 35, NULL, NULL),
(18, 0, '2023-12-27 12:04:33', 60, NULL, NULL),
(19, 0, '2023-12-27 12:04:43', 21, NULL, NULL),
(20, 0, '2023-12-26 12:04:54', 77, NULL, NULL),
(21, 0, '2023-12-27 12:05:04', 60, NULL, NULL),
(22, 0, '2023-12-27 12:05:14', 20, NULL, NULL),
(23, 0, '2023-12-27 12:05:24', 28, NULL, NULL),
(24, 0, '2023-12-27 12:05:35', 54, NULL, NULL),
(25, 0, '2023-12-27 12:05:45', 25, NULL, NULL),
(26, 0, '2023-12-27 12:05:55', 62, NULL, NULL),
(27, 0, '2023-12-27 12:06:05', 21, NULL, NULL),
(28, 0, '2023-12-27 12:06:15', 51, NULL, NULL),
(29, 0, '2023-12-27 12:06:25', 33, NULL, NULL),
(30, 0, '2023-12-27 12:06:35', 69, NULL, NULL),
(31, 0, '2023-12-27 12:06:45', 73, NULL, NULL),
(32, 0, '2023-12-27 12:06:55', 67, NULL, NULL),
(33, 0, '2023-12-27 12:07:05', 82, NULL, NULL),
(34, 0, '2023-12-27 12:07:15', 48, NULL, NULL),
(35, 0, '2023-12-27 12:07:25', 66, NULL, NULL),
(36, 0, '2023-12-27 12:07:35', 38, NULL, NULL),
(37, 0, '2023-12-27 12:07:45', 97, NULL, NULL),
(38, 0, '2023-12-27 12:07:56', 90, NULL, NULL),
(39, 0, '2023-12-27 12:08:06', 41, NULL, NULL),
(40, 0, '2023-12-27 12:08:16', 39, NULL, NULL),
(41, 0, '2023-12-27 12:08:26', 94, NULL, NULL),
(42, 0, '2023-12-27 12:08:36', 32, NULL, NULL),
(43, 0, '2023-12-27 12:08:46', 48, NULL, NULL),
(44, 0, '2023-12-27 12:08:56', 86, NULL, NULL),
(45, 0, '2023-12-27 12:09:06', 54, NULL, NULL),
(46, 0, '2023-12-27 12:09:16', 49, NULL, NULL),
(47, 0, '2023-12-27 12:09:26', 72, NULL, NULL),
(48, 0, '2023-12-27 12:09:36', 24, NULL, NULL),
(49, 0, '2023-12-27 12:09:47', 57, NULL, NULL),
(50, 0, '2023-12-27 12:09:57', 50, NULL, NULL),
(51, 0, '2023-12-27 12:10:07', 62, NULL, NULL),
(52, 0, '2023-12-27 12:10:17', 37, NULL, NULL),
(53, 0, '2023-12-27 12:10:27', 44, NULL, NULL),
(54, 0, '2023-12-27 12:10:37', 95, NULL, NULL),
(55, 0, '2023-12-27 12:10:47', 66, NULL, NULL),
(56, 0, '2023-12-27 12:10:57', 95, NULL, NULL),
(57, 0, '2023-12-27 12:11:07', 27, NULL, NULL),
(58, 0, '2023-12-27 12:11:17', 47, NULL, NULL),
(59, 0, '2023-12-27 12:11:27', 92, NULL, NULL),
(60, 0, '2023-12-27 12:11:37', 50, NULL, NULL),
(61, 0, '2023-12-27 15:31:39', 30.1, NULL, NULL);

-- --------------------------------------------------------

--
-- Stand-in structure for view `sensor_data_v`
-- (See below for the actual view)
--
CREATE TABLE `sensor_data_v` (
`sl_no` int(11)
,`sensor_type` varchar(100)
,`sensor_name` varchar(100)
,`read_date` date
,`read_time` varchar(13)
,`read_value` double
);

-- --------------------------------------------------------

--
-- Structure for view `sensor_data_v`
--
DROP TABLE IF EXISTS `sensor_data_v`;

CREATE ALGORITHM=UNDEFINED DEFINER=`admin`@`%` SQL SECURITY DEFINER VIEW `sensor_data_v`  AS SELECT `sf`.`row_wid` AS `sl_no`, `sd`.`sensor_type` AS `sensor_type`, `sd`.`sensor_name` AS `sensor_name`, cast(`sf`.`read_ts` as date) AS `read_date`, date_format(`sf`.`read_ts`,'%H:%i:%S') AS `read_time`, `sf`.`read_value` AS `read_value` FROM (`sensors_read_f` `sf` join `sensors_d` `sd`) WHERE `sf`.`sensor_id` = `sd`.`sensor_id` ORDER BY 1 DESC ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sensors_d`
--
ALTER TABLE `sensors_d`
  ADD PRIMARY KEY (`sensor_id`);

--
-- Indexes for table `sensors_read_f`
--
ALTER TABLE `sensors_read_f`
  ADD PRIMARY KEY (`row_wid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `sensors_d`
--
ALTER TABLE `sensors_d`
  MODIFY `sensor_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Index Column Auto Incremented', AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `sensors_read_f`
--
ALTER TABLE `sensors_read_f`
  MODIFY `row_wid` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Index Column Auto Incremented', AUTO_INCREMENT=62;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
