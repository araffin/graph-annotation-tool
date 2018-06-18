Graph Annotator with Flask and Javascript
==================

It is an annotation web app built on that project : [https://github.com/kyamagu/js-graph-annotator](https://github.com/kyamagu/js-graph-annotator)

[Online demo of the original project](http://kyamagu.github.io/js-graph-annotator/).

![screenshot](static/img/demo_annotation.png)

### Dependencies
- Flask
- numpy

### Instructions
1. Put your images (.jpg) in a folder in the directory `static/img/`

2. Launch the server passing as argument the name of the dataset folder (here `test_dataset`)

```
python app.py -n test_dataset
```

3. Start labelling at [http://127.0.0.1:5000/](http://127.0.0.1:5000/) !
The labels are saved when passing to previous/next image, the labels are stored in the `data/` folder.
