import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the player
player_width, player_height = 50, 50
player = pygame.Rect(width // 2 - player_width // 2, height - player_height - 10, player_width, player_height)

# Set up game variables
player_speed = 3
bullet_speed = 5
bullets = []
font = pygame.font.Font(None, 36)
score = 0
round_num = 1
drones_to_destroy = 7
enemies = []
enemy_width, enemy_height = 40, 40

def spawn_enemies():
    enemies.clear()
    for _ in range(drones_to_destroy):
        enemy = pygame.Rect(random.randint(0, width - enemy_width), random.randint(0, height // 2), enemy_width, enemy_height)
        enemies.append(enemy)

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player.centerx - 2, player.top - 10, 4, 10)
                bullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < width:
        player.x += player_speed

    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    if not enemies:
        round_num += 1
        drones_to_destroy = min(round_num * 2, 15)  # Max of 15 drones
        spawn_enemies()

    for enemy in enemies:
        enemy.y += 1
        if enemy.colliderect(player):
            display.fill(BLACK)
            end_text = font.render("You Lost!", True, RED)
            display.blit(end_text, (width // 2 - end_text.get_width() // 2, height // 2 - end_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()
        if enemy.bottom > height:
            spawn_enemies()

    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                if score == 100:
                    display.fill(BLACK)
                    end_text = font.render("You Won!", True, RED)
                    display.blit(end_text, (width // 2 - end_text.get_width() // 2, height // 2 - end_text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    pygame.quit()
                    sys.exit()

    display.fill(BLACK)
    pygame.draw.rect(display, RED, player)
    for enemy in enemies:
        pygame.draw.rect(display, WHITE, enemy)
    for bullet in bullets:
        pygame.draw.rect(display, WHITE, bullet)

    score_text = font.render(f"Score: {score}", True, WHITE)
    round_text = font.render(f"Round: {round_num}", True, WHITE)
    display.blit(score_text, (10, 10))
    display.blit(round_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)
