CREATE TABLE Category (
                id INT AUTO_INCREMENT NOT NULL,
                level INT NOT NULL,
                name VARCHAR(100) NOT NULL,
                url_link VARCHAR(100),
                PRIMARY KEY (id)
);

CREATE TABLE Product (
                id INT AUTO_INCREMENT NOT NULL,
                name VARCHAR(100) NOT NULL,
                brands VARCHAR(100) NOT NULL,
                nutrition_grade VARCHAR(1) NOT NULL,
                url_link VARCHAR(100) NOT NULL,
                description VARCHAR(1000) NOT NULL,
                stores VARCHAR(100),
                PRIMARY KEY (id)
);

CREATE TABLE Favorite (
                product_id INT NOT NULL,
                substitute_id INT NOT NULL,
                PRIMARY KEY (product_id, substitute_id)
);

CREATE TABLE CategoryProduct (
                category_id INT NOT NULL,
                product_id INT NOT NULL,
                PRIMARY KEY (category_id, product_id)
);

-- constraint 1
ALTER TABLE CategoryProduct ADD CONSTRAINT category_category_product_fk
FOREIGN KEY (category_id)
REFERENCES Category (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
-- constraint 2
ALTER TABLE CategoryProduct ADD CONSTRAINT product_category_product_fk
FOREIGN KEY (product_id)
REFERENCES Product (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
-- constraint 3
ALTER TABLE Favorite ADD CONSTRAINT product_favorite_fk
FOREIGN KEY (product_id)
REFERENCES Product (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
-- constraint 4
ALTER TABLE Favorite ADD CONSTRAINT subsitute_favorite_fk
FOREIGN KEY (substitute_id)
REFERENCES Product (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;