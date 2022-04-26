import sys
from .password_gen import PasswordGenerator

def password_from_config_file(filepath: str) -> str:
    try:
        with open(filepath) as f:
            config = f.read()
    except:
        print("File path is invalid, or file cannot be opened.")
        sys.exit(1)
    pgen = PasswordGenerator(config)
    return pgen.new()