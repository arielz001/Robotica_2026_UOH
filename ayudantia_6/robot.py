import numpy as np
import roboticstoolbox as rtb

def iniciar_robot_articulado_L():
    H  = 0.2   
    L2 = 0.2   
    L3 = 0.2  
    L4 = 0.2   
    L5 = 0.2  
    L6 = 0.2   
    
    print("=========================================================")
    print("   robot    ")
    print("=========================================================\n")
    
    robot = rtb.DHRobot([
        rtb.RevoluteDH(d=H,  a=0,  alpha=np.deg2rad(90)),   
        rtb.RevoluteDH(d=0,  a=L2, alpha=np.deg2rad(0)),    
        rtb.RevoluteDH(d=0,  a=L3, alpha=np.deg2rad(-90)),   
        rtb.RevoluteDH(d=L4, a=0,  alpha=np.deg2rad(90)),  
        rtb.RevoluteDH(d=0,  a=L5,  alpha=np.deg2rad(-90)),   
        rtb.RevoluteDH(d=L6, a=0,  alpha=np.deg2rad(0))     
    ], name="Robot")

    print("Tabla DH:")
    print(robot)

    q_inicial = [0, 0, 0, 0, 0, 0]

    print("\nLanzando simulador interactivo...")
    robot.teach(q_inicial, block=True)

if __name__ == "__main__":
    iniciar_robot_articulado_L()
