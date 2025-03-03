import cv2
import face_recognition
import mysql.connector
import numpy as np

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="attendance_system"
)
cursor = conn.cursor()

# Capture student's face
video_capture = cv2.VideoCapture(0)
print("Press 's' to capture and register face.")

while True:
    ret, frame = video_capture.read()
    cv2.imshow("Face Registration", frame)

    # Press 's' to save the face
    if cv2.waitKey(1) & 0xFF == ord('s'):
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
            encoding_str = ",".join(map(str, face_encoding))

            # Save the face encoding in MySQL (change 'John Doe' & 'REG123' as needed)
            cursor.execute("INSERT INTO students (name, registration_number, email, face_encoding) VALUES (%s, %s, %s, %s)",
                           ("John Doe", "REG123", "johndoe@email.com", encoding_str))
            conn.commit()
            print("Face registered successfully!")
            break

video_capture.release()
cv2.destroyAllWindows()
conn.close()
