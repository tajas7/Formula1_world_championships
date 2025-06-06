import pandas as pd


# Which drivers have recorded the most DNFs in their careers?


def get_driver_with_most_dnfs():
    """
    Finds the 3 drivers who did not finish (DNF) the most races in their career.

    Returns
    -------
    str
        A string that contains the 3 drivers as well as their numbers of DNFs.

    """
    results = pd.read_csv('./data/results.csv')
    status = pd.read_csv('./data/status.csv')
    drivers = pd.read_csv('./data/drivers.csv')

    finished_and_excluded_status = (
        status[
            status['status'].str.match(
                r'^(Finished|\+\d+ Lap[s]?|Withdrew|Did not start|'
                r'Did not qualify|Did not prequalify|107% Rule)$'
            )
        ]['status']
        .tolist()
    )

    dnf_status_ids = status[
        ~status['status'].isin(finished_and_excluded_status)
        ]['statusId']

    dnf_results = results[results['statusId'].isin(dnf_status_ids)]

    dnf_counts = dnf_results['driverId'].value_counts().head(3)

    lines = []
    lines.append("Drivers with most DNFs")
    lines.append("-----------------------------------------------------")
    for driver_id, count in dnf_counts.items():
        driver = drivers[drivers['driverId'] == driver_id].iloc[0]
        full_name = f"{driver['forename']} {driver['surname']}"
        lines.append(f"{full_name:<25} {count:>5} DNFs")
    lines.append("-----------------------------------------------------")

    return "\n".join(lines)
