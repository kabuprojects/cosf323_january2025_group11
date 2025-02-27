<?php
session_start();
$conn = new mysqli("localhost", "root", "password", "admin_db");

if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}

$email = $_POST['email'];
$password = $_POST['password'];

// Use prepared statements to prevent SQL injection
$sql = "SELECT * FROM admins WHERE email=?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $email);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    
    // Verify the entered password against the hashed password
    if (password_verify($password, $row['password'])) {
        $_SESSION['admin'] = $email;
        header("Location: dashboard.html");
        exit();
    } else {
        echo "<script>
                alert('Invalid email or password. Please try again.');
                window.location.href = 'index.html';
              </script>";
        exit();
    }
} else {
    echo "<script>
            alert('Invalid email or password. Please try again.');
            window.location.href = 'index.html';
          </script>";
    exit();
}

$stmt->close();
$conn->close();
?>

