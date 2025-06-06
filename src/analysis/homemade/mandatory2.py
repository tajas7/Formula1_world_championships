from src.parsers.parse_csv import parse_csv


# What was the final drivers ranking for the 2023 season?


def ranking_nopd(yy):
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
    drivers = parse_csv('./data/drivers.csv')
    results = parse_csv('./data/results.csv')
    driver_standings = parse_csv('./data/driver_standings.csv')
    races = parse_csv('./data/races.csv')

    races_yy = []
    for line in races:
        if int(line['year']) == yy:
            races_yy.append(line)

    races_yy_ids = []
    for race in races_yy:
        races_yy_ids.append(race['raceId'])

    id_last_race_yy = max(races_yy_ids)

    ranking_with_exaequos = dict()
    for line in driver_standings:
        if line['raceId'] == id_last_race_yy:
            ranking_with_exaequos[line['driverId']] = line['points']

    ranking_sorted = dict(sorted(
        ranking_with_exaequos.items(),
        key=lambda item: float(item[1]),
        reverse=True
    ))

    ranking_sorted

    id_to_name = {
        driver['driverId']: f"{driver['forename']} {driver['surname']}"
        for driver in drivers
    }

    from collections import defaultdict

    finishes = defaultdict(lambda: [0]*10)

    for result in results:
        if result['raceId'] in races_yy_ids:
            position = result['position']
            driver_id = result['driverId']

            if position.isdigit():
                pos = int(position)
                if 1 <= pos <= 10:
                    finishes[driver_id][pos - 1] += 1

    final_ranking_ids = sorted(
        ranking_with_exaequos.keys(),
        key=lambda d: (float(ranking_with_exaequos[d]), finishes[d]),
        reverse=True
    )

    final_ranking_named = [
        (rank, id_to_name[driver_id], float(ranking_with_exaequos[driver_id]))
        for rank, driver_id in enumerate(final_ranking_ids, 1)
    ]

    def format_list(standings, title):
        rank_width = max(len("Rank"), max(len(str(rank)) for rank, _, _ in standings))
        name_width = max(len("Driver"), max(len(name) for _, name, _ in standings))
        points_width = max(len("Points"), max(len(str(int(points)))
                                              for _, _, points in standings))

        header = (f"{'Rank':<{rank_width}}   "
                  f"{'Driver':<{name_width}}   "
                  f"{'Points':>{points_width}}")
        separator = "-" * len(header)
        rows = [
            (
                f"{str(rank):<{rank_width}}   "
                f"{name:<{name_width}}   "
                f"{int(points):>{points_width}}"
            )
            for rank, name, points in standings
        ]

        return "\n".join([title, separator, header, separator] + rows + [separator])

    return format_list(final_ranking_named, f"Drivers' ranking - Season {yy}")
