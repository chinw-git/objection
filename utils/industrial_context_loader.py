from pathlib import Path

def get_rubric_context(query: str = None) -> str:
    """
    Currently reads the full rubric from a flat file.
    Later: swap this out to do a similarity search against vectordb
    and return only the top-k relevant chunks instead of the whole file.
    """
    rubric_path = Path("data/rubric.txt")
    return rubric_path.read_text(encoding="utf-8")