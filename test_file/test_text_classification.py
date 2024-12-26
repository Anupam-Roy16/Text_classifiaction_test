import pytest
from source.text_classifiaction import ExtendedMessage  
class MockMessage:
    def __init__(self, text):
        self.text = text

@pytest.fixture
def mock_message():
    def create_mock_message(text):
        return MockMessage(text)
    return create_mock_message

@pytest.mark.parametrize(
    "input_text, expected_type",
    [
        ("/","cmd"),
        ("/ ","cmd"),
        ("/start", "cmd"), 
        ("S75Q 123 Jayapataka example", "quote"),  
        ("WARNING: This is a test warning.", "warning"),  
        ("Hello, this is a normal message.", "misc"), 
    ]
)
def test_determine_msg_type(mock_message, input_text, expected_type):
    message = mock_message(input_text)
    ext_msg = ExtendedMessage(message)
    assert ext_msg.msg_type == expected_type
