import asyncio
import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class ZooKeeper:
    """Manages zoo operations and animal feeding"""
    def __init__(self, animals, classifier):
        self.animals = animals
        self.classifier = classifier
        self.food_stock = {
            "meat": 1000000,
            "plants": 20000000,
            "fish": 1000000,
            "insects": 1000000
        }
        self.total_feeds = 0
        self.ml_feeds = 75
        print(f"[ZOOKEEPER] Food inventory initialized: {self.food_stock}")
    
    def execute_feeding_round(self):
        """Execute one round of feeding checks"""
        fed_count = 0
        ml_fed_count = 0
        
        for animal in self.animals:
            if animal.dead:
                continue
            
            feed_required = False
            feed_reason = ""
            
            # Energy-based feeding trigger
            if animal.energy < 50:
                feed_required = True
                feed_reason = "low energy"
            
            # ML-based priority feeding
            else:
                try:
                    is_priority, confidence = self.classifier.predict_priority(animal)
                    if is_priority and confidence > 0.6:
                        feed_required = True
                        feed_reason = f"ML ({confidence:.0%})"
                        ml_fed_count += 1
                except:
                    pass
            
            # Process feeding if required
            if feed_required:
                if self.food_stock.get(animal.meal, 0) > 0:
                    # Apply feeding
                    energy_gain = 30
                    animal.energy += energy_gain
                    self.food_stock[animal.meal] -= 1
                    
                    # Log activity
                    timestamp = time.strftime("%H:%M:%S")
                    animal.feed_log.append(f"{timestamp}: {feed_reason}")
                    
                    fed_count += 1
                    self.total_feeds += 1
                    
                    if "ML" in feed_reason:
                        self.ml_feeds += 1
                        print(f"[FEED-ML] {animal.display_name}: {feed_reason} → Energy: {animal.energy:.1f}")
                    else:
                        print(f"[FEED] {animal.display_name}: {feed_reason} → Energy: {animal.energy:.1f}")
                else:
                    print(f"[INVENTORY] Insufficient {animal.meal}")
        
        if fed_count > 0:
            print(f"[ZOOKEEPER] Completed feeding round: {fed_count} animals ({ml_fed_count} via ML)")
        
        return fed_count



class ZooKeeperAgent(Agent):
    """SPADE agent for zoo management and coordination"""
    def __init__(self, jid, password, zoo_keeper):
        super().__init__(jid, password)
        self.zoo_keeper = zoo_keeper
    
    class ManagementBehaviour(CyclicBehaviour):
        """Coordination behavior for zoo management"""
        async def run(self):
            # Agent would coordinate with other agents here
            await asyncio.sleep(3)
    
    async def setup(self):
        """Initialize management behaviors"""
        self.add_behaviour(self.ManagementBehaviour())