import cv2
from playsound import playsound
import threading

# ✅ Load cascades (USE FULL PATH for safety)
face_cascade = cv2.CascadeClassifier(
    'C:/Users/Joy/Desktop/drowsiness-detector/haarcascade_frontalface_default.xml'
)
eye_cascade = cv2.CascadeClassifier(
    'C:/Users/Joy/Desktop/drowsiness-detector/haarcascade_eye.xml'
)

# ✅ Check if loaded properly
print("Face loaded:", not face_cascade.empty())
print("Eye loaded:", not eye_cascade.empty())

# ✅ Start camera (FIX for Windows)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Set resolution
cap.set(3, 640)
cap.set(4, 480)

score = 0
alarm_on = False

def play_alarm():
    playsound('C:/Users/Joy/Desktop/drowsiness-detector/alarm.wav')

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ Camera not working")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ✅ Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # ✅ Detect eyes
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # ✅ Drowsiness logic
        if len(eyes) == 0:
            score += 1
        else:
            score = 0
            alarm_on = False

        # ✅ Trigger alarm
        if score > 10:
            cv2.putText(frame, "DROWSY!", (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

            if not alarm_on:
                threading.Thread(target=play_alarm).start()
                alarm_on = True

    # ✅ Show output
    cv2.imshow("Driver Monitor", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()