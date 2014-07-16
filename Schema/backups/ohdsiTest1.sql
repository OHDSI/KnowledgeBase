-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 17, 2014 at 04:12 PM
-- Server version: 5.5.37
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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `drug_HOI_evidence`
--

INSERT INTO `drug_HOI_evidence` (`id`, `drug_HOI_key`, `evidence_type`, `evidence_source_code_id`, `evidence_target_id`, `evidence_body_id`) VALUES
(1, '89013-35738560', 'product_label', 1, 1, 1),
(2, '36567-36110715', 'product_label', 2, 2, 2),
(3, '6944-10038435', 'literature_case_report', 3, 3, 3),
(4, '6944-10038435', 'literature_specific_review', 4, 4, 4);

-- --------------------------------------------------------

--
-- Table structure for table `drug_HOI_index`
--

CREATE TABLE IF NOT EXISTS `drug_HOI_index` (
  `drug_HOI_pair` varchar(30) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'A key constructed from drug CUI - HOI - CUI',
  `drug` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'RxNorm CUI for the drug',
  `drug_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'A string nlabel for the drug',
  `HOI` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'MedDRA CUI for the HOI',
  `HOI_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'A string label for the HOI',
  PRIMARY KEY (`drug_HOI_pair`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `drug_HOI_index`
--

INSERT INTO `drug_HOI_index` (`drug_HOI_pair`, `drug`, `drug_name`, `HOI`, `HOI_name`) VALUES
('36567-36110715', '36567', 'Simvastatin', '36110715', 'Upper respiratory tract infection'),
('6944-10038435', '6944', 'Metronidazole', '10038435', 'Renal failure'),
('89013-35738560', '89013', 'Aripiprazole', '35738560', 'Abdominal discomfort');

-- --------------------------------------------------------

--
-- Table structure for table `evidence_bodies`
--

CREATE TABLE IF NOT EXISTS `evidence_bodies` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `body_id` int(20) NOT NULL COMMENT 'an id useful for retrieving all body attributes associated with an evidence item ',
  `semantic_tag_id` int(20) NOT NULL COMMENT 'The concept identifier from the OHDSI Standard Vocabulary of the semantic tag used to annotate a body resource',
  `semantic_tag_label` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'the label of the semantic tag used to annotate a body resource',
  `value_as_concept` int(20) DEFAULT NULL COMMENT 'The  value from the Standard Vocabulary of the tagged concept',
  `value_as_string` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT 'the string value of a body attribute',
  `value_as_int` int(50) DEFAULT NULL COMMENT 'The integer value of the tagged concept',
  `value_as_double` double DEFAULT NULL COMMENT 'The double precision float  value of the tagged concept',
  `value_as_date` date DEFAULT NULL COMMENT 'The date value of the tagged concept',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=9 ;

--
-- Dumping data for table `evidence_bodies`
--

INSERT INTO `evidence_bodies` (`id`, `body_id`, `semantic_tag_id`, `semantic_tag_label`, `value_as_concept`, `value_as_string`, `value_as_int`, `value_as_double`, `value_as_date`) VALUES
(1, 1, 0, 'DATE OF THE SPC', NULL, NULL, NULL, NULL, '2011-01-21'),
(2, 1, 0, 'AGE GROUP', NULL, NULL, 0, NULL, NULL),
(3, 2, 0, 'SPL_DATE', NULL, NULL, NULL, NULL, '2013-08-10'),
(4, 2, 0, 'SPL_SECTION', NULL, 'Adverse Reactions', NULL, NULL, NULL),
(5, 1, 0, 'MEDDRA_PT_CODE', 35738560, 'ABDOMINAL DISCOMFORT', NULL, NULL, NULL),
(6, 1, 0, 'MEDDRA_SOC', 35700000, 'Gastrointestinal disorders', NULL, NULL, NULL),
(7, 3, 0, 'MEDLINE_PUBLISH_DATE', NULL, NULL, NULL, NULL, '1994-03-01'),
(8, 4, 0, 'MEDLINE_PUBLISH_DATE', NULL, NULL, NULL, NULL, '2001-03-03');

-- --------------------------------------------------------

--
-- Table structure for table `evidence_sources`
--

CREATE TABLE IF NOT EXISTS `evidence_sources` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'a short name for the evidence source. Same as http://purl.org/dc/elements/1.1/title',
  `description` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'Description of the evidence source. Same as http://purl.org/dc/elements/1.1/description',
  `contributer` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'Same as http://purl.org/dc/elements/1.1/contributor',
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'Same as http://purl.org/dc/elements/1.1/creator',
  `creation_date` date NOT NULL COMMENT 'Date that the source was created. For example, if the source was created in 2010 but added to the knowledge base in 2014, the creation date would be 2010',
  `rights` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'Same as http://purl.org/dc/elements/1.1/rights',
  `source` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'The source from which this data was derived. Same as http://purl.org/dc/elements/1.1/source',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `evidence_sources`
--

INSERT INTO `evidence_sources` (`id`, `title`, `description`, `contributer`, `creator`, `creation_date`, `rights`, `source`) VALUES
(1, 'EU_SPC_ADR', 'Adverse drug events extracted from European product labeling (SmPCs)', 'WHO', 'WHO', '2014-06-16', '', ''),
(2, 'US_SPL_ADR', 'Adverse drug reactions extracted from United States product labeling', 'SPLICER', 'Jon Duke', '2014-06-16', '', ''),
(3, 'MEDLINE_MeSH', 'MeSH tagged titles and abstracts in MEDLINE', 'Patrick Ryan', 'National Library of Medicine', '2014-06-17', '', ''),
(4, 'MEDLINE_SemMedDB', 'Titles and abstracts in MEDLINE processed with Metamap and SemRep', 'Richard Boyce', 'National Library of Medicine', '2014-06-17', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `evidence_targets`
--

CREATE TABLE IF NOT EXISTS `evidence_targets` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `uri` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'a unique resource identifer that can be used to retrieve the target from the RDF store',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `evidence_targets`
--

INSERT INTO `evidence_targets` (`id`, `uri`) VALUES
(1, 'http://purl.ohdsi.org/SmPC:Abilify'),
(2, 'http://purl.ohdsi.org/SPL:dc6c3d16-b7ab-46ee-83dc-846445beeee7'),
(3, 'http://purl.ohdsi.org/MEDLINE_MeSH:7817353'),
(4, 'http://purl.ohdsi.org/MEDLINE_SemMedDB:11085348');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
