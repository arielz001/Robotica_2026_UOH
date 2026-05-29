# 🤖 Guía Completa de Cinemática y Rotaciones: El Nuevo Bucle de Movimiento

¡Buenas, muchachos! En esta guía vamos a destripar matemáticamente el comportamiento de nuestro robot industrial de **2 ejes**. El objetivo es entender cómo se calculan las matrices de rotación reales cuando alteramos el orden del movimiento tradicional y cómo se encadenan estos movimientos en el espacio tridimensional.

---

## 1. La Anatomía del Robot (Configuración $Z-Y$)

Para esta prueba, configuramos el robot con una estructura antropomórfica particular:

1. **Eslabón 1 (Hombro - $j_1$):** Rota en el eje **$Z$** (Giro horizontal / Panorámico).
2. **Eslabón 2 (Codo - $j_2$):** Rota en el eje **$Y$** (Elevación vertical / Cabeceo).
3. **Efector Final (Pinza):** Va rígidamente soldado al final del Eslabón 2.

### Dimensiones mecánicas del modelo XML:
* Altura de la base ($z_{base}$): $0.1\text{ m}$
* Longitud del Brazo 1 ($L_1$): $0.5\text{ m}$
* Longitud del Brazo 2 ($L_2$): $0.4\text{ m}$

---

## 2. El Ciclo de Movimiento Programado

La rutina en Python rompe el orden común del Pick & Place para analizar la composición de matrices paso a paso:

* **Fase 1 (0-2s) - Normalidad Inicial (Home):** El robot parte completamente vertical ($\theta_1 = 0^\circ, \theta_2 = 0^\circ$).
* **Fase 2 (2-4s) - Quiebre de Codo:** El hombro se queda quieto ($\theta_1 = 0^\circ$) y el codo rota a **$\theta_2 = 90^\circ$** apuntando hacia adelante.
* **Fase 3 (4-6s) - Giro en Bloque:** Con el codo ya quebrado, el hombro rota en $Z$ a **$\theta_1 = 90^\circ$**. El brazo barre el espacio de forma horizontal.
* **Fase 4 (6-8s) - Regreso a la Normalidad:** Ambos motores vuelven a $0^\circ$ en seco para reiniciar el bucle.

---

## 3. Las Herramientas Universales: Matrices Canónicas de Rotación

En el espacio tridimensional, cualquier objeto puede rotar respecto a los tres ejes del sistema cartesiano. Para calcular estos movimientos, la robótica utiliza **3 Matrices Canónicas fundamentales**. Grábenselas, porque son universales para cualquier robot del planeta:

### Rotación en el Eje X ($R_x$)
Si un eslabón gira alrededor del eje $X$ un ángulo $\alpha$, las coordenadas en $X$ no cambian y el plano $Y-Z$ se transforma así:
$$R_x(\alpha) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos(\alpha) & -\sin(\alpha) \\ 0 & \sin(\alpha) & \cos(\alpha) \end{bmatrix}$$

### Rotación en el Eje Y ($R_y$)
Si un eslabón gira alrededor del eje $Y$ un ángulo $\beta$ (como nuestro codo $j_2$), el eje $Y$ se mantiene estable y se cruzan las proyecciones de $X$ y $Z$:
$$R_y(\beta) = \begin{bmatrix} \cos(\beta) & 0 & \sin(\beta) \\ 0 & 1 & 0 \\ -\sin(\beta) & 0 & \cos(\beta) \end{bmatrix}$$

### Rotación en el Eje Z ($R_z$)
Si un eslabón gira alrededor del eje $Z$ un ángulo $\gamma$ (como nuestro hombro $j_1$), la altura en $Z$ no se altera, variando el plano horizontal $X-Y$:
$$R_z(\gamma) = \begin{bmatrix} \cos(\gamma) & -\sin(\gamma) & 0 \\ \sin(\gamma) & \cos(\gamma) & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

---

## 4. Composición de nuestro Robot ($R_z \cdot R_y$)

La matriz de rotación total de la pinza respecto a la base del mundo ($R_{base}^{pinza}$) se calcula multiplicando las transformaciones de cada articulación **desde la base hacia afuera**. 

Como nuestro hombro se mueve en $Z$ ($\theta_1$) y nuestro codo se mueve en $Y$ ($\theta_2$), la combinación matemática exacta es:

$$R_{base}^{pinza} = R_z(\theta_1) \cdot R_y(\theta_2)$$

Al desarrollar el producto, la ecuación generalizada que MuJoCo resuelve en cada milisegundo es:

$$R_{base}^{pinza} = \begin{bmatrix} \cos(\theta_1) & -\sin(\theta_1) & 0 \\ \sin(\theta_1) & \cos(\theta_1) & 0 \\ 0 & 0 & 1 \end{bmatrix} \cdot \begin{bmatrix} \cos(\theta_2) & 0 & \sin(\theta_2) \\ 0 & 1 & 0 \\ -\sin(\theta_2) & 0 & \cos(\theta_2) \end{bmatrix}$$

$$R_{base}^{pinza} = \begin{bmatrix} \cos(\theta_1)\cos(\theta_2) & -\sin(\theta_1) & \cos(\theta_1)\sin(\theta_2) \\ \sin(\theta_1)\cos(\theta_2) & \cos(\theta_1) & \sin(\theta_1)\sin(\theta_2) \\ -\sin(\theta_2) & 0 & \cos(\theta_2) \end{bmatrix}$$

---

## 5. ⚠️ ¡OJO ACÁ! No es una multiplicación Punto a Punto (Element-wise)

Un error clásico cuando uno está partiendo es pensar que "multiplicar matrices" es multiplicar el término de la esquina con el de la esquina (punto a punto o tipo *Hadamard*). **¡Si hacen eso en un certamen o proyecto, el robot va a chocar contra la pared!**

En el espacio físico, los movimientos se acumulan. Que el codo rote depende de hacia dónde esté apuntando el hombro. Por eso se usa la multiplicación **Fila por Columna**, que acopla los movimientos.

#### Demostración en la pizarra para la primera casilla ($R_{11}$):
Para calcular la esquina superior izquierda de la matriz final, tomamos la **Fila 1 de $R_z$** y la combinamos con la **Columna 1 de $R_y$**:

* Fila 1 de $R_z$: $\begin{bmatrix} \cos(\theta_1) & -\sin(\theta_1) & 0 \end{bmatrix}$
* Columna 1 de $R_y$: $\begin{bmatrix} \cos(\theta_2) \\ 0 \\ -\sin(\theta_2) \end{bmatrix}$

Multiplicamos término a término y sumamos los resultados:
$$R_{11} = (\cos(\theta_1) \cdot \cos(\theta_2)) + (-\sin(\theta_1) \cdot 0) + (0 \cdot -\sin(\theta_2))$$
$$R_{11} = \cos(\theta_1)\cos(\theta_2)$$

¿Se dan cuenta? El ángulo del hombro y el del codo terminan unidos en un solo componente. Esto demuestra matemáticamente que la orientación final del robot depende de ambos eslabones al mismo tiempo.

---

## 6. Comprobación de las Fases en la Consola

Vamos a evaluar la gran ecuación final usando los ángulos reales de nuestro bucle en Python:

### Caso A: Fase 2 - Codo a $90^\circ$ ($\theta_1 = 0^\circ, \theta_2 = 90^\circ$)
Sabiendo que $\cos(0^\circ)=1$, $\sin(0^\circ)=0$ y que $\cos(90^\circ)=0$, $\sin(90^\circ)=1$:

$$R_{base}^{pinza} = \begin{bmatrix} (1)(0) & -0 & (1)(1) \\ (0)(0) & 1 & (0)(1) \\ -1 & 0 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 1 \\ 0 & 1 & 0 \\ -1 & 0 & 0 \end{bmatrix}$$

* **Significado físico:** Al doblar solo el codo hacia el frente, el eje $Z$ de la pinza se acostó por completo y ahora apunta hacia donde antes apuntaba el eje $X$ del mundo. El signo negativo en la posición $R_{31}$ indica que el eje $X$ de la pinza quedó mirando directo al suelo.

### Caso B: Fase 3 - Hombro a $90^\circ$ y Codo a $90^\circ$ ($\theta_1 = 90^\circ, \theta_2 = 90^\circ$)
Aquí viene el quiebre tridimensional de nuestro bucle. Evaluamos la matriz con $\cos(90^\circ)=0$ y $\sin(90^\circ)=1$ para ambos actuadores:

$$R_{base}^{pinza} = \begin{bmatrix} (0)(0) & -1 & (0)(1) \\ (1)(0) & 0 & (1)(1) \\ -1 & 0 & 0 \end{bmatrix} = \begin{bmatrix} 0 & -1 & 0 \\ 0 & 0 & 1 \\ -1 & 0 & 0 \end{bmatrix}$$

* **¿Qué significa esto en el gráfico de barras de Matplotlib?**
  * $R_{11} = 0$, $R_{22} = 0$: Las barras principales caen a cero porque los ejes originales se desalinearon por completo.
  * Los valores cruzados ($R_{12} = -1$ y $R_{23} = 1$) demuestran matemáticamente que la pinza cambió de frente y ahora opera en un plano ortogonal al que inició.

---

## 7. Desafío para el Laboratorio

Cuando corran la simulación con los dos gráficos en paralelo, fíjense en estos fenómenos:
1. **La caída de $R_{33}$:** Miren cómo en la Fase 2 la barra que representa la altura del eje $Z$ local se desploma a cero cuando el codo se quiebra.
2. **El cruce de datos:** Observen cómo en la Fase 3 cambian los valores impresos en la consola, validando la multiplicación matricial.
3. **El Freno de Emergencia:** Al activar el bloqueo en el script, verán cómo las matrices se congelan en valores decimales intermedios (ej. $\cos(45^\circ) \approx 0.707$), demostrando que la cinemática es continua y real.