import cv2
from datetime import datetime

cap = cv2.VideoCapture(2)

if cap.isOpened():
    print("Logitech C922 Pro Stream - Focus Control")
    print("Press 'q' to quit")
    print("Press 'SPACE' to capture photo")
    print("Use UP/DOWN arrows to adjust focus")
    print("Press 'r' to reset focus to auto")

    # Enable manual focus mode
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # 0 = manual focus

    # Get initial focus value
    current_focus = cap.get(cv2.CAP_PROP_FOCUS)
    print(f"Initial focus: {current_focus}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Create a clean copy for saving photos (without text)
        clean_frame = frame.copy()

        # Display current focus value
        focus_text = f"Focus: {current_focus:.0f}"
        cv2.putText(
            frame, focus_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2
        )

        # Display controls
        cv2.putText(
            frame,
            "UP/DOWN: Focus | SPACE: Capture | Q: Quit",
            (10, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )

        cv2.imshow("Logitech C922 - Focus Control", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == 32:  # SPACE
            filename = f"foto_focus_{current_focus:.0f}.jpg"
            cv2.imwrite(filename, clean_frame)  # Save clean frame without text
            print(f"Photo saved: {filename}")
        elif key == 82:  # UP arrow - increase focus
            current_focus = min(255, current_focus + 5)
            cap.set(cv2.CAP_PROP_FOCUS, current_focus)
            print(f"Focus: {current_focus}")
        elif key == 84:  # DOWN arrow - decrease focus
            current_focus = max(0, current_focus - 5)
            cap.set(cv2.CAP_PROP_FOCUS, current_focus)
            print(f"Focus: {current_focus}")
        elif key == ord("r"):  # Reset to auto focus
            cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            print("Focus reset to auto")

    cap.release()
    cv2.destroyAllWindows()
else:
    print("Camera not accessible")
