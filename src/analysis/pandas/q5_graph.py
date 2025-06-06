import pandas as pd
import matplotlib.pyplot as plt


# Which constructors have won the most Constructors’ Championships?


def most_constructor_championships_won(save_path=None):
    """
    Plots the top 5 of the constructors who won the most constructor championships

    Returns
    -------
    None : Displays the graph

    """
    from src.analysis.pandas.q4 import constructor_winner
    constructors_champions = []

    for year in range(1958, 2025):
        constructors_champions.append(constructor_winner(year))

    counts = dict()

    for elt in constructors_champions:
        if elt in counts.keys():
            counts[elt] += 1
        else:
            counts[elt] = 1

    counts_df = pd.DataFrame.from_dict(counts, orient='index',
                                       columns=['championships'])
    counts_df = counts_df.sort_values(by='championships', ascending=False)

    top5 = counts_df.head(5)

    top5.plot(kind='barh', legend=False, color='purple')

    plt.title("Top 5 Constructors with Most Championships")
    plt.xlabel('Number of Championships')
    plt.ylabel('Constructor')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    for index, value in enumerate(top5['championships']):
        plt.text(value + 0.1, index, str(value), va='center')
    plt.gca().axes.get_xaxis().set_visible(False)

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()
