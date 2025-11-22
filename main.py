# main.py
import asyncio
from agents.animal_agent import AnimalAgent
from agents.zookeeper_agent import ZookeeperAgent
from agents.food_supply_agent import FoodSupplyAgent
import config

async def main():
    # --- List of animal agents ---
    animals_info = [
        ("lion", config.LION_JID, config.LION_PASSWORD),
        ("elephant", config.ELEPHANT_JID, config.ELEPHANT_PASSWORD),
        ("frog", config.FROG_JID, config.FROG_PASSWORD),
        ("crow", config.CROW_JID, config.CROW_PASSWORD),
    ]

    animal_agents = []
    animal_jids = []

    # --- Create Animal Agents dynamically ---
    for name, jid, pwd in animals_info:
        agent = AnimalAgent(jid, pwd)
        agent.animal_name = name
        animal_agents.append(agent)
        animal_jids.append(jid)

    # --- Create Zookeeper Agent ---
    zookeeper = ZookeeperAgent(config.ZOOKEEPER_JID, config.ZOOKEEPER_PASSWORD)
    zookeeper.animal_agents = animal_jids

    # --- Create Food Supply Agent ---
    food_supply = FoodSupplyAgent(config.FOOD_JID, config.FOOD_PASSWORD)
    food_supply.zookeeper_jid = config.ZOOKEEPER_JID

    # --- Start all agents ---
    for agent in animal_agents + [zookeeper, food_supply]:
        await agent.start(auto_register=True)

    # --- Let simulation run ---
    await asyncio.sleep(15)

    # --- Stop all agents ---
    for agent in animal_agents + [zookeeper, food_supply]:
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
