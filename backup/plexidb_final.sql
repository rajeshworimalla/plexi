-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 01, 2024 at 04:37 PM
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
  `application_id` int(11) NOT NULL,
  `job_id` int(11) DEFAULT NULL,
  `date_applied` datetime DEFAULT NULL,
  `app_status` varchar(10) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`application_id`, `job_id`, `date_applied`, `app_status`, `user_id`) VALUES
(2, 2, '2024-11-02 00:00:00', 'Reviewed', 31),
(3, 3, '2024-11-03 00:00:00', 'Rejected', 31),
(4, 4, '2024-11-04 00:00:00', 'Accepted', 204),
(5, 5, '2024-11-05 00:00:00', 'Pending', 205),
(6, 6, '2024-11-06 00:00:00', 'Pending', 206),
(7, 7, '2024-11-07 00:00:00', 'Reviewed', 207),
(8, 8, '2024-11-08 00:00:00', 'Rejected', 208),
(9, 9, '2024-11-09 00:00:00', 'Accepted', 209),
(10, 10, '2024-11-10 00:00:00', 'Pending', 210),
(11, 11, '2024-11-11 00:00:00', 'Accepted', 211),
(12, 12, '2024-11-12 00:00:00', 'Rejected', 212),
(13, 13, '2024-11-13 00:00:00', 'Reviewed', 213),
(14, 14, '2024-11-14 00:00:00', 'Pending', 214),
(15, 15, '2024-11-15 00:00:00', 'Rejected', 215),
(16, 16, '2024-11-16 00:00:00', 'Pending', 216),
(17, 17, '2024-11-17 00:00:00', 'Reviewed', 217),
(18, 18, '2024-11-18 00:00:00', 'Accepted', 218),
(21, 41, '2024-12-01 01:13:50', 'Rejected', 31),
(27, 41, '2024-12-01 01:25:30', 'Rejected', 31),
(30, 41, '2024-12-01 14:26:37', 'Rejected', 31),
(33, 47, '2024-12-01 20:45:54', 'Accepted', 221);

-- --------------------------------------------------------

--
-- Table structure for table `chats`
--

CREATE TABLE `chats` (
  `id` int(11) NOT NULL,
  `user1_id` int(11) NOT NULL,
  `user2_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chats`
--

INSERT INTO `chats` (`id`, `user1_id`, `user2_id`, `created_at`) VALUES
(14, 31, 203, '2024-11-28 10:17:00'),
(15, 31, 204, '2024-11-28 14:20:56'),
(16, 31, 207, '2024-11-28 15:17:21'),
(20, 31, 221, '2024-12-01 15:01:46');

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
  `requester_id` int(11) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`job_id`, `title`, `employer`, `salary`, `location`, `description`, `requester_id`, `phone`, `email`, `date_added`) VALUES
(1, 'Software Developer', 'Tech Innovators', 85000, 'New York, NY', 'Develop and maintain software applications.', 101, '123-456-7890', 'hr@techinnovators.com', NULL),
(2, 'Data Analyst', 'DataWiz Corp', 70000, 'San Francisco, CA', 'Analyze data trends to support business decisions.', 102, '987-654-3210', 'careers@datawiz.com', NULL),
(3, 'Graphic Designer', 'Creative Studio', 55000, 'Austin, TX', 'Design marketing materials and branding assets.', 103, '456-123-7890', 'jobs@creativestudio.com', NULL),
(4, 'Project Manager', 'BuildIt Inc', 90000, 'Chicago, IL', 'Manage project timelines and deliverables.', 104, '321-654-9870', 'pm@buildit.com', NULL),
(5, 'Marketing Specialist', 'AdVentures LLC', 60000, 'Miami, FL', 'Develop and execute marketing campaigns.', 105, '789-456-1230', 'marketing@adventures.com', NULL),
(6, 'IT Support Specialist', 'NetSecure Solutions', 50000, 'Dallas, TX', 'Provide technical support and troubleshoot issues.', 106, '567-890-1234', 'itsupport@netsecure.com', NULL),
(7, 'HR Coordinator', 'PeopleFirst HR', 52000, 'Seattle, WA', 'Assist with recruitment and employee relations.', 107, '123-789-4560', 'hr@peoplefirst.com', NULL),
(8, 'Accountant', 'FinancePros', 62000, 'Denver, CO', 'Manage financial records and prepare reports.', 108, '890-567-1234', 'accounting@financepros.com', NULL),
(9, 'Content Writer', 'WriteWell Agency', 45000, 'Portland, OR', 'Create engaging content for blogs and websites.', 109, '654-321-9870', 'jobs@writewell.com', NULL),
(10, 'Web Developer', 'CodeCraft', 78000, 'Boston, MA', 'Build and maintain websites and web apps.', 110, '567-123-8901', 'careers@codecraft.com', NULL),
(11, 'UX Designer', 'DesignHub', 80000, 'San Jose, CA', 'Design user-friendly interfaces for web and mobile.', 111, '789-012-3456', 'hr@designhub.com', NULL),
(12, 'Operations Manager', 'LogiTech', 95000, 'Atlanta, GA', 'Oversee daily operations and logistics.', 112, '234-567-8901', 'operations@logitech.com', NULL),
(13, 'Research Scientist', 'BioTech Labs', 100000, 'San Diego, CA', 'Conduct research and develop new products.', 113, '432-109-8765', 'research@biotechlabs.com', NULL),
(14, 'Social Media Manager', 'TrendMakers', 58000, 'Orlando, FL', 'Manage social media channels and campaigns.', 114, '210-345-6789', 'socialmedia@trendmakers.com', NULL),
(15, 'Customer Service Rep', 'ClientCare Inc', 42000, 'Houston, TX', 'Handle customer inquiries and resolve issues.', 115, '789-654-1234', 'support@clientcare.com', NULL),
(16, 'Sales Representative', 'Global Reach', 55000, 'Las Vegas, NV', 'Drive sales and maintain client relationships.', 116, '876-543-2109', 'sales@globalreach.com', NULL),
(17, 'Teacher', 'LearningTree Academy', 40000, 'Phoenix, AZ', 'Teach and mentor students in a classroom setting.', 117, '321-678-5432', 'careers@learningtree.com', NULL),
(18, 'Mechanical Engineer', 'Engineered Solutions', 85000, 'Detroit, MI', 'Design and test mechanical components.', 118, '123-543-6789', 'engineers@engineeredsolutions.com', NULL),
(19, 'Business Analyst', 'CorpConsult', 75000, 'Charlotte, NC', 'Analyze business needs and recommend solutions.', 119, '765-432-1098', 'jobs@corpconsult.com', NULL),
(20, 'Photographer', 'Picture Perfect Studios', 35000, 'Nashville, TN', 'Capture and edit professional photographs.', 120, '543-210-9876', 'info@pictureperfect.com', NULL),
(41, 'testjob', 'requester', 5, 'kansas, kentucky', 'life aint daijobu', 31, '123123', 'requester@gmail.com', '2024-11-30 19:18:38'),
(46, 'helloworld', 'requester', 5, 'catmandu', 'idk bro', 31, '123123', 'requester@gmail.com', '2024-12-01 19:00:06'),
(47, 'testjob2', 'requester123', 51, 'dogmandu', 'chill', 31, '123123', 'requester123@gmail.com', '2024-12-01 20:44:44');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `chat_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `chat_id`, `sender_id`, `message`, `timestamp`) VALUES
(11, 14, 31, 'hey bro wassup', '2024-11-28 10:17:08'),
(12, 15, 31, 'hello brother', '2024-11-28 14:21:04'),
(13, 16, 31, 'hello', '2024-11-28 15:17:35'),
(18, 15, 31, 'sup', '2024-11-30 10:06:32'),
(24, 20, 31, 'lorem ipsum bro', '2024-12-01 15:01:57'),
(25, 20, 221, 'aight mate', '2024-12-01 15:02:28');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `review_id` int(11) NOT NULL,
  `review` text NOT NULL,
  `by_user` int(11) NOT NULL,
  `to_user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `role` varchar(200) DEFAULT NULL,
  `bio` varchar(500) DEFAULT NULL,
  `main_job` varchar(100) DEFAULT NULL,
  `task_completed` int(11) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `role`, `bio`, `main_job`, `task_completed`, `age`, `location`, `phone_number`, `created_at`) VALUES
(1, 'dummy_user', 'dummy_password', 'dummy_user@example.com', 'admin', 'This is a dummy bio.', 'Software Engineer', 0, 25, 'New York, USA', '1234567890', '2024-12-01 10:08:28'),
(31, 'requester123', 'password123', 'requester123@gmail.com', 'requester', '            test123\r\n        ', 'test123', 90, 123, 'test', '123123', '2024-11-13 08:50:48'),
(203, 'alicejohnson', 'password123', 'alicejohnson@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(204, 'bobbrown', 'password123', 'bobbrown@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(205, 'charliedavis', 'password123', 'charliedavis@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(206, 'dianaevans', 'password123', 'dianaevans@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(207, 'evewhite', 'password123', 'evewhite@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(208, 'frankmiller', 'password123', 'frankmiller@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(209, 'gracelee', 'password123', 'gracelee@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(210, 'harrymoore', 'password123', 'harrymoore@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(211, 'ivyadams', 'password123', 'ivyadams@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(212, 'jackwilson', 'password123', 'jackwilson@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(213, 'karentaylor', 'password123', 'karentaylor@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(214, 'leoharris', 'password123', 'leoharris@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(215, 'meganscott', 'password123', 'meganscott@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(216, 'nathanyoung', 'password123', 'nathanyoung@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(217, 'oliviaking', 'password123', 'oliviaking@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(218, 'paulwright', 'password123', 'paulwright@example.com', 'applicant', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(221, 'testname', '123', 'test@user.com', 'tasker', '', 'god', 0, 10, 'heaven', '12312', '2024-12-01 14:03:44');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`application_id`),
  ADD KEY `applications_ibfk_2` (`user_id`),
  ADD KEY `applications_ibfk_1` (`job_id`);

--
-- Indexes for table `chats`
--
ALTER TABLE `chats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chats_ibfk_1` (`user1_id`),
  ADD KEY `chats_ibfk_2` (`user2_id`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`job_id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `messages_ibfk_1` (`chat_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`review_id`),
  ADD KEY `fk_by_user` (`by_user`),
  ADD KEY `fk_to_user` (`to_user`);

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
  MODIFY `application_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `chats`
--
ALTER TABLE `chats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `job_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=222;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `applications_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `chats`
--
ALTER TABLE `chats`
  ADD CONSTRAINT `chats_ibfk_1` FOREIGN KEY (`user1_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `chats_ibfk_2` FOREIGN KEY (`user2_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`chat_id`) REFERENCES `chats` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `fk_by_user` FOREIGN KEY (`by_user`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_to_user` FOREIGN KEY (`to_user`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
