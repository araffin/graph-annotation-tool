Graph Annotator with Flask and Javascript
==================

It is an annotation web app built on that project : [https://github.com/kyamagu/js-graph-annotator](https://github.com/kyamagu/js-graph-annotator)

[Online demo of the original project](http://kyamagu.github.io/js-graph-annotator/).

![screenshot](static/img/demo_annotation.png)

### Dependencies
- Flask
- numpy
- gunicorn for multiprocess server

### Instructions
1. Put your images (.jpg) in a folder in the directory `static/img/`

2. Edit the config file `config.json` to match your dataset.
If your dataset folder is named `my_dataset` (path: `static/img/my_dataset/`):
```json
{
  "DATASET_NAME": "my_dataset"
}
```

### Launch the server

```
python app.py
```

or
```
./start.sh
```
