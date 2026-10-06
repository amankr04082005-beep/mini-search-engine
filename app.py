from flask import Flask, render_template, request, jsonify

from database import init_db
from index import add_document, delete_document, get_all_documents, search

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"results": [], "query": ""})
    results = search(query)
    return jsonify({"results": results, "query": query})


@app.route("/api/documents", methods=["GET"])
def api_list_documents():
    docs = get_all_documents()
    return jsonify(
        [{"id": d["id"], "title": d["title"], "content": d["content"]} for d in docs]
    )


@app.route("/api/documents", methods=["POST"])
def api_add_document():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400

    doc_id = add_document(title, content)
    return jsonify({"id": doc_id, "message": "Document added"}), 201


@app.route("/api/documents/<int:doc_id>", methods=["DELETE"])
def api_delete_document(doc_id):
    delete_document(doc_id)
    return jsonify({"message": "Document deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5050)
