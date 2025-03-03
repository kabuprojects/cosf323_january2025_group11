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

# Load registered students' faces
cursor.execute("SELECT id, face_encoding FROM students")
students = cursor.fetchall()

known_face_encodings = []
known_student_ids = []

for student in students:
    student_id, encoding_str = student
    face_encoding = np.array(list(map(float, encoding_str.split(','))))
    known_face_encodings.append(face_encoding)
    known_student_ids.append(student_id)

# Start webcam for face detection
video_capture = cv2.VideoCapture(0)
print("Looking for faces...")

while True:
    ret, frame = video_capture.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if True in matches:
            matched_index = matches.index(True)
            student_id = known_student_ids[matched_index]

            # Mark attendance
            cursor.execute("UPDATE attendance SET status = 'Present' WHERE student_id = %s AND DATE(timestamp) = CURDATE()", (student_id,))
            conn.commit()
            print(f"Attendance marked for student ID: {student_id}")

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
conn.close()
