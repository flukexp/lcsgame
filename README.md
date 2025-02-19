# LCS Game

LCS Game is an interactive and engaging game that challenges players to find the **Longest Common Subsequence (LCS)** between two words. Built using **Python** and **Pygame**, this game enhances logical thinking and pattern recognition skills.

## Features
- **Random word pairs** to keep the game dynamic
- **Real-time input validation** for an interactive experience
- **Timer-based gameplay** to add a challenge
- **Score and level progression** for rewarding gameplay
- **Tutorial mode** to help new players understand LCS concepts

## Installation
### Prerequisites
- Python **3.8+**

### Install Dependencies
```sh
pip install -r requirements.txt
```

## How to Play
### Objective
The goal is to find the **Longest Common Subsequence (LCS)** between two given words. The LCS is the longest sequence of characters that appears in both words in the same order, but not necessarily consecutively.

### Starting the Game
1. **Run the Game**
   - Open a terminal or command prompt.
   - Navigate to the game directory.
   - Run the following command:
     ```sh
     python main.py
     ```
2. **Main Menu**
   - Use the **Up/Down arrow keys** to navigate.
   - Press **Enter** to select an option:
     - **Start Game** → Begin a new game.
     - **Tutorial** → Learn how to play with a step-by-step guide.
     - **Quit** → Exit the game.

### Gameplay Mechanics
#### Game Screen
- Two words will be displayed on the screen.
- Your task is to find and type a **valid LCS**.

#### Typing and Submitting a Sequence
- Type the common subsequence using your keyboard.
- The entered sequence will be displayed in real time.
- **Press Enter** to submit:
  - ✅ **Correct sequence** → Earn points and progress to the next level.
  - ❌ **Incorrect sequence** → A shake effect and sound indicate a wrong answer.

#### Additional Controls
- **Backspace** → Delete the last character.
- **Spacebar** → Reveal the correct LCS (highlighted for 3 seconds).
- **Escape** → Quit the game and return to the main menu.

### Scoring & Levels
- **Scoring**: Each correct character in the LCS earns **10 points**.
- **Level Progression**: Advancing to the next level presents a new word pair.

### Tutorial Mode
The tutorial provides a **step-by-step guide** with examples to help new players understand the LCS concept.

## Controls
| Key           | Action                        |
|--------------|------------------------------|
| **Enter**    | Submit the typed sequence    |
| **Backspace** | Delete the last character   |
| **Spacebar**  | Reveal the correct LCS      |
| **Escape**    | Quit the game               |
| **Up/Down**   | Navigate menu/tutorial      |
| **Left/Right**| Change words in tutorial    |

## Example
- **Given Words**: `HELLO` and `WORLD`
- **Valid LCS**: `LO`

## Project Structure
```
LCS-Game/
│── assets/            # Game assets (e.g., sounds, images, scores)
│── lcs.py             # Core game logic
│── main.py            # Entry point, handles menu & game flow
│── menu.py            # Implements game menu and high scores
│── settings.py        # Configuration settings (screen size, colors, etc.)
│── tutorial.py        # Tutorial module for guiding new players
│── score.json         # Stores high scores and level progress
│── requirements.txt   # Dependencies list
│── README.md          # Project documentation
```

## License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---


