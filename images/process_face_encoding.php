<?php
$regno = $_GET['regno']; // Make sure to pass regno in the request

$command = escapeshellcmd("python capture_face.py $regno");
$output = shell_exec($command);

echo $output;
?>
