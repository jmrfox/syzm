import pygame
import sys
import numpy as np
import networkx as nx

from names import generate_random_name
import random
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
COLORS = [WHITE, BLACK, BLUE, RED, GREEN, ORANGE, YELLOW, PURPLE, CYAN, MAGENTA]


def opposite_color(rbg):
    return tuple(255 - x for x in rbg)


BACKGROUND_COLOR = np.ones(3) * 50
FRAMERATE_DEFAULT = 30
WIDTH = 720
HEIGHT = 1280
TORUS = True

RESOURCE_LIST = ["dew", "bast", "sap"]

N_AGENTS = 20

STEPRATE_DEFAULT = 0.5
STEPSIZE_DEFAULT = 5
TURN_VARIANCE_DEFAULT = 0.4
TRADE_DISTANCE_DEFAULT = 100


def make_name(sylb=3):
    return generate_random_name(sylb)


def choose_random_other(lst, item):
    return random.choice([x for x in lst if x != item])


class Resources(dict):
    def __init__(self):
        super().__init__()
        for resource in RESOURCE_LIST:
            self[resource] = 0

    def __str__(self):
        return ", ".join([str(v) + " " + k for k, v in self.items()])

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        result = Resources()
        for k in self.keys():
            result[k] = self[k] + other[k]
        return result

    def __sub__(self, other):
        result = Resources()
        for k in self.keys():
            result[k] = self[k] - other[k]
        return result

    def randomize(self):
        for k in self.keys():
            self[k] = np.random.randint(0, 10)

    def get_tuple(self):
        return (self["dew"], self["bast"], self["sap"])


class Agent:
    def __init__(self, name, loc=np.array([0, 0]), bearing=0.0, color=None):
        self.name = name
        self.loc = loc
        self.bearing = bearing
        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color

        self.resources = Resources()
        self.resources.randomize()
        self.trading_with = None
        self.want = random.choice(RESOURCE_LIST)

        self.steprate = STEPRATE_DEFAULT  # ratio
        self.stepsize = STEPSIZE_DEFAULT  # int
        self.turn_variance = TURN_VARIANCE_DEFAULT

    def step(self, step=np.array([0, 0])):
        if TORUS:
            self.loc = np.mod(self.loc + step, np.array([WIDTH, HEIGHT]))
        else:
            self.loc = np.clip(self.loc + step, np.array([0, 0]), np.array([WIDTH, HEIGHT]))

    def __str__(self):
        """print all properties"""
        out = []
        out.append(f"name\t{self.name}")
        out.append(f"loc\t{self.loc}")
        out.append(f"color\t{self.color}")
        out.append(f"resources\t{self.resources}")
        out.append(f"trading_with\t{self.trading_with}")
        out.append(f"want\t{self.want}")
        return "\n".join(out)

    def __repr__(self):
        return self.__str__()


class AgentGraph(nx.Graph):
    def __init__(self, agents=None):
        super().__init__()
        if agents is not None:
            for agent in agents:
                self.add_agent(agent)
        self.trade_distance = TRADE_DISTANCE_DEFAULT
        self.traded_edges = set()  # Track edges where trades occur

    def add_agent(self, agent):
        self.add_node(agent)
        others = [node for node in self.nodes if node != agent]
        for other in others:
            self.add_edge(agent, other)

    def __str__(self):
        out = "Agents:\n"
        if len(self.nodes) == 0:
            out += "None"
        else:
            out += "\n".join([str(agent) for agent in self.nodes])
        return out

    def __repr__(self):
        return self.__str__()

    def distance(self, agent1, agent2):
        return np.linalg.norm(agent1.loc - agent2.loc)

    def do_steps(self):
        for agent in self.nodes:
            if np.random.rand() < agent.steprate:
                agent.bearing += np.random.randn() * agent.turn_variance
                step = np.array([np.cos(agent.bearing), np.sin(agent.bearing)]) * agent.stepsize
                agent.step(step)

    def get_distances(self, agent):
        distances = {}
        others = [node for node in self.nodes if node != agent]
        for other in others:
            distances[other] = self.distance(agent, other)
        return distances

    def trade(self, agent1, agent2):
        success = False
        for r1 in RESOURCE_LIST:
            for r2 in RESOURCE_LIST:
                if r1 == r2:
                    continue
                if r1 == agent1.want and agent2.resources[r1] > 0:
                    agent2.resources[r1] -= 1
                    agent1.resources[r1] += 1
                    success = True
                if r1 == agent2.want and agent1.resources[r1] > 0:
                    agent1.resources[r1] -= 1
                    agent2.resources[r1] += 1
                    success = True
        return success

    def do_trades(self):
        self.traded_edges.clear()  # Clear previous trades
        for pair in self.edges:
            agent1, agent2 = pair
            if self.distance(agent1, agent2) < self.trade_distance:
                if agent1.want != agent2.want:
                    success = self.trade(agent1, agent2)
                    if success:
                        agent1.trading_with = agent2
                        agent2.trading_with = agent1
                        self.traded_edges.add(pair)  # Mark this edge as traded
                        agent1.step((agent2.loc - agent1.loc) / 2)
                        agent2.step((agent1.loc - agent2.loc) / 2)
                        print(
                            agent1.name
                            + " : "
                            + str(agent1.resources.get_tuple())
                            + " <-> "
                            + agent2.name
                            + " : "
                            + str(agent2.resources.get_tuple())
                        )
                else:
                    agent1.trading_with = None
                    agent2.trading_with = None
            else:
                agent1.trading_with = None
                agent2.trading_with = None

    def count_all_resources(self):
        resources = Resources()
        for agent in self.nodes:
            resources += agent.resources
        return resources

    def update(self):
        self.do_steps()
        self.do_trades()

    def check_for_winner(self):
        win_amount = 50
        for agent in self.nodes:
            if max(agent.resources.get_tuple()) >= win_amount:
                return agent
        return None


class App:
    def __init__(self, width=WIDTH, height=HEIGHT):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("syzm")
        pygame_icon = pygame.image.load("icon.png")
        pygame.display.set_icon(pygame_icon)
        self.clock = pygame.time.Clock()
        self.agents = []
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 16, bold=True)

    def draw_button(self, text, rect, color, text_color):
        """Draw a button with text."""
        pygame.draw.rect(self.screen, color, rect)
        button_text = self.font.render(text, True, text_color)
        text_rect = button_text.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
        self.screen.blit(button_text, text_rect)

    def start_screen(self):
        """Display the start screen with a Start button."""
        running = True
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)  # Button dimensions
        while running:
            self.screen.fill(BLACK)
            self.draw_button("START", button_rect, RED, WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):  # Check if the button is clicked
                        running = False  # Exit the start screen

            pygame.display.flip()
            self.clock.tick(FRAMERATE_DEFAULT)

    def draw_graph(self, graph: "AgentGraph"):
        # Draw edges
        for edge in graph.edges:
            agent1, agent2 = edge
            if edge in graph.traded_edges:
                pygame.draw.line(self.screen, MAGENTA, agent1.loc, agent2.loc, 3)  # Light color
            else:
                if self.clock.get_time() % 2 == 0:
                    pygame.draw.line(self.screen, random.choice(COLORS), agent1.loc, agent2.loc, 1)
                else:
                    pygame.draw.line(self.screen, BACKGROUND_COLOR + (10, 10, 10), agent1.loc, agent2.loc, 1)

        # Draw agents
        for agent in graph.nodes:
            pygame.draw.circle(self.screen, agent.color, agent.loc, 10)

            text = self.font.render(
                agent.name + " " + str(agent.resources.get_tuple()),
                True,
                opposite_color(agent.color),
            )
            text_rect = text.get_rect(center=(agent.loc[0], agent.loc[1]))
            self.screen.blit(text, text_rect)

            if agent.trading_with is not None:
                pygame.draw.line(self.screen, RED, agent.loc, agent.trading_with.loc, 5)

    def update(self, graph: "AgentGraph"):
        self.screen.fill(BACKGROUND_COLOR)
        graph.update()
        self.draw_graph(graph)
        pygame.display.flip()
        winner = graph.check_for_winner()
        if winner is not None:
            print(winner.name + " wins!")
            pygame.quit()
            sys.exit()

    def run(self, graph: "AgentGraph"):
        self.start_screen()  # Show the start screen before starting the simulation
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update(graph)
            self.clock.tick(FRAMERATE_DEFAULT)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    n_agents = N_AGENTS
    graph = AgentGraph()
    for i in range(n_agents):
        name = make_name(random.choice([1, 2, 3]))
        loc = np.random.randint(0, min(WIDTH, HEIGHT), 2)
        bearing = np.random.rand() * 2 * np.pi
        agent = Agent(name, loc=loc, bearing=bearing, color=random.choice(COLORS))
        graph.add_agent(agent)
    app = App()
    app.run(graph)
