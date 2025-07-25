from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>LianBot Document Explorer</title>
<style>
	body { background: #111; color: #0f0; font-family: monospace; }
	#output { white-space: pre-wrap; max-height: 400px; overflow-y: auto; border: 1px solid #0f0; padding: 10px; margin-bottom: 10px; }
	input, button { padding: 10px; width: 100%; margin-bottom: 10px; background: #000; color: #0f0; border: 1px solid #0f0; }
</style>
</head>
<body>
<h1>LianBot Document Explorer</h1>
<input id="path" placeholder="Enter root folder path, e.g. J:\\root\\tema" />
<input id="query" placeholder="Enter search term (optional)" />
<button onclick="search()">Search Documents</button>
<div id="output"></div>

<script>
function search() {
	const path = document.getElementById('path').value.trim();
	const query = document.getElementById('query').value.trim();
	if (!path) {
	alert('Please enter a root folder path.');
	return;
	}
	fetch('/list_documents', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({root_path: path, search_query: query})
	})
	.then(res => res.json())
	.then(data => {
    const output = document.getElementById('output');
    if (data.error) {
    	output.textContent = "Error: " + data.error;
    } else if (data.documents.length === 0) {
	output.textContent = "No documents found.";
    } else {
    output.textContent = data.documents.join('\\n');
    }
	});
}
</script>
</body>
</html>
"""

document_extensions = {
    ".pdf",
    ".docx",
    ".doc",
    ".txt",
    ".xlsx",
    ".xls",
    ".pptx",
    ".ppt",
}


def list_documents(root_dir):
    docs = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            ext = os.path.splitext(file)[1].lower()
            if ext in document_extensions:
                full_path = os.path.join(dirpath, file)
                docs.append(full_path)
    return docs


def query_documents(doc_list, query):
    if not query:
        return doc_list
    query_lower = query.lower()
    return [doc for doc in doc_list if query_lower in doc.lower()]


@app.route("/")
def index():
    return render_template_string(html)


@app.route("/list_documents", methods=["POST"])
def list_documents_route():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json(force=True)

        root_path = data.get("root_path", "").strip()
        search_query = data.get("search_query", "").strip()

        if not root_path or not os.path.exists(root_path):
            return jsonify({"error": f"Invalid path: {root_path}"}), 400

        doc_list = list_documents(root_path)
        filtered = query_documents(doc_list, search_query)

        return jsonify({"documents": filtered})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
