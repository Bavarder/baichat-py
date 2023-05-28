# BAIChat API Python

## Installation

### Pypi

``` shell
pip install baichat-py
```

### Codeberg

``` shell
pip install --index-url https://codeberg.org/api/packages/Bavarder/pypi/simple/ baichat-py
```

## Usage

``` python 
from baichat_py import Completion

prompt = "Hello, world!"
for token in Completion.create(prompt):
    print(token, end="", flush=True)
    print("")
```