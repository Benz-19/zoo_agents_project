import pandas as pd
import time
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier

class SimpleAnimal:
    def __init__(self, species, animal_id, energy, diet):
        self.species = species
        self.id = animal_id
        self.display_name = f"{species}_{animal_id}"
        self.energy = energy
        self.dead = False
        self.death_time = None
        self.feed_log = []
        self.diet = diet
        self.meal = "plants"
        
        if diet == 'carnivore':
            self.meal = "meat"
        elif diet == 'herbivore':
            self.meal = "plants"
        elif diet == 'insectivore':
            self.meal = "insects"
    
    def update(self):
        if self.dead:
            return
            
        self.energy -= 5  # Energy decay
        
        if self.energy <= 0:
            self.energy = 0
            self.dead = True
            self.death_time = time.strftime("%H:%M:%S")
            print(f"[DEATH] {self.display_name} at {self.death_time}")

class SimpleZookeeper:
    def __init__(self, animals):
        self.animals = animals
        self.food_stock = {"meat": 50, "plants": 100, "fish": 30, "insects": 40}
        self.running = True
    
    def feed_animals(self):
        for animal in self.animals:
            if animal.dead:
                continue
                
            if 10 <= animal.energy <= 20:
                if self.food_stock.get(animal.meal, 0) > 0:
                    animal.energy += 15
                    self.food_stock[animal.meal] -= 1
                    animal.feed_log.append(time.strftime("%H:%M:%S"))
                    print(f"[FEED] {animal.display_name} ate {animal.meal}")
                else:
                    print(f"[FOOD OUT] {animal.meal} exhausted!")
                    self.running = False
                    return

def train_classifier():
    print("\n=== TRAINING CLASSIFIER ===")
    data = pd.read_csv("data/animals_dataset.csv")
    
    X = data[["avg_weight_kg", "avg_speed_kmh", "gestation_days", "intelligence_score"]]
    y = data["animal_class"]
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    accuracy = model.score(X, y)
    print(f"[Classifier] RandomForest trained with accuracy: {accuracy:.2%}")
    
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n[Classifier] Feature Importance:")
    print(feature_importance)
    
    return model

def run_simulation():
    # Load data
    df = pd.read_csv("data/animals_dataset.csv")
    
    # Create animals
    animals = []
    for _, row in df.iterrows():
        animal = SimpleAnimal(
            species=row['species'],
            animal_id=row['id'],
            energy=row['energy'],
            diet=row['diet']
        )
        animals.append(animal)
    
    # Create zookeeper
    zookeeper = SimpleZookeeper(animals)
    
    # Run simulation
    print("\n=== STARTING SIMULATION ===")
    tick = 0
    max_ticks = 20  # Run for 20 cycles
    
    while tick < max_ticks and zookeeper.running:
        print(f"\n--- Tick {tick + 1} ---")
        
        # Update all animals
        for animal in animals:
            animal.update()
            if not animal.dead:
                print(f"[STATUS] {animal.display_name} | Energy={animal.energy}")
        
        # Feed animals
        zookeeper.feed_animals()
        
        # Print food stock
        print(f"[FOOD] Stock: {zookeeper.food_stock}")
        
        tick += 1
        time.sleep(1)  # Wait 1 second between ticks
    
    # Generate final plot
    print("\n=== GENERATING FINAL PLOT ===")
    species_energy = defaultdict(list)
    
    for animal in animals:
        species_energy[animal.species].append(animal.energy)
    
    plt.figure(figsize=(10, 6))
    for species, energies in species_energy.items():
        plt.plot(energies, label=species, marker='o')
    
    plt.title("Final Energy Distribution by Species")
    plt.xlabel("Animal Index")
    plt.ylabel("Energy Level")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("simulation_results.png")
    plt.show()
    
    # Print final statistics
    print("\n=== FINAL STATISTICS ===")
    for species in set(a.species for a in animals):
        species_animals = [a for a in animals if a.species == species]
        dead_count = sum(1 for a in species_animals if a.dead)
        avg_energy = sum(a.energy for a in species_animals) / len(species_animals)
        print(f"{species}: {dead_count}/{len(species_animals)} dead | Avg energy: {avg_energy:.1f}")

if __name__ == "__main__":
    # Train ML classifier
    model = train_classifier()
    
    # Run simulation
    run_simulation()
    
    print("\n=== PROJECT COMPLETED SUCCESSFULLY ===")