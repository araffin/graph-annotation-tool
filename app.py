import argparse
import json
import os

import numpy as np
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
# app.config.from_object('api.config')
app.config["DEBUG"] = True
port = 5000
# Default dataset
DATASET_NAME = "test_dataset"


def load_images(dataset_name):
    global images, labels, images_path, DATASET_NAME
    DATASET_NAME = dataset_name
    DATASET_FOLDER = f"static/img/{DATASET_NAME}/"

    images = [f for f in os.listdir(DATASET_FOLDER) if f.endswith(".jpg")]
    images.sort(key=lambda name: int(name.split(".jpg")[0]))
    images_path = [DATASET_FOLDER + im for im in images]
    labels = {}
    try:
        with open(f"data/{DATASET_NAME}_labels.json") as f:
            labels = json.load(f)
    except OSError:
        pass


@app.route("/", methods=["GET"])
def home():
    idx = int(request.args.get("idx", 0))
    idx = np.clip(idx, 0, len(images) - 1)
    image = images_path[idx]
    percent = round(100 * ((idx + 1) / len(images)), 0)
    label = labels.get(images[idx], [])
    # if label is None:
    #     # get previous image label
    #     label = labels.get(images[idx - 1], [])
    return render_template(
        "home.html",
        idx=idx,
        total=len(images),
        image=image,
        percent=percent,
        label=label,
    )


@app.route("/save_labels", methods=["POST"])
def save_labels():
    label = json.loads(request.data.decode("utf8"))
    global labels
    key = images[int(label["idx"])]
    # Delete incomplete labels
    if None in label["values"] and key in labels:
        del labels[key]
    else:
        # Save only labels with 3 labels (3 points)
        if len(label["values"]) == 3:
            labels[key] = label["values"]
    with open(f"data/{DATASET_NAME}_labels.json", "w") as f:
        json.dump(labels, f)
    return jsonify(status="ok", label=label)


@app.route("/online", methods=["GET"])
def online():
    image = images_path[0]
    percent = 0
    label = []
    return render_template(
        "online.html",
        idx=0,
        total=len(images),
        image=image,
        percent=percent,
        label=label,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a line detector")
    parser.add_argument(
        "-n", "--name", help="Dataset name", type=str, default=DATASET_NAME
    )
    args = parser.parse_args()
    load_images(args.name)
    app.run(port=port)
