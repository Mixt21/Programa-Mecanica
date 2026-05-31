# Simulador de cargas eléctricas, fuerza eléctrica y campo eléctrico

## Integrantes del Equipo
* **Pedro Gonzalez Santiago**
* **Castro Alvarado Tristan Humberto**
* **Vargas Aguilera Rodrigo**

## Institución y Asignatura
* **Instituto Politécnico Nacional (IPN)**
* **Escuela Superior de Cómputo (ESCOM)**
* **Asignatura:** Mecánica y Electromagnetismo
* **Fecha de Entrega:** 2 de Junio de 2026

---

## Descripción 
Este simulador de cargas electricas elaborado en **Python** permite simular cargas electricas puntuales en entorno 1D como entorno 2D. 

Este programa calcula las fuerzas electrostáticas mediante la **Ley de Coulomb**, determina la **fuerza neta** sobre cualquier carga, y evalúa el **campo eléctrico** en 3 puntos del espacio. Además, genera una representacion gráfica del análisis visual de las cargas y los puntos del campo electrico.

---

## Lenguaje y Librerías Utilizadas
* Lenguaje de programacion: **Python**
* **Matplotlib**: Genera de planos vectoriales, posicionamiento de cargas y renderizado de la gráfica.
* **Math**: Biblioteca para el manejo de funciones trigonométricas, cálculo de distancias y raíces cuadradas.

---

## Instrucciones de Instalación y Ejecución
Pasos para poder ejecutar el programa

1. **Descargar Python desde la pagina oficial (version 3.14.5 o recientes):** Al descargar se necesita poner la casilla de Add Python to PATH
* Despues de la descarga puedes verificar escribiendo en la terminal:
   ```bash
   python --version

2. **Instala la librería de gráficos (Matplotlib):** En la terminar se necesita escribir
   ```bash
   pip install matplotlib
   
3. **Ejecuta el simulador:** Abre la terminal, navega hasta la carpeta donde descargaste el archivo ProgramaMecanica.py y ejecutalo con 
   ```bash
   python ProgramaMecanica.py

## Ejemplo de uso
Al iniciar el programa
* **1.- Selección del Entorno:** Elige si deseas trabajar una sola línea recta (1D) o en un plano cartesiano (2D).
* **2.- Registro de Cargas:** El programa pide el valor de la carga en Coulombs (ej. 1e-6 para 1x10^-6) y sus coordenadas en metros.
        El programa evalua si la cargas estan en el mismo punto, si es asi manda un error y reinicia el registro.
* **3.- Menú de Opciones:** Este menu permite elegir si, visualizar los datos de las cargas, calcular la fuerza individual y neta sobre una carga específica, proyectar el campo eléctrico en 3 puntos espaciales independientes, abrir la interfaz gráfica, reiniciar el programa para volver a elegir el entorno y salir del programa

## Explicacion de los calculos implementados
Se utilizaron las leyes fundamentales del electromagnetismo como:
* **1. Ley de Coulomb y Descomposición Vectorial:** El programa calcula la magnitud de la fuerza mediante $F = K \frac{|q_1 q_2|}{r^2}$. Posteriormente, determina la dirección proyectando el vector sobre los ejes utilizando componentes de vectores unitarios directores.
* **2. Principio de Superposición:** Para hallar la fuerza total sobre una carga, se excluye interacción de la carga consigo misma y se realiza una sumatoria independiente de componentes.

## Descripcion de las visuales - Grafica
* 🔴 **Círculos Rojos (+):** Son las cargas positivas.
* 🔵 **Círculos Azules (-):** Son las cargas negativas.
* 🟩 **Vector Verde (──►):** Representa la direccion, sentido y magnitud de la Fuerza Neta calculada sobre la carga analizada.
* ░ **Vectores Grises (╌►):** Representan las fuerzas individuales de las demás cargas.
* ✖️ **Cruces y Vectores Morados:** Localización de los puntos de prueba del campo electrico y su orientación.
* **Caja de Resumen Flotante:** Un cuadro en la esquina superior que resume los datos de todas las cargas y los resultados calculados.
