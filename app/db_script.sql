-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Position`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Position` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Position` (
  `Position` INT NOT NULL,
  `Chromosome` INT NOT NULL,
  `ID_position` INT NOT NULL,
  PRIMARY KEY (`ID_position`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Stats`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Stats` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Stats` (
  `ID_stats` INT NOT NULL,
  `REF` VARCHAR(50) NOT NULL,
  `ALT` VARCHAR(50) NOT NULL,
  `AF` INT NOT NULL,
  `Position_ID_position` INT NOT NULL,
  PRIMARY KEY (`ID_stats`, `Position_ID_position`),
  INDEX `fk_Stats_Position_idx` (`Position_ID_position` ASC) VISIBLE,
  CONSTRAINT `fk_Stats_Position`
    FOREIGN KEY (`Position_ID_position`)
    REFERENCES `mydb`.`Position` (`ID_position`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
