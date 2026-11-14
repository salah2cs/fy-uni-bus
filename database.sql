CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(20) UNIQUE NOT NULL,
  password VARCHAR(100) NOT NULL,
  college VARCHAR(100),
  route VARCHAR(50)
);

CREATE TABLE bookings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_name VARCHAR(100) NOT NULL,
  student_phone VARCHAR(20) NOT NULL,
  route VARCHAR(50) NOT NULL,
  trip_date DATE NOT NULL,
  trip_type VARCHAR(20) NOT NULL,
  transfer_number VARCHAR(50),
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);