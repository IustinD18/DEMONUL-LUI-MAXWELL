import pygame
import random
import math

# Inițializare Pygame
pygame.init()

# Dimensiuni ecran (similar cu 800x600 din turtle)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maxwell's Demon Model (Pygame)")

clock = pygame.time.Clock()

# Limitele containerului în coordonate "simulare"
sim_left = -300
sim_right = 300
sim_top = 200
sim_bottom = -200


def sim_to_screen(x, y):
    # În Pygame (0,0) e în stânga sus; mutăm originea în centrul ecranului și inversăm axa y
    screen_x = x + screen_width // 2
    screen_y = screen_height // 2 - y
    return (screen_x, screen_y)

# Clasa pentru molecule
class Molecule:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        # Calculăm magnitudinea vitezei 
        self.speed = math.sqrt(dx**2 + dy**2)
        self.color = color
        self.radius = 3  # Raza cercului ce reprezintă molecula

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        pos = sim_to_screen(self.x, self.y)
        pygame.draw.circle(surface, self.color, pos, self.radius)

# Listele de viteze, similare cu cele din codul original:
speed_warm = [-3, -2.8, -2.5, -2.3, -2, -1.5, -1, 1, 1.5, 2, 2.3, 2.5, 2.8, 3]
speed_cold = [-2, -1.5, -1.3, -1.2, -1, -0.7, -0.5, -0.2, 0.2, 0.5, 0.7, 1, 1.3, 1.5, 2]

N = 300  # Numărul de molecule pentru fiecare grup

ball_list_warm = []
ball_list_cold = []

# Creăm moleculele "reci" (albastre) în camera din stânga:
for i in range(N):
    x = random.randint(-280, -100)
    y = random.randint(sim_bottom, sim_top)
    dx = random.choice(speed_cold)
    dy = random.choice(speed_cold)
    ball_list_cold.append(Molecule(x, y, dx, dy, (0, 0, 255)))  # Albastru

# Creăm moleculele "calde" (roșii) în camera din dreapta:
for i in range(N):
    x = random.randint(100, 290)
    y = random.randint(sim_bottom + 10, sim_top - 10)
    dx = random.choice(speed_warm)
    dy = random.choice(speed_warm)
    ball_list_warm.append(Molecule(x, y, dx, dy, (255, 0, 0)))  # Roșu

# Bucla principală
running = True
while running:
    clock.tick(60)  # Limităm la 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizare molecule "calde"
    for ball in ball_list_warm[:]:
        ball.move()
        # Demonul la lucru pentru moleculele calde:
        if ball.x < 10 and ball.speed < 2.2:
            ball_list_warm.remove(ball)
            ball_list_cold.append(ball)
            ball.color = (0, 255, 255)  # Cyan
            ball.x = -10  # Mutăm molecula în camera rece
        else:
            # Verificăm coliziunile cu pereții: pentru moleculele calde se respinge la x<0 și x>290
            if ball.x < 0 or ball.x > 290:
                ball.dx *= -1
            # Verificăm coliziunile cu tavanul și podeaua (folosim y = -190 și y = 190)
            if ball.y < -190 or ball.y > 190:
                ball.dy *= -1

    # Actualizare molecule "reci"
    for ball in ball_list_cold[:]:
        ball.move()
        # Demonul la lucru pentru moleculele reci:
        if ball.x > -10 and ball.speed > 2.2:
            ball_list_cold.remove(ball)
            ball_list_warm.append(ball)
            ball.color = (255, 165, 0)  # Orange
            ball.x = 10  # Mutăm molecula în camera caldă
        else:
            # Moleculele reci se resping dacă ating x > 0 sau x < -290
            if ball.x > 0 or ball.x < -290:
                ball.dx *= -1
            if ball.y < -190 or ball.y > 190:
                ball.dy *= -1

    # Desenăm totul
    screen.fill((0, 0, 0))  # Fundal negru

    # Desenăm pereții containerului: dreptunghiul exterior
    outer_points = [(-300, 200), (300, 200), (300, -200), (-300, -200)]
    outer_points_screen = [sim_to_screen(x, y) for (x, y) in outer_points]
    pygame.draw.lines(screen, (255, 255, 255), True, outer_points_screen, 3)

    # Desenăm linia de divizare (ușa demonului) de la (0,200) la (0,-200)
    start_line = sim_to_screen(0, 200)
    end_line = sim_to_screen(0, -200)
    pygame.draw.line(screen, (255, 255, 255), start_line, end_line, 3)

    # Desenăm moleculele
    for ball in ball_list_warm:
        ball.draw(screen)
    for ball in ball_list_cold:
        ball.draw(screen)

    pygame.display.flip()

pygame.quit()
