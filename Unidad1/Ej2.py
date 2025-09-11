import cv2
import numpy as np


def find_min_resolution(cam):
    """Find the minimum supported resolution for the camera"""
    print("=== BUSCANDO RESOLUCIÓN MÍNIMA ===")

    # Test common low resolutions
    test_resolutions = [
        (160, 120),
        (176, 144),
        (320, 240),
        (352, 288),
        (640, 480),
        (800, 600),
        (1024, 768),
    ]

    min_resolution = None

    for w, h in test_resolutions:
        # Try to set resolution
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

        # Check if setting was successful
        actual_w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if actual_w == w and actual_h == h:
            print(f"✓ {w}x{h} - Soportada")
            if min_resolution is None:
                min_resolution = (w, h)
        else:
            print(f"✗ {w}x{h} - No soportada (obtuvo {actual_w}x{actual_h})")

    if min_resolution:
        print(
            f"\n🎯 Resolución mínima encontrada: {min_resolution[0]}x{min_resolution[1]}"
        )
        # Set to minimum resolution
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, min_resolution[0])
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, min_resolution[1])
    else:
        print("⚠️ No se pudo determinar resolución mínima")

    print("=" * 40)
    return min_resolution


cam = cv2.VideoCapture(2)
if not cam.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

# Find minimum resolution
min_res = find_min_resolution(cam)

print("=== ANÁLISIS DE CÁMARA ===")
w, h = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(
    f"Resolución actual: {w}x{h} | FPS: {cam.get(cv2.CAP_PROP_FPS):.0f} | Backend: {cam.getBackendName()}"
)
if min_res:
    print(f"Resolución mínima: {min_res[0]}x{min_res[1]}")
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
