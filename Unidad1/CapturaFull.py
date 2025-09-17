import cv2
from datetime import datetime

cap = cv2.VideoCapture(2)

if cap.isOpened():
    print("Logitech C922 Pro Stream - Full Control")
    print("Press 'q' to quit")
    print("Press 'SPACE' to capture photo")
    print("Use UP/DOWN arrows to adjust focus")
    print("Use LEFT/RIGHT arrows to adjust gain (ISO)")
    print("Use W/S keys to adjust exposure")
    print("Press 'r' to reset focus to auto")
    print("Press 'm' to toggle manual/auto exposure mode")

    # Enable manual focus mode
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # 0 = manual focus

    # Switch to manual exposure mode
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # 1 = manual mode

    # Get initial values
    current_focus = cap.get(cv2.CAP_PROP_FOCUS)
    current_gain = cap.get(cv2.CAP_PROP_GAIN)
    current_exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    print(f"Initial focus: {current_focus}")
    print(f"Initial gain: {current_gain}")
    print(f"Initial exposure: {current_exposure}")

    # Create fullscreen window (independent of camera resolution)
    window_name = "Logitech C922 - Full Control"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Create a clean copy for saving photos (without text)
        clean_frame = frame.copy()

        # Get current values
        current_focus = cap.get(cv2.CAP_PROP_FOCUS)
        current_gain = cap.get(cv2.CAP_PROP_GAIN)
        current_exposure = cap.get(cv2.CAP_PROP_EXPOSURE)

        # Display current values on screen overlay
        focus_text = f"Focus: {current_focus:.0f}"
        gain_text = f"Gain (ISO): {current_gain:.0f}"
        exposure_text = f"Exposure: {current_exposure:.0f}us"

        cv2.putText(
            frame, focus_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2
        )
        cv2.putText(
            frame, gain_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2
        )
        cv2.putText(
            frame,
            exposure_text,
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
        )

        # Display controls
        cv2.putText(
            frame,
            "UP/DOWN: Focus | LEFT/RIGHT: Gain | W/S: Exposure | SPACE: Capture | Q: Quit",
            (10, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 255, 0),
            1,
        )

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == 32:  # SPACE
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"foto_focus_{current_focus:.0f}_gain_{current_gain:.0f}_exp_{current_exposure:.0f}_{timestamp}.jpg"
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
        elif key == 81:  # LEFT arrow - decrease gain
            current_gain = max(0, current_gain - 1)
            cap.set(cv2.CAP_PROP_GAIN, current_gain)
            print(f"Gain: {current_gain}")
        elif key == 83:  # RIGHT arrow - increase gain
            current_gain = current_gain + 1
            cap.set(cv2.CAP_PROP_GAIN, current_gain)
            print(f"Gain: {current_gain}")
        elif key == ord("w"):  # W key - increase exposure
            current_exposure = current_exposure + 10
            cap.set(cv2.CAP_PROP_EXPOSURE, current_exposure)
            print(f"Exposure: {current_exposure}")
        elif key == ord("s"):  # S key - decrease exposure
            current_exposure = max(0, current_exposure - 10)
            cap.set(cv2.CAP_PROP_EXPOSURE, current_exposure)
            print(f"Exposure: {current_exposure}")
        elif key == ord("r"):  # Reset to auto focus
            cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            print("Focus reset to auto")
        elif key == ord("m"):  # Toggle manual/auto exposure
            current_mode = cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
            new_mode = 0 if current_mode == 1 else 1
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, new_mode)
            print(f"Exposure mode: {'manual' if new_mode == 1 else 'auto'}")

    cap.release()
    cv2.destroyAllWindows()
else:
    print("Camera not accessible")
