import cv2
import os

# Ask student name
name = input("Enter student name: ")

# Create folder
path = os.path.join("dataset", name)

if not os.path.exists(path):
    os.makedirs(path)

# Open webcam
cap = cv2.VideoCapture(0)

count = 0

print("Press 's' to save image")
print("Press 'q' to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to access webcam")
        break

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1)

    # Press S to save image
    if key == ord('s'):

        img_path = os.path.join(path, f"{count}.jpg")

        cv2.imwrite(img_path, frame)

        print(f"Saved: {img_path}")

        count += 1

    # Press Q to quit
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()