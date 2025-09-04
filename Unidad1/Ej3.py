import cv2
import os
from datetime import datetime

cap = cv2.VideoCapture(2)
if cap.isOpened():
    print("Camera opened successfully. Press 'q' to quit.")
    print("Press 'm' to toggle manual/auto mode")
    print("Press 'up/down' arrows to adjust exposure")
    print("Press 'left/right' arrows to adjust gain")
    print("Press 'SPACE' to capture photo")

    # Switch to manual mode
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # 1 = manual mode

    # Photo counter for unique filenames
    photo_counter = 1

    # Try different camera properties for ISO
    iso_props = [
        cv2.CAP_PROP_ISO_SPEED,
        cv2.CAP_PROP_AUTO_EXPOSURE,
        cv2.CAP_PROP_EXPOSURE,
        cv2.CAP_PROP_BRIGHTNESS,
        cv2.CAP_PROP_CONTRAST,
        cv2.CAP_PROP_GAIN,
    ]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Get current gain (ISO equivalent)
        current_gain = cap.get(cv2.CAP_PROP_GAIN)
        current_exposure = cap.get(cv2.CAP_PROP_EXPOSURE)

        # Display current ISO info prominently at the top
        iso_text = f"Current ISO (Gain): {current_gain:.0f} | Exposure: {current_exposure:.0f}us"
        cv2.putText(
            frame,
            iso_text,
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            1,
        )

        # Try multiple properties to get camera info
        camera_info = []
        for prop in iso_props:
            value = cap.get(prop)
            if value != -1:
                camera_info.append(f"{prop}: {value:.2f}")

        # Display available camera properties
        y_pos = 50
        for info in camera_info:
            cv2.putText(
                frame, info, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1
            )
            y_pos += 20

        # Show frame
        cv2.imshow("Camera with ISO Display", frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("m"):
            # Toggle between manual and auto
            current_mode = cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
            new_mode = 0 if current_mode == 1 else 1
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, new_mode)
            print(f"Switched to {'manual' if new_mode == 1 else 'auto'} mode")
        elif key == 32:  # SPACE key - capture photo
            # Create unique filename with ISO and timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = (
                f"photo_{photo_counter:03d}_ISO{current_gain:.0f}_{timestamp}.jpg"
            )

            # Save photo
            success = cv2.imwrite(filename, frame)
            if success:
                print(f"Photo saved: {filename}")
                photo_counter += 1
            else:
                print(f"Failed to save photo: {filename}")
        elif key == 82:  # Up arrow - increase exposure
            current_exp = cap.get(cv2.CAP_PROP_EXPOSURE)
            cap.set(cv2.CAP_PROP_EXPOSURE, current_exp + 10)
        elif key == 84:  # Down arrow - decrease exposure
            current_exp = cap.get(cv2.CAP_PROP_EXPOSURE)
            cap.set(cv2.CAP_PROP_EXPOSURE, max(0, current_exp - 10))
        elif key == 81:  # Left arrow - decrease gain
            current_gain = cap.get(cv2.CAP_PROP_GAIN)
            cap.set(cv2.CAP_PROP_GAIN, max(0, current_gain - 1))
        elif key == 83:  # Right arrow - increase gain
            current_gain = cap.get(cv2.CAP_PROP_GAIN)
            cap.set(cv2.CAP_PROP_GAIN, current_gain + 1)

    cap.release()
    cv2.destroyAllWindows()
else:
    print("Camera not accessible")
