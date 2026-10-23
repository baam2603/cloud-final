CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;
CREATE TABLE IF NOT EXISTS students(
  id INT PRIMARY KEY AUTO_INCREMENT,
  student_id VARCHAR(10),
  fullname VARCHAR(100),
  dob DATE,
  major VARCHAR(50)
);
INSERT INTO students(student_id, fullname, dob, major) VALUES
  ('SV001', 'Võ Gia Khang', '2006-7-15', 'Computer Science'),
  ('SV002', 'Đỗ Quang huy', '2006-10-18', 'Data Science'),
  ('SV003', 'Võ Văn Khôi Nguyên', '2006-05-17', 'Cybersecurity');
