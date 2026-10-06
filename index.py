"""Tokenizing, indexing, and TF-IDF search over the documents table."""
import math
import re
from collections import Counter

from database import get_connection

# A short, standard stopword list -- common words that carry little meaning
# for search and would otherwise dominate every document's word list.
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
    "to", "was", "were", "will", "with", "this", "these", "those",
    "or", "but", "not", "can", "they", "their", "you", "your",
}


def tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, split into words, drop stopwords."""
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def add_document(title: str, content: str) -> int:
    """Insert a document and update the inverted index for it."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO documents (title, content) VALUES (?, ?)", (title, content)
    )
    doc_id = cur.lastrowid

    tokens = tokenize(f"{title} {content}")
    term_freq = Counter(tokens)

    cur.executemany(
        "INSERT INTO inverted_index (word, doc_id, term_freq) VALUES (?, ?, ?)",
        [(word, doc_id, freq) for word, freq in term_freq.items()],
    )

    conn.commit()
    conn.close()
    return doc_id


def delete_document(doc_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM inverted_index WHERE doc_id = ?", (doc_id,))
    cur.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()


def get_all_documents():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, title, content FROM documents ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows


def _total_doc_count(cur) -> int:
    return cur.execute("SELECT COUNT(*) AS c FROM documents").fetchone()["c"]


def search(query: str, limit: int = 10):
    """
    Rank documents for a query using TF-IDF.

    For each query word:
      tf  = how often the word appears in a document (already stored)
      idf = log(total_docs / docs_containing_word)
    A document's score is the sum of tf*idf over all matching query words.
    This rewards documents that use the query words often, while words that
    appear in almost every document (and so distinguish little) count less.
    """
    conn = get_connection()
    cur = conn.cursor()

    total_docs = _total_doc_count(cur)
    if total_docs == 0:
        conn.close()
        return []

    query_words = tokenize(query)
    if not query_words:
        conn.close()
        return []

    scores: dict[int, float] = {}
    matched_words: dict[int, set] = {}

    for word in set(query_words):
        rows = cur.execute(
            "SELECT doc_id, term_freq FROM inverted_index WHERE word = ?",
            (word,),
        ).fetchall()

        if not rows:
            continue

        doc_freq = len(rows)  # how many documents contain this word at all
        idf = math.log((total_docs + 1) / (doc_freq + 1)) + 1  # smoothed idf

        for row in rows:
            doc_id = row["doc_id"]
            tf = row["term_freq"]
            scores[doc_id] = scores.get(doc_id, 0.0) + tf * idf
            matched_words.setdefault(doc_id, set()).add(word)

    if not scores:
        conn.close()
        return []

    ranked_ids = sorted(scores, key=lambda d: scores[d], reverse=True)[:limit]

    placeholders = ",".join("?" * len(ranked_ids))
    docs = cur.execute(
        f"SELECT id, title, content FROM documents WHERE id IN ({placeholders})",
        ranked_ids,
    ).fetchall()
    docs_by_id = {d["id"]: d for d in docs}

    conn.close()

    results = []
    for doc_id in ranked_ids:
        doc = docs_by_id[doc_id]
        snippet = doc["content"][:220] + ("..." if len(doc["content"]) > 220 else "")
        results.append(
            {
                "id": doc_id,
                "title": doc["title"],
                "snippet": snippet,
                "score": round(scores[doc_id], 3),
                "matched_words": sorted(matched_words[doc_id]),
            }
        )
    return results
