import pygame
import sys
import random  # Import random for generating random positions and colors

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visual Display")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load image
icon = pygame.image.load("icon.png")
icon_rect = icon.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the image

# Number of pixels to change
N = 3


# Main loop
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(BLACK)  # Background is black

        # Draw shapes
        pygame.draw.rect(screen, RED, (100, 100, 200, 150))
        pygame.draw.circle(screen, BLUE, (400, 300), 50)

        # Draw the image
        screen.blit(icon, icon_rect)

        # Change N random pixels to random colors and then back to black
        pixels = []
        for _ in range(N):
            random_x = random.randint(0, WIDTH - 1)
            random_y = random.randint(0, HEIGHT - 1)
            random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            screen.set_at((random_x, random_y), random_color)  # Set the pixel to a random color
            pixels.append((random_x, random_y))  # Store the pixel coordinates

        pygame.display.flip()  # Update the display to show the changes
        pygame.time.delay(50)  # Delay to make the changes visible

        # Set the pixels back to black
        for x, y in pixels:
            screen.set_at((x, y), BLACK)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
