-- Create the 'owner' table
CREATE TABLE owner
(
    owner_id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50)  NOT NULL,
    last_name  VARCHAR(50)  NOT NULL,
    phone      VARCHAR(15)  NOT NULL,
    email      VARCHAR(100) NOT NULL
);

-- Create the 'car' table
CREATE TABLE car
(
    car_id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    make     VARCHAR(20) NOT NULL,
    model    VARCHAR(20) NOT NULL,
    year     INT         NOT NULL,
    owner_id INT UNSIGNED,
    FOREIGN KEY (owner_id) REFERENCES owner (owner_id)
);

-- Create the 'employee' table
CREATE TABLE employee
(
    employee_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    hire_date   DATE        NOT NULL
);

-- Create the 'service' table
CREATE TABLE service
(
    service_id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    service_name        VARCHAR(50) NOT NULL,
    service_description TEXT
);

-- Create the 'repair' table
CREATE TABLE repair
(
    repair_id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    car_id      INT UNSIGNED NOT NULL,
    service_id  INT UNSIGNED NOT NULL,
    employee_id INT UNSIGNED NOT NULL,
    repair_date DATE         NOT NULL,
    FOREIGN KEY (car_id) REFERENCES car (car_id),
    FOREIGN KEY (service_id) REFERENCES service (service_id),
    FOREIGN KEY (employee_id) REFERENCES employee (employee_id)
);