-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 20, 2014 at 01:13 PM
-- Server version: 5.5.35
-- PHP Version: 5.3.10-1ubuntu3.11

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ohdsiTest1`
--

-- --------------------------------------------------------

--
-- Table structure for table `drug_HOI_evidence`
--

CREATE TABLE IF NOT EXISTS `drug_HOI_evidence` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `drug_HOI_key` varchar(30) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'foreign key to drug_HOI_index',
  `evidence_type` varchar(30) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'the type of evidence (literature, product label, pharmacovigilance, EHR)',
  `evidence_source_code_id` int(8) NOT NULL COMMENT 'a code indicating the actual source of evidence (e.g., PubMed, US SPLs, EU SPC, VigiBase, etc)',
  `evidence_target_id` int(20) NOT NULL COMMENT 'a foreign key to data about the information artifact from which this evidence was found',
  `evidence_body_id` int(20) NOT NULL COMMENT 'a foreign key to a resource that adds additional information derived from this evidence item',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `drug_HOI_evidence`
--

INSERT INTO `drug_HOI_evidence` (`id`, `drug_HOI_key`, `evidence_type`, `evidence_source_code_id`, `evidence_target_id`, `evidence_body_id`) VALUES
(1, '36567-36110715', 'product_label', 1, 1, 1),
(2, '89013-10000059', 'product_label', 2, 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `drug_HOI_index`
--

CREATE TABLE IF NOT EXISTS `drug_HOI_index` (
  `drug_HOI_pair` varchar(30) NOT NULL COMMENT 'A key constructed from drug CUI - HOI - CUI',
  `drug` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'RxNorm CUI for the drug',
  `HOI` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'MedDRA CUI for the drug',
  PRIMARY KEY (`drug_HOI_pair`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `drug_HOI_index`
--

INSERT INTO `drug_HOI_index` (`drug_HOI_pair`, `drug`, `HOI`) VALUES
('36567-36110715', '36567', '36110715'),
('89013-10000059', '89013', '10000059');

-- --------------------------------------------------------

--
-- Table structure for table `evidence_bodies`
--

CREATE TABLE IF NOT EXISTS `evidence_bodies` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `body_id` int(20) NOT NULL COMMENT 'an id useful for retrieving all body attributes associated with an evidence item ',
  `body_tag` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'the tag name of a body attribute',
  `body_value_as_string` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'the string value of a body attribute',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `evidence_bodies`
--

INSERT INTO `evidence_bodies` (`id`, `body_id`, `body_tag`, `body_value_as_string`) VALUES
(1, 1, 'DATE OF THE SPC', '1/21/2011'),
(2, 1, 'AGE GROUP', '0'),
(3, 2, 'SPL_DATE', '10/3/2013'),
(4, 2, 'SPL_SECTION', 'Adverse Reactions');

-- --------------------------------------------------------

--
-- Table structure for table `evidence_sources`
--

CREATE TABLE IF NOT EXISTS `evidence_sources` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `evidence_source_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'a short name for the evidence source',
  `evidence_source_description` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'description of the evidence source ',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `evidence_sources`
--

INSERT INTO `evidence_sources` (`id`, `evidence_source_name`, `evidence_source_description`) VALUES
(1, 'EU_SPC', 'European product labeling'),
(2, 'SPLs', 'United States product labeling');

-- --------------------------------------------------------

--
-- Table structure for table `evidence_targets`
--

CREATE TABLE IF NOT EXISTS `evidence_targets` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `identifier` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'an identifer that can be used to retrieve the target',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `evidence_targets`
--

INSERT INTO `evidence_targets` (`id`, `identifier`) VALUES
(1, 'Abilify'),
(2, '105e5e20-8501-461e-b9cc-50e05b879157');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
