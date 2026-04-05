"""A simple CLI betting game where players draw marbles for money."""

import os
import random
from collections import namedtuple
from dataclasses import dataclass


# --- Namedtuples ---
Marble = namedtuple("Marble", ["emoji", "multiplier", "outcome"])
Multiplier = namedtuple("Multiplier", ["low", "medium", "high"])


# --- Constants ---
TOTAL_MARBLES = 10

MENU = {
    "1": "Low Stakes (1x)",
    "2": "Medium Stakes (2x)",
    "3": "High Stakes (3x)",
    "4": "Super Game",
    "5": "Marble Menu",
    "6": "Exit",
}

STAKE_TO_FIELD = {"1": "low", "2": "medium", "3": "high"}

MARBLE_WEIGHTS = {"green": 5, "red": 3, "black": 1, "white": 1}

MARBLES = {
    "green": Marble("🟢", Multiplier(1, 2, 3), "win"),
    "red": Marble("🔴", Multiplier(1, 2, 3), "lose"),
    "black": Marble("⚫️", 10, "win"),
    "white": Marble("⚪️", 5, "lose"),
}


# --- Dataclass ---
@dataclass
class GameSession:
    """Store game session state and statistics."""
    deposit: int
    rounds: int
    menu_number: str
    marble_pool: dict[str, int]
    marbles_count: dict[str, int]
    win_loss_amount: dict[str, int]


# --- Display ---
def clear_screen() -> None:
    """Clear terminal for better interaction."""
    os.system("cls" if os.name == "nt" else "clear")


def get_colored_string(amount: int, color: int = None, bold: bool = False) -> str:
    """Return a colored ANSI string, optionally bold."""
    color = color or (92 if amount > 0 else 91)
    prefix = f"1;{color}" if bold else color
    return f"\033[{prefix}m{abs(amount)}\033[0m"


def print_banner(text: str, border: str = "$", color: int = 92, menu_number: str = None) -> None:
    """Print stylish colored banner with centered text."""
    menu_colors = {"1": 92, "2": 93, "3": 94, "4": 95}
    if menu_number in menu_colors:
        color = menu_colors[menu_number]
    border_line = border * 40
    print(f"\n\033[{color}m{border_line}\n{text.center(40)}\n{border_line}\033[0m")


def print_header(text: str, border: str = "–", color: int = 90):
    """Print a colored bordered header with centered text."""
    left_border = border * ((38 - len(text)) // 2)
    right_border = border * ((38 - len(text) + 1) // 2)
    print(f"\n\033[{color}m{left_border} {text} {right_border}\033[0m")


def print_game_menu() -> None:
    """Print the game menu."""
    print_header("Game Menu", "=")
    for i, option in MENU.items():
        print(f"{i}. {option}")


def print_marble_menu(menu_number: str = "5") -> None:
    """Print the marble menu for a given menu selection."""
    if menu_number not in MENU or menu_number == "6":
        return

    if menu_number == "5":
        print_header(MENU[menu_number], "=")
        for marble in MARBLES.values():
            mult = (
                "/".join(str(m) for m in marble.multiplier)
                    if isinstance(marble.multiplier, Multiplier)
                    else marble.multiplier
            )
            print(f"{marble.emoji} – {mult}x ({marble.outcome})")
    else:
        field = STAKE_TO_FIELD.get(menu_number, "high")
        for marble in MARBLES.values():
            if menu_number != "4" and not isinstance(marble.multiplier, Multiplier):
                continue  # skips black & white for menu 1-3
            mult = getattr(marble.multiplier, field, marble.multiplier)
            print(f"{marble.emoji} – {mult}x ({marble.outcome})")


def print_draw_result(marble_color: str, bet: int, result: int, marble_pool: dict[str, int]) -> None:
    """Print draw result based on the marble color."""
    messages = {
        "win": ["You win 🎉", "Excellent!", "You rock 🚀", "Here we go!"],
        "lose": ["Maybe next time", "Try again", "Let's try another one", "You lose"]
    }
    outcome = MARBLES[marble_color].outcome
    msg = random.choice(messages[outcome])

    label, color = ("Win", 92) if result > 0 else ("Lose", 91)
    print_banner(msg, "-") if outcome == "win" else print_banner(msg, "-", 31)

    print(f"Marble: {MARBLES[marble_color].emoji}")
    print(f"Bet: ${bet}")
    print(f"{label}: $\033[{color}m{abs(result)}\033[0m")
    print(f"Marbles left: {sum(marble_pool.values())}")


def print_final_result(session: GameSession) -> None:
    """Print final result of the session."""
    print_header("Final Result", "=")
    win_count = get_colored_string(session.win_loss_amount["win"], 92)
    loss_count = get_colored_string(session.win_loss_amount["lose"], 91)
    balance = get_colored_string(session.deposit, bold=True)

    row = " | ".join(f"{MARBLES[c].emoji}: {session.marbles_count[c]}" for c in session.marble_pool)

    print(row.center(40))
    print(f"Rounds played: {session.rounds - 1}")
    print(f"Marbles left: {sum(session.marble_pool.values())}")
    print(f"Total win: ${win_count}")
    print(f"Total loss: ${loss_count}")
    print("-" * 40)
    print(f"Balance: ${balance}")


# --- Audio ---
def beep(event: str) -> None:
    """Play a sound effect based on marble color or game event."""
    if os.name == "nt":
        return

    sounds = {
        "1": "Tink.aiff",
        "2": "Pop.aiff",
        "3": "Blow.aiff",
        "4": "Submarine.aiff",
        "5": "Bottle.aiff",
        "6": "Sosumi.aiff",
        "green": "Glass.aiff",
        "red": "Basso.aiff",
        "black": "Hero.aiff",
        "white": "Funk.aiff",
        "welcome": "Ping.aiff",
        "broke": "Basso.aiff",
        "final": "Purr.aiff",
    }

    sound = sounds.get(event, "Glass.aiff")
    os.system(f"afplay /System/Library/Sounds/{sound}")


# --- Input ---
def get_deposit() -> int:
    """Ask player for a valid deposit."""
    while True:
        try:
            deposit = int(input("Enter deposit (min $20): "))
            if deposit >= 20:
                return deposit
            print("\n⚠️ Deposit is lower than $20.")
        except ValueError:
            print("\n⚠️ Invalid input. Enter a number.")


def get_menu_number() -> str:
    """Return menu number from player input."""
    while True:
        choice = input("\nChoose from menu (1-6): ").strip()
        if choice == "6":
            print("\nGoodbye 👋")
            exit()
        elif choice in MENU:
            return choice
        else:
            print("\n⚠️ Number is out of range. Please enter number (1-6).")


def get_bet(session: GameSession) -> int | None:
    """Ask player for a valid bet and withdraw on demand."""
    while True:
        raw = input("Enter your bet: ").strip()
        if raw == "":
            confirm = input("\nDo you want to withdraw and exit (y/n)?: ").strip().lower()
            if confirm in ("y", "yes"):
                clear_screen()
                print_final_result(session)
                return None
            continue
        try:
            bet = int(raw)
            if 0 < bet <= session.deposit:
                return bet
            print(f"\n⚠️ Bet must be within ${session.deposit} (min 1$).")
        except ValueError:
            print("\n⚠️ Invalid value. Enter a valid bet.")


# --- Logic ---
def split_marbles(menu_number: str) -> dict[str, int]:
    """Split total marbles into counts based on weights."""
    colors = MARBLES.keys() if menu_number == "4" else ["green", "red"]
    total_weight = sum(MARBLE_WEIGHTS[c] for c in colors)
    return {
        color: round(TOTAL_MARBLES * MARBLE_WEIGHTS[color] / total_weight)
        for color in colors
    }


def get_multiplier(marble: Marble, field: str) -> int:
    """Return the multiplier value for a given stake field."""
    if isinstance(marble.multiplier, Multiplier):
        return getattr(marble.multiplier, field)
    return marble.multiplier


def draw_marble(marble_pool: dict[str, int]) -> str:
    """Draw a random marble and reduce pool count."""
    colors = [color for color, count in marble_pool.items() if count > 0]
    weights = [marble_pool[color] for color in colors]
    color = random.choices(colors, weights=weights)[0]
    marble_pool[color] -= 1
    return color


def get_result(color: str, bet: int, multiplier: int) -> int:
    """Return win/loss amount based on marble color and bet."""
    if MARBLES[color].outcome == "win":
        return bet * multiplier
    return -bet * multiplier


# --- Main ---
def run_marble_bet() -> None:
    """Run the main marble game loop."""
    clear_screen()
    print_banner("Welcome to Marble Bet!")
    print_marble_menu()
    beep("welcome")

    while True:
        print_game_menu()
        menu_number = get_menu_number()
        marble_pool = split_marbles(menu_number)

        print_header("Deposit", "-")
        deposit = get_deposit()

        session = GameSession(
            menu_number=menu_number,
            marble_pool=marble_pool,
            deposit=deposit,
            rounds=1,
            marbles_count={color: 0 for color in marble_pool},
            win_loss_amount={"win": 0, "lose": 0}
        )

        field = STAKE_TO_FIELD.get(menu_number, "high")
        clear_screen()
        print_banner(MENU[menu_number], "=", menu_number=menu_number)
        print_marble_menu(menu_number)
        print(f"Marbles: {sum(marble_pool.values())}")
        print("-" * 40)
        print("ℹ️ Note: press Enter without a bet to exit.")
        beep(menu_number)

        while sum(marble_pool.values()) > 0:
            print_header(f"Round {session.rounds}")
            balance = get_colored_string(session.deposit, bold=True)
            print(f"Balance: ${balance}")

            bet = get_bet(session)
            if bet is None:
                return
            clear_screen()

            color = draw_marble(marble_pool)
            multiplier = get_multiplier(MARBLES[color], field)
            result = get_result(color, bet, multiplier)

            session.deposit += result
            session.rounds += 1
            session.marbles_count[color] += 1
            outcome = MARBLES[color].outcome
            session.win_loss_amount[outcome] += result
            print_draw_result(color, bet, result, session.marble_pool)
            beep(color)

            if session.deposit <= 0:
                print_banner(f"💸 Out of funds 💸", "-", 34)
                beep("broke")
                break

        print_final_result(session)
        if session.deposit > 0:
            beep("final")

        confirm = input("\nContinue? (y/n): ").strip().lower()
        clear_screen()
        if not confirm in ("y", "yes"):
            print("\nGoodbye 👋")
            beep("6")
            exit()


if __name__ == "__main__":
    run_marble_bet()