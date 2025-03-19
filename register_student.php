<?php

$servername = "localhost";
$username = "root"; 
$password = ""; 
$dbname = "attendance_system_v2"; 

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

    $sql = "INSERT INTO students (name, reg_number, email, face_encoding, created_at) 
            VALUES ('$name', '$regno', '$email', '$face_encoding', NOW())";

///if ($conn->query($sql) === TRUE) {
    //echo "Student registered successfully! <br>";
    
    // Redirect user to the page where the "Capture Face" button was previously referring to
    //echo "<a href='capture_face.php?reg_number=$regno'>Click here to capture face</a>";
//} else {
    //echo "Error: " . $conn->error;
//}

if ($conn->query($sql) === TRUE) {
    echo "<p style='color: green;'>Student registered successfully!</p>";
    echo "<a href='process_face_encoding.php?regno=$regno' style='font-size: 18px; color: blue; text-decoration: underline;'>Click here to capture face encoding</a>";
} else {
    echo "<p style='color: red;'>Error: " . $conn->error . "</p>";
}
}

$conn->close();
?>
