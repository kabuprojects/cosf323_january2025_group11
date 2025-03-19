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
    $sql = "DELETE FROM students WHERE id=$id";
    echo (mysqli_query($conn, $sql)) ? "Student deleted successfully!" : "Error deleting student.";
}
?>