import sqlite3

DB_PATH = "search.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """
    )

    # inverted index: for every (word, doc_id) pair, how many times the word
    # appears in that document (term frequency).
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS inverted_index (
            word TEXT NOT NULL,
            doc_id INTEGER NOT NULL,
            term_freq INTEGER NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documents (id) ON DELETE CASCADE,
            PRIMARY KEY (word, doc_id)
        )
        """
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_inverted_word ON inverted_index (word)"
    )

    conn.commit()
    conn.close()
