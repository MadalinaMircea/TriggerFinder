# TriggerFinder

This repository implements a Google Chrome extension that censors words and phrases on webpages that can be triggering to people with emetophobia (a specific phobia of vomiting).

This application is made up of a server (in the "backend" folder) and a client (in the "frontent" folder). The "results" folder contains images with the results and the application in action. The "Google Colab files" folder contains the Colab notebook that creates the word2vec pickle file used for embedding. If you already have this file, skip the Google Colab stepx.

### Backend:
- Prerequisites: Python 3.8.0, Keras 2.0, Tensorflow 2.2.0, NLTK 3.5, Numpy 1.18.4
- Obtain the word2vec file:
    - Try downloading it from this WeTransfer: https://we.tl/t-3esKK2SQHv


### Frontend:

### References:
- GloVe Twitter Embeddings: https://nlp.stanford.edu/projects/glove/
