# Liveblog

## Requirements

- Python 3
- pip
- SQLite

## How to use

### Run the website

```sh
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
$ python3 run.py
```

### Environment variables

* GLOBAL_KEYPASS: the password used to authorize new posts

## Documentation and testing

### Documentation

The documentation can be generated in the docs directory with

```sh
$ pdoc -o docs/ app
```

### Testsuite

The first step is to set the environment variables to their test values:

* GLOBAL_KEYPASS - `44ea01b1aede885735cb3284076137543f7a264cbddc527fc1c8af2116bf6cd7`
  * This string corresponds to sha256(test_keypass)

The final step is to launch the testsuite with

```sh
$ pytest
```
