import pandas as pd


# Which constructors have encountered the most technical failures?


def most_technical_issues_constructors(top_n=5):
    """
    Finds the top_n constructors with the highests technical issues records.

    Parameters
    ----------
    top_n : int

    Returns
    -------
    str
        A string with the constructors and their numbers of technical failures.

    """

    results = pd.read_csv('./data/results.csv')
    status = pd.read_csv('./data/status.csv')
    constructors = pd.read_csv('./data/constructors.csv')

    technical_statuses = [
        'Engine', 'Transmission', 'Clutch', 'Hydraulics', 'Electrical',
        'Suspension', 'Overheating', 'Fuel pressure', 'Fuel system',
        'Oil leak', 'Water leak', 'Driveshaft', 'Exhaust',
        'Power loss', 'Wheel', 'Brake failure', 'Chassis', 'Turbo'
    ]

    tech_status_ids = status[status['status'].isin(technical_statuses)]['statusId']
    tech_failures = results[results['statusId'].isin(tech_status_ids)]

    failure_counts = tech_failures['constructorId'].value_counts().head(top_n)

    failure_counts_named = (
        failure_counts.rename(
            index=lambda i: constructors.loc[constructors['constructorId'] == i,
                                             'name'].values[0]
            )
    )

    lines = []
    lines.append("Constructor                 Technical failures")
    lines.append("----------------------------------------------")
    for name, count in failure_counts_named.items():
        lines.append(f"{name:<25} {count:>20}")
    lines.append("----------------------------------------------")

    return "\n".join(lines)
