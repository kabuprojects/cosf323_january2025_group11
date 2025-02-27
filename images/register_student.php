<?php
$servername = "localhost";
$username = "root"; 
$password = "password"; 
$dbname = "admin_db"; 

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'];
    $regno = $_POST['regno'];
    $email = $_POST['email'];
    $face_encoding = $_POST['face_encoding'];

    $sql = "INSERT INTO students (name, regno, email, face_encoding, created_at) 
            VALUES ('$name', '$regno', '$email', '$face_encoding', NOW())";

    if ($conn->query($sql) === TRUE) {
        echo "Student registered successfully!";
    } else {
        echo "Error: " . $conn->error;
    }
}

$conn->close();
?>
