<?php
$conn = new mysqli("localhost", "root", "", "admin_db");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$email = "admin@example.com";
$password = password_hash("admin123", PASSWORD_DEFAULT); // Hashing the password

$sql = "INSERT INTO admins (email, password) VALUES (?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $email, $password);

if ($stmt->execute()) {
    echo "Admin user created successfully!";
} else {
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
