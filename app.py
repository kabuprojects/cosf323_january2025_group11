from flask import Flask, render_template, request, jsonify
import cv2
import face_recognition
import numpy as np
import mysql.connector

app = Flask(__name__)

# ✅ Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add your MySQL password if any
        database="face_recognition"
    )

# ✅ Home Page (Register)
@app.route('/')
def index():
    return render_template('register1.html')

# ✅ Capture Face and Store in Database
@app.route('/capture', methods=['POST'])
def capture():
    if 'name' not in request.form or 'registration_number' not in request.form or 'email' not in request.form:
        return jsonify({"error": "Missing required fields"}), 400

    name = request.form['name']
    reg_no = request.form['registration_number']
    email = request.form['email']

    # Open webcam
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    video_capture.release()

    if not ret:
        return jsonify({"error": "Failed to capture image"}), 500

    # Detect face
    face_locations = face_recognition.face_locations(frame)
    if face_locations:
        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
        encoding_str = ",".join(map(str, face_encoding))

        # Store in database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, registration_number, email, face_encoding) VALUES (%s, %s, %s, %s)",
                       (name, reg_no, email, encoding_str))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Face registered successfully!"})

    return jsonify({"error": "No face detected. Try again."}), 400

# ✅ Face Recognition (Login)
@app.route('/login', methods=['POST'])
def login():
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    video_capture.release()

    if not ret:
        return jsonify({"error": "Failed to capture image"}), 500

    # Detect face
    face_locations = face_recognition.face_locations(frame)
    if not face_locations:
        return jsonify({"error": "No face detected. Try again."}), 400

    face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

    # Fetch stored encodings from DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, face_encoding FROM students")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    for user in users:
        stored_name, stored_encoding_str = user
        stored_encoding = np.array([float(num) for num in stored_encoding_str.split(",")])

        # Compare captured face with stored encodings
        match = face_recognition.compare_faces([stored_encoding], face_encoding)[0]

        if match:
            return jsonify({"message": f"Welcome, {stored_name}!"})

    return jsonify({"error": "Face not recognized. Try again."}), 401

# ✅ Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
