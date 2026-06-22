import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

INPUT_PATH = "parking.jpg"
OUTPUT_PATH = "output/result.png"

os.makedirs("output", exist_ok=True)

def count_vehicles(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Gambar tidak ditemukan!")
        return
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_result = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 5)

    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 35))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open)

    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    morph = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_close)

    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    valid_count = 0
    for c in contours:
        area = cv2.contourArea(c)
        
        if 14000 < area < 60000:
            x, y, w, h = cv2.boundingRect(c)
            aspect_ratio = w / float(h)

            if 0.5 < aspect_ratio < 3.5:
                valid_count += 1
                cv2.rectangle(img_result, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(OUTPUT_PATH, img_result)
    print(f"Total Mobil Terdeteksi: {valid_count}")

    plt.figure(figsize=(16, 10))
    
    plt.subplot(2, 2, 1)
    plt.imshow(img_rgb)
    plt.title("1. Citra Asli")
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(thresh, cmap='gray')
    plt.title("2. Adaptive Threshold (Block 31)")
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(morph, cmap='gray')
    plt.title("3. Open 35x35 & Close 25x25")
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB))
    plt.title(f"4. Hasil Akhir: {valid_count} Mobil")
    plt.axis('off')

    plt.tight_layout()
    plt.savefig("output/steps_visualization.png")
    plt.show()

    return valid_count

if __name__ == "__main__":
    count_vehicles(INPUT_PATH)