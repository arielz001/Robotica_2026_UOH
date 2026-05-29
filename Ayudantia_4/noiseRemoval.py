import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

# =========================
# LEER IMAGEN EN GRIS
# =========================
imagen = plt.imread("./imgs/road3.jpg")
imagen = Image.fromarray(imagen).convert('L')
imagen = np.array(imagen)

# =========================
# AGREGAR RUIDO SAL Y PIMIENTA
# =========================
ruido = imagen.copy()

prob = 0.08
rand = np.random.rand(*imagen.shape)

ruido[rand < prob/2] = 0
ruido[rand > 1 - prob/2] = 255

# =========================
# GAUSSIANO FUERTE
# =========================
gauss = cv2.GaussianBlur(ruido, (9, 9), 2.5)

# =========================
# CANNY
# =========================
edges_original = cv2.Canny(imagen.astype(np.uint8), 50, 150)
edges_noisy = cv2.Canny(ruido.astype(np.uint8), 50, 150)
edges_gauss = cv2.Canny(gauss.astype(np.uint8), 50, 150)

# =========================
# FIGURA 2x3
# =========================
fig, ax = plt.subplots(2, 3, figsize=(15, 8))

# =========================
# FILA 1
# =========================
ax[0, 0].imshow(imagen, cmap='gray')
ax[0, 0].set_title("Original")

ax[0, 1].imshow(ruido, cmap='gray')
ax[0, 1].set_title("Con ruido")

ax[0, 2].imshow(gauss, cmap='gray')
ax[0, 2].set_title("Gaussian Blur")

# =========================
# FILA 2
# =========================
ax[1, 0].imshow(edges_original, cmap='gray')
ax[1, 0].set_title("Canny original")

ax[1, 1].imshow(edges_noisy, cmap='gray')
ax[1, 1].set_title("Canny con ruido")

ax[1, 2].imshow(edges_gauss, cmap='gray')
ax[1, 2].set_title("Gaussian + Canny")

# =========================
# LIMPIAR EJES
# =========================
for i in range(2):
    for j in range(3):
        ax[i, j].axis('off')

plt.tight_layout()
plt.show()