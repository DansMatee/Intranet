-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               9.0.1 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping data for table intranet.jobs: ~5 rows (approximately)
INSERT INTO `jobs` (`id`, `table_id`, `job_number`, `job_severity`, `job_header`, `job_desc`, `timestamp`, `employee_id`, `archived`) VALUES
	(9, 'support-2', '35425252', 'low', 'test', 'test', '2024-10-30 11:24:51', 3, 0),
	(10, 'support-2', 'S00038762', 'medium', 'Test Header 2', 'Test Description 2', '2024-10-30 10:22:33', 3, 0),
	(11, 'support-2', 'S00038762', 'high', 'Test Header 2', 'Test Description 2', '2024-10-30 13:22:33', 3, 0),
	(12, 'support-2', 'S00038762', 'critical', 'Test Header 2', 'Test Description 2', '2024-10-30 15:13:00', 3, 0),
	(13, 'support-2', 'S00038762', 'resolved', 'Test Header 2 YY', 'Test Description 2', '2024-10-30 12:35:52', 3, 0);

-- Dumping data for table intranet.links: ~2 rows (approximately)
INSERT INTO `links` (`id`, `table_id`, `link_name`, `link_dest`, `timestamp`, `employee_id`, `archived`) VALUES
	(16, 'support-1', 'Teest', 'testse', '2024-10-30 11:27:37', 3, 0),
	(17, 'support-1', 'testse', 'testsees', '2024-10-30 11:56:44', 3, 0);

-- Dumping data for table intranet.logs: ~24 rows (approximately)
INSERT INTO `logs` (`id`, `username`, `action`, `desc`, `ip_address`, `timestamp`) VALUES
	(43, 'dans', 'Created New Support Link', 'Created new support link with ID:  in support link section support-1', '127.0.0.1', '2024-10-29 15:31:14'),
	(44, 'dans', 'Created New Support Link', 'Created new support link with ID: 15 in support link section support-1', '127.0.0.1', '2024-10-29 15:32:01'),
	(45, 'dans', 'Activated User', 'User dans activated account id 5.', '127.0.0.1', '2024-10-29 15:42:17'),
	(46, 'dans', 'Updated User', 'User dans updated account id: 5, new account settings: Is Active: True, Permissions: TANK, Department Admin: False.', '127.0.0.1', '2024-10-29 15:44:32'),
	(47, 'dans', 'Deleted Support Link', 'User dans deleted support link with ID: 15.', '127.0.0.1', '2024-10-29 15:50:34'),
	(48, 'dans', 'Updated Support Link', 'User dans updated support link with ID: 14, new details: Link Name: Test Test, Link Destination: Test.', '127.0.0.1', '2024-10-29 15:50:49'),
	(49, 'dans', 'Created New Support Job', 'User dans created new support job with ID: 10 in support job section support-2.', '127.0.0.1', '2024-10-30 11:20:46'),
	(50, 'dans', 'Updated Support Job', 'User dans updated support job with ID: 10, new details: Severity: medium, Job Header: Test Header 2, Job Description: Test Description 2.', '127.0.0.1', '2024-10-30 11:21:05'),
	(51, 'dans', 'Archived Support Job', 'User dans archived support job with ID: 0 in support job sectionsupport-2.', '127.0.0.1', '2024-10-30 11:22:33'),
	(52, 'dans', 'Updated Support Job', 'User dans updated support job with ID: 9, new details: Severity: medium, Job Header: test, Job Description: test.', '127.0.0.1', '2024-10-30 11:23:40'),
	(53, 'dans', 'Updated Support Job', 'User dans updated support job with ID: 9, new details: Severity: resolved, Job Header: test, Job Description: test.', '127.0.0.1', '2024-10-30 11:23:58'),
	(54, 'dans', 'Updated Support Job', 'User dans updated support job with ID: 9, new details: Severity: low, Job Header: test, Job Description: test.', '127.0.0.1', '2024-10-30 11:24:49'),
	(55, 'dans', 'Archived Support Job', 'User dans archived support job with ID: 9 in support job sectionsupport-2.', '127.0.0.1', '2024-10-30 11:24:51'),
	(56, 'dans', 'Updated Support Link', 'User dans updated support link with ID: 14, new details: Link Name: Test Test A, Link Destination: Test.', '127.0.0.1', '2024-10-30 11:24:57'),
	(57, 'dans', 'Deleted Support Link', 'User dans deleted support link with ID: 14.', '127.0.0.1', '2024-10-30 11:25:03'),
	(58, 'dans', 'Created New Support Link', 'User dans created new support link with ID: 16 in support link section support-1.', '127.0.0.1', '2024-10-30 11:27:37'),
	(59, 'dans', 'Archived Support Link', 'User dans archived support link with ID: 16.', '127.0.0.1', '2024-10-30 11:28:11'),
	(60, 'dans', 'Created New Support Link', 'User dans created new support link with ID: 17 in support link section support-1.', '127.0.0.1', '2024-10-30 11:56:44'),
	(61, 'dans', 'Updated Support Job', 'User dans updated support job with ID: 13, new details: Severity: resolved, Job Header: Test Header 2 YY, Job Description: Test Description 2.', '127.0.0.1', '2024-10-30 12:35:52'),
	(62, 'dans', 'Updated Support Job', 'User dans updated support job with ID: 12, new details: Severity: critical, Job Header: Test Header 2, Job Description: Test Description 2.', '127.0.0.1', '2024-10-30 15:13:00'),
	(63, 'dans', 'Created New Support Notice', 'User dans created new support notice with ID: 1 in support notice section support-3.', '127.0.0.1', '2024-10-31 10:21:01'),
	(64, 'dans', 'Updated Support Job', 'User dans updated support job with ID: 1, new details: Severity: Test Notice Header, Job Header: Test Notice Description, Job Description: None.', '127.0.0.1', '2024-10-31 10:40:18'),
	(65, 'dans', 'Archived Support Job', 'User dans archived support job with ID: 1 in support job sectionsupport-3.', '127.0.0.1', '2024-10-31 10:40:24'),
	(66, 'dans', 'Archived Support Notice', 'User dans archived support notice with ID: 1.', '127.0.0.1', '2024-10-31 10:40:52'),
	(67, 'dans', 'Archived Support Notice', 'User dans archived support notice with ID: 8.', '127.0.0.1', '2024-10-31 11:21:49');

-- Dumping data for table intranet.notices: ~8 rows (approximately)
INSERT INTO `notices` (`id`, `table_id`, `notice_header`, `notice_desc`, `timestamp`, `employee_id`, `archived`) VALUES
	(1, 'support-3', 'Test Notice Header', 'Test Notice Description', '2024-10-31 10:21:01', 3, 0),
	(2, 'support-3', 'Test Notice Header', 'Test Notice Description', '2024-10-31 15:21:01', 3, 0),
	(3, 'support-3', 'Test Notice Header', 'Test Notice Description', '2024-10-30 10:21:01', 3, 0),
	(4, 'support-3', 'Test Notice Header', 'Test Notice Description', '2024-10-10 20:21:01', 3, 0),
	(5, 'support-3', 'Test Notice Header', 'Test Notice Description', '2024-10-31 11:21:01', 3, 0),
	(6, 'support-3', 'Test Notice Header', 'Test Notice Description', '2024-10-31 10:21:01', 3, 0),
	(7, 'support-3', 'Test Notice Header', 'Test Notice Description', '2024-10-21 10:21:01', 3, 0),
	(8, 'support-3', 'Test Notice Header', 'Test Notice Description', '2024-10-31 19:21:01', 3, 1);

-- Dumping data for table intranet.users: ~7 rows (approximately)
INSERT INTO `users` (`id`, `username`, `password`, `isActive`, `permSet`, `firstname`, `lastname`, `email`, `departmentAdmin`) VALUES
	(3, 'dans', 'scrypt:32768:8:1$PnOvKpKiLgBOsMBT$1bf0f659ec684f788741d9135b10a48cd7261107518d63769a3d4f6fe050692e68a4ec1c768eed3c00fe32a7f98b97aa8e792fb5fd9c8fd0dc2c1994c59bc06a', 1, 'ADMIN', 'Daniel', 'Americo', 'Daniel@Americo.com.au', 0),
	(5, 'dansa', 'scrypt:32768:8:1$PnOvKpKiLgBOsMBT$1bf0f659ec684f788741d9135b10a48cd7261107518d63769a3d4f6fe050692e68a4ec1c768eed3c00fe32a7f98b97aa8e792fb5fd9c8fd0dc2c1994c59bc06a', 1, 'GUEST', 'Mary', 'Smith', 'Mary@Smith.com.au', 0),
	(8, 't435t34', 'scrypt:32768:8:1$PnOvKpKiLgBOsMBT$1bf0f659ec684f788741d9135b10a48cd7261107518d63769a3d4f6fe050692e68a4ec1c768eed3c00fe32a7f98b97aa8e792fb5fd9c8fd0dc2c1994c59bc06a', 1, 'TANK', 'John', 'Smith', 'John@Smith.com.au', 0),
	(9, '453', 'scrypt:32768:8:1$PnOvKpKiLgBOsMBT$1bf0f659ec684f788741d9135b10a48cd7261107518d63769a3d4f6fe050692e68a4ec1c768eed3c00fe32a7f98b97aa8e792fb5fd9c8fd0dc2c1994c59bc06a', 1, 'SUPPORT', 'John', 'Appleseed', 'John@Appleseed.com.au', 0),
	(12, 'hrthrt', 'scrypt:32768:8:1$PnOvKpKiLgBOsMBT$1bf0f659ec684f788741d9135b10a48cd7261107518d63769a3d4f6fe050692e68a4ec1c768eed3c00fe32a7f98b97aa8e792fb5fd9c8fd0dc2c1994c59bc06a', 1, 'GENERAL', 'John', 'Doe', 'John@Doe.com.au', 0),
	(14, 'feef42rt3', 'scrypt:32768:8:1$PnOvKpKiLgBOsMBT$1bf0f659ec684f788741d9135b10a48cd7261107518d63769a3d4f6fe050692e68a4ec1c768eed3c00fe32a7f98b97aa8e792fb5fd9c8fd0dc2c1994c59bc06a', 1, 'SALES', 'John', 'Jones', 'John@Jones.com.au', 1),
	(15, 't5y343t', 'scrypt:32768:8:1$PnOvKpKiLgBOsMBT$1bf0f659ec684f788741d9135b10a48cd7261107518d63769a3d4f6fe050692e68a4ec1c768eed3c00fe32a7f98b97aa8e792fb5fd9c8fd0dc2c1994c59bc06a', 1, 'SUPPORT', 'Mary', 'Appleseed', 'Mary@Appleseed.com.au', 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
