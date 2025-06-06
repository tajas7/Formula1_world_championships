import csv


def parse_csv(filepath: str, delimiter=None):
    """
    Reads a CSV file and detects the demimiter if necessary.

    Parameters
    ----------
    filepath : path to the CSV file
    delimiter : character that separates fields in the CSV file

    Returns
    -------
    list[dict] : each line is a dictionnary whose keys are the columns

    """
    with open(filepath, newline='', encoding='utf-8') as df:
        sample = df.read(1024)
        df.seek(0)

        if delimiter is None:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            delimiter = dialect.delimiter

        reader = csv.DictReader(df, delimiter=delimiter)
        return list(reader)
