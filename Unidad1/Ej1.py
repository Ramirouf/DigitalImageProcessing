import cv2

camara = cv2.VideoCapture(2)

# Verificar si la cámara se abrió correctamente
if not camara.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

# Opcional: Configurar la resolución de la cámara (ejemplo: 1280x720)
# camara.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Presione la tecla 'espacio' para capturar una foto.")
print("Presione la tecla 'esc' para salir sin capturar.")

while True:
    # Leer un frame (fotograma) desde la cámara
    ret, frame = camara.read()

    # Si la lectura del frame falla, salir del bucle
    if not ret:
        print("Error: No se pudo recibir un frame. Saliendo...")
        break

    # Mostrar el frame en una ventana
    cv2.imshow("Capturador de Fotos - TP1", frame)

    # Esperar por la presión de una tecla (1 milisegundo)
    tecla = cv2.waitKey(1)

    if tecla == 27:  # 27 es el código ASCII para la tecla 'esc'
        print("Saliendo sin guardar.")
        break
    elif tecla == 32:  # 32 es el código ASCII para la tecla 'espacio'
        # Definir un nombre para el archivo de imagen
        nombre_archivo = "foto_capturada_tp1.jpg"
        # Guardar la imagen en el disco
        cv2.imwrite(nombre_archivo, frame)
        print(f"¡Foto guardada como {nombre_archivo}!")
        break

# Liberar la cámara y cerrar todas las ventanas abiertas por OpenCV
camara.release()
cv2.destroyAllWindows()
