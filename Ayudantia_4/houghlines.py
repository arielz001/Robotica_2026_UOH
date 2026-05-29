import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

# =========================
# LEER IMAGEN EN GRIS
# =========================
imagen = plt.imread("./imgs/road.jpg")
imagen = Image.fromarray(imagen).convert('L')
imagen = np.array(imagen).astype(np.uint8)

# =========================
# GAUSSIANO FUERTE
# =========================
gauss = cv2.GaussianBlur(imagen, (9, 9), 2.5)

# =========================
# CANNY
# =========================
edges_orig = cv2.Canny(imagen, 50, 150)
edges_gauss = cv2.Canny(gauss, 50, 150)

# =========================
# HOUGH LINES
# =========================
def hough_lines_img(edge_img, orig_img):
    img_hough = cv2.cvtColor(orig_img, cv2.COLOR_GRAY2BGR)
    lines = cv2.HoughLinesP(edge_img, rho=1, theta=np.pi/180,
                            threshold=80, minLineLength=50, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img_hough, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return img_hough

hough_orig = hough_lines_img(edges_orig, imagen)
hough_gauss = hough_lines_img(edges_gauss, gauss)

# =========================
# FIGURA 2x3
# =========================
fig, ax = plt.subplots(2, 3, figsize=(18, 10))

# Fila 1: original
ax[0,0].imshow(imagen, cmap='gray')
ax[0,0].set_title("Original")
ax[0,1].imshow(edges_orig, cmap='gray')
ax[0,1].set_title("Canny Original")
ax[0,2].imshow(hough_orig)
ax[0,2].set_title("Hough Original")

# Fila 2: blur gaussiano
ax[1,0].imshow(gauss, cmap='gray')
ax[1,0].set_title("Gaussian Blur")
ax[1,1].imshow(edges_gauss, cmap='gray')
ax[1,1].set_title("Canny Blur")
ax[1,2].imshow(hough_gauss)
ax[1,2].set_title("Hough Blur")

# Limpiar ejes
for i in range(2):
    for j in range(3):
        ax[i,j].axis('off')

plt.tight_layout()
plt.show()