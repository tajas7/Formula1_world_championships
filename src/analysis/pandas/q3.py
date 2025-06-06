import pandas as pd


# Which circuit has been the most dangerous historically?


def most_dangerous_circuit(country=None):
    """
    Finds the circuit where most accidents took place.
    If country is specified, finds the most dangerous circuit in country.

    Parameters
    ----------
    country : str

    Returns
    -------
    str : Name of the circuit

    """
    results = pd.read_csv('./data/results.csv')
    status = pd.read_csv('./data/status.csv')
    races = pd.read_csv('./data/races.csv')
    circuits = pd.read_csv('./data/circuits.csv')

    status_ids = status[
                     (status['status'] == 'Accident') |
                     (status['status'] == 'Collision') |
                     (status['status'] == 'Spun off') |
                     (status['status'] == 'Damage') |
                     (status['status'] == 'Debris')
                 ]['statusId'].tolist()

    accidents = results[results['statusId'].isin(status_ids)]

    accidents = accidents.merge(races[['raceId', 'circuitId']],
                                on='raceId',
                                how='left')

    accidents = accidents.merge(circuits[['circuitId', 'name', 'country']],
                                on='circuitId',
                                how='left')

    if country:
        accidents = accidents[accidents['country'] == country]

    circuits_counts = accidents['name'].value_counts()

    if circuits_counts.empty:
        return None

    if not country:
        return (f"The most dangerous circuit in the world is "
                f"the {circuits_counts.idxmax()}")

    return f"{country}'s most dangerous circuit is the {circuits_counts.idxmax()}"
