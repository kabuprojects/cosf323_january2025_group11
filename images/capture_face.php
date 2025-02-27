<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capture Face</title>
</head>
<body>
    <h2>Capture Face</h2>
    <button onclick="startCapture()">Start Capture</button>
    <video id="video" width="640" height="480" autoplay></video>
    <button onclick="captureAndSend()">Save Face Encoding</button>
    
    <script>
        let video = document.getElementById('video');

        function startCapture() {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    video.srcObject = stream;
                })
                .catch(err => console.error("Error accessing webcam: ", err));
        }

        function captureAndSend() {
            fetch("process_face_encoding.php")
                .then(response => response.text())
                .then(data => {
                    alert(data);
                    window.location.href = "register2.html"; // Redirect after capture
                });
        }
    </script>
</body>
</html>
