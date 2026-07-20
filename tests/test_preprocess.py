from utils.preprocess import clean_text
from utils.preprocess import build_document


def test_clean_text_lowercase():

    assert clean_text("HELLO") == "hello"


def test_clean_text_newlines():

    assert clean_text("Hello\nWorld") == "hello world"


def test_clean_text_spaces():

    assert clean_text("Hello     World") == "hello world"


def test_clean_text_none():

    assert clean_text(None) == ""


def test_build_document():

    row = {
        "ExplanatoryNote":
        "Annual Value TOO HIGH"
    }

    assert build_document(row) == "annual value too high"