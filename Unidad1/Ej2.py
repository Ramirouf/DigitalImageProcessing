import cv2
import numpy as np

cam = cv2.VideoCapture(2)
if not cam.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

print("=== ANÁLISIS DE CÁMARA ===")
w, h = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(
    f"Resolución: {w}x{h} | FPS: {cam.get(cv2.CAP_PROP_FPS):.0f} | Backend: {cam.getBackendName()}"
)
print("=" * 30)
print("R: análisis | ESC: salir")

# Crear ventana una sola vez
cv2.namedWindow("Análisis de Cámara", cv2.WINDOW_NORMAL)


def analyze_frame(frame):
    h, w = frame.shape[:2]
    channels = frame.shape[2] if len(frame.shape) > 2 else 1
    print(f"Frame: {w}x{h} | Canales: {channels}")

    # Bit depth analysis
    dtype_str = str(frame.dtype)
    if "uint8" in dtype_str:
        bit_depth, max_val = 8, 255
    elif "uint16" in dtype_str:
        bit_depth, max_val = 16, 65535
    elif "uint32" in dtype_str:
        bit_depth, max_val = 32, 4294967295
    elif "float32" in dtype_str:
        bit_depth, max_val = 32, "Float (0.0-1.0)"
    elif "float64" in dtype_str:
        bit_depth, max_val = 64, "Double (0.0-1.0)"
    else:
        bit_depth, max_val = "Desconocido", "Desconocido"

    print(f"Bits: {bit_depth} | Max: {max_val} | Tipo: {frame.dtype}")

    # Value range analysis
    min_val, max_val = frame.min(), frame.max()
    unique_count = len(np.unique(frame))
    print(f"Rango: {min_val}-{max_val} | Valores únicos: {unique_count}")

    if frame.dtype == np.uint8 and unique_count > 256:
        print("⚠️ Posible profundidad > 8-bit")
    elif unique_count <= 20:
        print(f"Valores: {np.unique(frame)}")


while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: No se pudo recibir frame.")
        break

    cv2.imshow("Análisis de Cámara", frame)
    key = cv2.waitKey(1)

    if key == 27:  # ESC
        print("Saliendo...")
        break
    elif key == ord("r"):  # R
        analyze_frame(frame)

cam.release()
cv2.destroyAllWindows()
