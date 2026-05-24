import cv2
import face_recognition
import os
import numpy as np
import pandas as pd
from datetime import datetime

known_faces = []
known_names = []

dataset_path = "dataset"

# Load all saved images
for person_name in os.listdir(dataset_path):

    person_folder = os.path.join(dataset_path, person_name)

    for image_name in os.listdir(person_folder):

        image_path = os.path.join(person_folder, image_name)

        image = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:

            known_faces.append(encodings[0])
            known_names.append(person_name)

print("Faces Loaded Successfully!")

# Open webcam
video_capture = cv2.VideoCapture(0)

marked_names = []

while True:

    ret, frame = video_capture.read()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)

    face_encodings = face_recognition.face_encodings(
        rgb_frame,
        face_locations
    )

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = face_recognition.compare_faces(
            known_faces,
            face_encoding
        )

        name = "Unknown"

        face_distances = face_recognition.face_distance(
            known_faces,
            face_encoding
        )

        if len(face_distances) > 0:

            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_names[best_match_index]

                # Mark attendance once
                if name not in marked_names:

                    now = datetime.now()

                    current_time = now.strftime("%H:%M:%S")

                    attendance = pd.DataFrame({
                        "Name": [name],
                        "Time": [current_time]
                    })

                    attendance.to_csv(
                        "attendance.csv",
                        mode="a",
                        header=not os.path.exists("attendance.csv"),
                        index=False
                    )

                    marked_names.append(name)

                    print(f"Attendance marked for {name}")

        # Draw rectangle
        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

        # Show name
        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Recognition Attendance System", frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()