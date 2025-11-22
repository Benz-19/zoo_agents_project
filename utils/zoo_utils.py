import pandas as pd

def load_zoo_dataset(path="data/zoo.data"):
    """Load zoo dataset and return a DataFrame with proper column names."""
    df = pd.read_csv(path, header=None)
    df.columns = ["animal_name", "hair", "feathers", "eggs", "milk", "airborne",
                  "aquatic", "predator", "toothed", "backbone", "breathes", 
                  "venomous", "fins", "legs", "tail", "domestic", "catsize", "type"]
    return df

def get_animal_traits(df, animal_name):
    """Return the row of the dataset for a specific animal."""
    return df[df["animal_name"] == animal_name].iloc[0]

def print_report(reports):
    """Pretty print a list of animal reports."""
    print("\n--- Zoo Report ---")
    for r in reports:
        print(f"{r['name']} | Hunger: {r.get('hunger', 'N/A')} | Energy: {r.get('energy', 'N/A')} | Predator: {r.get('predator', 'N/A')} | Legs: {r.get('legs', 'N/A')}")
    print("--- End of Report ---\n")
