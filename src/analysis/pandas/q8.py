import pandas as pd


# What is the average pit stop time across races? The maximum? The minimum?


def average_pit_stop_time(outliers=False, sup=60):
    """
    Computes the average, minimum, and maximum pit stop times,
    optionally excluding outliers.

    Parameters
    ----------
    outliers : bool
        If True, excludes pit stops longer than `sup` seconds from the calculation.
        If False, considers all pit stops.
    sup : float, optional
        Threshold value in seconds to define an outlier (default is 60 seconds).

    Returns
    -------
    str
        A string with:
            - 'Mean' : average pit stop time in seconds (float)
            - 'Min' : shortest pit stop time in seconds (float)
            - 'Max' : longest pit stop time in seconds (float)

    """

    pit_stops = pd.read_csv('./data/pit_stops.csv')

    if not outliers:
        pit_stops = pit_stops[pit_stops['milliseconds']/1000 <= sup]

    avg = round(pit_stops['milliseconds'].mean() / 1000, 2)
    min_time = round(pit_stops['milliseconds'].min() / 1000, 2)
    max_time = round(pit_stops['milliseconds'].max() / 1000, 2)

    tableau = (
        "-------------------------------------\n"
        " Statistic                     Value \n"
        "--------------------------------------\n"
        f" Mean                      {avg:10.2f} s \n"
        f" Min                  {min_time:10.2f} s \n"
        f" Max                  {max_time:10.2f} s \n"
        "-------------------------------------"
    )

    return tableau
