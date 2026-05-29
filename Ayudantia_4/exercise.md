## 3. Ejercicio Práctico para Resolver en Clase (Lápiz y Papel)

**Enunciado:** En una imagen binaria con dimensiones de $100 \times 100$ píxeles, se han detectado únicamente **3 píxeles activos (puntos blancos)** en una diagonal perfecta. Sus coordenadas en el espacio de la imagen $(x, y)$ son:
* $P_1 = (30, 30)$
* $P_2 = (50, 50)$
* $P_3 = (70, 70)$

Para analizar la presencia de esta línea recta mediante la **Transformada de Hough**, evaluaremos el espacio de parámetros utilizando tres ángulos de prueba: $\theta = \{-45^\circ, 0^\circ, 45^\circ\}$.

La ecuación de evaluación es:  
$$\rho = x \cos(\theta) + y \sin(\theta)$$

---

### Tarea 1: El Cálculo Matemático Paso a Paso

Pida a los alumnos que calculen el valor de la distancia $\rho$ para cada punto con los tres ángulos propuestos.

Recuerde a la clase los valores trigonométricos aproximados y exactos para agilizar la pizarra:
* **Para $-45^\circ$:** $\cos(-45^\circ) = \frac{\sqrt{2}}{2}$, $\sin(-45^\circ) = -\frac{\sqrt{2}}{2}$
* **Para $0^\circ$:** $\cos(0^\circ) = 1$, $\sin(0^\circ) = 0$
* **Para $45^\circ$:** $\cos(45^\circ) \approx 0.7$, $\sin(45^\circ) \approx 0.7$ *(Usaremos la aproximación rápida $0.7$ para la suma)*

#### Desarrollando los cálculos en la pizarra:

1. **Para el Punto $P_1(30, 30)$:**
   * Con $\theta = -45^\circ$: $\rho = 30\left(\frac{\sqrt{2}}{2}\right) + 30\left(-\frac{\sqrt{2}}{2}\right) = 15\sqrt{2} - 15\sqrt{2} = \mathbf{0.0}$
   * Con $\theta = 0^\circ$: $\rho = 30(1) + 30(0) = \mathbf{30.0}$
   * Con $\theta = 45^\circ$: $\rho = 30(0.7) + 30(0.7) = 21 + 21 = \mathbf{42.0}$

2. **Para el Punto $P_2(50, 50)$:**
   * Con $\theta = -45^\circ$: $\rho = 50\left(\frac{\sqrt{2}}{2}\right) + 50\left(-\frac{\sqrt{2}}{2}\right) = 25\sqrt{2} - 25\sqrt{2} = \mathbf{0.0}$
   * Con $\theta = 0^\circ$: $\rho = 50(1) + 50(0) = \mathbf{50.0}$
   * Con $\theta = 45^\circ$: $\rho = 50(0.7) + 50(0.7) = 35 + 35 = \mathbf{70.0}$

3. **Para el Punto $P_3(70, 70)$:**
   * Con $\theta = -45^\circ$: $\rho = 70\left(\frac{\sqrt{2}}{2}\right) + 70\left(-\frac{\sqrt{2}}{2}\right) = 35\sqrt{2} - 35\sqrt{2} = \mathbf{0.0}$
   * Con $\theta = 0^\circ$: $\rho = 70(1) + 70(0) = \mathbf{70.0}$
   * Con $\theta = 45^\circ$: $\rho = 70(0.7) + 70(0.7) = 49 + 49 = \mathbf{98.0}$

#### Tabla de Resultados de Hough:

| Punto $(x, y)$ | $\theta = -45^\circ$ | $\theta = 0^\circ$ | $\theta = 45^\circ$ |
| :--- | :---: | :---: | :---: |
| **$P_1(30, 30)$** | $\rho = \mathbf{0.0}$ | $\rho = \mathbf{30.0}$ | $\rho = \mathbf{42.0}$ |
| **$P_2(50, 50)$** | $\rho = \mathbf{0.0}$ | $\rho = \mathbf{50.0}$ | $\rho = \mathbf{70.0}$ |
| **$P_3(70, 70)$** | $\rho = \mathbf{0.0}$ | $\rho = \mathbf{70.0}$ | $\rho = \mathbf{98.0}$ |

---

### Tarea 2: El Tablero de Votación (El Acumulador)

Dibuje el acumulador modificado en la pizarra. Muestre cómo la nueva columna de $45^\circ$ genera distancias altas que se dispersan en su propia ruta, dejando nuevamente a la celda de $-45^\circ$ como la ganadora absoluta:

| Valor de $\rho$ \ Ángulo $\theta$ | $-45^\circ$ | $0^\circ$ | $45^\circ$ |
| :---: | :---: | :---: | :---: |
| **$98.0$** | $0$ | $0$ | $1$ *(Voto de $P_3$)* |
| **$70.0$** | $0$ | $1$ *(Voto de $P_3$)* | $1$ *(Voto de $P_2$)* |
| **$50.0$** | $0$ | $1$ *(Voto de $P_2$)* | $0$ |
| **$42.0$** | $0$ | $0$ | $1$ *(Voto de $P_1$)* |
| **$30.0$** | $0$ | $1$ *(Voto de $P_1$)* | $0$ |
| **$0.0$** | **$3$** *(Votos de $P_1, P_2, P_3$)* | $0$ | $0$ |

---
