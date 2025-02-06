# LCS Game

A fun interactive game that tests your ability to find the **Longest Common Subsequence (LCS)** between two words. The game is built using Python and **Pygame**.

## Features
- Random word pairs
- Real-time user input validation
- Timer-based gameplay
- Score and level progression

## Installation
### Prerequisites
- Python 3.8+

### Install Dependencies
```sh
pip install -r requirements.txt
```

## How to Play
1. Run the game:
   ```sh
   python main.py
   ```
2. Two words will appear on the screen.
3. Type a **common subsequence** of the two words.
4. Press **Enter** to submit.
5. Earn points for correct sequences.
6. Press **Backspace** to delete.
7. Press **Spacebar** to reveal the solution.
8. The game ends when time runs out.

## Controls
- **Enter** → Submit sequence
- **Backspace** → Delete character
- **Spacebar** → Show correct LCS
- **Escape** → Quit game

## Example
If the words are **HELLO** and **WORLD**, a valid subsequence would be `LO`.

## License
MIT