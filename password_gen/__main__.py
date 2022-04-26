import sys
from .password_from_config_file import password_from_config_file

if len(sys.argv) < 2:
    print("No config file provided.")
    sys.exit(1)

if len(sys.argv) > 2:
    print("Only one config file can be provided at a time.")
    sys.exit(1)

config_path = sys.argv[1]

print(password_from_config_file(config_path))
