import pandas as pd


# Which constructor won the Constructors’ Championship in 2023?


def constructor_winner(yy):
    """
    Finds which constructor won the yy-championship

    Parameters
    ----------
    yy : int

    Returns
    -------
    str : name of the constructor

    """
    races = pd.read_csv('./data/races.csv')

    races_yy = races[races['year'] == yy]

    nb_races_yy = races_yy['round'].max()

    race_id_last_race_yy = (
        races[
            (races['round'] == nb_races_yy) &
            (races['year'] == yy)
        ]['raceId']
        .squeeze()
    )

    constructor_standings = pd.read_csv('./data/constructor_standings.csv')

    constructor_id_champion_yy = (
        constructor_standings[
            (constructor_standings['raceId'] == race_id_last_race_yy) &
            (constructor_standings['position'] == 1)
        ]['constructorId']
        .squeeze()
    )

    if isinstance(constructor_id_champion_yy, pd.Series):
        if constructor_id_champion_yy.empty:
            return None
        constructor_id_champion_yy = constructor_id_champion_yy.iloc[0]

    constructors = pd.read_csv('./data/constructors.csv')

    name = (constructors[constructors['constructorId'] == constructor_id_champion_yy]
            ['name'].squeeze())

    return name
