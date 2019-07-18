# Iris model example search app

This is an example application that passes over all required steps to train a model 
and make prediction on example dataset.

## Running the app
Install auger.ai from this repo:
```
pip install -e .[all]
```
or (optionally) pypi:

```
pip install auger.ai
```
We strongly encourage using virtualenv.
Download your credentials file from Auger.AI cloud or sign in using augerai CLI:
```
augerai auth login
```

Run the app:
```
python app.py
```
Running the app may take a while, depending on dataset and training preferences. 
For Iris it's usually less than 10 minutes. After train and prediction finished, your result will be in `iris_data_test_predict.csv` file