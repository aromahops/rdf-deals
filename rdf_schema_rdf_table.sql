-- MySQL dump 10.13  Distrib 8.0.15, for Win64 (x86_64)
--
-- Host: localhost    Database: rdf_schema
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `rdf_table`
--

DROP TABLE IF EXISTS `rdf_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `rdf_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `votes` int(11) NOT NULL,
  `thread_creation_time` datetime NOT NULL,
  `url` varchar(200) NOT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url_UNIQUE` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdf_table`
--

LOCK TABLES `rdf_table` WRITE;
/*!40000 ALTER TABLE `rdf_table` DISABLE KEYS */;
INSERT INTO `rdf_table` VALUES (1,'[Visions Electronics] Kingston MicroSD and USB 3.0 $5/$7/$14/$29 - 16GB/32GB/64GB/128GB',200,'2018-03-17 16:32:00','http://forums.redflagdeals.com/ebay-ca-amazon','2019-04-30 04:15:43'),(3,'eBay.ca eBay - $3.00 USD off min $3.01 - possible YMMV',343,'2019-04-29 09:22:00','http://forums.redflagdeals.com/ebay-canada-ebay-3-00-usd-off-min-3-01-possible-ymmv-2281672/','2019-04-30 04:39:00'),(7,'Reebok Reebok.ca Friends & Family Sale! Save 50% sitewide',125,'2019-04-26 02:48:00','http://forums.redflagdeals.com/reebok-reebok-ca-friends-family-sale-save-50-sitewide-2281054/','2019-04-30 04:40:26'),(8,'Costco Charging Essentials Wi-Fi Smart Plug x 2 $18.99/Smart Dimmer Switch x 2 $39.99',52,'2018-08-11 16:23:00','http://forums.redflagdeals.com/costco-charging-essentials-wi-fi-smart-plug-x-2-18-99-smart-dimmer-switch-x-2-39-99-2214317/','2019-04-30 04:41:35'),(10,'Costco [Costco East] (Brossard + Candiac + Sherbrooke + Boisbriand) April 29 to May 05, 2019...',54,'2019-04-29 14:58:00','http://forums.redflagdeals.com/costco-costco-east-brossard-candiac-sherbrooke-boisbriand-april-29-may-05-2019-2281793/','2019-04-30 04:41:35'),(11,'Rogers YMMV - Home Internet - Rogers retention plan - $35, 500mbps, unlimited',57,'2019-01-03 16:43:00','http://forums.redflagdeals.com/rogers-ymmv-home-internet-rogers-retention-plan-35-500mbps-unlimited-2254659/','2019-04-30 04:41:35'),(20,'[Manulife] Manulife Bank HISA 182 days 3.35% [on deposits to Advantage Account(s) opened between January 7, 2019 & May 15, 2019]',71,'2019-04-27 07:17:00','http://forums.redflagdeals.com/manulife-manulife-bank-hisa-182-days-3-35-deposits-advantage-account-s-opened-between-january-7-2019-may-15-2019-2281288/','2019-04-30 04:42:55'),(24,'TD Bank TD Aeroplan Visa Infinite Card - 30K Aeroplan & FYF is back',212,'2019-02-14 15:11:00','http://forums.redflagdeals.com/td-bank-td-aeroplan-visa-infinite-card-30k-aeroplan-fyf-back-2264814/','2019-04-30 17:49:28'),(25,'Amazon Canada $5.33 - Add-on Item: (2 Pack) AmazonBasics Indoor Extension Cord - Flat Plug, Grounded, White, 8-Foot',67,'2019-04-29 22:19:00','http://forums.redflagdeals.com/amazon-ca-5-33-add-item-2-pack-amazonbasics-indoor-extension-cord-flat-plug-grounded-white-8-foot-2281880/','2019-04-30 17:49:28'),(26,'eBay.ca eBay - $3.00 USD off min $3.01 - possible YMMV',414,'2019-04-29 09:22:00','http://forums.redflagdeals.com/ebay-3-00-usd-off-min-3-01-possible-ymmv-2281672/','2019-04-30 17:49:28'),(27,'[Manulife] Manulife Bank HISA 182 days 3.25% [on new Advantage Account deposits] ***Updated April 30, 2019***',73,'2019-04-27 07:17:00','http://forums.redflagdeals.com/manulife-manulife-bank-hisa-182-days-3-25-new-advantage-account-deposits-updated-april-30-2019-2281288/','2019-04-30 17:49:28'),(28,'eBay.ca (Neweggcanada) 10% off all newegg items on their eBay. Use code: PICKNEWEGG on the eBay App',56,'2019-04-25 10:27:00','http://forums.redflagdeals.com/ebay-canada-neweggcanada-10-off-all-newegg-items-their-ebay-use-code-picknewegg-ebay-app-2280867/','2019-04-30 17:49:28'),(29,'[Various Retailers] Gift Card Deals And Discounts (2019)',260,'2019-01-07 06:15:00','http://forums.redflagdeals.com/various-retailers-gift-card-deals-discounts-2019-2255585/','2019-04-30 17:49:28'),(31,'Costco East - GTA Clearance Items Ending in .97 - General Thread',245,'2017-11-24 01:23:00','http://forums.redflagdeals.com/east-gta-clearance-items-ending-97-general-thread-2146900/','2019-04-30 21:20:50'),(33,'[Samsung] Samsung Galaxy S10 up to $400 off w/ trade in (+ additional discounts too)',63,'2019-02-20 22:50:00','http://forums.redflagdeals.com/samsung-samsung-galaxy-s10-up-400-off-w-trade-additional-discounts-too-2266313/','2019-04-30 21:20:50'),(35,'American Express AMEX - Shop Small (Spring 2019) - Spend $5 Get $5 - Up To 5 Times = $25',105,'2019-03-01 10:18:00','http://forums.redflagdeals.com/american-express-amex-shop-small-spring-2019-spend-5-get-5-up-5-times-25-2268293/','2019-04-30 21:20:50'),(41,'[eBay.ca/amazon.ca] Wear24 Google WearOS 2.24 Smartwatch by Verizon from $45 (Certified Refurbished)',236,'2018-03-17 16:32:00','http://forums.redflagdeals.com/ebay-ca-amazon-ca-wear24-google-wearos-2-24-smartwatch-verizon-45-certified-refurbished-2179148/','2019-04-30 21:39:33'),(47,'[Public Mobile] Public Mobile $13 now includes UNLIMITED INCOMING CALLS',132,'2019-05-01 11:03:00','http://forums.redflagdeals.com/public-mobile-public-mobile-13-now-includes-unlimited-incoming-calls-2282235/','2019-05-03 03:32:13'),(48,'[Manulife] Manulife Bank HISA 182 days 3.25% [on new Advantage Account deposits] ***Updated April 30, 2019***',99,'2019-04-27 07:17:00','http://forums.redflagdeals.com/manulife-bank-hisa-182-days-3-25-new-advantage-account-deposits-updated-april-30-2019-2281288/','2019-05-03 03:32:13'),(55,'Rona Armor All pressure washer 1600psi/1.3gpm $79',35,'2019-05-02 13:50:00','http://forums.redflagdeals.com/rona-armor-all-pressure-washer-1600psi-1-3gpm-79-2282508/','2019-05-03 03:34:41'),(57,'Staples Samsung Galaxy Tab S5E + headphones - $414 after 10% instore coupon (YMMV)',38,'2019-05-01 17:00:00','http://forums.redflagdeals.com/staples-samsung-galaxy-tab-s5e-headphones-414-after-10-instore-coupon-ymmv-2282325/','2019-05-03 03:34:41'),(59,'Costco USA (April 17 - May 12th) Bellingham (380 pics)',31,'2019-05-01 16:30:00','http://forums.redflagdeals.com/costco-usa-april-17-may-12th-bellingham-380-pics-2282318/','2019-05-03 03:34:41'),(66,'[Fido] 3GB LTE Data Plan $15, BYOD, no contract',294,'2017-02-03 01:30:00','http://forums.redflagdeals.com/fido-3gb-lte-data-plan-15-byod-no-contract-2078212/','2019-05-03 16:31:48'),(68,'TD Bank TD First Class Travel Visa Infinite (80k WB + FYF)',76,'2019-03-01 13:49:00','http://forums.redflagdeals.com/td-bank-td-first-class-travel-visa-infinite-80k-wb-fyf-2268347/','2019-05-04 00:05:01'),(69,'[Giztop] Xiaomi Redmi Airdots US$23.99 *Pre Order*',61,'2019-04-02 14:09:00','http://forums.redflagdeals.com/giztop-xiaomi-redmi-airdots-us-23-99-pre-order-2276014/','2019-05-04 00:05:01');
/*!40000 ALTER TABLE `rdf_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-04  0:43:35
