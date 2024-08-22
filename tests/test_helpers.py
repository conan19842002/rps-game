from utils import get_game_key, determine_winner, save_games_to_file, load_games

def test_get_game_key():
    assert get_game_key("An", "Binh") == "An_Binh"
    assert get_game_key("Player1", "Player2") == "Player1_Player2"

def test_determine_winner():
    assert determine_winner("rock", "scissors") == "player1"
    assert determine_winner("scissors", "rock") == "player2"
    assert determine_winner("paper", "rock") == "player1"
    assert determine_winner("rock", "paper") == "player2"
    assert determine_winner("scissors", "scissors") == "tie"

def test_save_and_load_games():
    games = {"An_Binh": {"player1_score": 2, "player2_score": 1}}
    
    save_games_to_file(games)
    
    loaded_games = load_games()
    
    assert loaded_games == games