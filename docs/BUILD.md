# Enviroment requirements:

- Python 3.11.x
- Miniconda

## Creating isolate env called 'kaggle-competition'

Use the following command after installing conda. 

```
conda create --name kaggle-competition python=3.11
```

Then, use `requriments.reduce` file to add  python package:

```
pip install -r requirements.reduce
``` 

_WARNING_ : Validate that `which pip` is a binary from `~/conda/env/kaggle-competition` folder. 
