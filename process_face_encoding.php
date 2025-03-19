<?php
if (isset($_GET['regno'])) {
    $regno = $_GET['regno'];
    
    // Flask API URL
    $api_url = "http://127.0.0.1:5000/capture_face";
    
    // JSON payload
    $data = json_encode(array("regno" => $regno));

    // cURL to send request
    $ch = curl_init($api_url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: application/json"));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    // Status Message
    if ($http_code == 200) {
        $status_message = "<p class='text-green-600 font-bold text-lg'>Face encoding captured successfully!</p>";
    } else {
        $status_message = "<p class='text-red-600 font-bold text-lg'>Error: " . htmlspecialchars($response) . "</p>";
    }
} else {
    $status_message = "<p class='text-red-600 font-bold text-lg'>Error: Registration number not provided.</p>";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Face Encoding Status</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="flex items-center justify-center h-screen bg-gray-100">

    <div class="bg-white p-6 rounded-lg shadow-md w-96 text-center">
        <h2 class="text-2xl font-bold text-gray-700 mb-4">Face Encoding Status</h2>
        <?php echo $status_message; ?>
        <br>
        <a href="register2.html" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition">Go Back</a>
    </div>

</body>
</html>
