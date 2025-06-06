import pandas as pd


# What is Lewis Hamilton's average starting position?


def driver_mean_grid(first_name, last_name):
    """
    Compute the average starting position of a Formula 1 driver across
    all their races.

    Parameters
    ----------
    first_name : str
        Driver's first name

    last_name : str
        Driver's last name

    Returns
    -------
    str
        A sentence that specifies the average grid of the specified driver.

    """
    drivers = pd.read_csv('./data/drivers.csv')

    driver_id = drivers[(drivers['forename'] == first_name) &
                        (drivers['surname'] == last_name)]['driverId'].squeeze()

    if pd.isna(driver_id):
        raise ValueError('Driver not found')

    results = pd.read_csv('./data/results.csv')

    return (f"{first_name} {last_name}'s mean position on the grid is "
            f"{round(results[results['driverId'] == driver_id]['grid'].mean())}")
