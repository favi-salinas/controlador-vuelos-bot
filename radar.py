import pygame
import math
import sys
import os
import time

# Inicialización
pygame.init()
WIDTH, HEIGHT = 800, 800
CENTER = WIDTH // 2, HEIGHT // 2
RADAR_RADIUS = 350
FPS = 60

# Colores
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radar de Aviones con Permisos desde GitHub")
font = pygame.font.SysFont(None, 24)

# Clase Avión
class Plane:
    def __init__(self, id, angle, mode):
        self.id = id
        self.angle = angle
        self.distance = RADAR_RADIUS
        self.mode = mode  # "aterrizar" o "despegar"
        self.speed = 0.3
        self.waiting = False
        self.landed = False
        self.departed = False

    def move(self):
        if self.mode == "aterrizar":
            if self.landed:
                return
            if self.distance > 50:
                self.distance -= self.speed
            else:
                if not self.waiting:
                    self.waiting = True
                    print(f"🛬 Avión {self.id} solicita permiso para aterrizar.")
                elif check_permission(self.id):
                    self.landed = True
                    print(f"✅ Avión {self.id} ha aterrizado.")
        elif self.mode == "despegar":
            if self.departed:
                return
            if self.distance < RADAR_RADIUS:
                if check_permission(self.id):
                    self.distance += self.speed
                else:
                    if not self.waiting:
                        print(f"🛫 Avión {self.id} solicita permiso para despegar.")
                        self.waiting = True
            else:
                self.departed = True
                print(f"✅ Avión {self.id} ha despegado.")

    def get_position(self):
        rad = math.radians(self.angle)
        x = CENTER[0] + math.cos(rad) * self.distance
        y = CENTER[1] + math.sin(rad) * self.distance
        return int(x), int(y)

# Verifica permiso con archivo de texto
def check_permission(plane_id):
    return os.path.exists(f"permisos/permiso_{plane_id}.txt")

# Lista de aviones
planes = [
    Plane("AV101", 45, "aterrizar"),
    Plane("AV202", 135, "despegar"),
    Plane("AV303", 250, "aterrizar"),
    Plane("AV404", 320, "despegar"),
]

# Animación
clock = pygame.time.Clock()
angle = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(GRAY)

    # Fondo del radar
    pygame.draw.rect(screen, BLACK, (50, 50, WIDTH - 100, HEIGHT - 100))
    pygame.draw.circle(screen, GREEN, CENTER, RADAR_RADIUS, 1)

    # Barrido del radar
    rad = math.radians(angle)
    end_x = CENTER[0] + math.cos(rad) * RADAR_RADIUS
    end_y = CENTER[1] + math.sin(rad) * RADAR_RADIUS
    pygame.draw.line(screen, DARK_GREEN, CENTER, (end_x, end_y), 2)
    angle = (angle + 1) % 360

    for plane in planes:
        plane.move()
        if not plane.landed and not plane.departed:
            x, y = plane.get_position()
            pygame.draw.circle(screen, WHITE, (x, y), 5)
            label = font.render(plane.id, True, WHITE)
            screen.blit(label, (x + 5, y - 5))

    pygame.display.flip()
    clock.tick(FPS)
