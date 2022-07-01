import config
import utils
import os
import re


class Readme:
    def __init__(self, levels, problems):
        self.problems = problems

        variables = {
            '__TOTAL_CHALLENGES__': sum(levels.values())
        }
        self.readme_contents, self.readme_end = utils.fill_template('readme', variables=variables)

    def compile(self):
        for problem in sort_problems(self.problems):
            self.readme_contents.append('<tr>')
            info = problem['info']

            # Display problem
            self.readme_contents += [
                '<td>',
                f"<a href=\"{problem['path']}\"><b>{info['title']}</b></a>",
                '<br>'
            ]
            topics = info['topics']
            for i, topic in enumerate(topics):
                comma = '' if i == len(topics) - 1 else ','
                self.readme_contents.append(f"<a href=\"{topic['link']}\"><sub>{topic['name']}{comma}</sub></a>")
            self.readme_contents.append('</td>')

            # Display level
            self.readme_contents += [
                '<td align="center">',
                info['level'],
                '</td>'
            ]

            # Display solutions
            solutions = problem['solutions']
            self.readme_contents.append('<td>')
            for i, solution in enumerate(solutions):
                _, ext = os.path.splitext(solution)
                if ext in config.EXTENSIONS:
                    self.readme_contents.append(f"<a href=\"{solution}\">{config.EXTENSIONS[ext]}</a>")
                    if i != len(solutions) - 1:
                        self.readme_contents.append('<br>')
            self.readme_contents.append('</td>')

            self.readme_contents.append('</tr>')
        self.readme_contents += self.readme_end
        self.readme_contents.append('')

    def save(self, path):
        with open(path, 'w') as file:
            utils.indent(self.readme_contents)
            file.write('\n'.join(self.readme_contents))


def sort_problems(problems):
    level_order = {}
    for i, level_info in enumerate(config.LEVELS):
        level_order[level_info[0]] = i

    def sort_helper(x):
        info = x['info']
        level = info['level'].lower()
        if level in level_order:
            level_weight = level_order[level]
            title = info['title']
            match = re.search('^\\d+', title)
            if match:
                start, end = match.span()
                return level_weight, end - start, title
            else:
                return level_weight, float('inf'), title

    return sorted(problems, key=sort_helper)
