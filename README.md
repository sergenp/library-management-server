### Readme

#### How to run the server

First, intall Pipenv
```
pip install pipenv
```

Install the requirements using Pipenv

`pipenv install`

Once done, create your database, you can change the name of the database in config.toml, and path the database gets created in

```
flask db init
flask db migrate
```
If you make any changes to models, upgrade the database via
```flask db upgrade```

If it fails to create the database, try this:
```
flask db stamp head
flask db migrate
flask db upgrade
````

Be sure to have a "files" folder in your root directory, Resources that takes images will be saved there. (Or you can configure where the images get saved in the config.toml)

With all of these done, simply run your server
```python app.py```
Or you can use flask
```flask run```
this will search for app.py in the current working directory and run it 

This app is created in Python version 3.8.5