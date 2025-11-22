# zookeeper_agent.py
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
import asyncio
from utils.zoo_utils import print_report

class ZookeeperAgent(Agent):
    class MonitorBehaviour(CyclicBehaviour):
        async def on_start(self):
            print("ZookeeperAgent starting...")
            self.reports = []

        async def run(self):
            # Request reports from all animals
            for animal_jid in self.agent.animal_agents:
                msg = Message(to=animal_jid)
                msg.body = "report"
                await self.send(msg)
                # print(f"Requested report from {animal_jid}")

            # Collect replies
            for _ in self.agent.animal_agents:
                reply = await self.receive(timeout=5)
                if reply:
                    report = json.loads(reply.body)
                    self.reports.append(report)

            if self.reports:
                print_report(self.reports)
                self.reports = []

            await asyncio.sleep(3)  # Wait before next check

    async def setup(self):
        print("ZookeeperAgent setup complete.")
        behaviour = self.MonitorBehaviour()
        self.add_behaviour(behaviour)
