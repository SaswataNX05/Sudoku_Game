# 🧩 Sudoku Auto Solver & Visualizer

A responsive desktop application built with **Python** and **Tkinter** that solves any valid 9x9 Sudoku puzzle using a recursive **backtracking algorithm**. Features both an instant solver and a step-by-step real-time visualizer with adjustable speed.

![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=flat)
![Dependencies](https://img.shields.io/badge/Dependencies-Standard--Library-orange?style=flat)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgrey?style=flat)

---

## 🌟 Features

- **⚡ Dual Solving Modes**:
  - **Instant Solve**: Calculates and displays the complete solution in milliseconds.
  - **Step-by-Step Visualization**: Animates the recursive backtracking algorithm in real-time, showing attempts and backtracks.
- **⏱️ Adjustable Animation Speed**: An interactive slider lets you set delay intervals anywhere from **0 ms** (fastest) to **150 ms** (detailed exploration).
- **🎨 Color-Coded States**:
  - 🟨 **Yellow**: Currently placed candidate number being tested.
  - 🟥 **Red**: Backtracking / undoing an invalid placement.
  - 🟦 **Light Blue**: Final solved cell digits.
  - ⬜ **Light Gray**: Fixed initial / preset clue digits.
- **🛡️ Board Validation**:
  - Restricts cell inputs strictly to digits `1-9` (1 character max per cell).
  - Pre-solve conflict detection checks rows, columns, and 3×3 blocks for duplicates before starting.
- **🧵 Responsive Multi-Threaded Engine**: The backtracking logic runs in a background daemon thread, ensuring the Tkinter user interface never freezes during visualization.
- **📋 Built-in Sample Puzzle**: Quickly populate a valid sample Sudoku puzzle with a single click.
- **🪶 Zero External Dependencies**: Powered entirely by the Python standard library (`tkinter`, `threading`, `time`).

---

## 🎮 GUI & Controls Overview

```
+-------------------------------------------------------------+
|                       SUDOKU SOLVER                         |
|                    Status: Ready / Solving...               |
+-------------------------------------------------------------+
|  +-------+-------+-------+                                  |
|  | 5 3 . | . 7 . | . . . |                                  |
|  | 6 . . | 1 9 5 | . . . |   Interactive 9x9 Grid           |
|  | . 9 8 | . . . | . 6 . |   (Separated into 3x3 blocks)    |
|  +-------+-------+-------+                                  |
|  |  ...  |  ...  |  ...  |                                  |
|  +-------+-------+-------+                                  |
+-------------------------------------------------------------+
|  Visualization Delay (ms): [-----●-------------] (0 - 150)  |
+-------------------------------------------------------------+
| [Solve Instant]  [Visualize Step]  [Load Sample]  [Clear]   |
+-------------------------------------------------------------+
```

### Button Functions

| Button | Action |
|---|---|
| **Solve Instant** | Runs backtracking algorithm in the background and renders the solved board immediately. |
| **Visualize Step** | Runs animated backtracking live with step-by-step cell highlights and custom delays. |
| **Load Sample** | Fills the grid with a pre-configured, standard Sudoku puzzle. |
| **Clear** | Clears the board back to empty cells; stops an active visualization if currently running. |

---

## 🧠 How the Backtracking Algorithm Works

The solver implements **recursive depth-first backtracking**:

1. **Find Empty Cell**: Scans the grid from top-left to bottom-right to locate the first cell with `0` (empty).
2. **Try Candidates (1–9)**: For each number from 1 to 9:
   - Checks validity against Sudoku rules:
     - No duplicate in current **row**.
     - No duplicate in current **column**.
     - No duplicate in current **3×3 subgrid**.
   - If valid, places the number and visually highlights the cell.
3. **Recursive Call**: Recursively attempts to solve the remainder of the board with this candidate in place.
4. **Backtrack**: If no downstream number leads to a valid solution, resets the cell to `0`, highlights it in red, and backtracks to try the next candidate.
5. **Completion**: If all cells are filled legally, the puzzle is solved!

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+** installed on your system.
- **Tkinter** (usually included with standard Python installations).

> [!NOTE]
> On certain Linux distributions (like Ubuntu/Debian), you may need to install Tkinter manually if not pre-installed:
> ```bash
> sudo apt update
> sudo apt install python3-tk
> ```

### Installation & Running

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SaswataNX05/Sudoku_Game.git
   cd Sudoku_Game
   ```

2. **Launch the application**:
   ```bash
   python3 Sudoku.py
   ```
   *(Or `python Sudoku.py` on Windows)*

---

## 📂 Project Structure

```text
Sudoku_Game/
├── Sudoku.py       # Core application (Tkinter UI + Backtracking solver + Multi-threading)
└── README.md       # Project documentation & usage guide
```

---

## 🎨 Color Coding Legend

| State | Background Color | Text Color | Meaning |
|---|---|---|---|
| **Initial Clue** | `#f3f4f6` (Light Gray) | `#111827` (Dark Gray) | Pre-filled clue or loaded sample puzzle digit |
| **Exploring** | `#fef08a` (Light Yellow) | `#2563eb` (Blue) | Candidate number currently being tested |
| **Backtracking** | `#fee2e2` (Soft Red) | `#dc2626` (Red) | Invalid candidate removed / backtracking step |
| **Solved Cell** | `#e0f2fe` (Soft Blue) | `#0369a1` (Dark Blue) | Successfully solved number placed by solver |

---

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are always welcome!
Feel free to open an issue or submit a pull request:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👤 Author 

Developed by Saswata (@SaswataNX05).

Feel free to fork, open an issue, or submit a pull request if you have ideas for improvements!
