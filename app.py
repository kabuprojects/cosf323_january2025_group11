from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cv2
import face_recognition
import numpy as np
import mysql.connector
import time

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="attendance_system_v2"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Mark attendance
@app.route('/start_attendance', methods=['POST'])
def start_attendance():
    try:
        data = request.get_json()
        unit_code = data.get("unit")  # Get unit code from request

        if not unit_code:
            return jsonify({"error": "Unit code is required"}), 400

        print("Attendance process started...")  # Debug message

        # Open webcam
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            print("Error: Could not open webcam.")
            return jsonify({"error": "Could not open webcam"}), 500

        start_time = time.time()
        frame_captured = False
        frame = None

        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Error: Failed to grab frame from webcam.")
                return jsonify({"error": "Failed to grab frame"}), 500

            cv2.imshow("Attendance Capture", frame)
            key = cv2.waitKey(1) & 0xFF
            print(f"Key Pressed: {key}")  # Debugging key press

            if key == ord('s'):  # User presses 's' to capture
                print("Frame captured successfully!")
                frame_captured = True
                break

            if time.time() - start_time > 20:  # Allow 20 seconds before auto-closing
                print("Timeout reached")
                break

        video_capture.release()
        cv2.destroyAllWindows()

        if frame is None or not frame_captured:
            print("No frame captured from the webcam.")
            return jsonify({"error": "No frame captured"}), 500

        # Convert frame to RGB for face recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=face_locations)

        print(f"Number of faces detected: {len(face_locations)}")
        if len(face_encodings) == 0:
            print("No face encodings found in the captured frame.")
            return jsonify({"error": "No face detected! Please try again."}), 400

        # Get the encoding of the captured face
        captured_encodings = face_encodings

        # Fetch stored encodings from database
        db = get_db_connection()
        if db is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, face_encoding FROM students WHERE face_encoding IS NOT NULL")
        students = cursor.fetchall()

        if not students:
            print("No students with face encodings found in the database.")
            return jsonify({"error": "No students with face encodings found in the database."}), 400

        present_students = set()
        for captured_encoding in captured_encodings:
            for student in students:
                try:
                    stored_encoding = np.array(list(map(float, student['face_encoding'].split(','))))
                    match = face_recognition.compare_faces([stored_encoding], captured_encoding, tolerance=0.5)
                    if match[0]:  # If a match is found
                        present_students.add(student["id"])
                except Exception as e:
                    print(f"Error processing student {student['id']}: {e}")

        # Mark attendance
        all_student_ids = {student["id"] for student in students}
        absent_students = all_student_ids - present_students

        for student_id in present_students:
            cursor.execute("INSERT INTO attendance (student_id, status, timestamp, unit_code) VALUES (%s, %s, NOW(), %s)",
                           (student_id, "Present", unit_code))

        for student_id in absent_students:
            cursor.execute("INSERT INTO attendance (student_id, status, timestamp, unit_code) VALUES (%s, %s, NOW(), %s)",
                           (student_id, "Absent", unit_code))

        db.commit()
        cursor.close()
        db.close()

        print("Attendance process completed successfully.")  # Debug message
        return jsonify({
            "message": "Attendance process completed.",
            "present_students": list(present_students),
            "absent_students": list(absent_students)
        }), 200

    except Exception as e:
        print(f"Error in start_attendance: {e}")  # Log the error
        return jsonify({"error": "An error occurred while starting attendance."}), 500

# API to fetch attendance data for visualization
@app.route('/attendance_report', methods=['GET'])
def attendance_report():
    try:
        db = get_db_connection()
        if db is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.name, 
                a.status, 
                a.unit_code,
                COUNT(a.id) AS count 
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            GROUP BY s.name, a.status, a.unit_code
        """)
        attendance_data = cursor.fetchall()
        cursor.close()
        db.close()

        return jsonify(attendance_data)
    except Exception as e:
        print(f"Error in attendance_report: {e}")  # Log the error
        return jsonify({"error": "An error occurred while fetching attendance data."}), 500

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
