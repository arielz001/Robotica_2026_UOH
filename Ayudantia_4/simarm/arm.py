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

# Control de impresiones en consola para cada etapa de la rutina
estado = {
    'home': False,
    'bajar_pick': False,
    'levantar': False,
    'rotar': False,
    'bajar_place': False
}

def imprimir_etapa(nombre_etapa, data):
    pos_pinza = data.body('pinza').xpos
    print(f"\n========================================================")
    print(f" ETAPA: {nombre_etapa.upper()}")
    print(f"========================================================")
    print(f"-> Ángulos actuales: J1 (Hombro)={np.rad2deg(data.joint('j1').qpos[0]):.1f}°, J2 (Codo)={np.rad2deg(data.joint('j2').qpos[0]):.1f}°")
    print(f"-> Coordenadas Pinza: X={pos_pinza[0]:.3f}, Y={pos_pinza[1]:.3f}, Z={pos_pinza[2]:.3f}")

# 2. Función de control (Rutina de 5 Pasos)
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
    
    # --- RUTINA DE MOVIMIENTO REAL (CICLO DE 12 SEGUNDOS) ---
    
    # PASO 1: PARTIDA / ESPERA (0s a 2s) -> Todo vertical en Home
    if tiempo_simulacion < 2.0:
        data.actuator('servo_j1').ctrl[0] = np.deg2rad(0.0)
        data.actuator('servo_j2').ctrl[0] = np.deg2rad(0.0)
        
        if tiempo_simulacion > 1.0 and not estado['home']:
            imprimir_etapa("Home (Espera)", data)
            estado['home'] = True
            
    # PASO 2: BAJAR AL SUELO A BUSCAR ALGO (2s a 4s) -> Hombro 0°, Codo baja a 90° (Pick)
    elif tiempo_simulacion < 4.0:
        data.actuator('servo_j1').ctrl[0] = np.deg2rad(0.0)
        data.actuator('servo_j2').ctrl[0] = np.deg2rad(90.0) # El codo se dobla por completo hacia el piso
        
        if tiempo_simulacion > 3.0 and not estado['bajar_pick']:
            imprimir_etapa("Bajando al suelo (Pick)", data)
            estado['bajar_pick'] = True
            
    # PASO 3: LEVANTAR EL OBJETO (4s a 6s) -> Hombro 0°, Codo sube a 30° (Seguridad)
    elif tiempo_simulacion < 6.0:
        data.actuator('servo_j1').ctrl[0] = np.deg2rad(0.0)
        data.actuator('servo_j2').ctrl[0] = np.deg2rad(30.0) # Retrae el brazo para no chocar al rotar
        
        if tiempo_simulacion > 5.0 and not estado['levantar']:
            imprimir_etapa("Levantando del suelo", data)
            estado['levantar'] = True
            
    # PASO 4: ROTAR EL HOMBRO (6s a 8s) -> Hombro gira -90° (al otro lado), Codo mantiene 30°
    elif tiempo_simulacion < 8.0:
        data.actuator('servo_j1').ctrl[0] = np.deg2rad(-90.0) # Gira horizontalmente hacia el destino
        data.actuator('servo_j2').ctrl[0] = np.deg2rad(30.0)
        
        if tiempo_simulacion > 7.0 and not estado['rotar']:
            imprimir_etapa("Rotando Hombro (J1 a -90°)", data)
            estado['rotar'] = True
            
    # PASO 5: BAJAR AL SUELO OTRA VEZ (8s a 10s) -> Hombro se queda en -90°, Codo baja a 90° (Place)
    elif tiempo_simulacion < 10.0:
        data.actuator('servo_j1').ctrl[0] = np.deg2rad(-90.0)
        data.actuator('servo_j2').ctrl[0] = np.deg2rad(90.0) # Vuelve a estirarse contra el suelo en el punto nuevo
        
        if tiempo_simulacion > 9.0 and not estado['bajar_place']:
            imprimir_etapa("Bajando al suelo otra vez (Place)", data)
            estado['bajar_place'] = True
            
    # PASO 6: VOLVER A HOME PARA EL SIGUIENTE CICLO (10s a 12s)
    elif tiempo_simulacion < 12.0:
        data.actuator('servo_j1').ctrl[0] = np.deg2rad(0.0)
        data.actuator('servo_j2').ctrl[0] = np.deg2rad(0.0)
        
    else:
        mujoco.mj_resetData(model, data)
        proximo_registro = 0.0
        for clave in estado:
            estado[clave] = False
        print("\n--> [RUTINA] Ciclo Pick & Place finalizado de forma segura. Reiniciando...")

mujoco.set_mjcb_control(controller)

print("Abriendo simulación Pick and Place a ras de suelo en Tiempo Real...")
with mujoco.viewer.launch_passive(modelo, datos) as visor:
    while visor.is_running():
        tiempo_inicio_paso = time.time()
        mujoco.mj_step(modelo, datos)
        visor.sync()
        
        tiempo_computo = time.time() - tiempo_inicio_paso
        tiempo_espera = modelo.opt.timestep - tiempo_computo
        if tiempo_espera > 0:
            time.sleep(tiempo_espera)