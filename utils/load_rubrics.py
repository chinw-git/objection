# -----------------------------
# Load rubrics text file (no vector store creation)
# -----------------------------

rubrics_path = "data/rubrics.txt"

def load_rubrics():
    with open(rubrics_path, "r", encoding="utf-8") as f:
        return f.read()