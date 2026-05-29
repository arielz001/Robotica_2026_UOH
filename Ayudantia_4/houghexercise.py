import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# 1. CREAR UNA IMAGEN EN NEGRO (100x100) Y PUNTOS
# ==================================================
imagen = np.zeros((100, 100))
puntos = [(30, 30), (50, 50), (70, 70)]  # Diagonal a 45° que pasa por el origen

for (x, y) in puntos:
    imagen[y, x] = 255 

# ==================================================
# 2. CONFIGURAR EL ESPACIO DE HOUGH
# ==================================================
thetas = np.deg2rad(np.arange(-90.0, 90.0))
num_thetas = len(thetas)
diagonal = int(np.ceil(np.sqrt(imagen.shape[0]**2 + imagen.shape[1]**2)))
acumulador = np.zeros((2 * diagonal, num_thetas))

# ==================================================
# 3. VOTACIÓN EN EL ACUMULADOR
# ==================================================
for (x, y) in puntos:
    for t_idx in range(num_thetas):
        theta = thetas[t_idx]
        rho = x * np.cos(theta) + y * np.sin(theta)
        rho_idx = int(round(rho)) + diagonal
        acumulador[rho_idx, t_idx] += 1

# Encontrar el máximo (Sabemos que dará Theta = -45° y Rho = 0)
idx_maximo = np.unravel_index(np.argmax(acumulador), acumulador.shape)
rho_ganador = idx_maximo[0] - diagonal
theta_ganador = thetas[idx_maximo[1]]

# ==================================================
# 4. VISUALIZACIÓN ENRIQUECIDA CON ÁNGULOS
# ==================================================
fig, ax = plt.subplots(1, 2, figsize=(15, 7))

# --- PANEL 1: ESPACIO DE LA IMAGEN CON GEOMETRÍA ---
ax[0].imshow(imagen, cmap='gray', origin='lower')
ax[0].set_title("Geometría de la Línea y Vector de Hough", fontsize=12, fontweight='bold')
ax[0].set_xlabel("Eje X")
ax[0].set_ylabel("Eje Y")

# 1. Dibujar los puntos originales
for (x, y) in puntos:
    ax[0].plot(x, y, 'ro', markersize=8, zorder=5)

# 2. Dibujar la línea recta reconstruida (Cian) de extremo a extremo
x_vals = np.array([0, 99])
y_vals = x_vals  # Ya que pasa por el origen en diagonal perfecta
ax[0].plot(x_vals, y_vals, color='cyan', linewidth=2.5, label="Línea Recta Detectada (45°)")

# 3. Dibujar el Vector Normal de Hough (Flecha Roja)
# Nota: Como rho=0, para que se vea la dirección en la pizarra, simulamos una flecha
# que apunta en la dirección de theta_ganador (-45°) desde el origen.
dx = 25 * np.cos(theta_ganador)
dy = 25 * np.sin(theta_ganador)
ax[0].arrow(0, 0, dx, dy, head_width=3, head_length=3, fc='red', ec='red', linewidth=2, label=r'Vector Hough ($\theta$ = -45°)')

# 4. Dibujar el cuadradito de ángulo recto (90°) para demostrar perpendicularidad
ax[0].plot([0, 5], [0, -5], color='yellow', linestyle=':', linewidth=2)
ax[0].plot([5, 10], [-5, 0], color='yellow', linestyle=':', linewidth=2)
ax[0].plot([10, 5], [0, 5], color='yellow', linestyle=':', linewidth=2)

# 5. Textos e indicadores de los ángulos en el gráfico
ax[0].text(45, 55, r"Inclinación Línea = 45°", color='cyan', fontsize=11, fontweight='bold')
ax[0].text(22, -15, r"$\theta$ de Hough = -45°", color='red', fontsize=11, fontweight='bold')
ax[0].text(8, -2, r"90°", color='yellow', fontsize=10, fontweight='bold')

# Ajustes de visualización del Panel 1
ax[0].axhline(0, color='white', linewidth=0.5, linestyle='--')
ax[0].axvline(0, color='white', linewidth=0.5, linestyle='--')
ax[0].set_xlim(-20, 99)
ax[0].set_ylim(-20, 99)
ax[0].legend(loc='upper left')
ax[0].grid(True, alpha=0.2)

# --- PANEL 2: ESPACIO DE HOUGH (ACUMULADOR) ---
ax[1].imshow(
    acumulador, 
    cmap='hot', 
    extent=[-90, 90, -diagonal, diagonal], 
    aspect='auto',
    origin='lower'
)
ax[1].set_title("Espacio de Hough (Intersección de Curvas)", fontsize=12, fontweight='bold')
ax[1].set_xlabel("Ángulo Theta (grados)")
ax[1].set_ylabel("Distancia Rho (píxeles)")

# Pintar la cruz azul en el exacto (-45, 0)
ax[1].plot(np.rad2deg(theta_ganador), rho_ganador, 'cx', markersize=15, markeredgewidth=3)
ax[1].text(np.rad2deg(theta_ganador)+5, rho_ganador+5, f"Ganador\n(-45°, 0.0)\n3 Votos", color='cyan', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()