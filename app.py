from flask import Flask, request, send_from_directory, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML template for file upload
upload_page = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Upload and Access Files</title>
  </head>
  <body>
    <h1>Upload and Access Files</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    <br>
    <h2>Uploaded Files:</h2>
    <ul>
    {% for filename in files %}
        <li><a href="/uploads/{{ filename }}">{{ filename }}</a></li>
    {% endfor %}
    </ul>
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def upload_file():
    # Handles the file upload and shows the upload form with the list of files
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            print(f"File saved to {file_path}")

    # List all files in the upload folder to display on the page
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(upload_page, files=files)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    # Serves the uploaded file for download or view
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")
