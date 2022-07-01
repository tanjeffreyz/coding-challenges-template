import utils
import config


class Stats:
    def __init__(self):
        self.stats = utils.default_stats()

    def levels(self, data):
        levels = self.stats['levels']
        for level, color in config.LEVELS:
            if level in data:
                levels.append({
                    'name': level,
                    'count': data[level],
                    'color': color
                })

    def languages(self, data):
        result = []
        for language, pair in config.LANGUAGES.items():
            ext = '.' + pair[0]
            color = pair[1]
            if ext in data:
                result.append({
                    'name': language,
                    'count': data[ext],
                    'color': color
                })
        self.stats['languages'] = list(sorted(result, key=lambda x: x['count'], reverse=True))

    def save(self, path):
        utils.save_to_json(self.stats, path)
