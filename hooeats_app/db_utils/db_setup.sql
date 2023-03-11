CREATE TABLE user(
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    profile_img VARCHAR(255),
    PRIMARY KEY(username)
);