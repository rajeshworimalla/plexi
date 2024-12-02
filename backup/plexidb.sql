-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 24, 2024 at 04:51 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `plexidb`
--

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `id` int(11) NOT NULL,
  `job_id` int(11) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  `user_phone` int(11) DEFAULT NULL,
  `cover_letter` varchar(500) DEFAULT NULL,
  `date_applied` datetime DEFAULT NULL,
  `application_status` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`id`, `job_id`, `username`, `user_email`, `user_phone`, `cover_letter`, `date_applied`, `application_status`) VALUES
(15, 1, 'tasker', 'tasker@gmail.com', 1111111, 'i like this job', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `job_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `employer` varchar(255) DEFAULT NULL,
  `salary` float DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `requester_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`job_id`, `title`, `employer`, `salary`, `location`, `description`, `requester_id`) VALUES
(1, 'Babysitter', 'requester', 15, 'New York, NY', 'Looking for a responsible babysitter for two kids, aged 3 and 5.', 101),
(2, 'Lawn Mower', 'requester', 12.5, 'Los Angeles, CA', 'Need someone to mow lawns for residential properties.', 102),
(3, 'Dog Walker', 'requester', 18, 'Chicago, IL', 'Looking for an experienced dog walker for multiple dogs.', 103),
(4, 'House Cleaner', 'requester', 20, 'Houston, TX', 'Provide thorough cleaning services for small apartments.', 104),
(5, 'Grocery Shopper', 'QuickMart Services', 14, 'Phoenix, AZ', 'Shop for groceries and deliver them to customers.', 105),
(6, 'Snow Shoveler', 'Winter Solutions', 25, 'Denver, CO', 'Clear snow from residential driveways and walkways.', 106),
(7, 'Gardener', 'Bloom Landscaping', 18.5, 'San Diego, CA', 'Assist with planting and maintaining gardens.', 107),
(8, 'Tutor', 'Bright Minds Tutoring', 30, 'Boston, MA', 'Tutor elementary school students in math and science.', 108),
(9, 'Delivery Helper', 'QuickFix Deliveries', 16, 'Seattle, WA', 'Help with delivering small packages around the city.', 109),
(10, 'Car Washer', 'Shiny Wheels', 15, 'Miami, FL', 'Wash and detail cars for a local auto shop.', 110),
(31, 'Software Engineer', 'TechCorp Inc.', 120000, 'New York, NY', 'Develop and maintain software applications.', 101),
(32, 'Data Analyst', 'DataVision LLC', 80000, 'Chicago, IL', 'Analyze data to drive business decisions.', 102),
(33, 'Graphic Designer', 'CreativeEdge', 65000, 'San Francisco, CA', 'Design and create digital assets.', 103),
(34, 'Marketing Manager', 'AdPulse', 95000, 'Austin, TX', 'Manage marketing campaigns and strategies.', 104),
(35, 'Project Manager', 'BuildPro', 110000, 'Seattle, WA', 'Oversee project execution and deliverables.', 105),
(36, 'Web Developer', 'CodeWave', 70000, 'Denver, CO', 'Design and maintain company websites.', 106),
(37, 'Accountant', 'FinServe Solutions', 75000, 'Atlanta, GA', 'Manage financial records and reporting.', 107),
(38, 'HR Specialist', 'PeopleFirst', 60000, 'Miami, FL', 'Recruit and manage employee relations.', 108),
(39, 'Sales Executive', 'MarketMax', 72000, 'Dallas, TX', 'Drive sales and client relationships.', 109),
(40, 'Content Writer', 'WordCraft Agency', 50000, 'Boston, MA', 'Create compelling and engaging content.', 110);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `role` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `role`) VALUES
(31, 'requester', 'password', 'requester@gmail.com', 'requester'),
(32, 'tasker', 'password', 'tasker@gmail.com', 'tasker');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`job_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `job_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
