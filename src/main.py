import os
import json
import utils
import glob
from plot import Plot


OUTPUT_PATH = os.path.join('src', 'output')
STATS_PATH = os.path.join(OUTPUT_PATH, 'stats.json')
METRICS_PATH = os.path.join(OUTPUT_PATH, 'metrics.png')
IGNORED_FILES = set(glob.glob('./*.*'))

extension_counts = {}

# Parse all files
cache = utils.load_cache()
parsed_cache = cache['parsed']
levels_cache = cache['levels']
for folder in glob.glob('./*/'):
    for file in glob.glob(os.path.join(folder, '**', '*.*'), recursive=True):
        if file in IGNORED_FILES:
            continue
        if file.lower().endswith('info.json'):
            if file not in parsed_cache:
                with open(file, 'r') as target:
                    info = json.load(target)

                    # Parse information
                    level = info['level'].lower()
                    if level not in levels_cache:
                        levels_cache[level] = 0
                    levels_cache[level] += 1

                    parsed_cache.add(file)
        else:
            _, ext = os.path.splitext(file)
            if ext not in extension_counts:
                extension_counts[ext] = 0
            extension_counts[ext] += 1

# Compile total challenge statistics
stats = utils.default_stats()
stats['levels'] = levels_cache
languages = stats['languages']
for language, pair in utils.LANGUAGES.items():
    ext = '.' + pair[0]
    color = pair[1]
    if ext in extension_counts:
        languages[language] = {
            'count': extension_counts[ext],
            'color': color
        }
utils.save_to_json(stats, STATS_PATH)

# Generate graphics
plot = Plot(stats)
plot.levels()
plot.languages()
plot.save(METRICS_PATH, dpi=200)

# Generate README.md
with open('README.md', 'w') as file:
    readme_lines = utils.fill_template('readme')[0]
    readme_lines.append('')
    utils.indent(readme_lines)
    file.write(''.join(readme_lines))

# Save cache for future runs
utils.save_cache(cache)
