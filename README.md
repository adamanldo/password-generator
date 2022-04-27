# Password Generator

## IMPORTANT: I would not use this library to generate actual passwords. It's purely a coding exercise and hasn't been reviewed for security vulnerabilities.


This was the result of a coding challenge in which the prompt was to create a command line app/library in Python to generate a random password based on a provided JSON configuration file. The full specification can be found [here](specifications.txt).

## Installation and Usage

To install the package: clone the repo, change directory into the project folder, and run the setup.py script:
```
git clone https://github.com/adamanldo/password-generator.git
cd password-generator
python3 setup.py install
```

### Command line usage
The most straightforward way to generate a password is on the command line, using one of the two provided configuration files:
```bash
python -m password_gen config_examples/config.json
```
This will print a random password that matches the specification in the config.json file to stdout.

### Library usage
Alternatively, you can use it as part of a Python script of your own:
```python
from password_gen import PasswordGenerator

with open('config_examples/config.json', 'rt') as f:
    config = f.read()

pgen = PasswordGenerator(config)

new_password = pgen.new()
```


## JSON Configuration Options

The most detailed explanation of all the configuration options can be found in the [specification](specifications.txt), but here is a summary:

There are 4 possible key-value pairs: length, allowed_characters, required_characters, and violations. The only section that needs to be present in a config file is "allowed_characters". Here is a sample of a full configuration file:

```json
{
    "length": 12,

    "allowed_characters": {
        "groups": {
            "special": "!@#$%&*()[]{}"
        },
        "constants": {
            "lowercase": "ascii_lowercase",
            "uppercase": "ascii_uppercase",
            "numbers": "digits"
        }
    },

    "required_characters" : [
        [1, "group", "special"],
        [2, "constant", "uppercase"],
        [2, "constant", "lowercase"],
        [2, "constant", "numbers"]
    ],

    "violations" : {
        "consecutive": 2,
        "occurrence": 2,
        "sequential": [
            [3, "constant", "numbers"],
            [3, "constant", "uppercase"],
            [3, "constant", "lowercase"]
        ],
        "verboten": [
            "password",
            "topsecret",
            "foobar",
            "spam"
        ]
    }
}
```