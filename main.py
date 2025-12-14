from flask import Flask, send_from_directory, abort, request, render_template
import os

app = Flask(__name__)

# Folders you want to expose
BASE_DIR = os.path.abspath(".")
SERVE_FOLDERS = {
    "css": os.path.join(BASE_DIR, "css"),
    "fonts": os.path.join(BASE_DIR, "fonts"),
    "images": os.path.join(BASE_DIR, "images"),
    "indexes": os.path.join(BASE_DIR, "indexes"),
    "js": os.path.join(BASE_DIR, "js"),
    "scss": os.path.join(BASE_DIR, "scss")
}

@app.route("/<folder>/<path:filename>")
def serve_file(folder, filename):
    if folder not in SERVE_FOLDERS:
        abort(404)

    root = SERVE_FOLDERS[folder]

    # Prevent path traversal
    full_path = os.path.abspath(os.path.join(root, filename))
    if not full_path.startswith(root):
        abort(403)

    return send_from_directory(root, filename)

@app.route("/")
def index():
    host = request.host.split(":")[0]
    domain = host.replace("www.", "")
    template = f"indexes/{domain}.html"
    try:
        return render_template(template)
    except:
        return "Site not found", 404