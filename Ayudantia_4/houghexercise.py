import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# 1. CREAR UNA IMAGEN EN NEGRO (100x100) Y PUNTOS
# ==================================================
imagen = np.zeros((100, 100))
# Puntos de la diagonal inversa 
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

# ENCONTRAR EL MÁXIMO REAL DINÁMICAMENTE
idx_maximo = np.unravel_index(np.argmax(acumulador), acumulador.shape)
rho_ganador = idx_maximo[0] - diagonal
theta_ganador = thetas[idx_maximo[1]]

theta_deg = np.rad2deg(theta_ganador)
print(f"Ganador Real -> Theta: {theta_deg:.6f}°, Rho: {rho_ganador}")

# ==================================================
# 4. VISUALIZACIÓN CORREGIDA Y DINÁMICA
# ==================================================
fig, ax = plt.subplots(1, 2, figsize=(15, 7))

# --- PANEL 1: ESPACIO DE LA IMAGEN CON GEOMETRÍA REAL ---
ax[0].imshow(imagen, cmap='gray', origin='lower')
ax[0].set_title("Geometría de la Línea y Vector de Hough Real", fontsize=12, fontweight='bold')
ax[0].set_xlabel("Eje X")
ax[0].set_ylabel("Eje Y")

# 1. Dibujar los puntos originales
for (x, y) in puntos:
    ax[0].plot(x, y, 'ro', markersize=8, zorder=5)

# 2. DIBUJAR LA LÍNEA RECONSTRUIDA REAL (Cian)
# Usamos la ecuación de la recta derivada de Hough: y = (rho - x*cos(theta)) / sin(theta)
x_vals = np.array([-20, 99])
if np.sin(theta_ganador) != 0:
    y_vals = (rho_ganador - x_vals * np.cos(theta_ganador)) / np.sin(theta_ganador)
    ax[0].plot(x_vals, y_vals, color='cyan', linewidth=2.5, label=f"Línea Detectada ({theta_deg:.0f}°)")

# 3. DIBUJAR EL VECTOR NORMAL HOUGH REAL (Flecha Roja)
# El vector normal nace en (0,0) y termina perpendicular a la recta en (x_p, y_p)
x_p = rho_ganador * np.cos(theta_ganador)
y_p = rho_ganador * np.sin(theta_ganador)
ax[0].arrow(0, 0, x_p, y_p, head_width=3, head_length=3, fc='red', ec='red', linewidth=2, length_includes_head=True, label=f'Vector Rho ({rho_ganador:.1f} px)')

# 4. Dibujar símbolo geométrico de ángulo recto (90°) en la intersección
# Calculamos un pequeño desfase perpendicular para armar el cuadrado
size = 4
dx_linea = size * np.cos(theta_ganador + np.pi/2)
dy_linea = size * np.sin(theta_ganador + np.pi/2)
dx_vec = -size * np.cos(theta_ganador)
dy_vec = -size * np.sin(theta_ganador)

p1 = [x_p + dx_linea, y_p + dy_linea]
p2 = [x_p + dx_linea + dx_vec, y_p + dy_linea + dy_vec]
p3 = [x_p + dx_vec, y_p + dy_vec]

ax[0].plot([x_p, p1[0]], [y_p, p1[1]], color='yellow', linestyle=':', linewidth=2)
ax[0].plot([p1[0], p2[0]], [p1[1], p2[1]], color='yellow', linestyle=':', linewidth=2)
ax[0].plot([p2[0], p3[0]], [p2[1], p3[1]], color='yellow', linestyle=':', linewidth=2)

# 5. Textos dinámicos basados en la detección real
ax[0].text(35, 50, f"Inclinación Línea = {-theta_deg:.0f}°", color='cyan', fontsize=11, fontweight='bold')
ax[0].text(x_p/2 - 18, y_p/2 + 5, f"$\\theta$ = {theta_deg:.0f}°\n$\\rho$ = {rho_ganador:.1f}", color='red', fontsize=11, fontweight='bold')
ax[0].text(x_p - 4, y_p - 6, "90°", color='yellow', fontsize=10, fontweight='bold')

# Ajustes de visualización del Panel 1
ax[0].axhline(0, color='white', linewidth=0.5, linestyle='--')
ax[0].axvline(0, color='white', linewidth=0.5, linestyle='--')
ax[0].set_xlim(-20, 99)
ax[0].set_ylim(-20, 99)
ax[0].legend(loc='upper right')
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

# Pintar la cruz azul en el máximo real encontrado
ax[1].plot(theta_deg, rho_ganador, 'cx', markersize=15, markeredgewidth=3)
ax[1].text(theta_deg + 5, rho_ganador + 5, f"Ganador\n({theta_deg:.0f}°, {rho_ganador:.1f})\n3 Votos", color='cyan', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()
