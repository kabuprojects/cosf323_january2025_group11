<?php
$servername = "localhost";
$username = "root"; 
$password = "password"; 
$database = "admin_db"; 

$conn = new mysqli($servername, $username, $password, $database);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT id, name, reg_number,email FROM students";
$result = $conn->query($sql);

$students = [];
while ($row = $result->fetch_assoc()) {
    $students[] = $row;
}

$conn->close();
echo json_encode($students);
?>