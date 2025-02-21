import pygame
import sys

class Agent:
    def __init__(self, name, xyloc=(0, 0)):
        self.name = name
        self.xyloc = xyloc
    
    def move(self, x, y):
        self.xyloc = (x, y)
    
    def __str__(self):
        return self.name + " is at " + str(self.xyloc)
    
    def goal(self, x, y):

class App:
    def __init__(self, width=400, height=400):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Agent App")
        self.agents = []
        self.clock = pygame.time.Clock()
    
    def add_agent(self, agent):
        self.agents.append(agent)
        self.draw_agent(agent)
    
    def draw_agent(self, agent):
        x, y = agent.xyloc
        pygame.draw.circle(self.screen, (0, 0, 255), (x, y), 10)
        font = pygame.font.Font(None, 24)
        text = font.render(agent.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)
    
    def update_agents(self):
        self.screen.fill((0, 0, 0))
        for agent in self.agents:
            self.draw_agent(agent)
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
    
    agent1 = Agent("Agent1", (50, 50))
    agent2 = Agent("Agent2", (100, 100))
    
    app.add_agent(agent1)
    app.add_agent(agent2)
    
    agent1.move(150, 150)
    
    app.run()