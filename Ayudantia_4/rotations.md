## 4. Ejercicio Práctico: Cinemática de Rotación en Robot Articulado de Dos Ejes

**Enunciado:** Considere el croquis del robot articulado de dos ejes de la figura. Para analizar los cambios de orientación que sufren sus eslabones debido a los movimientos de las articulaciones **$j_1$** y **$j_2$**, definiremos tres sistemas de referencia:
* **Sistema $\{A\}$ (Base Fija):** Ubicado en el centro de la base del robot. El eje $z_a$ apunta hacia arriba, el eje $x_a$ apunta hacia adelante (en la dirección del primer eslabón en reposo) y el eje $y_a$ sigue la regla de la mano derecha.
* **Sistema $\{B\}$ (Hombro):** Acoplado al primer eslabón. Cuando la articulación $j_1$ gira un ángulo $\alpha = 90^\circ$, el eslabón se levanta verticalmente.
* **Sistema $\{C\}$ (Pinza/Efector final):** Acoplado a la pinza. La articulación $j_2$ permite que la pinza rote un ángulo $\beta = 90^\circ$ sobre el eje longitudinal del brazo.

---

### Tarea 1: Rotación del Hombro ($j_1$ gira $\alpha = 90^\circ$)

Asuma que el robot arranca en reposo y la articulación $j_1$ realiza un giro de exactamente **$90^\circ$** hacia arriba. Al observar el nuevo estado del primer eslabón, los alumnos identifican visualmente la posición de los ejes del sistema $\{B\}$ con respecto a la base $\{A\}$:
* El eje $x_b$ ahora apunta hacia **arriba** (en la misma dirección que $z_a$).
* El eje $y_b$ no cambia de dirección, se mantiene paralelo a $y_a$.
* El eje $z_b$ ahora apunta hacia **atrás** (en sentido opuesto a $x_a$, o sea, es $-x_a$).

#### Construcción de la Matriz de Rotación $^A_BR$ en la pizarra:

Pida a los alumnos aplicar la regla de proyección o cosenos directores columna por columna:

1. **Columna 1 ($x_b$):** Apunta igual que $z_a \to \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$
2. **Columna 2 ($y_b$):** Apunta igual que $y_a \to \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}$
3. **Columna 3 ($z_b$):** Apunta opuesto a $x_a \to \begin{bmatrix} -1 \\ 0 \\ 0 \end{bmatrix}$

Juntando las columnas en la pizarra obtenemos la primera matriz de transformación:
$$^A_BR = \begin{bmatrix} 0 & 0 & -1 \\ 0 & 1 & 0 \\ 1 & 0 & 0 \end{bmatrix}$$

---

### Tarea 2: Rotación del Codo y Pinza ($j_2$ gira $\beta = 90^\circ$)


Ahora, manteniendo el hombro fijo, la articulación del codo **$j_2$** realiza un giro de **$90^\circ$** (torsión de la pinza). Al analizar el sistema de la pinza $\{C\}$ con respecto al sistema del eslabón previo $\{B\}$, los alumnos determinan que:
* El eje $x_c$ se mantiene sobre la línea del brazo (alineado con $x_b$).
* El eje $y_c$ gira y se alinea con la dirección que tenía $z_b$.
* El eje $z_c$ gira y apunta en sentido opuesto a $y_b$ (es decir, $-y_b$).

#### Construcción de la Matriz de Rotación $^B_CR$ en la pizarra:

Evaluamos la orientación de los ejes de $\{C\}$ usando como base al sistema $\{B\}$:

1. **Columna 1 ($x_c$):** Alineado con $x_b \to \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}$
2. **Columna 2 ($y_c$):** Alineado con $z_b \to \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$
3. **Columna 3 ($z_c$):** Opuesto a $y_b \to \begin{bmatrix} 0 \\ -1 \\ 0 \end{bmatrix}$

La matriz relativa entre el eslabón 1 y la pinza es:
$$^B_CR = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{bmatrix}$$

---

### Tarea 3: La Composición Total (Multiplicación de Matrices)

Explique a la clase que para saber la orientación final de la pinza $\{C\}$ vista directamente desde los ojos de la base fija $\{A\}$, se debe aplicar la propiedad de composición multiplicando ambas matrices en orden secuencial:

$$^A_CR = ^A_BR \cdot ^B_CR$$

#### Desarrollando el producto matricial paso a paso en la pizarra:

$$^A_CR = \begin{bmatrix} 0 & 0 & -1 \\ 0 & 1 & 0 \\ 1 & 0 & 0 \end{bmatrix} \cdot \begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{bmatrix}$$

* **Fila 1 de $^A_CR$:** * $c_{11} = (0)(1) + (0)(0) + (-1)(0) = \mathbf{0}$
  * $c_{12} = (0)(0) + (0)(0) + (-1)(1) = \mathbf{-1}$
  * $c_{13} = (0)(0) + (0)(-1) + (-1)(0) = \mathbf{0}$
* **Fila 2 de $^A_CR$:**
  * $c_{21} = (0)(1) + (1)(0) + (0)(0) = \mathbf{0}$
  * $c_{22} = (0)(0) + (1)(0) + (0)(1) = \mathbf{0}$
  * $c_{23} = (0)(0) + (1)(-1) + (0)(0) = \mathbf{-1}$
* **Fila 3 de $^A_CR$:**
  * $c_{31} = (1)(1) + (0)(0) + (0)(0) = \mathbf{1}$
  * $c_{32} = (1)(0) + (0)(0) + (0)(1) = \mathbf{0}$
  * $c_{33} = (1)(0) + (0)(-1) + (0)(0) = \mathbf{0}$

#### Matriz Resultante Final:
$$^A_CR = \begin{bmatrix} 0 & -1 & 0 \\ 0 & 0 & -1 \\ 1 & 0 & 0 \end{bmatrix}$$

---

### Conclusiones Analíticas para debatir con la clase

1. **¿Cómo lee el operador humano esta matriz final $^A_CR$ al mirar el robot real?**
   * *Respuesta esperada:* Al mirar las columnas de la matriz resultante, sabemos la orientación de la pinza directo desde la base:
     * El eje $x_c$ de la pinza (Columna 1) apunta hacia arriba (eje $z_a$ de la base).
     * El eje $y_c$ de la pinza (Columna 2) apunta hacia atrás (eje $-x_a$ de la base).
     * El eje $z_c$ de la pinza (Columna 3) apunta a la izquierda (eje $-y_a$ de la base).

2. **¿Por qué es vital respetar el orden de la multiplicación matricial?**
   * *Respuesta:* Porque la multiplicación de matrices no es conmutativa ($A \cdot B \neq B \cdot A$). Como los giros se realizan sobre ejes móviles (cinemática directa sucesiva), multiplicar al revés daría una posición espacial completamente errónea y destructiva para el software del robot.