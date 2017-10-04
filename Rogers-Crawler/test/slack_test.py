from utils.slack import send_message


def test_slack():
    res = send_message("#monitoring", "Test message")
    assert res.status_code == 200
