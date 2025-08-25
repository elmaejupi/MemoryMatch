# 🧠 Memory Match Game

**Memory Match** is an interactive card-matching game developed using **Python** and **Streamlit**. The game challenges players to find pairs of matching cards with as few moves and in the shortest time possible. It includes AI-inspired features such as intelligent card shuffling and tracking moves to improve gameplay.

## Features

* Multiple difficulty levels:

  * Easy (4 x 4)
  * Medium (4 x 6)
  * Hard (6 x 6)
* Time and move tracking for performance analysis.
* AI-inspired card shuffling for more challenging and unpredictable gameplay.
* Interactive and responsive interface built with **Streamlit**.
* Feedback for unmatched pairs with a “Continue” button to turn them back over.
* Simple, user-friendly design with emojis as cards.

## How to Play

1. Click two cards to reveal them.
2. If they match, they stay face-up. If not, press *Continue* to turn them back over.
3. Clear the board with the fewest moves possible.
4. Change *Grid size* or *Shuffle seed* from the sidebar → *New Game*.

## Installation

1. Install Python (>=3.9).
2. Install required packages:

   ```bash
   pip install streamlit
   ```
3. Run the game:

   ```bash
   streamlit run app.py
   ```

## Technologies Used

* Python
* Streamlit
* Random module for AI-inspired shuffling

## License

This project is open-source and available under the MIT License.
