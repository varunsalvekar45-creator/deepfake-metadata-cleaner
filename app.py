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
<!DOCTYPE html>
<html>
<head>
<title>DeepFake Metadata Cleaner</title>
<style>
body{
background:#f4f4f4;
font-family:Arial;
text-align:center;
padding-top:50px;
}

.card{
background:white;
width:400px;
margin:auto;
padding:20px;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,0.2);
}

button{
background:#007bff;
color:white;
padding:10px;
border:none;
border-radius:5px;
}
</style>
</head>

<body>

<div class="card">
<h2>DeepFake Metadata Cleaner</h2>

<form method="post" enctype="multipart/form-data">
<input type="file" name="image"><br><br>
<button type="submit">Check</button>
</form>

<p>{{result}}</p>

</div>

</body>
</html>
""", result=result)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
