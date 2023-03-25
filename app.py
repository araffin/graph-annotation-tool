import argparse
import json
import os
from typing import List, Dict

import numpy as np
from flask import Flask, jsonify, render_template, request


class MainApp:
    images_path: List[str]
    images: List[str]
    labels: Dict[str, List[int]]

    def __init__(self, dataset_name: str = "test_dataset", port: int = 5000) -> None:
        self.dataset_name = dataset_name
        self.dataset_folder = f"static/img/{self.dataset_name}/"
        self.app = Flask(__name__)
        self.app.config["DEBUG"] = True
        self.load_images()
        self.port = port

        # Register routes
        self.app.add_url_rule("/", "home", self.home, methods=["GET"])
        self.app.add_url_rule(
            "/save_labels", "save_labels", self.save_labels, methods=["POST"]
        )
        self.app.add_url_rule("/online", "online", self.online, methods=["GET"])

    def run(self) -> None:
        self.app.run(port=self.port)

    def load_images(self) -> None:
        self.images = [f for f in os.listdir(self.dataset_folder) if f.endswith(".jpg")]
        self.images.sort(key=lambda name: int(name.split(".jpg")[0]))
        self.images_path = [self.dataset_folder + im for im in self.images]
        self.labels = {}
        try:
            with open(f"data/{self.dataset_name}_labels.json") as f:
                self.labels = json.load(f)
        except OSError:
            pass

    def home(self) -> str:
        idx = int(request.args.get("idx", 0))
        idx = np.clip(idx, 0, len(self.images) - 1)
        image = self.images_path[idx]
        percent = round(100 * ((idx + 1) / len(self.images)), 0)
        label: List[int] = self.labels.get(self.images[idx], [])
        # if label is None:
        #     # get previous image label
        #     label = labels.get(self.images[idx - 1], [])
        return render_template(
            "home.html",
            idx=idx,
            total=len(self.images),
            image=image,
            percent=percent,
            label=label,
        )

    def save_labels(self):
        label = json.loads(request.data.decode("utf8"))
        key = self.images[int(label["idx"])]
        # Delete incomplete labels
        if None in label["values"] and key in self.labels:
            del self.labels[key]
        else:
            # Save only labels with 3 labels (3 points)
            if len(label["values"]) == 3:
                self.labels[key] = label["values"]
        with open(f"data/{self.dataset_name}_labels.json", "w") as f:
            json.dump(self.labels, f)
        return jsonify(status="ok", label=label)

    def online(self) -> str:
        image = self.images_path[0]
        percent = 0
        label: List[int] = []
        return render_template(
            "online.html",
            idx=0,
            total=len(self.images),
            image=image,
            percent=percent,
            label=label,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a line detector")
    parser.add_argument(
        "-n", "--name", help="Dataset name", type=str, default="test_dataset"
    )
    args = parser.parse_args()
    app = MainApp(args.name)
    app.run()
