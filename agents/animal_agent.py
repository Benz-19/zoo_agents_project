from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio
import time

class Animal:
    """Represents an animal in the zoo simulation"""
    def __init__(self, species, animal_id, energy, diet, features):
        self.species = species
        self.id = animal_id
        self.display_name = f"{species}_{animal_id}"
        self.energy = energy
        self.diet = diet
        self.features = features
        self.dead = False
        self.feed_log = []
        
        # Different energy decay based on size/metabolism
        if species in ['elephant', 'whale']:
            self.energy_decay = 1.5
        elif species in ['frog', 'eagle', 'penguin']:
            self.energy_decay = 4.0
        else:
            self.energy_decay = 2.5
        
        # Set meal type
        if diet == 'carnivore':
            self.meal = "meat"
        elif diet == 'herbivore':
            self.meal = "plants"
        elif diet == 'insectivore':
            self.meal = "insects"
        else:
            self.meal = "fish"

    def process_life_cycle(self, elapsed_time):
        """Process animal's energy decay and check for death"""
        if self.dead:
            return False
        
        # Calculate energy loss
        energy_loss = self.energy_decay * elapsed_time
        self.energy = max(0, self.energy - energy_loss)
        
        # Check for death
        if self.energy <= 0:
            self.energy = 0
            self.dead = True
            return True
        
        return False

class AnimalAgent(Agent):
    """SPADE agent representing an autonomous animal"""
    def __init__(self, jid, password, animal_instance):
        super().__init__(jid, password)
        self.animal = animal_instance
    
    class LifeCycleBehaviour(CyclicBehaviour):
        """Autonomous behavior for animal lifecycle management"""
        async def run(self):
            # This behavior would typically handle agent communication
            # For simulation purposes, we track agent activity
            await asyncio.sleep(1)
    
    async def setup(self):
        """Initialize agent behaviors"""
        self.add_behaviour(self.LifeCycleBehaviour())