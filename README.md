# TriggerFinder

This repository implements a Google Chrome extension that censors words and phrases on webpages that can be triggering to people with emetophobia (a specific phobia of vomiting).

This application is made up of a server (in the "backend" folder) and a client (in the "frontent" folder). The "results" folder contains images with the results and the application in action. The "Google Colab files" folder contains the Colab notebook that creates the word2vec pickle file used for embedding. If you already have this file, skip the Google Colab stepx.

### Backend:
- Prerequisites: Python 3.8.0, Keras 2.0, Tensorflow 2.2.0, NLTK 3.5, Numpy 1.18.4
- To obtain the word2vec file, either:
1. Try downloading it from this WeTransfer: https://we.tl/t-3esKK2SQHv , or
2. If the transfer doesn't work:
    - *Thanks to akshayuppal3 and the "language_vision" repository for this part*
    - Go to Google Colab, upload and open the Trigger_Finder.ipynb notebook (from the "Google Colab files" folder)
    - Download the GloVe 100-dimensional embeddings from the GloVe webside (see References)
    - Upload the glove file to Google Colab (this will take some time)
    - Run each piece of code in the notebook and wait for the pickle file to be created
    - Download the pickle file (this will take some time)
- Create folders such that this path exists: "backend/TriggerFinder/*PretrainedUtils/w2v*"
- Copy and paste the pickle file in the w2v folder you created

- To start the server:
    - install flask 
    ```
    pip install flask
    ```
    - create a python virtual environment in "backend/TriggerFinder" 
    ```
    (Windows) python -m venv venv
    (Ubuntu) python3 -m venv venv
    ```
    - start the virtual environment 
    ```
    (Windows) venv\Scripts\activate
    (Ubuntu) source venv/bin/activate
    ```
    - set the main file: 
    ```
    (Windows) set FLASK_APP=main.py
    (Ubuntu) export FLASK_APP=main.py
    ```
    - start the server (this will take some time)
    ```
    flask run
    ```

### Frontend:
- Install the Moesif Origins & CORS Changer Chrome Extension and turn it on (Remember to turn it off when not using the extension because it will affect Youtube and other websites)
- On Chrome, go to chrome://extensions
- Turn on "Developer mode" (top right corner)
- Click on "Load unpacked", navigate to the "TriggerFinder/frontend/TriggerFinderExtension" folder and click on "Select Folder"
- The extension will be added in the top right corner of the browser. Click on it and toggle it on and off from the on/off button.

### References:
- GloVe Twitter Embeddings: https://nlp.stanford.edu/projects/glove/
