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

    //var_dump($password);
//var_dump($row['password']);
//exit();
    
    // Verify the entered password against the hashed password
    if (password_verify($password, $row['password'])) {
        $_SESSION['admin'] = $email;
        echo "success";
        exit();
    } else {
        echo "<script>
                alert('Invalid email or password. Please try again.');
                window.location.href = 'index.html';
              </script>";
        exit();
    }
} 

$stmt->close();
$conn->close();
?>

