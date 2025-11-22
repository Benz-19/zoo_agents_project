from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import random

class FoodSupplyAgent(Agent):
    class FoodBehaviour(CyclicBehaviour):
        async def on_start(self):
            print("FoodSupply agent starting...")
            # Initialize food stock
            self.food_stock = 100  # max stock

        async def run(self):
            # Simulate food consumption
            self.food_stock -= random.randint(1, 5)  # animals eat a bit each cycle
            if self.food_stock < 30:
                # Alert the zookeeper if stock is low
                msg = Message(to=str(self.agent.zookeeper_jid))
                msg.body = f"Alert: Food stock is low ({self.food_stock} units left)"
                await self.send(msg)
                print(f"FoodSupply sent alert to Zookeeper. Stock: {self.food_stock}")
            else:
                print(f"FoodSupply stock: {self.food_stock}")
            
            # Stop if empty
            if self.food_stock <= 0:
                print("Food stock depleted!")
                await self.agent.stop()

            await asyncio.sleep(2)

    async def setup(self):
        # zookeeper_jid must be provided when creating the agent
        print("FoodSupplyAgent setup complete.")
        behaviour = self.FoodBehaviour()
        self.add_behaviour(behaviour)
