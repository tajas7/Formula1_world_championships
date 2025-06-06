from src.parsers.parse_csv import parse_csv


# Which drivers have won 30 or more races in their careers?


def at_least_n_races_nopd(n: int):
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
    drivers = parse_csv('./data/drivers.csv')
    results = parse_csv('./data/results.csv')

    wins = []
    for line in results:
        if line['positionOrder'] == '1':
            wins.append(line)

    wins_by_driver = dict()
    for win in wins:
        if win['driverId'] in wins_by_driver.keys():
            wins_by_driver[win['driverId']] += 1
        else:
            wins_by_driver[win['driverId']] = 1

    more_than_n_wins_by_driver = dict()
    for driver in wins_by_driver.keys():
        if wins_by_driver[driver] >= n:
            more_than_n_wins_by_driver[driver] = wins_by_driver[driver]

    drivers_fullnames = {
        driver_id: None for driver_id in more_than_n_wins_by_driver.keys()
        }

    for driver in drivers:
        for id in drivers_fullnames.keys():
            if driver['driverId'] == id:
                drivers_fullnames[id] = driver['forename'] + ' ' + driver['surname']

    more_than_n_wins_by_driver_named = {
        drivers_fullnames[driver_id]: count
        for driver_id, count in sorted(
            more_than_n_wins_by_driver.items(),
            key=lambda x: x[1],
            reverse=True
        )
    }

    def format_dict(dico, title):
        sorted_items = sorted(dico.items(), key=lambda x: x[1], reverse=True)

        driver_width = max(len("Driver"), max(len(name) for name in dico))
        wins_width = max(len("Wins"), max(len(str(wins)) for wins in dico.values()))

        line = "-" * 2*(driver_width + wins_width + 5)
        header = f"{'Driver'.center(driver_width)}        {'Wins'.center(wins_width)}"
        rows = [f"{name.ljust(driver_width)}         {str(wins).rjust(wins_width)}"
                for name, wins in sorted_items]

        return "\n".join([title, line, header, line] + rows + [line])

    return format_dict(more_than_n_wins_by_driver_named,
                       f"Drivers who won more than {n} races")
