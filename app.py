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
    background: linear-gradient(to right, #667eea, #764ba2);
    font-family: Arial, sans-serif;
    text-align:center;
    padding-top:60px;
}

.card{
    background:white;
    width:400px;
    margin:auto;
    padding:25px;
    border-radius:12px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.2);
}

h2{
    color:#333;
}

input[type=file]{
    margin:15px 0;
}

button{
    background:#667eea;
    color:white;
    border:none;
    padding:10px 20px;
    border-radius:6px;
    cursor:pointer;
}

button:hover{
    background:#5563c1;
}

.result{
    margin-top:15px;
    font-weight:bold;
    color:#444;
}
</style>
</head>

<body>

<div class="card">
<h2>DeepFake Metadata Cleaner</h2>

<form method="post" enctype="multipart/form-data">
<input type="file" name="image" required><br>
<button type="submit">Check Image</button>
</form>

<div class="result">
{{result}}
</div>

</div>

</body>
</html>
""", result=result)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
