<?php
$plain_password = "12345";
$hashed_password_from_db = '$2y$10$K9lko8knX2zOtE8zO5.p1OqQC1qiM3VMvlkSB0LXiLaNDxUywP.Xi';

if (password_verify($plain_password, $hashed_password_from_db)) {
    echo "Password is correct!";
} else {
    echo "Invalid password!";
}
?>
