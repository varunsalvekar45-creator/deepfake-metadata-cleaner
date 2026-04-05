from flask import Flask, request, render_template_string
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import os

app = Flask(__name__)

def get_metadata(image):
    exif = image._getexif()
    metadata = {}
    if exif:
        for tag, value in exif.items():
            decoded = TAGS.get(tag, tag)
            metadata[decoded] = value
    return metadata

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        file = request.files["image"]
        image = Image.open(file)
        metadata = get_metadata(image)

        if 'GPSInfo' in metadata:
            result = "Sensitive image (GPS found)"
        else:
            result = "No sensitive data found"

    return render_template_string("""
    <h2>DeepFake Metadata Cleaner</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="image">
        <input type="submit">
    </form>
    <p>{{result}}</p>
    """, result=result)

if __name__ == "__main__":
    app.run()