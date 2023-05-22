import os
import re
from collections import defaultdict
from functools import reduce
from tomlkit import parse, dumps, table

MODULE_TOML_REGEX = r"_(?P<module>[^\W_]+)_(?P<base>\w+).toml"
REMOVE_COMMAND = r"#\s*\[REMOVE\]"
EXTRACT_COMMAND = r"#\s*\[EXTRACT\]"
EXTEND_COMMAND = r"#\s*\[EXTEND\]"
DELETE_COMMAND = r"#\s*\[DELETE\]"


def list_toml_modules():
    modules = defaultdict(list)

    with os.scandir(".") as it:
        for entry in it:
            match = re.match(MODULE_TOML_REGEX, entry.name)
            if match:
                parent_file = f"{match.group('base')}.toml"
                parent_file_path = os.path.join(".", parent_file)
                modules[parent_file_path].append(entry.path)

    return modules


def safe_toml_open(path):
    with open(path, 'r') as f:
        return parse(f.read())


def safe_toml_write(path, toml_content):
    with open(path, 'w') as f:
        f.write(dumps(toml_content))


def parse_item(toml_item):
    parsed_items = []
    for k, v in toml_item.items():
        if v.is_table():
            parsed_items.extend([[k] + i if isinstance(i, list) else [k] + [i] for i in parse_item(v)])
        else:
            parsed_items.append(k)

    return parsed_items


def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


def assign_item(path, parent_toml, child_toml):
    cur_parent_path = parent_toml
    cur_child_path = child_toml
    while len(path) > 1:
        key = path[0]
        cur_child_path = cur_child_path.get(key)
        if not cur_parent_path.get(key):
            new_table = table()
            cur_parent_path.add(key, new_table)
            cur_parent_path = cur_parent_path.get(key)
        else:
            cur_parent_path = cur_parent_path.get(key)

        path.pop(0)

    key_name = path[-1]
    key_value = cur_child_path.get(key_name)
    comt = key_value.trivia.comment

    if comt:
        if re.match(DELETE_COMMAND, comt):
            cur_parent_path.pop(key_name)
        elif re.match(EXTEND_COMMAND, comt):
            cur_parent_path[key_name].extend(cur_child_path[key_name])
        elif re.match(REMOVE_COMMAND, comt):
            cur_parent_path[key_name].remove(cur_child_path[key_name])
        elif re.match(EXTRACT_COMMAND, comt):
            for i in cur_child_path[key_name]:
                cur_parent_path[key_name].remove(i)
    else:
        cur_parent_path[key_name] = cur_child_path[key_name]


def process_toml_modules(parent, children):
    parent_toml = safe_toml_open(parent)

    for child in children:
        child_toml = safe_toml_open(child)
        items = parse_item(child_toml)

        for path in items:
            if isinstance(path, str):
                path = [path]
            assign_item(path, parent_toml, child_toml)

    safe_toml_write(parent, parent_toml)


def process():
    modules = list_toml_modules()

    for parent, children in modules.items():
        process_toml_modules(parent, children)


process()
