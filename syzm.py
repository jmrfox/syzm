import pygame
import sys
import numpy as np

WIDTH = 800
HEIGHT = 600
TORUS = True

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

BACKGROUND_COLOR = np.ones(3) * 30

import random
import string

def generate_random_name(sylb=2):
    """Generate a random name following common English name tendencies."""
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    syllables = ["ba", "be", "bi", "bo", "bu", "da", "de", "di", "do", "du", "fa", "fe", "fi", "fo", "fu", "ga", "ge", "gi", "go", "gu", "ha", "he", "hi", "ho", "hu", "ja", "je", "ji", "jo", "ju", "ka", "ke", "ki", "ko", "ku", "la", "le", "li", "lo", "lu", "ma", "me", "mi", "mo", "mu", "na", "ne", "ni", "no", "nu", "pa", "pe", "pi", "po", "pu", "ra", "re", "ri", "ro", "ru", "sa", "se", "si", "so", "su", "ta", "te", "ti", "to", "tu", "va", "ve", "vi", "vo", "vu", "wa", "we", "wi", "wo", "wu", "ya", "ye", "yi", "yo", "yu", "za", "ze", "zi", "zo", "zu"]
    name = ""

    for i in range(sylb):
        name = name + random.choice(syllables)
        if random.random() < 0.1:
            name = name + random.choice(vowels)
        if random.random() < 0.1:
            name = name + random.choice(consonants)
                

    return ''.join(name).capitalize()

def name(sylb=3):
    return generate_random_name(sylb)
 
class Resources(dict):
    def __init__(self):
        super().__init__()
        self["dew"] = 0
        self["bast"] = 0
        self["sap"] = 0
        
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
    
        
class Agent:
    def __init__(self, name, loc=np.array([0, 0]), color=None):
        self.name = name
        self.loc = loc
        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color
        self.resources = Resources()
        self.trading = False
        self.trading_with = None
        
    def proximity(self, other: "Agent"):
        return np.linalg.norm(self.loc - other.loc)
    
    def step(self, step=np.array([0, 0])):
        if TORUS:
            self.loc = np.mod(self.loc + step, np.array([WIDTH, HEIGHT]))
        else:
            self.loc = np.clip(self.loc + step, np.array([0, 0]), np.array([WIDTH, HEIGHT]))
        
    def __str__(self):
        return self.name + " is at " + str(self.loc)
    

class App:
    def __init__(self, width=WIDTH, height=HEIGHT):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("syzm")
        pygame_icon = pygame.image.load('icon.png')
        pygame.display.set_icon(pygame_icon)
        self.clock = pygame.time.Clock()
        self.agents = []
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 20, bold=True)
        
        
    def add_agent(self, agent):
        self.agents.append(agent)
        self.draw_agent(agent)
    
    def draw_agent(self, agent):
        pygame.draw.circle(self.screen, agent.color, agent.loc, 20)
        text = self.font.render(agent.name, True, opposite_color(agent.color))
        text_rect = text.get_rect(center=agent.loc)
        self.screen.blit(text, text_rect)
    
    def update_agents(self):
        self.screen.fill(BACKGROUND_COLOR)
        for agent in self.agents:
            if np.random.rand() < 0.1:
                step = np.random.randint(-20, 20, 2)
                agent.step(step)
            distances = {}
            for other in self.agents:
                if other != agent:
                    distances[other] = agent.proximity(other)
            closest = min(distances, key=distances.get)
            if agent.proximity(closest) < 20:
                agent.trading = True
                agent.trading_with = closest
            else:
                agent.trading = False
                agent.trading_with = None
            self.draw_agent(agent)
            if agent.trading:
                print(agent.name + " is trading with " + agent.trading_with.name)
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update_agents()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()

    n_agents = 10
    
    for i in range(n_agents):
        agent = Agent(name(random.choice([1,2,3])), np.random.randint(0, min(WIDTH, HEIGHT), 2))
        app.add_agent(agent)
        
    app.run()