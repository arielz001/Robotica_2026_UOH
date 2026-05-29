import mujoco
import mujoco.viewer
import time
import numpy as np

# 1. Cargar el modelo XML estable
modelo = mujoco.MjModel.from_xml_path('robot_2ejes.xml')
datos = mujoco.MjData(modelo)

# --- CONFIGURACIÓN DE TELEMETRÍA ---
ARCHIVO_TXT = "rotations.txt"
INTERVALO_REGISTRO = 0.05  
proximo_registro = 0.0

estado = {
    'fase1': False,
    'fase2': False,
    'fase3': False
}

def imprimir_matrices_bucle(nombre_fase, data):
    print(f"\n========================================================")
    print(f" TELEMETRÍA: {nombre_fase.upper()}")
    print(f"========================================================")
    R_base_pinza = data.body('pinza').xmat.reshape(3, 3)
    pos_pinza = data.body('pinza').xpos
    print(f"-> Ángulos: J1 (Hombro Z) = {np.rad2deg(data.joint('j1').qpos[0]):.1f}°, J2 (Codo Y) = {np.rad2deg(data.joint('j2').qpos[0]):.1f}°")
    print(f"-> Posición Pinza: X={pos_pinza[0]:.2f}, Y={pos_pinza[1]:.2f}, Z={pos_pinza[2]:.2f}")
    print("-> Matriz R_base_pinza:")
    print(np.round(R_base_pinza, 2))

# 2. Función de control (El nuevo bucle solicitado)
def controller(model, data):
    global proximo_registro
    tiempo_simulacion = data.time
    
    # --- LOG DE DATOS PARA MATPLOTLIB ---
    if tiempo_simulacion >= proximo_registro:
        pos_j1 = data.body('eslabon1').xpos
        pos_j2 = data.body('eslabon2').xpos
        pos_pinza = data.body('pinza').xpos
        R_flat = data.body('pinza').xmat.flatten()
        
        cabecera = "tiempo,j1_x,j1_y,j1_z,j2_x,j2_y,j2_z,p_x,p_y,p_z,R11,R12,R13,R21,R22,R23,R31,R32,R33\n"
        linea_datos = [
            f"{tiempo_simulacion:.3f}",
            f"{pos_j1[0]:.4f}", f"{pos_j1[1]:.4f}", f"{pos_j1[2]:.4f}",
            f"{pos_j2[0]:.4f}", f"{pos_j2[1]:.4f}", f"{pos_j2[2]:.4f}",
            f"{pos_pinza[0]:.4f}", f"{pos_pinza[1]:.4f}", f"{pos_pinza[2]:.4f}"
        ]
        linea_datos.extend([f"{val:.4f}" for val in R_flat])
        
        with open(ARCHIVO_TXT, "w") as f:
            f.write(cabecera)
            f.write(",".join(linea_datos) + "\n")
            
        proximo_registro += INTERVALO_REGISTRO
    
    # --- EL BUCLE PEDIDO (CICLO DE 8 SEGUNDOS) ---
    
    # PASO 1: ANORMALIDAD / NORMALIDAD INICIAL (0s a 2s) -> Todo vertical en 0°
    if tiempo_simulacion < 2.0:
        data.actuator('servo_j1').ctrl[0] = np.deg2rad(0.0)
        data.actuator('servo_j2').ctrl[0] = np.deg2rad(0.0)
        
        if tiempo_simulacion > 1.0 and not estado['fase1']:
            imprimir_matrices_bucle("Normalidad Inicial (0°, 0°)", data)
            estado['fase1'] = True
            
    # PASO 2: PRIMERO ROTA EL J2 90 GRADOS (2s a 4s) -> Hombro 0°, Codo se dobla 90°
    elif tiempo_simulacion < 4.0:
        data.actuator('servo_j1').ctrl[0] = np.deg2rad(0.0)
        data.actuator('servo_j2').ctrl[0] = np.deg2rad(90.0) # <--- Codo primero
        
        if tiempo_simulacion > 3.0 and not estado['fase2']:
            imprimir_matrices_bucle("Codo J2 rotado a 90°", data)
            estado['fase2'] = True
            
    # PASO 3: LUEGO ROTA EL Z DEL J1 90 GRADOS (4s a 6s) -> Hombro gira 90°, Codo mantiene 90°
    elif tiempo_simulacion < 6.0:
        data.actuator('servo_j1').ctrl[0] = np.deg2rad(90.0) # <--- Hombro después
        data.actuator('servo_j2').ctrl[0] = np.deg2rad(90.0)
        
        if tiempo_simulacion > 5.0 and not estado['fase3']:
            imprimir_matrices_bucle("Hombro J1 rotado a 90° en Z", data)
            estado['fase3'] = True
            
    # PASO 4: VUELVE A LA NORMALIDAD (6s a 8s) -> Todo regresa a 0° para reiniciar
    elif tiempo_simulacion < 40.0:
        data.actuator('servo_j1').ctrl[0] = np.deg2rad(0.0)
        data.actuator('servo_j2').ctrl[0] = np.deg2rad(0.0)
        
    else:
        mujoco.mj_resetData(model, data)
        proximo_registro = 0.0
        for clave in estado:
            estado[clave] = False
        print("\n--> [BUCLE] Volviendo a la normalidad. Reiniciando secuencia...")

mujoco.set_mjcb_control(controller)

print("Corriendo el bucle solicitado en tiempo real...")
with mujoco.viewer.launch_passive(modelo, datos) as visor:
    while visor.is_running():
        tiempo_inicio_paso = time.time()
        mujoco.mj_step(modelo, datos)
        visor.sync()
        
        tiempo_computo = time.time() - tiempo_inicio_paso
        tiempo_espera = modelo.opt.timestep - tiempo_computo
        if tiempo_espera > 0:
            time.sleep(tiempo_espera)