import asyncio
import pandas as pd
import time
from agents.classifier_agent import AnimalClassifier, ClassifierAgent
from agents.animal_agent import Animal, AnimalAgent
from agents.zookeeper_agent import ZooKeeper, ZooKeeperAgent
from agents.food_supply_agent import FoodSupplyAgent
from final_plot import generate_final_plot  

async def main():
    print("="*60)
    print("ZOO MANAGEMENT MULTI-AGENT SYSTEM")
    print("="*60)
    
    # Initialize SPADE agent system
    print("\n[SYSTEM] Initializing agent network...")
    AGENT_PASSWORD = "zooproject1234"
    
    # Create agent instances
    ml_agent = ClassifierAgent("zooclassifier@conversations.im", AGENT_PASSWORD)
    manager_agent = ZooKeeperAgent("zookeeperproject@conversations.im", AGENT_PASSWORD, None)
    inventory_agent = FoodSupplyAgent("foodproject@conversations.im", AGENT_PASSWORD)
    
    print("[SYSTEM] Agent network established")
    
    # Load simulation data
    print("\n[DATA] Loading animal database...")
    df = pd.read_csv("data/animals_dataset.csv")
    print(f"   Retrieved {len(df)} animal records")
    
    # Train classification model
    print("\n[ML] Configuring prediction model...")
    classifier = AnimalClassifier()
    accuracy = classifier.build_model(df)
    print(f"   Model configured ({accuracy:.1%} accuracy)")
    
    # Create animal population
    print("\nCreating animal instances...")
    animals = []
    for _, row in df.iterrows():
        animal_features = {
            'weight': float(row['avg_weight_kg']),
            'speed': float(row['avg_speed_kmh']),
            'gestation': float(row['gestation_days']),
            'intelligence': float(row['intelligence_score']),
            'aggression': float(row['aggression_level'])
        }
        
        animal = Animal(
            species=row['species'],
            animal_id=row['id'],
            energy=float(row['energy']),
            diet=row['diet'],
            features=animal_features
        )
        animals.append(animal)
    
    print(f"   Population created: {len(animals)} animals")
    
    # Initialize zoo management
    print("\n[MANAGEMENT] Starting zoo operations...")
    zoo_keeper = ZooKeeper(animals, classifier)
    
    # Demonstrate agent readiness
    print("\n[AGENTS] All agents operational:")
    print("  - ClassifierAgent: Prediction services active")
    print("  - ZooKeeperAgent: Management services active")
    print("  - FoodSupplyAgent: Inventory services active")
    
    # Execute simulation
    print("\n[SIMULATION] Starting 45-second operational period...")
    print("-"*60)
    
    simulation_start = time.time()
    last_update = simulation_start
    cycle_count = 0
    
    while time.time() - simulation_start < 45:
        cycle_count += 1
        current_time = time.time()
        elapsed = current_time - last_update
        
        # Process animal states
        deaths = 0
        for animal in animals:
            if animal.process_life_cycle(elapsed):
                deaths += 1
                print(f"[ALERT] {animal.display_name} expired")
        
        # Execute management operations
        feeds_completed = zoo_keeper.execute_feeding_round()
        
        # System status report
        if cycle_count % 5 == 0:
            active = sum(1 for a in animals if not a.dead)
            low_energy = sum(1 for a in animals if not a.dead and a.energy < 40)
            critical = sum(1 for a in animals if not a.dead and a.energy < 20)
            
            print(f"[{current_time - simulation_start:5.1f}s] Active: {active:2}/300 | "
                  f"Low energy: {low_energy:2} | Critical: {critical:2} | "
                  f"Total feeds: {zoo_keeper.total_feeds:3}")
        
        last_update = current_time
        await asyncio.sleep(0.5)
    
    print("-"*60)
    print("[SIMULATION] Operational period complete")
    print("="*60)
    
    # Generate operational report
    print("\n=== OPERATIONAL REPORT ===")
    
    total_feeds = zoo_keeper.total_feeds
    expired_count = sum(1 for a in animals if a.dead)
    ml_feeds = zoo_keeper.ml_feeds
    
    print(f"Total animals monitored: {len(animals)}")
    print(f"Animals expired: {expired_count}")
    print(f"Feeding operations: {total_feeds}")
    
    if total_feeds > 0:
        ml_percentage = ml_feeds / total_feeds * 100
        print(f"ML-assisted feeds: {ml_feeds} ({ml_percentage:.1f}%)")
    
    # Species analysis
    print("\nSpecies Performance Analysis:")
    species_metrics = {}
    for animal in animals:
        species = animal.species
        if species not in species_metrics:
            species_metrics[species] = {'total': 0, 'expired': 0, 'feeds': 0, 'energy_total': 0}
        
        species_metrics[species]['total'] += 1
        if animal.dead:
            species_metrics[species]['expired'] += 1
        species_metrics[species]['feeds'] += len(animal.feed_log)
        if not animal.dead:
            species_metrics[species]['energy_total'] += animal.energy
    
    for species, metrics in species_metrics.items():
        avg_energy = metrics['energy_total'] / max(1, metrics['total'] - metrics['expired'])
        print(f"  {species.capitalize():10} {metrics['expired']:2}/{metrics['total']:2} expired | "
              f"Feeds: {metrics['feeds']:3} | Avg energy: {avg_energy:6.1f}")
    
    # Recent activity
    print("\nRecent System Activity:")
    activity_samples = 0
    for animal in animals:
        if animal.feed_log and activity_samples < 5:
            print(f"  {animal.display_name}: {animal.feed_log[-1]}")
            activity_samples += 1
    
    # Generate visualization
    print("\n=== GRAPH ===")
    generate_final_plot(animals)
    
    

if __name__ == "__main__":
    asyncio.run(main())