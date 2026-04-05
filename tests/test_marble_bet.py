"""Test for the marble bet."""

import pytest
from marble_bet import MARBLES, GameSession, get_multiplier, split_marbles, draw_marble, get_result, get_bet


# --- get_multiplier ---
def test_get_multiplier_green_low():
    assert get_multiplier(MARBLES["green"], "low") == 1


def test_get_multiplier_red_medium():
    assert get_multiplier(MARBLES["red"], "medium") == 2


def test_get_multiplier_black_flat():
    assert get_multiplier(MARBLES["black"], "high") == 10


def test_get_multiplier_white_flat():
    assert get_multiplier(MARBLES["white"], "high") == 5


# --- split_marbles ---
def test_split_marbles_menu_1():
    assert split_marbles("1") == {"green": 6, "red": 4}


def test_split_marbles_menu_2():
    assert split_marbles("2") == {"green": 6, "red": 4}


def test_split_marbles_menu_3():
    assert split_marbles("3") == {"green": 6, "red": 4}


def test_split_marbles_menu_4():
    assert split_marbles("4") == {"green": 5, "red": 3, "black": 1, "white": 1}


# --- draw_marble ---
def test_draw_marble_returns_valid_color():
    marble_pool = split_marbles("1")
    color = draw_marble(marble_pool)
    assert color in marble_pool


def test_draw_marble_decrements_pool():
    marble_pool = split_marbles("1")
    before = sum(marble_pool.values())
    draw_marble(marble_pool)
    assert sum(marble_pool.values()) == before - 1


# --- get_result ---
def test_get_positive_result():
    assert get_result("green", 10, 3) == 30


def test_get_negative_result():
    assert get_result("red", 10, 3) == -30


# --- get_bet ---
def test_get_bet_valid(monkeypatch, sample_session):
    monkeypatch.setattr("builtins.input", lambda _: "10")
    assert get_bet(sample_session) == 10


def test_get_bet_zero_rejected(monkeypatch, sample_session):
    inputs = iter(["0", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert get_bet(sample_session) == 10


def test_get_bet_exceeds_deposit_rejected(monkeypatch, sample_session):
    inputs = iter(["999", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert get_bet(sample_session) == 10


def test_get_bet_invalid_text_rejected(monkeypatch, sample_session):
    inputs = iter(["abc", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert get_bet(sample_session) == 10


def test_get_bet_withdraw_confirm_yes(monkeypatch, sample_session):
    inputs = iter(["", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("marble_bet.clear_screen", lambda: None)
    monkeypatch.setattr("marble_bet.print_final_result", lambda _: None)
    assert get_bet(sample_session) is None


# --- fixtures ---
@pytest.fixture
def sample_session():
    return GameSession(
        menu_number="1",
        marble_pool=split_marbles("1"),
        deposit=50,
        rounds=1,
        marbles_count={color: 0 for color in ["green", "red"]},
        win_loss_amount={"win": 0, "lose": 0}
    )