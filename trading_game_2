import pygame
import sys
import numpy as np
import random
import networkx as nx

# Constants
WIDTH, HEIGHT = 800, 600
TRADE_DISTANCE = 100
RESOURCE_LIST = ["dew", "bast", "sap"]
N_AGENTS = 20
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]


# Utility functions
def random_location():
    return np.random.randint(0, min(WIDTH, HEIGHT), 2)


def random_bearing():
    return np.random.rand() * 2 * np.pi


# Resources class
class Resources(dict):
    def __init__(self):
        super().__init__({resource: 0 for resource in RESOURCE_LIST})

    def randomize(self):
        for resource in self:
            self[resource] = np.random.randint(0, 10)

    def __add__(self, other):
        return Resources({k: self[k] + other[k] for k in self})

    def __sub__(self, other):
        return Resources({k: self[k] - other[k] for k in self})


# Agent class
class Agent:
    def __init__(self, name, loc, bearing, color):
        self.name = name
        self.loc = loc
        self.bearing = bearing
        self.color = color
        self.resources = Resources()
        self.resources.randomize()
        self.want = random.choice(RESOURCE_LIST)
        self.trading_with = None

    def step(self, step):
        self.loc = np.clip(self.loc + step, [0, 0], [WIDTH, HEIGHT])

    def __str__(self):
        return f"{self.name} at {self.loc} with {self.resources}"


# AgentGraph class
class AgentGraph(nx.Graph):
    def __init__(self, agents=None):
        super().__init__()
        if agents:
            for agent in agents:
                self.add_agent(agent)

    def add_agent(self, agent):
        self.add_node(agent)

    def distance(self, agent1, agent2):
        return np.linalg.norm(agent1.loc - agent2.loc)

    def trade(self, agent1, agent2):
        """Attempt a trade between two agents."""
        if agent1.want in agent2.resources and agent2.resources[agent1.want] > 0:
            agent2.resources[agent1.want] -= 1
            agent1.resources[agent1.want] += 1
            return True
        if agent2.want in agent1.resources and agent1.resources[agent2.want] > 0:
            agent1.resources[agent2.want] -= 1
            agent2.resources[agent2.want] += 1
            return True
        return False

    def do_trades(self):
        """Perform trades between agents within trade distance."""
        for agent1 in self.nodes:
            for agent2 in self.nodes:
                if agent1 != agent2 and self.distance(agent1, agent2) < TRADE_DISTANCE:
                    if self.trade(agent1, agent2):
                        agent1.trading_with = agent2
                        agent2.trading_with = agent1
                        print(f"{agent1.name} traded with {agent2.name}")
                    else:
                        agent1.trading_with = None
                        agent2.trading_with = None


# App class
class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Trading Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    def draw_agents(self, graph):
        for agent in graph.nodes:
            pygame.draw.circle(self.screen, agent.color, agent.loc, 10)
            text = self.font.render(agent.name, True, (255, 255, 255))
            self.screen.blit(text, agent.loc)

    def run(self, graph):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))
            graph.do_trades()
            self.draw_agents(graph)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


# Main
if __name__ == "__main__":
    agents = [Agent(f"Agent{i}", random_location(), random_bearing(), random.choice(COLORS)) for i in range(N_AGENTS)]
    graph = AgentGraph(agents)
    app = App()
    app.run(graph)
