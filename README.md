# Marble Bet
A simple CLI betting game where players draw marbles for money.

---

## Features
- Colored banners based on menu choice
- Marble emojis in menus and round results
- Weighted marble pool for different game modes
- Round-by-round result display (marble color, win/loss, marbles left)
- Early withdraw during the session
- Sound effects via `afplay` (macOS only, silent on Windows)

---

## Example Output
```
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        Welcome to Marble Bet!         
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

============= Marble Menu ==============
🟢 – 1/2/3x (win)
🔴 – 1/2/3x (lose)
⚫️ – 10x (win)
⚪️ – 5x (lose)

============== Game Menu ===============
1. Low Stakes (1x)
2. Medium Stakes (2x)
3. High Stakes (3x)
4. Super Game
5. Marble Menu
6. Exit

Choose from menu (1-6): 3

--------------- Deposit ----------------
Enter deposit (min $20): 50

========================================
            High Stakes (3x)            
========================================
🟢 – 3x (win)
🔴 – 3x (lose)
Marbles: 10
----------------------------------------
ℹ️ Note: press Enter without a bet to exit.

––––––––––––––– Round 1 ––––––––––––––––
Balance: $50
Enter your bet: 5

----------------------------------------
               Excellent!               
----------------------------------------
Marble: 🟢
Bet: $5
Win: $15
Marbles left: 9

––––––––––––––– Round 2 ––––––––––––––––
Balance: $65
Enter your bet: 10

----------------------------------------
                You lose                
----------------------------------------
Marble: 🔴
Bet: $10
Lose: $30
Marbles left: 8

––––––––––––––– Round 3 ––––––––––––––––
Balance: $35
Enter your bet: 
```

---

## Requirements
- **Python 3.10+**
- No external dependencies

---

## Installation
1. Clone the repository:
```bash
git clone https://github.com/michael-caenrich/marble-bet.git
```
2. Navigate to the project folder:
```bash
cd marble-bet
```

---

## Usage
```bash
python marble_bet.py
```

---

## Project Structure
```
📁 marble-bet/
├── marble_bet.py
├── tests/
│   └── test_marble_bet.py
├── requirements-dev.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## Run Tests
Install dependencies:
```bash
pip install -r requirements-dev.txt
```
  
Run all tests:
```bash
python -m pytest
```

---

## Future Ideas
- Save session history to a file (JSON/CSV)
- Leaderboard with top balances
- Configurable starting marbles and weights via CLI args

---

## License
[MIT License](LICENSE)

---

## Author
**Pavel Kandrichin**  
GitHub: [michael-caenrich](https://github.com/michael-caenrich)