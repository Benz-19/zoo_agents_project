from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import pandas as pd
import json
import random
import asyncio

class AnimalAgent(Agent):
    class AnimalBehaviour(CyclicBehaviour):
        async def on_start(self):
            print(f"{self.agent.animal_name} agent starting...")
            df = pd.read_csv("data/zoo.data", header=None)
            df.columns = ["animal_name", "hair", "feathers", "eggs", "milk", "airborne",
                          "aquatic", "predator", "toothed", "backbone", "breathes", 
                          "venomous", "fins", "legs", "tail", "domestic", "catsize", "type"]
            
            self.animal_row = df[df["animal_name"] == self.agent.animal_name].iloc[0]
            
            # Initialize simple states
            self.hunger = random.randint(0, 50)   # 0 = full, 100 = very hungry
            self.energy = random.randint(50, 100) # 0 = tired, 100 = full energy

        async def run(self):
            # Listen for messages
            msg = await self.receive(timeout=5)
            if msg:
                # If zookeeper asks for a report
                if msg.body == "report":
                    report = {
                        "name": self.agent.animal_name,
                        "hunger": self.hunger,
                        "energy": self.energy,
                        "predator": int(self.animal_row["predator"]),
                        "legs": int(self.animal_row["legs"])
                    }
                    reply = Message(to=str(msg.sender))
                    reply.body = json.dumps(report)
                    await self.send(reply)
                    print(f"{self.agent.animal_name} sent report to Zookeeper.")
            else:
                # Update internal states a little
                self.hunger = min(100, self.hunger + random.randint(1,5))
                self.energy = max(0, self.energy - random.randint(1,3))
                await asyncio.sleep(1)

    async def setup(self):
        # animal_name must be provided when creating the agent
        print(f"AnimalAgent for {self.animal_name} starting...")
        behaviour = self.AnimalBehaviour()
        self.add_behaviour(behaviour)
