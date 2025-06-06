import pandas as pd


# Which drivers have won 30 or more races in their careers?


def at_least_n_races(n: int):
    """
    Finds pilots who won at least n races

    Parameters
    ----------
    n : int
            Minimum number of wins drivers must have

    Returns
    -------
    str
        A string that contains the drivers and their numbers of wins.

    """
    drivers = pd.read_csv("./data/drivers.csv")
    results = pd.read_csv("./data/results.csv")

    wins = results[results["positionOrder"] == 1]

    wins_by_driver = wins.groupby("driverId").size().reset_index(name="win_count")

    top_winners = wins_by_driver[wins_by_driver["win_count"] >= n]

    top_winners_named = pd.merge(top_winners, drivers, on="driverId")

    top_winners_named = top_winners_named[["forename", "surname", "win_count"]]

    top_winners_named = top_winners_named.sort_values(by="win_count", ascending=False)

    lines = []
    lines.append(f"Drivers who won more than {n} races")
    lines.append("------------------------------------------------")
    lines.append(f"{'Driver':<30}{'Wins'}")
    lines.append("------------------------------------------------")

    for _, row in top_winners_named.iterrows():
        full_name = f"{row['forename']} {row['surname']}"
        lines.append(f"{full_name:<30}{row['win_count']:>9}")

    lines.append("------------------------------------------------")

    return "\n".join(lines)
