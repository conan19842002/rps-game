from app import scores


def test_index(client):
    """Test the index route."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Rock Paper Scissors" in rv.data 

def test_play_round(client):
    """Test playing a round."""
    scores["player1"] = 0
    scores["player2"] = 0
    data = {"player1": "An", "player2": "Binh", "player1_move": "rock", "player2_move": "scissors"}
    rv = client.post('/play', json=data)
    json_data = rv.get_json()

    assert rv.status_code == 200
    assert json_data["result"] == "An wins!"
    assert json_data["scores"]["player1"] == 1
    assert json_data["scores"]["player2"] == 0

def test_save_and_load_game(client):
    """Test saving and loading a game."""
    scores["player1"] = 2
    scores["player2"] = 1
    
    save_data = {
        "player1_name": "An",
        "player2_name": "Binh",
        "player1_score": scores["player1"],
        "player2_score": scores["player2"]
    }
    
    save_resp = client.post('/save', json=save_data)
    assert save_resp.status_code == 200
    assert save_resp.get_json()["message"] == "Game has been saved!"

    load_data = {"player1_name": "An", "player2_name": "Binh"}
    load_resp = client.post('/load', json=load_data)
    json_data = load_resp.get_json()

    assert load_resp.status_code == 200
    assert json_data["scores"]["player1"] == scores["player1"]
    assert json_data["scores"]["player2"] == scores["player2"]