-- Create the 'owner' table
CREATE TABLE owner (
    owner_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Create the 'car' table
CREATE TABLE car (
    car_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(20) NOT NULL,
    model VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    owner_id INT UNSIGNED,
    FOREIGN KEY (owner_id) REFERENCES owner(owner_id)
);

-- Create the 'employee' table
CREATE TABLE employee (
    employee_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    hire_date DATE NOT NULL
);

-- Create the 'service' table
CREATE TABLE service (
    service_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(20) NOT NULL,
    service_description TEXT
);

-- Create the 'repair' table
CREATE TABLE repair (
    repair_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    car_id INT UNSIGNED NOT NULL,
    service_id INT UNSIGNED NOT NULL,
    employee_id INT UNSIGNED NOT NULL,
    repair_date DATE NOT NULL,
    FOREIGN KEY (car_id) REFERENCES car(car_id),
    FOREIGN KEY (service_id) REFERENCES service(service_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- Insert sample records into the 'owner' table
INSERT INTO owner (first_name, last_name, phone, email) VALUES
('John', 'Doe', '555-1234', 'john.doe@example.com'),
('Jane', 'Smith', '555-5678', 'jane.smith@example.com');

-- Insert sample records into the 'car' table
INSERT INTO car (make, model, year, owner_id) VALUES
('Toyota', 'Camry', 2010, 1),
('Honda', 'Civic', 2012, 2),
('Ford', 'Mustang', 2015, 1);

-- Insert sample records into the 'employee' table
INSERT INTO employee (first_name, last_name, hire_date) VALUES
('Michael', 'Brown', '2020-01-10'),
('Emily', 'Johnson', '2021-03-15');

-- Insert sample records into the 'service' table
INSERT INTO service (service_name, service_description) VALUES
('Oil Change', 'Engine oil change and filter replacement'),
('Brake Inspection', 'Inspect and adjust brake components'),
('Tire Rotation', 'Rotate tires to ensure even wear');

-- Insert sample records into the 'repair' table
INSERT INTO repair (car_id, service_id, employee_id, repair_date) VALUES
(1, 1, 1, '2022-01-20'),
(2, 2, 1, '2022-02-10'),
(3, 3, 2, '2022-02-15');
