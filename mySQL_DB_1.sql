SET NAMES utf8;

DROP DATABASE IF EXISTS openfoodfacts;

CREATE DATABASE openfoodfacts;

USE openfoodfacts;

CREATE TABLE Food(
	id INT UNSIGNED AUTO_INCREMENT,
	name VARCHAR(250) NOT NULL,
	category_id_1 VARCHAR(300) NOT NULL,
	category_id_2 VARCHAR(300),
	category_id_3 VARCHAR(300),
	category_id_4 VARCHAR(300),
	category_id_5 VARCHAR(300),
	nutri_score INT,
	stores VARCHAR(150),
	url VARCHAR(400),
	PRIMARY KEY(id)
	)ENGINE=InnoDB;

CREATE TABLE Categories(
	id VARCHAR(300) NOT NULL,
	name VARCHAR(200),
	PRIMARY KEY(id)
	)ENGINE=InnoDB;

CREATE TABLE Favorites(
	id INT UNSIGNED AUTO_INCREMENT,
	product_id INT UNSIGNED NOT NULL,
	substitute_id INT UNSIGNED NOT NULL,
	PRIMARY KEY(id)
	)ENGINE=InnoDB;


INSERT INTO Categories (id, name) VALUES ('None', ""); -- Need an id for empty categories because of the foreign key
SELECT * FROM Categories ORDER BY name;
ALTER TABLE Food ADD CONSTRAINT fk_categories_id_1_food FOREIGN KEY (category_id_1) REFERENCES Categories(id);
ALTER TABLE Food ADD CONSTRAINT fk_categories_id_2_food FOREIGN KEY (category_id_2) REFERENCES Categories(id);
ALTER TABLE Food ADD CONSTRAINT fk_categories_id_3_food FOREIGN KEY (category_id_3) REFERENCES Categories(id);
ALTER TABLE Food ADD CONSTRAINT fk_categories_id_4_food FOREIGN KEY (category_id_4) REFERENCES Categories(id);
ALTER TABLE Food ADD CONSTRAINT fk_categories_id_5_food FOREIGN KEY (category_id_5) REFERENCES Categories(id);
ALTER TABLE Favorites ADD CONSTRAINT fk_product_id_favorites FOREIGN KEY (product_id) REFERENCES Food(id);
ALTER TABLE Favorites ADD CONSTRAINT fk_substitute_id_favorites FOREIGN KEY (substitute_id) REFERENCES Food(id);

