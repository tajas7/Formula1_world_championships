from src.parsers.parse_csv import parse_csv


# What is Lewis Hamilton's average starting position?


def driver_mean_grid_nopd(first_name, last_name):
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
    drivers = parse_csv("./data/drivers.csv")
    results = parse_csv("./data/results.csv")

    for line in drivers:
        if (line['forename'] == first_name and line['surname'] == last_name):
            driver_Id = line['driverId']
            break

    driver_grid_list = []
    for line in results:
        if line['driverId'] == driver_Id:
            driver_grid_list.append(int(line['grid']))

    return (f"{first_name} {last_name}'s mean position on the grid is "
            f"{round(sum(driver_grid_list)/len(driver_grid_list))}")
