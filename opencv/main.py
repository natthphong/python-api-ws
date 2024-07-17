import cv2
import numpy as np

eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("app cannot open your camera")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("cannot read frame ")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            eye_status = []

            for (ex, ey, ew, eh) in eyes:
                eye = roi_gray[ey:ey + eh, ex:ex + ew]
                eye_threshold = cv2.threshold(eye, 50, 255, cv2.THRESH_BINARY_INV)[1]
                eye_area = cv2.countNonZero(eye_threshold)
                eye_status.append(eye_area)

                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            print(f"eye_status {eye_status}")
            if len(eye_status) == 2 and (eye_status[0] == 0 or eye_status[1] == 0):
                cv2.putText(frame, "Blinking", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Blink Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
