import pandas as pd

def load_zoo_dataset():
    """
    Loads the zoo.data file as a pandas DataFrame.
    The dataset has no headers, so zoo.names provides the column names.
    """
    col_names = [
        "animal_name", "hair", "feathers", "eggs", "milk", "airborne",
        "aquatic", "predator", "toothed", "backbone", "breathes",
        "venomous", "fins", "legs", "tail", "domestic", "catsize",
        "type"
    ]

    df = pd.read_csv("data/zoo.data", header=None, names=col_names)
    return df
