import pygame
import random

WIDTH = 900
HEIGHT = 600
FPS = 70
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FIRSTLINE = 120
SECONDLINE = 175
THIRDLINE = 225
pygame.init()
enemy_list = []
lines_list = [FIRSTLINE,SECONDLINE,THIRDLINE]
liders = {}

window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

run = True
activLine = 0
score = 0
best_score = 0
spawn_timer = 10
work_name = ""
flag = True

with open('resources/Лидеры.txt', 'r') as file:
    for line in file:
        name, score_lider = line.strip().split()
        score_lider = int(score_lider)
        liders[name] = score_lider

font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))
def create_enemy():
    x = WIDTH
    y = random.choice([120, 175, 225])
    enemy_rect = image_enemy.get_rect()
    enemy_rect.width = 40
    enemy_rect.height = 40
    enemy_rect.x = 900
    enemy_rect.y = y
    enemy_list.append(enemy_rect)
def draw_enemies(enemy):
    for enemy_rect in enemy_list:
        window.blit(enemy, enemy_rect)

def move_enemies(speed):
    for enemy_rect in enemy_list:
        enemy_rect.left -= speed

def check_collision():
    for enemy_rect in enemy_list:
        if player_rect.colliderect(enemy_rect):
            return (True)

def clear():
    global score
    global enemy_list
    score = 0
    enemy_list.clear()

def save():
    global best_score
    liders[work_name] = best_score
    with open('resources/Лидеры.txt', 'w') as file:
        for name, score_le in liders.items():
            file.write(f"{name} {score_le}\n")

input_rect = pygame.Rect(50, 50, 200, 32)
button_rect = pygame.Rect(50, 100, 100, 50)
input_text = ""

imagePlayer = pygame.image.load('resources/car.png')
player_rect = imagePlayer.get_rect()
player_rect.width = 50
player_rect.height = 20
player_rect.x = 0
player_rect.y = FIRSTLINE
player = pygame.transform.scale(imagePlayer, (player_rect.width, player_rect.height))


image_enemy = pygame.image.load('resources/block.png')
enemy = pygame.transform.scale(image_enemy, (40, 40))

background_image = pygame.image.load('resources/road.png')
background_image = pygame.transform.scale(background_image, (3000, 600))
window.blit(background_image, (0, 0))

pygame.display.flip()

gamemode = "menu"
while run:
    if gamemode == "menu":
        window.fill(WHITE)

        draw_text("Главное меню", BLUE, WIDTH // 2, HEIGHT // 4)

        play_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
        leaderboard_button = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 70, WIDTH // 2, 50)

        pygame.draw.rect(window, GREEN, play_button)
        pygame.draw.rect(window, GREEN, leaderboard_button)

        draw_text("Играть", WHITE, WIDTH // 2, HEIGHT // 2 + 25)
        draw_text("Таблица лидеров", WHITE, WIDTH // 2, HEIGHT // 2 + 95)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    gamemode = "nik"
                elif leaderboard_button.collidepoint(event.pos):
                    gamemode = "liders"

    elif gamemode == "nik":
        window.fill(WHITE)
        flag = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for name in liders:
                        if name == input_text:
                            work_name = input_text
                            flag = False
                            break

                    if flag:
                        liders[input_text] = 0
                        work_name = input_text

                    best_score = liders[work_name]
                    gamemode = "start"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        pygame.draw.rect(window, BLACK, input_rect, 2)


        draw_text("Введите ник:", BLACK, WIDTH // 2, 25)

        input_surface = font.render(input_text, True, BLACK)
        window.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()

    elif gamemode == "start":
        window.blit(background_image, (0, 0))
        draw_score()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    if activLine > 0:
                        activLine -= 1
                elif i.key == pygame.K_DOWN:
                    if activLine < 2:
                        activLine += 1
                player_rect.y = lines_list[activLine]

        if spawn_timer == 0:
            create_enemy()
            spawn_timer = random.randint(30, 90)  # Рандомный интервал для спавна нового врага
        else:
            spawn_timer -= 1
        draw_enemies(enemy)
        move_enemies(4)

        if enemy_list and enemy_list[0].x == 0:
            score += 1
        enemy_list = [enemy_rect for enemy_rect in enemy_list if enemy_rect.right > 0]

        if check_collision():
            gamemode = "gameover"
        window.blit(player, player_rect)

    elif gamemode == "liders":
        window.fill(WHITE)

        draw_text("Назад", BLACK, 50, 25)
        draw_text("Таблица лидеров", BLACK, WIDTH // 2, 25)

        y_position = 60
        for name, score_l in liders.items():
            draw_text(f"{name}: {score_l}", BLACK, WIDTH // 2, y_position)
            y_position += 30

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Проверка клика по кнопке "Назад"
                if 10 < event.pos[0] < 100 and 10 < event.pos[1] < 50:
                    gamemode = "menu"
    elif gamemode == "gameover":
        window.fill(WHITE)

        draw_text("Game Over", BLUE, WIDTH // 2, HEIGHT // 4)
        draw_text(f"Score: {score}", BLUE, WIDTH // 2, HEIGHT // 4 + 40)
        draw_text(f"Best score: {best_score}", BLUE, WIDTH // 2, HEIGHT // 4 + 80)

        restart_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
        menu_button = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 70, WIDTH // 2, 50)

        pygame.draw.rect(window, GREEN, restart_button)
        pygame.draw.rect(window, GREEN, menu_button)

        draw_text("Заново", WHITE, WIDTH // 2, HEIGHT // 2 + 25)
        draw_text("В меню", WHITE, WIDTH // 2, HEIGHT // 2 + 95)

        pygame.display.flip()
        if (score > best_score):
            best_score = score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):

                    save()
                    clear()
                    gamemode = "start"
                elif menu_button.collidepoint(event.pos):
                    save()
                    clear()
                    gamemode = "menu"




    pygame.display.update()
    clock.tick(FPS)

pygame.quit()