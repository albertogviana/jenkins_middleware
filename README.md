Octopus provide an API to create pipelines on Jenkins.

# Technologies
- Python 3.4
- Flask

# Additional modules
## Virtualenv
`virtualenv` is a tool to create isolated Python environments.
```
pip install virtualenv
```

# How to start?

## Create virtual environment
```
virtualenv flask
```

## Install dependencies

### Development modules
```
flask/bin/pip install -r development-requirements.txt
```
### Production modules
```
flask/bin/pip install -r requirements.txt
```
## Starting the server
```
flask/bin/python3.4 app.py
```

## Running Tests
Without code coverage
```
flask/bin/py.test tests/
```
With code coverage
```
flask/bin/py.test --cov=middleware --cov-report=html tests/ -q -s
```
