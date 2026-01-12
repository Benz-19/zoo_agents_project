import matplotlib.pyplot as plt
from collections import defaultdict

def generate_final_plot(animals):
    """Generate energy distribution plot"""
    species_energy = defaultdict(list)
    
    for animal in animals:
        if not animal.dead:
            species_energy[animal.species].append(animal.energy)
    
    plt.figure(figsize=(12, 6))
    
    # Plot each species
    for species, energies in species_energy.items():
        if energies:  # Only plot if we have data
            plt.plot(range(len(energies)), sorted(energies), 'o-', label=species, alpha=0.7)
    
    plt.title("Final Energy Distribution by Species", fontsize=14, fontweight='bold')
    plt.xlabel("Animal Index (sorted by energy)", fontsize=12)
    plt.ylabel("Energy Level", fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save and show
    plt.savefig("zoo_simulation_results.png", dpi=150, bbox_inches='tight')
    print("\n[VISUALIZATION] Plot saved as 'zoo_simulation_results.png'")
    plt.show()
