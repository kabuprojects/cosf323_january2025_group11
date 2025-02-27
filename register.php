<?php
$conn = new mysqli("localhost", "root", "password", "admin_db");

if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}

// Get the email and password from the form
$email = $_POST['email'];
$password = $_POST['password'];

// Check if the email already exists
$sql_check = "SELECT * FROM admins WHERE email=?";
$stmt_check = $conn->prepare($sql_check);
$stmt_check->bind_param("s", $email);
$stmt_check->execute();
$result_check = $stmt_check->get_result();

if ($result_check->num_rows > 0) {
    echo "<script>
            alert('Email already exists! Please use a different one.');
            window.location.href = 'register.html';
          </script>";
    exit();
}

// Hash the password
$hashed_password = password_hash($password, PASSWORD_BCRYPT);

// Insert the admin into the database
$sql = "INSERT INTO admins (email, password) VALUES (?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $email, $hashed_password);

if ($stmt->execute()) {
    echo "<script>
            alert('Admin registered successfully!');
            window.location.href = 'index.html';
          </script>";
} else {
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
