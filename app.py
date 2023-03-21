from flask import Flask, jsonify, send_file, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_folder="web", static_url_path="/")
app.config['UPLOAD_FOLDER'] = "web/uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16MB


@app.route("/")
def hello_world():
    return send_file("web/index.html")

@app.route("/model/image", methods=["POST"])
def image():
    return "SUCCESS"

@app.route("/upload", methods=["POST"])
def image_upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return "File uploaded successfully"
  
if __name__ == "__main__":
    app.run()