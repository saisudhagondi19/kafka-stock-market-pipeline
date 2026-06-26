import json

def test_message_is_valid_json():
    """Stock market message should be valid JSON"""
    message = '{"ticker": "AAPL", "price": 182.5, "volume": 1000}'
    data = json.loads(message)
    assert isinstance(data, dict)

def test_message_has_required_fields():
    """Message must contain ticker, price, and volume"""
    message = {"ticker": "AAPL", "price": 182.5, "volume": 1000}
    assert "ticker" in message
    assert "price" in message
    assert "volume" in message

def test_price_is_positive():
    """Stock price should always be a positive number"""
    message = {"ticker": "AAPL", "price": 182.5, "volume": 1000}
    assert message["price"] > 0
