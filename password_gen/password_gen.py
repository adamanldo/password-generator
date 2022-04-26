import json
import secrets
import string
import copy
from typing import List
import collections

class PasswordGenerator:

    def __init__(self, config: str):
        try:
            self.config = json.loads(config)
        except json.JSONDecodeError:
            print("Could not load configuration file.")
            raise

        if 'length' in self.config:
            self.length = self.config['length']
        else:
            self.length = 12

        self.all_allowed_characters = []
        self.allowed_characters = {'group': {}, 'constant': {}}
        if 'groups' in self.config['allowed_characters']:
            for group_name, value in self.config['allowed_characters']['groups'].items():
                self.allowed_characters['group'][group_name] = value
                self.all_allowed_characters.extend([v for v in value])

        if 'constants' in self.config['allowed_characters']:
            for constant_name, value in self.config['allowed_characters']['constants'].items():
                constant_string = getattr(string, value)
                self.allowed_characters['constant'][constant_name] = constant_string
                self.all_allowed_characters.extend([v for v in constant_string])

        if 'required_characters' in self.config:
            self.required_characters = []
            for req in self.config['required_characters']:
                self.required_characters.append(req)

        if 'violations' in self.config:
            self.violations = {v:self.config['violations'][v] for v in self.config['violations']}

    def new(self) -> str:

        char_set = []

        # Prevent occurrences violation by keeping count
        # of characters added and removing them from allowed
        # characters if we reach one less than the max
        _all_allowed_characters = copy.deepcopy(self.all_allowed_characters)
        count = {c:0 for c in _all_allowed_characters}

        if self.required_characters:
            for req in self.required_characters:
                num, group_or_constant, name = req
                _associated_allowed_chars = list(self.allowed_characters[group_or_constant][name])
                for _ in range(num):
                    choice = secrets.choice(_associated_allowed_chars)
                    count[choice] += 1
                    char_set.append(choice)
                    if count[choice] == self.violations['occurrence'] - 1:
                        _associated_allowed_chars.remove(choice)
                        _all_allowed_characters.remove(choice)

        while len(char_set) < self.length:
            choice = secrets.choice(_all_allowed_characters)
            count[choice] += 1
            char_set.append(choice)
            if count[choice] == self.violations['occurrence'] - 1:
                _all_allowed_characters.remove(choice)

        # All other violations can be avoided by randomly shuffling chars
        while True:
            self.random_shuffle(char_set)
            if self.check_violations(char_set):
                break

        return ''.join(char_set)

    def allowed(self, password: str) -> bool:
        return self.check_violations(list(password))

    def random_shuffle(self, potential_password: List[str]) -> None:
        # Adapted from the in-place shuffle method from the random library,
        # but uses cryptographically strong random numbers as index
        # https://github.com/python/cpython/blob/3.10/Lib/random.py#L380
        for i in reversed(range(1, len(potential_password))):
            j = secrets.randbelow(i + 1)
            potential_password[i], potential_password[j] = potential_password[j], potential_password[i]

    def check_violations(self, potential_password: List[str]) -> bool:

        if len(potential_password) < self.length:
            return False

        if any(char not in self.all_allowed_characters for char in potential_password):
            return False

        if 'consecutive' in self.violations.keys():
            m = self.violations['consecutive']
            cur, count = None, 0
            for char in potential_password:
                if char == cur:
                    count += 1
                else:
                    cur, count = char, 1
                if count == m:
                    return False
        
        if 'occurrence' in self.violations.keys():
            count = collections.Counter(potential_password)
            if any([c for c in count.values() if c >= self.violations['occurrence']]):
                return False

        if 'sequential' in self.violations.keys():
            for seq in self.violations['sequential']:
                num, group_or_constant, name = seq
                reference_group = list(self.allowed_characters[group_or_constant][name])
                reference_group_reversed = list(reversed(self.allowed_characters[group_or_constant][name]))
                for i in range(len(reference_group) - num + 1):
                    v = reference_group[i:i+num]
                    for j in range(len(potential_password) - num + 1):
                        if potential_password[j:j+num] == v:
                            return False
                
                for i in range(len(reference_group_reversed) - num + 1):
                    v = reference_group_reversed[i:i+num]
                    for j in range(len(potential_password) - num + 1):
                        if potential_password[j:j+num] == v:
                            return False

        if 'verboten' in self.violations.keys():
            temp = ''.join(potential_password)
            for word in self.violations['verboten']:
                if word in temp:
                    return False

        return True