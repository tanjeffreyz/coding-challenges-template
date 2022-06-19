import utils


LEVELS = (
    ('hard',    '#d14026'),
    ('medium',  '#ffb84d'),
    ('easy',    '#46cc41'),
)
LANGUAGES = {       # Ext         Color
    'C++':          ('cpp',     '#f34b7d'),
    'Java':         ('java',    '#b07219'),
    'Python':       ('py',      '#3572A5'),
    'C':            ('c',       '#555555'),
    'C#':           ('cs',      '#178600'),
    'JavaScript':   ('js',      '#f1e05a'),
    'Ruby':         ('rb',      '#701516'),
    'Swift':        ('swift',   '#ffac45'),
    'Go':           ('go',      '#375eab'),
    'Scala':        ('sc',      '#DC322F'),
    'Kotlin':       ('kt',      '#F18E33'),
    'Rust':         ('rs',      '#dea584'),
    'PHP':          ('php',     '#4F5D95'),
    'TypeScript':   ('ts',      '#2b7489'),
    'Racket':       ('rkt',     '#22228f'),
    'Erlang':       ('erl',     '#B83998'),
    'Elixir':       ('ex',      '#6e4a7e')
}


class Stats:
    def __init__(self):
        self.stats = utils.default_stats()

    def levels(self, data):
        levels = self.stats['levels']
        for level, color in LEVELS:
            if level in data:
                levels.append({
                    'name': level,
                    'count': data[level],
                    'color': color
                })

    def languages(self, data):
        result = []
        for language, pair in LANGUAGES.items():
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
