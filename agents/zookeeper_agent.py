# zookeeper_agent.py
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import asyncio
import json

class ZookeeperAgent(Agent):
    class CollectReportsBehaviour(OneShotBehaviour):
        async def run(self):
            print("Zookeeper asking animals for reports...")

            for animal_jid in self.agent.animal_agents:
                # Create a message for each animal agent
                msg = Message(to=animal_jid)
                msg.body = "report"
                await self.send(msg)

            # Collect replies
            reports = []
            for _ in self.agent.animal_agents:
                reply = await self.receive(timeout=5)
                if reply:
                    report = json.loads(reply.body)
                    reports.append(report)
                else:
                    reports.append({"name": "unknown", "error": "No reply"})

            # Print the summary
            print("\n--- Zoo Daily Report ---")
            for r in reports:
                print(f"{r['name']} | Hunger: {r.get('hunger', 'N/A')} | Energy: {r.get('energy', 'N/A')} | Predator: {r.get('predator', 'N/A')} | Legs: {r.get('legs', 'N/A')}")
            print("--- End of Report ---\n")

            # Stop the agent after reporting
            await self.agent.stop()

    async def setup(self):
        print("Zookeeper agent starting...")
        behaviour = self.CollectReportsBehaviour()
        self.add_behaviour(behaviour)
