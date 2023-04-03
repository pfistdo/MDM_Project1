from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from transformers import AutoImageProcessor, AutoModelForObjectDetection
import torch
from PIL import Image

app = Flask(__name__, static_folder="web", static_url_path="/", template_folder="web/templates") 
app.config['UPLOAD_FOLDER'] = "web/uploads" # folder to save uploaded images
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16MB


# Index page
@app.route("/")
def hello_world():
    return render_template("index.html")

# Classify image
@app.route("/model/image", methods=["POST"])
def classify_image():
    if request.method == 'POST':
        image = Image.open(request.files['file'])
        print(image.size)

        image_processor = AutoImageProcessor.from_pretrained("hustvl/yolos-tiny")
        model = AutoModelForObjectDetection.from_pretrained("hustvl/yolos-tiny")

        inputs = image_processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # convert outputs (bounding boxes and class logits) to COCO API
        target_sizes = torch.tensor([image.size[::-1]])
        results = image_processor.post_process_object_detection(outputs, threshold=0.85, target_sizes=target_sizes)[0]

        # save the results as a list with dictionaries
        results_list = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            boxes = [round(i, 2) for i in box.tolist()]
            width = boxes[2] - boxes[0]
            height = boxes[3] - boxes[1]
            boxes = [boxes[0], boxes[1], width, height]
            results_list.append({'score':str(round(score.item(), 3)), 
                        'label': model.config.id2label[label.item()], 
                        'boxes': boxes})
            
        # colors for the bounding boxes
        colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'grey', 'black']
        return render_template("helper/result_boxes.html", img=image, results=results_list, colors=colors)

# Upload image
@app.route("/upload", methods=["POST"])
def image_upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return "File uploaded successfully"
  
if __name__ == "__main__":
    app.run(debug=True)