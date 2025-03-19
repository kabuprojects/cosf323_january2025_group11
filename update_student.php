<?php
$servername = "localhost";
$username = "root"; 
$password = "password"; 
$dbname = "admin_db"; 

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("<div class='text-red-600 font-bold text-lg'>Connection failed: " . $conn->connect_error . "</div>");
}
$data = json_decode(file_get_contents("php://input"));

if (isset($data->id)) {
    $id = $data->id;
    $name = $data->name;
    $reg_number = $data->reg_number;
    $email = $data->email;

    $sql = "UPDATE students SET name='$name', reg_number='$reg_number', email='$email' WHERE id=$id";
    echo (mysqli_query($conn, $sql)) ? "Student updated successfully!" : "Error updating student.";
}
?>