-- CREATE TABLE user(
--     username VARCHAR(255) NOT NULL,
--     password VARCHAR(255) NOT NULL,
--     email VARCHAR(255) NOT NULL UNIQUE,
--     profile_img VARCHAR(255),
--     PRIMARY KEY(username)
-- );

CREATE TABLE uva_meals(
    meal_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    dining_hall VARCHAR(255) NOT NULL,
    meal_type VARCHAR(255) NOT NULL,
    meal_date DATE NOT NULL,
    meal_description TEXT,
    section VARCHAR(255),
    serving_size VARCHAR(255),
    calories INT,
    calories_from_fat INT,
    total_fat VARCHAR(255),
    saturated_fat VARCHAR(255),
    sugar VARCHAR(255),
    protein VARCHAR(255),
    dietary_fiber VARCHAR(255),
    total_carbohydrates VARCHAR(255),
    sodium VARCHAR(255),
    PRIMARY KEY(meal_id)
);