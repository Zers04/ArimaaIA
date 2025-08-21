# ArimaaIA 🎲🤖

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/Zers04/ArimaaIA/blob/main/README.md)
[![es](https://img.shields.io/badge/lang-es-blue.svg)](https://github.com/Zers04/ArimaaIA/blob/main/README-es.md)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)
![AI](https://img.shields.io/badge/AI-Minimax%20%2B%20Alpha--Beta-red)

Implementation of the board game **Arimaa** with artificial intelligence based on the **Minimax algorithm with alpha-beta pruning**, developed in **Python** using **Pygame**.  
This project was carried out as a final project for the Artificial Intelligence course at **Universidad del Valle**.

---

## 📖 Project Description

Arimaa is a strategy game designed to be difficult for computers to solve.  
This project implements:

- **Game logic**: Rules, turns, piece movements, and victory conditions.
- **Graphical User Interface (GUI)**: Interactive board developed with Pygame.
- **Artificial Intelligence**: **Minimax algorithm with alpha-beta pruning** allowing the computer to compete against human players.

The system evaluates board positions and selects moves using a heuristic that considers:
- Difference in the number of pieces.
- Distance of rabbits to the goal.
- Pieces trapped in traps.
- Frozen pieces.
- Grouping of allied/enemy pieces.

---

## 🎯 Features

- Implement an interactive environment to play Arimaa against another player or the AI.
- Design an intuitive graphical board to easily visualize and move pieces.
- Incorporate an artificial intelligence based on **Minimax** for decision-making.

---

## 🕹️ Main Game Rules Implemented

- The board is **8x8**.
- Each player has **4 moves per turn**.
- Pieces move according to their type (e.g., Elephant = 1 square, Camel = 2 squares).
- Automatic capture when moving onto a square occupied by an enemy piece.
- A player wins if:
  - One of their rabbits reaches the opponent’s last row.
  - The opponent’s Camel is captured.

---

## 📋 Prerequisites

- Python 3.10 or higher  
- Pygame 2.0 or higher  

---

## 🚀 Installation

Follow these steps to install and set up the project:

### 1. Clone repository
```bash
git clone https://github.com/Zers04/ArimaaIA.git
cd ArimaaIA
```

### 2. Create a virtual environment (optional but recommended):
 ```bash
 python -m venv venv
 source venv/bin/activate  # Linux/Mac
 # o
 venv\Scripts\activate  # Windows
 ```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Run

To start the game, run:

```bash
python main.py
```

---

## 🎬 Game Scenes

* Start Menu

  <img width="350" height="350" alt="image" src="https://github.com/user-attachments/assets/3229ed3b-9648-487b-b3e4-086c6c28654d" />

* Initial board setup

  <img width="350" height="350" alt="image" src="https://github.com/user-attachments/assets/44128413-c627-46b3-b725-d411e4b8e184" />

* Available moves

  <img width="350" height="350" alt="image" src="https://github.com/user-attachments/assets/72e42685-a65f-42f4-92d1-b87f47a7ef06" />

---

## Authors ✒️

* **Juan David Cataño** - [Zers04](https://github.com/Zers04)
* **Valentina Londoño** - [Valtimore](https://github.com/valtimore)

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
