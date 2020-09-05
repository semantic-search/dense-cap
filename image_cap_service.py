import subprocess
import json
import os
result_dir = "vis/data/"
result_file = result_dir+"results.json"


def predict(file_name, doc=False):
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
    if doc:
        response = {
            "captions": captions,
            "scores": scores
        }
    else:
        response = {
            "file_name": file_name,
            "captions": captions,
            "scores": scores
        }


    os.remove(file_name)
    os.remove(result_dir + file_name)
    os.remove(result_file)
    return response

