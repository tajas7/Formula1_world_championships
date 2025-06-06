import pandas as pd


# What was the final drivers ranking for the 2023 season?


def ranking(yy):
    """
    Establishes the drivers standings for a specified year, and deals with
    equality cases.

    Parameters
    ----------
    yy : str

    Returns
    -------
    str
        A string that contains the drivers, their ranks, and their numbers of points.

    """
    drivers = pd.read_csv("./data/drivers.csv")
    results = pd.read_csv("./data/results.csv")
    races = pd.read_csv("./data/races.csv")
    driver_standings = pd.read_csv("./data/driver_standings.csv")

    races_yy = races[races['year'] == yy]

    yy_last_race_id = races_yy['raceId'].max()

    standings = driver_standings[driver_standings['raceId'] == yy_last_race_id]

    race_ids_yy = races_yy['raceId'].tolist()

    results_yy = results[results['raceId'].isin(race_ids_yy)]

    position_counts = (
        results_yy
        .groupby(['driverId', 'positionOrder'])
        .size()
        .unstack(fill_value=0)
    )

    ranking = (
        standings[['driverId', 'points']]
        .merge(position_counts, on='driverId', how='left')
        .merge(drivers[['driverId', 'forename', 'surname']], on='driverId', how='left')
    )

    cols_sort = ['points'] + list(range(1, position_counts.columns.max()+1))
    ranking = ranking.sort_values(by=cols_sort, ascending=[False]*len(cols_sort))

    ranking[['forename', 'surname', 'points'] + list(range(1, 11))]

    ranking = ranking.reset_index(drop=True)

    ranking.insert(0, 'rank', ranking.index + 1)

    lines = []
    lines.append(f"Drivers' ranking – Season {yy}")
    lines.append("------------------------------------------------")
    lines.append(f"{'Rank':<10}{'Driver':<25}{'Points'}")
    lines.append("------------------------------------------------")

    for _, row in ranking.iterrows():
        full_name = f"{row['forename']} {row['surname']}"
        lines.append(f"{int(row['rank']):<10}{full_name:<25}{float(row['points']):.1f}")

    lines.append("------------------------------------------------")

    return "\n".join(lines)
