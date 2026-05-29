import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# =========================
# IMAGEN EN GRIS
# =========================
imagen = plt.imread("imgs/cat.jpg")
imagen = Image.fromarray(imagen).convert('L')
imagen = np.array(imagen).astype(float)

# =========================
# ZOOM 2x2
# =========================
y1, y2 = 398, 400
x1, x2 = 728, 730

zoom = imagen[y1:y2, x1:x2]
h, w = zoom.shape

# =========================
# KERNEL GAUSSIANO
# =========================
kernel = np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
], dtype=float) / 16

# =========================
# PADDING (ceros fuera del zoom)
# =========================
pad_img = np.pad(zoom, 1, mode='constant', constant_values=0)

# =========================
# CONVOLUCIÓN SOLO EN ZOOM
# =========================
result = np.zeros_like(zoom)

for i in range(h):
    for j in range(w):
        window = pad_img[i:i+3, j:j+3]
        result[i, j] = np.sum(window * kernel)

# =========================
# FIGURA 2x3 = 6 IMÁGENES
# =========================
fig, ax = plt.subplots(2, 3, figsize=(18, 10))

# ==================================================
# 1. IMAGEN ORIGINAL + ZOOM MARCADO
# ==================================================
ax[0,0].imshow(imagen, cmap='gray', vmin=0, vmax=255)
rect = plt.Rectangle((x1, y1), w, h, edgecolor='red', facecolor='none', linewidth=2)
ax[0,0].add_patch(rect)
ax[0,0].set_title("Imagen Original")

# ==================================================
# 2. IMAGEN FILTRADA + ZOOM MARCADO
# ==================================================
# aplicar mismo filtro a imagen completa para mostrar
from scipy.signal import convolve2d
filtered_full = convolve2d(imagen, kernel, mode='same', boundary='symm')

ax[0,1].imshow(filtered_full, cmap='gray', vmin=0, vmax=255)
rect2 = plt.Rectangle((x1, y1), w, h, edgecolor='red', facecolor='none', linewidth=2)
ax[0,1].add_patch(rect2)
ax[0,1].set_title("Imagen Filtrada")

# ==================================================
# 3. ZOOM ORIGINAL CON VALORES
# ==================================================
ax[0,2].imshow(zoom, cmap='gray', vmin=0, vmax=255)
ax[0,2].set_title("Zoom Original")

for i in range(h):
    for j in range(w):
        ax[0,2].text(j, i, str(int(zoom[i,j])), color='red',
                     ha='center', va='center', fontsize=18)

# ==================================================
# 4. ZOOM FILTRADO CON VALORES
# ==================================================
ax[1,0].imshow(result, cmap='gray', vmin=0, vmax=255)
ax[1,0].set_title("Zoom Filtrado")

for i in range(h):
    for j in range(w):
        ax[1,0].text(j, i, f"{int(result[i,j])}", color='red',
                     ha='center', va='center', fontsize=18)

# ==================================================
# 5. PADDING (ceros fuera)
# ==================================================
ax[1,1].imshow(pad_img, cmap='gray', vmin=0, vmax=255)
ax[1,1].set_title("Zoom con Padding (0)")

for i in range(pad_img.shape[0]):
    for j in range(pad_img.shape[1]):
        ax[1,1].text(j, i, str(int(pad_img[i,j])),
                     color='red', ha='center', va='center', fontsize=18)

# ==================================================
# 6. KERNEL
# ==================================================
ax[1,2].imshow(kernel, cmap='gray', vmin=0, vmax=1)
ax[1,2].set_title("Kernel Gaussiano")

for i in range(3):
    for j in range(3):
        ax[1,2].text(j, i, f"{int(kernel[i,j])}",
                     color='red', ha='center', va='center', fontsize=18)

# =========================
# LIMPIAR EJES
# =========================
for a in ax.flatten():
    a.axis('off')

plt.tight_layout()
plt.show()