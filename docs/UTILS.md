## For export packages

*pip*
```
pip freeze > requirements.txt 
```

*conda*
```
conda env export | grep -v "^prefix: " > environment.yml
``` 
