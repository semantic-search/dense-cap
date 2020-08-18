from fastapi import FastAPI, File, UploadFile, Form
import json
import subprocess
import os

app = FastAPI()


result_dir = "vis/data/"
result_file = result_dir+"results.json"

@app.post("/uploadfile/")
def create_upload_file(file: UploadFile = File(...), image_id: str = Form(...)):
    file_name = file.filename
    with open(file_name, 'wb') as f:
        f.write(file.file.read())
    
    
    
    subprocess.call(["th", "run_model.lua", "-input_image", file_name])
    
    
    
    with open(result_file) as json_file:
        data = json.load(json_file)
    captions = []
    scores = []
    for items in data:
        if items == "results":
            for key, val in data[items][0].items():
                if key == "scores":
                    scores.append(val)
                elif key == "captions":
                    captions.append(val)
    captions = captions[0]
    scores = scores[0]
    response = {
        "image_id" : image_id,
        "captions" : captions,
        "scores": scores
    }

    os.remove(file_name)
    os.remove(result_dir + file_name)
    os.remove(result_file)
    return response
