import os
import json
import utils
import glob
from stats import Stats
from plot import Plot
from readme import Readme


OUTPUT_PATH = os.path.join('src', 'output')
STATS_PATH = os.path.join(OUTPUT_PATH, 'stats.json')
METRICS_PATH = os.path.join(OUTPUT_PATH, 'metrics.png')

IGNORED_FOLDERS = ('src', 'online-assessments')
IGNORED_FILES = set(glob.glob(os.path.join('.', '*.*')))
for folder in IGNORED_FOLDERS:
    matches = glob.glob(os.path.join('.', folder, '**', '*.*'), recursive=True)
    IGNORED_FILES.update(matches)


# Parse all files
extension_counts = {}
problems = []
cache = utils.load_cache()
info_cache = cache['info']
levels_cache = cache['levels']
for folder in glob.glob(os.path.join('.', '*')):
    for problem in glob.glob(os.path.join(folder, '*')):
        info_file = os.path.join(problem, 'info.json')
        if os.path.exists(info_file):
            # Parse information about the problem
            if info_file not in info_cache:
                with open(info_file, 'r') as target:
                    info = json.load(target)
                    info['title'] = info['title'].strip()

                    level = info['level'].lower()
                    if level not in levels_cache:
                        levels_cache[level] = 0
                    levels_cache[level] += 1

                    info_cache[info_file] = info

            # Parse solution files
            solutions = []
            for file in glob.glob(os.path.join(problem, '**', '*.*'), recursive=True):
                if file in IGNORED_FILES:
                    continue

                _, ext = os.path.splitext(file)
                if ext not in extension_counts:
                    extension_counts[ext] = 0
                extension_counts[ext] += 1
                solutions.append(file)

            # Compile information for the README.md table
            problems.append({
                'path': problem,
                'info': info_cache[info_file],
                'solutions': solutions
            })

# Compile total challenge statistics
stats = Stats()
stats.levels(levels_cache)
stats.languages(extension_counts)
stats.save(STATS_PATH)

# Generate graphics
plot = Plot(stats)
plot.levels()
plot.languages()
plot.save(METRICS_PATH, dpi=200)

# Generate README.md
readme = Readme(levels_cache, problems)
readme.compile()
readme.save('README.md')

# Save cache for future runs
utils.save_cache(cache)
