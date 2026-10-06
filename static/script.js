const queryInput = document.getElementById("query");
const searchBtn = document.getElementById("search-btn");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");

const titleInput = document.getElementById("doc-title");
const contentInput = document.getElementById("doc-content");
const addBtn = document.getElementById("add-btn");
const addStatusEl = document.getElementById("add-status");

const documentsEl = document.getElementById("documents");
const docCountEl = document.getElementById("doc-count");

async function runSearch() {
  const q = queryInput.value.trim();
  if (!q) {
    statusEl.textContent = "";
    resultsEl.innerHTML = "";
    return;
  }

  statusEl.textContent = "Searching...";
  try {
    const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
    const data = await res.json();

    if (data.results.length === 0) {
      statusEl.textContent = `No documents matched "${q}".`;
      resultsEl.innerHTML = "";
      return;
    }

    statusEl.textContent = `${data.results.length} result(s) for "${q}"`;
    resultsEl.innerHTML = data.results
      .map(
        (r) => `
        <li class="result-item">
          <h3>${escapeHtml(r.title)}</h3>
          <p>${escapeHtml(r.snippet)}</p>
          <span class="result-meta">score ${r.score} · matched: ${r.matched_words.join(", ")}</span>
        </li>`
      )
      .join("");
  } catch (err) {
    statusEl.textContent = "Could not reach the server.";
  }
}

async function loadDocuments() {
  const res = await fetch("/api/documents");
  const docs = await res.json();
  docCountEl.textContent = docs.length;
  documentsEl.innerHTML = docs
    .map(
      (d) => `
      <li class="doc-item">
        <div>
          <strong>${escapeHtml(d.title)}</strong>
          <p>${escapeHtml(d.content.slice(0, 100))}${d.content.length > 100 ? "..." : ""}</p>
        </div>
        <button class="delete-btn" data-id="${d.id}">Delete</button>
      </li>`
    )
    .join("");

  documentsEl.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await fetch(`/api/documents/${btn.dataset.id}`, { method: "DELETE" });
      loadDocuments();
    });
  });
}

async function addDocument() {
  const title = titleInput.value.trim();
  const content = contentInput.value.trim();

  if (!title || !content) {
    addStatusEl.textContent = "Title and content are both required.";
    return;
  }

  addStatusEl.textContent = "Adding...";
  const res = await fetch("/api/documents", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content }),
  });

  if (res.ok) {
    addStatusEl.textContent = "Document added.";
    titleInput.value = "";
    contentInput.value = "";
    loadDocuments();
  } else {
    const data = await res.json().catch(() => ({}));
    addStatusEl.textContent = data.message || "Could not add document.";
  }
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

searchBtn.addEventListener("click", runSearch);
queryInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") runSearch();
});
addBtn.addEventListener("click", addDocument);

loadDocuments();
