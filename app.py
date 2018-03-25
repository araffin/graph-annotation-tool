from __future__ import print_function, division
import json
import os
import numpy as np

from flask import Flask, request, session, render_template, jsonify


app = Flask(__name__)
# app.config.from_object('api.config')
app.config['DEBUG'] = True
port = 5000

DATASET_NAME = json.load(open("config.json", "r"))['DATASET_NAME']
DATASET_FOLDER = "static/img/{}/".format(DATASET_NAME)

images = [f for f in os.listdir(DATASET_FOLDER) if f.endswith('.jpg')]
images.sort(key=lambda name: int(name.split('.jpg')[0]))
images_path = [DATASET_FOLDER + im for im in images]
labels = {}
try:
    with open('data/{}_labels.json'.format(DATASET_NAME), 'r') as f:
        labels = json.load(f)
except IOError:
    pass

@app.route("/", methods=["GET"])
def home():
    idx = int(request.args.get('idx', 0))
    idx = np.clip(idx, 0, len(images) - 1)
    image = images_path[idx]
    percent = round(100 * ((idx + 1) / len(images)), 0)
    label = labels.get(images[idx], None)
    if label is None:
        # get previous image label
        label = labels.get(images[idx - 1], [])
    return render_template('home.html', idx=idx, total=len(images), image=image, percent=percent, label=label)

@app.route("/save_labels", methods=["POST"])
def save_labels():
    label = json.loads(request.data.decode('utf8'))
    global labels
    labels[images[int(label['idx'])]] = label['values']
    with open('data/{}_labels.json'.format(DATASET_NAME), 'w') as f:
        json.dump(labels, f)
    return jsonify(status="ok", label=label)

if __name__ == '__main__':
    app.run(port=port)
