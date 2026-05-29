import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

ARCHIVO_TXT = "rotations.txt"

# 1. CONFIGURACIÓN DE ESCALA PARA PROYECTOR (UOH)
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 13,
    'axes.titlesize': 15,
})

# Crear la ventana con proporciones grandes (12x6 pulgadas)
fig = plt.figure(figsize=(12, 6), dpi=110)

# Subplot 1 (Izquierda): Estructura Alámbrica 3D del Robot
ax_3d = fig.add_subplot(121, projection='3d')
linea_robot, = ax_3d.plot([], [], [], '-o', lw=4, markersize=8, color='darkgreen', label='Estructura')
ax_3d.set_xlim([-0.8, 0.8])
ax_3d.set_ylim([-0.8, 0.8])
ax_3d.set_zlim([0, 1.1])
ax_3d.set_title("Estructura 3D del Brazo (Instante Actual)", fontweight='bold')
ax_3d.set_xlabel("X")
ax_3d.set_ylabel("Y")
ax_3d.set_zlabel("Z")

# Subplot 2 (Derecha): Matriz de Rotación como Gráfico de Barras Dinámico
ax_bar = fig.add_subplot(122)
nombres_barras = ['R11 (Eje X)', 'R22 (Eje Y)', 'R33 (Eje Z)']
barras = ax_bar.bar(nombres_barras, np.zeros(3), color=['darkorange', 'purple', 'red'], edgecolor='black', lw=1.2)
ax_bar.set_ylim([-1.1, 1.1])
ax_bar.set_title("Diagonal de Matriz de Rotación (Pinza)", fontweight='bold')
ax_bar.set_ylabel("Valor Componente")
ax_bar.grid(axis='y', linestyle='--', alpha=0.7)

# Texto flotante para mostrar el tiempo exacto en pantalla
texto_tiempo = ax_bar.text(0.05, 0.95, '', transform=ax_bar.transAxes, fontsize=12, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8))

# 2. FUNCIÓN DE ACTUALIZACIÓN CONTINUA
def actualizar_dashboard(frame):
    if not os.path.exists(ARCHIVO_TXT):
        return linea_robot, *barras

    try:
        # Leer el TXT (saltando el encabezado). Al tener una sola línea, skiprows=1 nos da un vector plano
        datos = np.loadtxt(ARCHIVO_TXT, delimiter=',', skiprows=1)
        
        if datos.size == 0:
            return linea_robot, *barras

        # --- EXTRACCIÓN DE DATOS ---
        tiempo = datos[0]
        
        # Coordenadas 3D de los eslabones
        # Base= (0,0,0.1), J1= (col 1,2,3), J2= (col 4,5,6), Pinza= (col 7,8,9)
        x = [0.0, datos[1], datos[4], datos[7]]
        y = [0.0, datos[2], datos[5], datos[8]]
        z = [0.1, datos[3], datos[6], datos[9]]
        
        # Componentes de la matriz de rotación
        r11 = datos[10] # R11
        r22 = datos[14] # R22
        r33 = datos[18] # R33
        valores_matriz = [r11, r22, r33]

        # --- ACTUALIZAR ELEMENTOS GRÁFICOS ---
        # 1. Mover el brazo 3D
        linea_robot.set_data(x, y)
        linea_robot.set_3d_properties(z)
        
        # 2. Cambiar la altura de las barras en vivo
        for bar, val in zip(barras, valores_matriz):
            bar.set_height(val)
            
        # 3. Actualizar reloj digital
        texto_tiempo.set_text(f"Tiempo Sim: {tiempo:.2f} s")

    except Exception:
        # Si pilla el archivo justo a mitad de sobreescritura, ignora el frame para no caerse
        pass

    return linea_robot, *barras

# 3. ANIMACIÓN A 20 HZ (Cada 50ms igual que el arm.py)
ani = animation.FuncAnimation(fig, actualizar_dashboard, interval=50, blit=False, cache_frame_data=False)

plt.tight_layout()
plt.show()