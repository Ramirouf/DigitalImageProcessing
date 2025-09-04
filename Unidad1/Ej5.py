import cv2
import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np


def plot_histogram(image_path):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image {image_path}")
        return

    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Original image
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis("off")

    # RGB histogram
    colors = ["red", "green", "blue"]
    for i, color in enumerate(colors):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        axes[0, 1].plot(hist, color=color, alpha=0.7)
    axes[0, 1].set_title("RGB Histogram")
    axes[0, 1].set_xlabel("Pixel Value")
    axes[0, 1].set_ylabel("Frequency")
    axes[0, 1].legend(["Red", "Green", "Blue"])

    # Grayscale histogram
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    axes[1, 0].imshow(gray, cmap="gray")
    axes[1, 0].set_title("Grayscale Image")
    axes[1, 0].axis("off")

    hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])
    axes[1, 1].plot(hist_gray, color="black")
    axes[1, 1].set_title("Grayscale Histogram")
    axes[1, 1].set_xlabel("Pixel Value")
    axes[1, 1].set_ylabel("Frequency")

    plt.tight_layout()
    plt.savefig("histogram.png", dpi=300, bbox_inches="tight")
    print("Histogram saved as 'histogram.png'")


if __name__ == "__main__":
    # Example usage - replace with your image path
    image_path = (
        "foto_focus_50_gain_69_exp_268_20250903_232322.jpg"  # Adjust path as needed
    )
    plot_histogram(image_path)
