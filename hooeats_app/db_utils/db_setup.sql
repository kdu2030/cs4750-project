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
    section VARCHAR(255) NOT NULL,
    meal_type VARCHAR(255) NOT NULL,
    meal_date DATE NOT NULL,
    PRIMARY KEY (meal_id),
    FOREIGN KEY (title, dining_hall, section) REFERENCES uva_descriptions(title, dining_hall, section)
);

CREATE TABLE uva_descriptions(
    title VARCHAR(255) NOT NULL,
    dining_hall VARCHAR(255) NOT NULL,
    section VARCHAR(255) NOT NULL,
    serving_size VARCHAR(255),
    calories DOUBLE,
    calories_from_fat DOUBLE,
    total_fat DOUBLE,
    saturated_fat DOUBLE,
    sugar DOUBLE,
    protein DOUBLE,
    dietary_fiber DOUBLE,
    total_carbohydrates DOUBLE,
    sodium DOUBLE,
    PRIMARY KEY (title, dining_hall, section)
);



CREATE TABLE uva_meals(
    meal_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    dining_hall VARCHAR(255) NOT NULL,
    meal_type VARCHAR(255) NOT NULL,
    meal_date DATE NOT NULL,
    meal_description TEXT,
    section VARCHAR(255),
    serving_size VARCHAR(255),
    calories DOUBLE,
    calories_from_fat DOUBLE,
    total_fat DOUBLE,
    saturated_fat DOUBLE,
    sugar DOUBLE,
    protein DOUBLE,
    dietary_fiber DOUBLE,
    total_carbohydrates DOUBLE,
    sodium DOUBLE,
    PRIMARY KEY(meal_id)
);


CREATE TABLE recipe_ingredients(
    recipe_id INT NOT NULL,
    ingredient VARCHAR(255) NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipe.recipe_id,
    PRIMARY KEY (recipe_id, ingredient)
);

-- CREATE TABLE recipe_tags(
--     recipe_id INT NOT NULL,
--     tag VARCHAR(255) NOT NULL,
--     FOREIGN KEY (recipe_id) REFERENCES recipe.recipe_id,
--     PRIMARY KEY (recipe_id, tag)
-- );

-- CREATE TABLE meal_plan(
--     username VARCHAR(255) NOT NULL,
--     plan_id INT NOT NULL AUTO_INCREMENT,
--     plan_name VARCHAR(255),
--     week_start DATE,
--     FOREIGN KEY (username) REFERENCES user.username,
--     PRIMARY KEY (username, plan_Id)
-- );