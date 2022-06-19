import os
from matplotlib import pyplot as plt


class Plot:
    def __init__(self, stats_obj):
        self.stats = stats_obj.stats
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
        labels = []
        colors = []
        counts = []
        for level in self.stats['levels']:
            labels.append(level['name'].capitalize())
            colors.append(level['color'])
            counts.append(level['count'])

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

        for language in self.stats['languages']:
            labels.append(language['name'])
            counts.append(language['count'])
            colors.append(language['color'])

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
