import pandas as pd
import matplotlib.pyplot as plt


# Which nationality has the highest number of F1 drivers?


def nationalities(save_path=None):
    """
    Displays a bar chart showing the number of Formula 1 drivers by nationality since
    1950.

    Returns
    -------
    None : Displays the bar chart.

    """
    drivers = pd.read_csv('./data/drivers.csv')
    nationalities_counts = drivers['nationality'].value_counts()

    graph = nationalities_counts.plot(kind='bar',
                                      figsize=(16, 8),
                                      title="Drivers' nationalities since 1950")

    plt.xlabel('Nationality')
    plt.ylabel('Number of drivers')
    plt.xticks(rotation=90)
    graph.tick_params(axis='x', length=0)
    for spine in graph.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()
