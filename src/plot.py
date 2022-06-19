import os
from matplotlib import pyplot as plt


class Plot:
    def __init__(self, stats):
        self.stats = stats
        self.fig, axs = plt.subplots(1, 2, figsize=(9, 4))
        self.ax_levels, self.ax_languages = axs

    @staticmethod
    def get_formatter(values):
        total = sum(values)

        def helper(percent):
            value = int(round(percent * total / 100.0))
            return f'{percent:.1f}%\n({value})'

        return helper
    
    def levels(self):
        levels = self.stats['levels']
        level_order = ('hard', 'medium', 'easy')
        level_colors = ('red', 'orange', 'green')
        labels = []
        colors = []
        counts = []
        for level, color in zip(level_order, level_colors):
            if level in levels:
                labels.append(level.capitalize())
                colors.append(color)
                counts.append(levels[level])

        _, labels, _ = self.ax_levels.pie(
            counts, labels=labels, colors=colors,
            autopct=Plot.get_formatter(counts),
            startangle=90, textprops={'color': 'white'}
        )
        for label in labels:
            label.set_color('black')

    def languages(self):
        labels = []
        counts = []
        colors = []

        descending_counts = sorted(
            self.stats['languages'].items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        for language, info in descending_counts:
            labels.append(language)
            counts.append(info['count'])
            colors.append(info['color'])

        ax = self.ax_languages
        y_range = range(len(labels))
        b = ax.barh(y_range, counts, color=colors, align='center')
        ax.set_yticks(y_range)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()
        plt.bar_label(b, color='white', label_type='center')
        plt.bar_label(
            b, padding=6,
            labels=[f'{100 * x / sum(counts):.1f}%' for x in counts]
        )
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_ticks([])

    def save(self, path, dpi=100):
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        self.fig.tight_layout()
        self.fig.savefig(path, bbox_inches='tight', dpi=dpi)

    def show(self):
        self.fig.tight_layout()
        plt.show()
