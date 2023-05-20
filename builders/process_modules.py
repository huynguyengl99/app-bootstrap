import ast
import fileinput
import os
import re
from collections import defaultdict


def read_file(filename):
    with open(filename) as file:
        return file.read()


def write_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)


def find_node(node, variable_name):
    for assignment in node.body:
        if isinstance(assignment, ast.Assign) and isinstance(assignment.targets[0], ast.Name) and assignment.targets[0].id == variable_name:
            return assignment
    return None


def extend_node(node, variable_name, extended_value):
    for assignment in node.body:
        if isinstance(assignment, ast.Assign) and isinstance(assignment.targets[0], ast.Name) and assignment.targets[0].id == variable_name:
            if isinstance(assignment.value, ast.List | ast.Tuple):
                assignment.value.elts.extend(extended_value.elts)
                return assignment


def evaluate_content(base_tree, extend_content):
    modified_variables_base = set()
    modified_variables_extend = set()
    extend_tree = ast.parse(extend_content)

    for statement in extend_tree.body:
        if isinstance(statement, ast.AugAssign) and isinstance(statement.value, ast.List | ast.Tuple):
            node = extend_node(base_tree, statement.target.id, statement.value)
            if node:
                modified_variables_base.add(node)
                modified_variables_extend.add(statement)
        elif isinstance(statement, ast.Assign):
            existing_node = find_node(base_tree, statement.targets[0].id)
            if existing_node is not None:
                existing_node.value = statement.value
                modified_variables_base.add(existing_node)
                modified_variables_extend.add(statement)
                continue

    return modified_variables_base, modified_variables_extend


def replace_base_modified_variables(base_file, modified_variables):
    replace_lines = [(mod_var.lineno, mod_var.end_lineno, ast.unparse(mod_var)) for mod_var in modified_variables]
    replace_lines.sort()

    with fileinput.input(base_file, inplace=True) as f:
        if replace_lines:
            item = replace_lines.pop(0)

            for line in f:
                ln = fileinput.lineno()
                if ln == item[0]:
                    print(item[2])
                elif ln == item[1]:
                    if replace_lines:
                        item = replace_lines.pop(0)
                    else:
                        item = (0, 0, "")
                elif item[0] < ln < item[1]:
                    continue
                else:
                    print(line, end="")


def get_remain_extend_variables(extend_file, modified_variables_extend):
    remove_lines = {ln for mod_var in modified_variables_extend for ln in range(mod_var.lineno, mod_var.end_lineno + 1)}

    content = []
    with open(extend_file) as f:
        for idx, line in enumerate(f, 1):
            if idx not in remove_lines:
                content.append(line)

    return content


def append_lines_to_base(base_file, lines):
    if lines:
        with open(base_file, "a") as f:
            f.writelines(lines)


def combine_modules(base_file, extend_files):
    if not os.path.exists(base_file):
        return

    base_content = read_file(base_file)
    base_tree = ast.parse(base_content)

    all_modified_base = set()
    all_modified_module = {}

    for ext_file in extend_files:
        if not os.path.exists(ext_file):
            continue

        extend_content = read_file(ext_file)

        modified_variables_base, modified_variables_extend = evaluate_content(base_tree, extend_content)

        all_modified_base.update(modified_variables_base)
        all_modified_module[ext_file] = modified_variables_extend

    replace_base_modified_variables(base_file, all_modified_base)

    for ext_file, modified_module_variables in all_modified_module.items():
        remain_lines = get_remain_extend_variables(ext_file, modified_module_variables)

        append_lines_to_base(base_file, remain_lines)


def list_modules(base_dir):
    module_file_regex = r"_(?P<module>[^\W_]+)_(?P<base>\w+).py"

    modules = defaultdict(list)
    for (root, _dirs, files) in os.walk(base_dir, topdown=True):
        files.sort()
        for file in files:
            match = re.match(module_file_regex, file)
            if match:
                parent_file = f"{match.group('base')}.py"
                parent_file_path = os.path.join(root, parent_file)
                child_file_path = os.path.join(root, file)
                modules[parent_file_path].append(child_file_path)

    return modules


def clean_up_submodules(children):
    for child in children:
        if os.path.exists(child):
            os.remove(child)


def process_modules(root):
    modules = list_modules(root)
    for parent, children in modules.items():
        combine_modules(parent, children)

        clean_up_submodules(children)
