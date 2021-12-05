# az-py-cli
Pythonic wrapper for az cli

Requires Python 3

## Install requirements
Note: We recommend first creating a virtual env and activating it
```
pip install -r requirements.txt
```

## Usage
```
% python3
>>> import pyaz
>>> result = pyaz.version()
>>> print(result)
{'azure-cli': '2.28.1', 'azure-cli-core': '2.28.1', 'azure-cli-telemetry': '1.0.6', 'extensions': {}}
```

## How to generate the code
By default the code will be generated in the "output" directory.
```
% python generate_code.py
generating code module for: pyaz/acr
generating code module for: pyaz
generating code module for: pyaz/acr/credential
generating code module for: pyaz/acr/repository
generating code module for: pyaz/acr/webhook
generating code module for: pyaz/acr/replication
... (list shortened)

```

## Run the tests
```
python -m unittest test.test_integration
```
