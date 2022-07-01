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

EXTENSIONS = {f'.{value[0]}': key for key, value in LANGUAGES.items()}
