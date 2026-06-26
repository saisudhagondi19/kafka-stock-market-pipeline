import json

def test_message_is_valid_json():
    message = '{"ticker": "AAPL", "price": 182.5, "volume": 1000}'
    data = json.loads(message)
    assert isinstance(data, dict)

def test_message_has_required_fields():
    message = {"ticker": "AAPL", "price": 182.5, "volume": 1000}
    assert "ticker" in message
    assert "price" in message
    assert "volume" in message

def test_price_is_positive():
    message = {"ticker": "AAPL", "price": 182.5, "volume": 1000}
    assert message["price"] > 0
