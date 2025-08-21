# ArimaaIA 🎲🤖

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/Zers04/ArimaaIA/blob/main/README.md)
[![es](https://img.shields.io/badge/lang-es-blue.svg)](https://github.com/Zers04/ArimaaIA/blob/main/README-es.md)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)
![IA](https://img.shields.io/badge/IA-Minimax%20%2B%20Alpha--Beta-red)

Implementación del juego de mesa **Arimaa** con inteligencia artificial basada en el algoritmo **Minimax con poda alfa-beta**, desarrollada en **Python** utilizando **Pygame**.  
Este proyecto fue realizado como trabajo final para el curso de Inteligencia Artificial de la **Universidad del Valle**.

---

## 📖 Descripción

Arimaa es un juego de estrategia diseñado para ser difícil de resolver por computadoras.  
En este proyecto se implementa:

- **Lógica del juego**: Reglas, turnos, movimientos de piezas y condiciones de victoria.
- **Interfaz gráfica (GUI)**: Tablero interactivo desarrollado con Pygame.
- **Inteligencia Artificial**: Algoritmo **Minimax con poda alfa-beta** que permite a la máquina competir contra jugadores humanos.

El sistema evalúa posiciones y selecciona movimientos usando una heurística que considera:
- Diferencia en número de piezas.
- Distancia de los conejos a la meta.
- Piezas atrapadas en trampas.
- Piezas congeladas.
- Agrupación de piezas aliadas/enemigas.

---

## 🎯 Objetivos

- Implementar un entorno interactivo para jugar Arimaa contra otro jugador o contra la IA.
- Diseñar un tablero gráfico intuitivo que permita visualizar y mover piezas fácilmente.
- Incorporar una inteligencia artificial basada en **Minimax** para la toma de decisiones.

---

## 🕹️ Reglas principales del juego implementadas

- El tablero es de **8x8**.
- Cada jugador dispone de **4 movimientos por turno**.
- Las piezas se mueven según su tipo (ejemplo: Elefante = 1 casilla, Camello = 2 casillas).
- Captura automática al mover una pieza hacia la casilla de otra enemiga.
- Un jugador gana si:
  - Uno de sus conejos alcanza la fila final del oponente.
  - El Camello del rival es capturado.

---

## 📋 Pre-requisitos 

  - Python 3.10 o superior
  - Pygame 2.0 o superior

## 🚀 Instalación y ejecución

Sigue estos pasos para instalar y preparar el proyecto:

### 1. Clonar repositorio
```bash
git clone https://github.com/Zers04/ArimaaIA.git
cd ArimaaIA
```

### 2. Crea un entorno virtual (opcional pero recomendado):
 ```bash
 python -m venv venv
 source venv/bin/activate  # Linux/Mac
 # o
 venv\Scripts\activate  # Windows
 ```

### 3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## ⚙️ Ejecución

Para iniciar el juego, ejecuta:

```bash
python main.py
```

---

## 🎬 Escenas del juego

* Menú de inicio

  <img width="350" height="350" alt="image" src="https://github.com/user-attachments/assets/3229ed3b-9648-487b-b3e4-086c6c28654d" />

* Tablero en su posición inicial

  <img width="350" height="350" alt="image" src="https://github.com/user-attachments/assets/44128413-c627-46b3-b725-d411e4b8e184" />

* Movimientos disponibles

  <img width="350" height="350" alt="image" src="https://github.com/user-attachments/assets/72e42685-a65f-42f4-92d1-b87f47a7ef06" />

---

## Autores ✒️

* **Juan David Cataño** - [Zers04](https://github.com/Zers04)
* **Valentina Londoño** - [Valtimore](https://github.com/valtimore)

## Licencia 📄

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
