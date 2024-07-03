from streamlit.testing.v1 import AppTest


def test_the_app_loads():
    at = AppTest.from_file("Cora.py").run(timeout=10_000)

    assert at.title != ""
