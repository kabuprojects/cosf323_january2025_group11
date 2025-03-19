from flask import Flask, request, jsonify
import cv2
import face_recognition
import numpy as np
import mysql.connector
import os
import time

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="attendance_system_v2"
    )

@app.route('/capture_face', methods=['POST'])
def capture_face():
    regno = request.json.get('regno')
    if not regno:
        return jsonify({"error": "Registration number is required"}), 400

    print(f"Starting face capture for: {regno}")

    # Open webcam
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        return jsonify({"error": "Could not open webcam"}), 500

    print("Press 's' to capture face and exit.")

    start_time = time.time()
    timeout = 10

    frame = None
    while True:
        ret, frame = video_capture.read()
        if not ret:
            return jsonify({"error": "Failed to grab frame"}), 500

        cv2.putText(frame, "Press 's' to capture face", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

        cv2.imshow("Capture Face", frame)

        key = cv2.waitKey(1) & 0xFF
        if time.time() - start_time > timeout:
            print("Auto-closing due to timeout")
            break

        if key == ord('s'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    if frame is None:
        return jsonify({"error": "No frame captured"}), 500

    # Convert to RGB for face recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=face_locations)

    if len(face_encodings) > 0:
        encoding = face_encodings[0].tolist()
        encoding_str = ",".join(map(str, encoding))

        # Store in database
        try:
            db = get_db_connection()
            cursor = db.cursor()
            sql = "UPDATE students SET face_encoding=%s WHERE reg_number=%s"
            cursor.execute(sql, (encoding_str, regno))
            db.commit()
            cursor.close()
            db.close()
            return jsonify({"message": "Face encoding saved successfully!"}), 200

        except mysql.connector.Error as err:
            return jsonify({"error": f"Database update error: {err}"}), 500
    else:
        return jsonify({"error": "No face detected! Try adjusting lighting or moving closer."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
