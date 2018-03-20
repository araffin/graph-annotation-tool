import json
import os
import numpy as np

from flask import Flask, request, session, render_template, jsonify


app = Flask(__name__)
# app.config.from_object('api.config')
app.config['DEBUG'] = True
port = 5000

images = ['demo.jpg', 'example.jpg']
labels = {}

@app.route("/", methods=["GET"])
def home():
    idx = int(request.args.get('idx', 0))
    idx = np.clip(idx, 0, len(images) - 1)
    image = images[idx]
    percent = round(100 * ((idx + 1) / len(images)), 0)
    return render_template('home.html', idx=idx, total=len(images), image=images[idx], percent=percent)

@app.route("/save_labels", methods=["POST"])
def save_labels():
    new_labels = json.loads(request.data.decode('utf8'))
    idx = request.form.get('idx')
    print(new_labels)
    global labels

    # with open('data/skills_remove_list.json', 'w') as f:
    #     json.dump(labels, f)
    return jsonify(status="ok")

if __name__ == '__main__':
    app.run(port=port)
