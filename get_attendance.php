<?php
header('Content-Type: application/json');

// Database Connection
$host = "localhost";
$user = "root"; // Change if needed
$pass = ""; // Change if needed
$dbname = "attendance_system_v2";

$conn = new mysqli($host, $user, $pass, $dbname);

if ($conn->connect_error) {
    die(json_encode(["error" => "Connection failed: " . $conn->connect_error]));
}

// Query for attendance stats
$sql = "
    SELECT 
        SUM(status = 'Present') AS present, 
        SUM(status = 'Absent') AS absent, 
        SUM(status = 'Late') AS late 
    FROM attendance";
$result = $conn->query($sql);
$row = $result->fetch_assoc();

// Query for weekly attendance
$sql_weekly = "
    SELECT 
        WEEK(timestamp) AS week, 
        COUNT(*) AS total
    FROM attendance
    WHERE status = 'Present'
    GROUP BY week
    ORDER BY week";
$result_weekly = $conn->query($sql_weekly);

$weekly_data = [];
while ($row_week = $result_weekly->fetch_assoc()) {
    $weekly_data[] = $row_week['total'];
}

// Return JSON response
echo json_encode([
    "present" => (int)$row['present'],
    "absent" => (int)$row['absent'],
    "late" => (int)$row['late'],
    "weeklyAttendance" => $weekly_data
]);

$conn->close();
?>
