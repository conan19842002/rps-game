import json
import os
from collections import defaultdict
from typing import Dict

# Type alias for the games dictionary
GamesDict = Dict[str, Dict[str, int]]

# File path to store game data
GAME_DATA_FILE = os.getenv('GAME_DATA_FILE', 'game_data.json')

def get_game_key(player1_name: str, player2_name: str) -> str:
    """
    Generate a unique key for a game based on player names.

    Args:
        player1_name (str): The name of player 1.
        player2_name (str): The name of player 2.

    Returns:
        str: A unique key representing the game.
    """
    return f"{player1_name}_{player2_name}"


def save_games_to_file(games: GamesDict) -> None:
    """
    Save the games dictionary to a file.

    Args:
        games (GamesDict): The dictionary containing all game states.
    """
    try:
        with open(GAME_DATA_FILE, 'w') as file:
            json.dump(games, file)
        print("Games saved successfully.")
    except IOError as e:
        print(f"Failed to save games: {e}")

def load_games() -> GamesDict:
    """
    Load the games dictionary from a file.

    Returns:
        GamesDict: The loaded games dictionary.
    """
    try:
        if os.path.exists(GAME_DATA_FILE):
            with open(GAME_DATA_FILE, 'r') as file:
                return json.load(file)
    except IOError as e:
        print(f"Failed to load games: {e}")
    return defaultdict(dict)

def determine_winner(player1_move: str, player2_move: str) -> str:
    """
    Determine the winner based on the moves of player 1 and player 2.

    Args:
        player1_move (str): The move chosen by player 1 (rock, paper, or scissors).
        player2_move (str): The move chosen by player 2 (rock, paper, or scissors).

    Returns:
        str: The result of the round ('player1', 'player2', or 'tie').
    """
    outcomes = {
        "rock": {"rock": "tie", "paper": "player2", "scissors": "player1"},
        "paper": {"rock": "player1", "paper": "tie", "scissors": "player2"},
        "scissors": {"rock": "player2", "paper": "player1", "scissors": "tie"},
    }
    return outcomes.get(player1_move, {}).get(player2_move, "Invalid move")
