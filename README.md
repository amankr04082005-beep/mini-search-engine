# Mini Search Engine

A small search engine built from scratch in Python/Flask: documents are tokenized, stored in an **inverted index**, and ranked with **TF-IDF** scoring at query time.

## Features
- Add/delete text documents (title + content)
- Inverted index: maps each word to the documents containing it, with term frequency
- TF-IDF ranking: scores documents by how distinctively they match the query
- Simple web UI: search box + live results, plus a document manager

## Tech Stack
Python, Flask, SQLite (no external APIs, no API keys needed)

## Run Locally
```bash
pip install -r requirements.txt
python seed_data.py   # loads 10 sample documents (one-time)
python app.py
```
Open http://localhost:5050

## How it works
1. **Indexing** (`index.py: add_document`): each document's title+content is tokenized (lowercased, punctuation stripped, stopwords removed), and for every unique word we store how many times it appears in that document (term frequency) in the `inverted_index` table.
2. **Search** (`index.py: search`): for each word in the query, we look up every document containing it, and score it as `tf * idf`, where `idf = log((N+1)/(doc_freq+1)) + 1`. Words that appear in many documents (like "the") contribute less; words that are rare and frequent in a specific document contribute more. Scores are summed per document and sorted descending.

## API
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/search?q=... | Search documents, TF-IDF ranked |
| GET | /api/documents | List all documents |
| POST | /api/documents | Add a document `{title, content}` |
| DELETE | /api/documents/:id | Delete a document |
