import cv2
import face_recognition
import numpy as np
import sys
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="admin_db"
)
cursor = db.cursor()

# Open webcam
video_capture = cv2.VideoCapture(0)
ret, frame = video_capture.read()
video_capture.release()

if not ret:
    print("Failed to capture image")
    sys.exit(1)

# Process face encoding
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
face_encodings = face_recognition.face_encodings(rgb_frame)

if len(face_encodings) > 0:
    encoding = face_encodings[0].tolist()  # Convert encoding to list for storage
    regno = sys.argv[1]  # Registration number from command-line argument

    # Convert encoding list to string for storage
    encoding_str = ",".join(map(str, encoding))

    sql = "UPDATE students SET face_encoding=%s WHERE regno=%s"
    cursor.execute(sql, (encoding_str, regno))
    db.commit()

    print("Face encoding saved successfully!")

else:
    print("No face detected!")

cursor.close()
db.close()
