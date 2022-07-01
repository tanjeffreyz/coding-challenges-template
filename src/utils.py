import json
import os
import pickle


CACHE_PATH = os.path.join('src', 'resources', 'cache')
TEMPLATES_DIR = os.path.join('src', 'resources', 'templates')
IGNORED_TAGS = ('meta', 'link', '!DOCTYPE', 'br', 'hr')


def default_cache():
    return {
        'levels': {},
        'parsed': set()
    }


def default_stats():
    return {
        'levels': [],
        'languages': []
    }


def save_cache(cache):
    with open(CACHE_PATH, 'wb') as target:
        pickle.dump(cache, target)


def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, 'rb') as target:
            return pickle.load(target)
    else:
        new_cache = default_cache()
        save_cache(new_cache)
        return new_cache


def save_to_json(obj, path):
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    with open(path, 'w') as file:
        json.dump(obj, file, indent=2, sort_keys=True)
        file.write('\n')


def load_template(name):
    blocks = []
    lines = []
    with open(os.path.join(TEMPLATES_DIR, f'{name}.txt')) as file:
        for line in file.readlines():
            line = line.strip(' ')
            if line != '__DIVIDER__':
                if line != '':
                    lines.append(line)
            else:
                blocks.append(lines)
                lines = []
    if len(lines) > 0:
        blocks.append(lines)
    return blocks


def fill_template(name, variables=dict()):
    blocks = load_template(name)
    for block in blocks:
        for i in range(len(block)):
            for var in variables:
                block[i] = block[i].replace(var, str(variables[var]))
    return blocks


def indent(contents):
    """Mutatively indents each line in CONTENTS."""

    curr_indent = 0
    for i in range(len(contents)):
        line = contents[i]
        next_indent = curr_indent
        if not any(line.startswith(f'<{x}') for x in IGNORED_TAGS):
            first = True
            for j in range(len(line)):
                if line[j] == '<':
                    if j < len(line) - 1 and line[j + 1] == '/':
                        if first:
                            curr_indent -= 1  # If '</' comes first, decrease current indent
                        next_indent -= 1
                    else:
                        next_indent += 1
                    first = False
                elif line[j] == '/' and j < len(line) - 1 and line[j + 1] == '>':
                    next_indent -= 1
        contents[i] = ' ' * 4 * max(0, curr_indent) + line
        curr_indent = next_indent
