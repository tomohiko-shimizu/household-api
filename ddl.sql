CREATE TABLE `revenue_category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
)
insert into revenue_category(category_name) VALUES('給与');
insert into revenue_category(category_name) VALUES('賞与');
insert into revenue_category(category_name) VALUES('売電');

CREATE TABLE revenue (
  id INT NOT NULL AUTO_INCREMENT,
  category_id INT DEFAULT NULL,
  price INT,
  date DATE,
  detail text,
  PRIMARY KEY (`id`),
  KEY category_id_index (category_id),
  FOREIGN KEY (category_id) REFERENCES `revenue_category` (`id`)
);

insert into revenue(category_id, price, date) VALUES(1, 300000, '2022-09-25');
insert into revenue(category_id, price, detail, date) VALUES(1, 300000, '交通費支給含む', '2022-09-25');
insert into revenue(category_id, price, date) VALUES(3, 25000, '2022-09-15');




CREATE TABLE expense (
  id INT NOT NULL AUTO_INCREMENT,
  category_detail_id INT DEFAULT NULL,
  price INT,
  date DATE,
  detail text,
  place text,
  PRIMARY KEY (`id`),
  KEY category_detail_index (category_detail_id),
  FOREIGN KEY (category_detail_id) REFERENCES expense_category_detail (id)
);