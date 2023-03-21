from flask import Flask, send_file, request
from werkzeug.utils import secure_filename
import os
from transformers import AutoImageProcessor, AutoModelForObjectDetection
import torch
from PIL import Image

app = Flask(__name__, static_folder="web", static_url_path="/")
app.config['UPLOAD_FOLDER'] = "web/uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16MB


@app.route("/")
def hello_world():
    return send_file("web/index.html")

@app.route("/model/image", methods=["POST"])
def classify_image():
    if request.method == 'POST':
        image = Image.open(request.files['file'])

        image_processor = AutoImageProcessor.from_pretrained("hustvl/yolos-tiny")
        model = AutoModelForObjectDetection.from_pretrained("hustvl/yolos-tiny")

        inputs = image_processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # convert outputs (bounding boxes and class logits) to COCO API
        target_sizes = torch.tensor([image.size[::-1]])
        results = image_processor.post_process_object_detection(outputs, threshold=0.85, target_sizes=target_sizes)[0]

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            print(
                f"Detected {model.config.id2label[label.item()]} with confidence "
                f"{round(score.item(), 3)} at location {box}"
            )
        return "Image classified successfully"

@app.route("/upload", methods=["POST"])
def image_upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return "File uploaded successfully"
  
if __name__ == "__main__":
    app.run()