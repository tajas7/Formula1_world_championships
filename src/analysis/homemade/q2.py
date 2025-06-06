from src.parsers.parse_csv import parse_csv


# Which drivers have recorded the most DNFs in their careers?


def get_driver_with_most_dnfs_nopd():
    """
    Finds the 3 drivers who did not finish (DNF) the most races in their career.

    Returns
    -------
    str
        A string that contains the 3 drivers as well as their numbers of DNFs.

    """
    results = parse_csv('./data/results.csv')
    status = parse_csv('./data/status.csv')
    drivers = parse_csv('./data/drivers.csv')

    finished_and_excluded_status = ["Finished", "+1 Lap", "Withdrew",
                                    "Did not start", "Did not qualify",
                                    "Did not prequalify", "107% Rule"]

    for i in range(2, 100):
        finished_and_excluded_status.append(f"+{i} Laps")

    dnf_status_ids = []
    for line in status:
        if line['status'] not in finished_and_excluded_status:
            dnf_status_ids.append(line['statusId'])

    dnf_results = []
    for line in results:
        if line['statusId'] in dnf_status_ids:
            dnf_results.append(line)

    dnf_counts = dict()

    for line in dnf_results:
        if line['driverId'] in dnf_counts.keys():
            dnf_counts[line['driverId']] += 1
        else:
            dnf_counts[line['driverId']] = 1

    top3_dnf = dict(
        sorted(dnf_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    )

    id_to_name = {d['driverId']: f"{d['forename']} {d['surname']}" for d in drivers}

    top3_dnf_named = {
        id_to_name[driver_id]: count
        for driver_id, count in top3_dnf.items()
    }

    def format_dict(dico, title):
        sorted_items = sorted(dico.items(), key=lambda x: x[1], reverse=True)

        driver_width = max(len("Driver"), max(len(name) for name in dico))
        wins_width = max(len("Wins"), max(len(str(dnfs)) for dnfs in dico.values()))

        line = "-" * 2*(driver_width + wins_width + 5)
        header = f"{'Driver'.center(driver_width)}        {'DNFs'.center(wins_width)}"
        rows = [f"{name.ljust(driver_width)}         {str(dnfs).rjust(wins_width)}"
                for name, dnfs in sorted_items]

        return "\n".join([title, line, header, line] + rows + [line])

    return format_dict(top3_dnf_named, "Drivers with most DNFs")
