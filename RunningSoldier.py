# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading

from pygame import mixer

import pygame

import time

pygame.init()

# Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Running Soldier")

Ico = pygame.image.load("assets/Soldier/r_run/tile008.png")
pygame.display.set_icon(Ico)


RUNNING = [
    pygame.image.load(os.path.join("assets/TheProtectorOfWorld/ship", "tile006.png")),
    pygame.image.load(os.path.join("assets/TheProtectorOfWorld/ship", "tile007.png")),
    pygame.image.load(os.path.join("assets/TheProtectorOfWorld/ship", "tile008.png")),
]
DEAD = [pygame.image.load(os.path.join("assets/Soldier/r_dead", "tile007.png"))]

Slime = pygame.image.load(os.path.join("assets/TheProtectorOfWorld/Monster", "slime.png"))

Alien = pygame.image.load(os.path.join("assets/TheProtectorOfWorld/Monster", "alien.png"))

BIG_EYE = pygame.image.load(os.path.join("assets/TheProtectorOfWorld/Monster", "bigeye.png"))

SHOOT = pygame.image.load(os.path.join("assets/TheProtectorOfWorld/ship", "tile007.png"))

BG = pygame.image.load(os.path.join("assets/TheProtectorOfWorld/background", "background.png"))

BULLET = pygame.image.load(os.path.join("assets/Other", "bullet_image.png"))

BULLET_Boss = pygame.image.load(os.path.join("assets/Boss", "bossbulet.png"))

Boss1 = pygame.image.load(os.path.join("assets/Boss", "BossLevel1.png"))

Boss2 = pygame.image.load(os.path.join("assets/Boss", "BossLevel2.png"))

BOMB = pygame.image.load(os.path.join("assets/Other","Bomb_03.png"))

scaled_image = pygame.transform.scale(BOMB, (64, 64))

scaled_bg = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

scaled_bigeye = pygame.transform.scale(BIG_EYE, (64, 64))

scaled_Slime = pygame.transform.scale(Slime, (64,64))

scaled_Alien = pygame.transform.scale(Alien, (64,64))

scaled_Bullet = pygame.transform.scale(BULLET_Boss, (98,98))

scaled_Boss1 = pygame.transform.scale(Boss1, (128,128))

scaled_Boss2 = pygame.transform.scale(Boss2, (128,128))

FONT_COLOR=(0,0,0)

class Background():
    def __init__(self):
        self.bg_images = [pygame.image.load(os.path.join("assets/TheProtectorOfWorld/background/background3.PNG")) for _ in range(4)]
        #self.bg_image2 =  [pygame.image.load(os.path.join("assets/Other", "Background.png")) for _ in range(4)]
        self.rectBGimg = self.bg_images[0].get_rect()

        self.bgY = 0
        self.bgX = [i * self.rectBGimg.width for i in range(4)]

        self.bgY2 = self.rectBGimg.height

    def update(self):
        for i in range(4):
            self.bgX[i] -= game_speed
            if self.bgX[i] <= -self.rectBGimg.width:
                self.bgX[i] = (3 * self.rectBGimg.width) + self.bgX[i]

    def render(self):
        for i in range(4):
            SCREEN.blit(self.bg_images[i], (self.bgX[i], self.bgY))
            SCREEN.blit(self.bg_images[i], (self.bgX[i], self.bgY2))

fireballs=[]
bullet_items = []
fireball_count = 3
bomb_items=[]
back_ground = Background()

# class music_bgm:
#     def __init__(self):
#         self.music_channel = mixer.Channel(0)
#         self.music_channel.set_volume(0.2)

#         self.sounds_list = {
#             'bgm':mixer.Sound('sounds/bgm.wav')
#         }

class Fireball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = BULLET
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 20

    def move(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def collides_with(self, obstacle):
        # Use the rect attribute for collision detection
        return self.rect.colliderect(obstacle.rect)

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = scaled_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 20

    def move(self):
        self.rect.x += self.speed

    def draw(self, screen):
        scaled_image = pygame.transform.scale(BOMB, (64, 64))
        screen.blit(scaled_image, self.rect)
    
    def collides_with(self, obstacle):
        # Use the rect attribute for collision detection
        return self.rect.colliderect(obstacle.rect)

class soldier:

    X_POS = 80
    Y_POS = 330
    JUMP_VEL = 8.5
    MAX_Y_POS = 550  
    MIN_Y_POS = 100  
    MAX_X_POS = 1000  
    MIN_X_POS = 100 
    VERTICAL_MOVE_SPEED = 10  # Speed of vertical movement

    def __init__(self):
        self.run_img = RUNNING
        self.dead_img = DEAD
        self.shoot_img = SHOOT

        self.soldier_duck = False
        # self.soldier_run = True
        self.soldier_jump = False
        self.soldier_dead = False
        self.soldier_shoot = False

        self.step_index = 0
        self.jump_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.soldier_rect = self.image.get_rect()
        self.soldier_rect.x = self.X_POS
        self.soldier_rect.y = self.Y_POS
        self.hitbox = self.soldier_rect.inflate(-20, -10)
        
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        
        self.last_shot_time = 0
        self.shoot_delay = 500

        self.sounds_list = {
            'item_collect': mixer.Sound('sounds/item_collect.wav'),
            'bomb': mixer.Sound('sounds/bomb.wav'),
            'Hit': mixer.Sound('sounds/Hit.wav'),
            'jump': mixer.Sound('sounds/jump.wav'),
            'next_level': mixer.Sound('sounds/next_level.wav'),
            'shot': mixer.Sound('sounds/shot.wav'),
            'slow': mixer.Sound('sounds/slow.wav')
        }
        
        self.hit=False


    def update(self, userInput):
        self.hitbox = self.soldier_rect.inflate(-100, 0)

        if self.soldier_duck:
            self.duck()
        # if self.soldier_run:
        #     self.run()
        if self.soldier_jump:
            self.jump()
        if self.soldier_dead:
            if self.hit==False:
                self.music_channel.play(self.sounds_list['Hit'])
                self.hit=True
            self.dead()
        
        if userInput[pygame.K_UP] and self.soldier_rect.y > self.MIN_Y_POS:
            self.soldier_rect.y -= self.VERTICAL_MOVE_SPEED
        elif userInput[pygame.K_DOWN] and self.soldier_rect.y < self.MAX_Y_POS:
            self.soldier_rect.y += self.VERTICAL_MOVE_SPEED
        elif userInput[pygame.K_RIGHT] and self.soldier_rect.x < self.MAX_X_POS:
            self.soldier_rect.x += self.VERTICAL_MOVE_SPEED
        elif userInput[pygame.K_LEFT] and self.soldier_rect.x > self.MIN_X_POS:
            self.soldier_rect.x -= self.VERTICAL_MOVE_SPEED
        
        if self.soldier_shoot:
            self.shoot()

        if self.step_index >= 8:
            self.step_index = 0

        # if (userInput[pygame.K_UP]) and not self.soldier_jump:
        #     self.soldier_rect.y -=10
        # elif userInput[pygame.K_DOWN] and not self.soldier_jump:
        #     self.soldier_rect.y +=10
        # elif not (self.soldier_jump or userInput[pygame.K_DOWN]):
        #     self.soldier_duck = False
        #     self.soldier_run = True
        #     self.soldier_jump = False

        if self.soldier_dead:
            self.soldier_run = False
            self.soldier_duck = False
            self.soldier_jump = False
            self.soldier_dead = True

    # def run(self):
    #     if self.step_index == 2:
    #         self.step_index = 0
    #     self.image = self.run_img[self.step_index]
    #     self.soldier_rect = self.image.get_rect()
    #     self.step_index += 1

    def jump(self):
        self.image = self.jump_img[self.jump_index]
        if self.soldier_jump:
            self.soldier_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.soldier_jump = False
            self.jump_vel = self.JUMP_VEL
        
    
    def dead(self):
        self.image = self.dead_img[0]
    
    def shoot(self):
        current_time = pygame.time.get_ticks()

        # Check if enough time has passed since the last shot
        if current_time - self.last_shot_time > self.shoot_delay:
            # Update the last shot time
            self.last_shot_time = current_time

            # Perform shooting actions
            self.image = self.shoot_img
            self.music_channel.play(self.sounds_list['shot'])
            fireballs.append(Fireball(self.soldier_rect.x, self.soldier_rect.y))
            return True
        return False

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.soldier_rect.x, self.soldier_rect.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.health = 0

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)


class SLIME(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)
        self.rect.y = random.randint(200,SCREEN_HEIGHT-200)
        self.health = 1


class ALIEN(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = random.randint(200,SCREEN_HEIGHT-200)
        self.health = 2


class Big_eye(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(200,SCREEN_HEIGHT-200)
        self.index = 0
        self.health = 4

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        self.index += 1
class Boss(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)  # Use type 0 for the boss
        self.rect.y = SCREEN_HEIGHT // 2  # Initial vertical position
        self.rect.x = SCREEN_WIDTH -200
        self.health = 4
        self.direction = 1

    def update(self):
        self.rect.y += 2 * self.direction  

        if self.rect.y <= 0 or self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.direction *= -1
            
    def is_dead(self):
        return self.health <= 0

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        
class BossStage2(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)  # Use type 0 for the boss
        self.rect.y = SCREEN_HEIGHT // 2  # Initial vertical position
        self.rect.x = SCREEN_WIDTH -200
        self.health = 8
        self.direction = 1

    def update(self):
        self.rect.y += 4 * self.direction  

        if self.rect.y <= 0 or self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.direction *= -1
            
    def is_dead(self):
        return self.health <= 0

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        
class Boss_Bullet(Obstacle):  
    def __init__(self, image, boss_rect_y):
        super().__init__(image, 0) 
        self.rect.y = boss_rect_y
        self.rect.x = SCREEN_WIDTH -200
        self.health = 1000
        
class BulletItem:
    def __init__(self):
        self.image = pygame.image.load(os.path.join("assets/Other", "bullet_image.png"))  # Replace with your item image path
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, 350)  # Random height
        
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)

        self.sounds_list = {
            'item_collect': mixer.Sound('sounds/item_collect.wav'),
            'bomb': mixer.Sound('sounds/bomb.wav'),
        }

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            # Remove the item if it goes off the screen
            bullet_items.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class BombItem:
    def __init__(self):
        self.image = scaled_image  # Replace with your item image path
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, 350)  # Random height
        
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)

        self.sounds_list = {
            'bomb': mixer.Sound('sounds/bomb.wav')
        }

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            # Remove the item if it goes off the screen
            bomb_items.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main_l1():
    global fireballs, fireball_count, death_count, distance_l1
    global game_speed, x_pos_bg, y_pos_bg, points_l1, obstacles
    distance_l1 = 0
    run = True
    clock = pygame.time.Clock()
    player = soldier()
    # music = music_bgm()
    game_speed = 2
    x_pos_bg = 0
    y_pos_bg = 380
    points_l1 = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False
    fireball_count = 3
    
    last_obstacle_spawn_time = time.time()
    
    boss_appear = False

    pygame.key.set_repeat(50, 50)

    def display_bullet_count():
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render(f'Bullets: {fireball_count}', True, FONT_COLOR)
        text_rect = text.get_rect(topleft=(10, 10))  # Position at top-left corner
        SCREEN.blit(text, text_rect)

    def score_l1():
        global points_l1, game_speed, distance_l1
        distance_l1 += 1
        if distance_l1 % 300 == 0:
            game_speed += 1
        # with open("score.txt", "r") as f:
        #     score_ints = [int(x) for x in f.read().split()]  
        #     highscore = max(score_ints)
        #     if points_l1 > highscore:
        #         highscore=points_l1 
        #     text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points_l1), True, FONT_COLOR)
        text = font.render("  Points: " + str(points_l1), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    # def background():
    #     global x_pos_bg, y_pos_bg
    #     image_width = BG.get_width()
    #     SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    #     SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    #     if x_pos_bg <= -image_width:
    #         SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    #         x_pos_bg = 0
    #     x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    run = False
                    paused()
                
                if event.key == pygame.K_SPACE and fireball_count > 0:
                    if player.shoot():
                        fireball_count -= 1
                if event.key == pygame.K_UP:
                    player.soldier_rect.y = max(player.MIN_Y_POS, player.soldier_rect.y - player.VERTICAL_MOVE_SPEED)
                if event.key == pygame.K_DOWN:
                    player.soldier_rect.y = min(player.MAX_Y_POS, player.soldier_rect.y + player.VERTICAL_MOVE_SPEED)


            # Add bullet items to the game
        if random.randint(0, 60) == 5:  # Adjust the frequency as needed
            bullet_items.append(BulletItem())
        
        if random.randint(0, 200) == 5:  # Adjust the frequency as needed
            bomb_items.append(BombItem())

        # Update and draw bullet items
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            item.update()
            item.draw(SCREEN)
        
        for item in bomb_items[:]:
            item.update()
            item.draw(SCREEN)

        # Check for collisions with bullet items
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            if player.soldier_rect.colliderect(item.rect):
                player.music_channel.play(player.sounds_list['item_collect'])
                fireball_count += 1  # Increase bullet count
                bullet_items.remove(item)  # Remove the collected item
        
        for item in bomb_items[:]:  # Use a slice copy to iterate safely when removing items
            if player.soldier_rect.colliderect(item.rect):
                if boss_appear == False:
                    player.music_channel.play(player.sounds_list['bomb'])
                    points_l1 += len(obstacles)*50
                    obstacles.clear()
                    bomb_items.remove(item)  # Remove the collected item
            # player.music_channel.play(player.sounds_list['bgm'], loops=-1)
                else:
                    for obstacle in obstacles:
                        obstacle.health-=1
                        print("Obstacle Health:", obstacle.health)
                    player.music_channel.play(player.sounds_list['bomb'])
                    bomb_items.remove(item)
        fireballs = [fireball for fireball in fireballs if fireball.x < SCREEN_WIDTH]

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        # background()
        back_ground.update()
        back_ground.render()
        player.draw(SCREEN)
        player.update(userInput)
        
        if boss_appear == False:
            if len(obstacles) <= 3:
                current_time = time.time()
                time_since_last_spawn = current_time - last_obstacle_spawn_time
                if time_since_last_spawn > 1.5:  
                    if random.randint(0, 2) == 0:
                        obstacles.append(SLIME(scaled_Slime))
                    elif random.randint(0, 2) == 1:
                        obstacles.append(ALIEN(scaled_Alien))
                    else:
                        obstacles.append(Big_eye(scaled_bigeye))

                    last_obstacle_spawn_time = current_time
        else:
            if len(obstacles) <= 3:
                current_time = time.time()
                time_since_last_spawn = current_time - last_obstacle_spawn_time
                if time_since_last_spawn > 1.5:  
                    boss_instance = next((obstacle for obstacle in obstacles if isinstance(obstacle, Boss)), None)
                    obstacles.append(Boss_Bullet(scaled_Bullet, boss_instance.rect.y))
                    last_obstacle_spawn_time = current_time
            
        if points_l1 >= 1000 and not boss_appear:
            obstacles.clear()

            # Append a boss
            obstacles.append(Boss(scaled_Boss1))
            boss_appear = True
            
        for obstacle in obstacles:
            if isinstance(obstacle, Boss) and obstacle.is_dead():
                level_transition()

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.hitbox.colliderect(obstacle.rect):
                death_count+=1
                player.dead()
                pygame.time.delay(1000)
                menu(death_count)

            for fireball in fireballs:
                if fireball.collides_with(obstacle):
                    if obstacle.health>0:
                        obstacle.health-=1
                        print("Obstacle Health:", obstacle.health)
                    else:
                        obstacles.remove(obstacle)
                        points_l1 += 50
                    fireballs.remove(fireball)
                    break
        
        

        for fireball in fireballs:
            fireball.move()
            fireball.draw(SCREEN)
        
        for item in bomb_items[:]:
            item.draw(SCREEN)
        
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            item.draw(SCREEN)
        display_bullet_count()

        score_l1()

        clock.tick(60)
        pygame.display.update()
    

def main_l2():
    global fireballs, fireball_count, death_count, distance_l2
    global game_speed, x_pos_bg, y_pos_bg, points_l2, obstacles
    distance_l2 = 0
    run = True
    clock = pygame.time.Clock()
    player = soldier()
    game_speed = 2
    x_pos_bg = 0
    y_pos_bg = 380
    points_l2 = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False
    fireball_count = 3
    
    boss_appear = False
    
    last_obstacle_spawn_time = time.time()

    pygame.key.set_repeat(50, 50)

    def display_bullet_count():
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render(f'Bullets: {fireball_count}', True, FONT_COLOR)
        text_rect = text.get_rect(topleft=(10, 10))  # Position at top-left corner
        SCREEN.blit(text, text_rect)

    def score_l2():
        global points_l2, game_speed, distance_l2
        distance_l2 += 1
        if distance_l2 % 200 == 0:
            game_speed += 1
        # with open("score.txt", "r") as f:
        #     score_ints = [int(x) for x in f.read().split()]  
        #     highscore = max(score_ints)
        #     if points_l1 > highscore:
        #         highscore=points_l1 
        #     text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points_l1), True, FONT_COLOR)
        text = font.render("  Points: " + str(points_l2), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    # def background():
    #     global x_pos_bg, y_pos_bg
    #     image_width = BG.get_width()
    #     SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    #     SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    #     if x_pos_bg <= -image_width:
    #         SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    #         x_pos_bg = 0
    #     x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    run = False
                    paused()
                if event.key == pygame.K_SPACE and fireball_count > 0:
                    if player.shoot():
                        fireball_count -= 1
                if event.key == pygame.K_UP:
                    player.soldier_rect.y = max(player.MIN_Y_POS, player.soldier_rect.y - player.VERTICAL_MOVE_SPEED)
                if event.key == pygame.K_DOWN:
                    player.soldier_rect.y = min(player.MAX_Y_POS, player.soldier_rect.y + player.VERTICAL_MOVE_SPEED)


            # Add bullet items to the game
        if random.randint(0, 60) == 5:  # Adjust the frequency as needed
            bullet_items.append(BulletItem())
        
        if random.randint(0, 200) == 5:  # Adjust the frequency as needed
            bomb_items.append(BombItem())

        # Update and draw bullet items
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            item.update()
            item.draw(SCREEN)
        
        for item in bomb_items[:]:
            item.update()
            item.draw(SCREEN)

        # Check for collisions with bullet items
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            if player.soldier_rect.colliderect(item.rect):
                player.music_channel.play(player.sounds_list['item_collect'])
                fireball_count += 1  # Increase bullet count
                bullet_items.remove(item)  # Remove the collected item
        
        for item in bomb_items[:]:  # Use a slice copy to iterate safely when removing items
            if player.soldier_rect.colliderect(item.rect):
                if boss_appear == False:
                    player.music_channel.play(player.sounds_list['bomb'])
                    points_l2 += len(obstacles)*50
                    obstacles.clear()
                    bomb_items.remove(item)  # Remove the collected item
            # player.music_channel.play(player.sounds_list['bgm'], loops=-1)
                else:
                    for obstacle in obstacles:
                        obstacle.health-=1
                        print("Obstacle Health:", obstacle.health)
                    player.music_channel.play(player.sounds_list['bomb'])
                    bomb_items.remove(item)
        
        fireballs = [fireball for fireball in fireballs if fireball.x < SCREEN_WIDTH]

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        # background()
        back_ground.update()
        back_ground.render()

        player.draw(SCREEN)
        player.update(userInput)
        if boss_appear == False:
            if len(obstacles) <= 5:
                current_time = time.time()
                time_since_last_spawn = current_time - last_obstacle_spawn_time
                if time_since_last_spawn > 1.0: 
                    if random.randint(0, 2) == 0:
                        obstacles.append(SLIME(scaled_Slime))
                    elif random.randint(0, 2) == 1:
                        obstacles.append(ALIEN(scaled_Alien))
                    else:
                        obstacles.append(Big_eye(scaled_bigeye))
                    last_obstacle_spawn_time = current_time
        else:
            if len(obstacles) <= 2:
                current_time = time.time()
                time_since_last_spawn = current_time - last_obstacle_spawn_time
                if time_since_last_spawn > 1.0:  
                    boss_instance = next((obstacle for obstacle in obstacles if isinstance(obstacle, BossStage2)), None)
                    obstacles.append(Boss_Bullet(scaled_Bullet, boss_instance.rect.y-30))
                    obstacles.append(Boss_Bullet(scaled_Bullet, boss_instance.rect.y+30))
                    last_obstacle_spawn_time = current_time

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.hitbox.colliderect(obstacle.rect):
                death_count+=1
                player.dead()
                pygame.time.delay(1000)
                menu(death_count)
            for fireball in fireballs:
                if fireball.collides_with(obstacle):
                    if obstacle.health>0:
                        obstacle.health-=1
                        print("Obstacle Health:", obstacle.health)
                    else:
                        obstacles.remove(obstacle)
                        points_l2 += 50
                    fireballs.remove(fireball)
                    break


        if points_l2 >= 2500 and not boss_appear:
            obstacles.clear()

            # Append a boss
            obstacles.append(BossStage2(scaled_Boss2))
            boss_appear = True
            
        for obstacle in obstacles:
            if isinstance(obstacle, BossStage2) and obstacle.is_dead():
                end_dialogue()

        for fireball in fireballs:
            fireball.move()
            fireball.draw(SCREEN)
        
        for item in bomb_items[:]:
            item.draw(SCREEN)
        
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            item.draw(SCREEN)

        display_bullet_count()

        score_l2()

        clock.tick(60)
        pygame.display.update()


def menu(death_count):
    global points_l1, points_l2
    global FONT_COLOR
    run = True
    while run:
        FONT_COLOR=(255,255,255)
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Protector Of World, Press enter to play", True, FONT_COLOR)
        elif death_count > 0:
            text = font.render("World have been invaded!", True, FONT_COLOR)
            score = font.render("Your Score: " + str(points_l1), True, FONT_COLOR)
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            f = open("score.txt", "a")
            f.write(str(points_l1) + "\n")
            f.close()
            with open("score.txt", "r") as f:
                score = (
                    f.read()
                )  # Read all file in case values are not on a single line
                score_ints = [int(x) for x in score.split()]  # Convert strings to ints
            highscore = max(score_ints)  # sum all elements of the list
            hs_score_text = font.render(
                "High Score : " + str(highscore), True, FONT_COLOR
            )
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(hs_score_text, hs_score_rect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(scaled_bg, (0,0))
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and death_count == 0:
                dialogue()
            if event.type == pygame.KEYDOWN and death_count >= 1:
                main_l1()

def level_transition():
    global FONT_COLOR
    run = True
    while run:
        FONT_COLOR=(255,255,255)
        SCREEN.fill((0, 0, 0))
        font = pygame.font.Font("freesansbold.ttf", 18)
        SCREEN.blit(font.render("You defeated the first wave of the enemies.", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 - 60))
        SCREEN.blit(font.render("The next and final wave will be brutal and hard to defeat", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 - 30))
        SCREEN.blit(font.render("All hope lies with you.", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2))
        SCREEN.blit(font.render("Defeat them and save the world. Collect 2500 points to save the world", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 + 30))
        SCREEN.blit(font.render("Press Any Key to Continue", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 + 60))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main_l2()

def end_dialogue():
    global FONT_COLOR
    run = True
    while run:
        FONT_COLOR=(255,255,255)
        SCREEN.fill((0, 0, 0))
        font = pygame.font.Font("freesansbold.ttf", 18)
        SCREEN.blit(font.render("Congratulations!!! You defeated the enemies.", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 - 60))
        SCREEN.blit(font.render("The world is save for now", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 - 30))
        SCREEN.blit(font.render("We will prepare the next threat.", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2))
        SCREEN.blit(font.render("Press Any Key to Retry", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 + 60))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                menu(0)

def dialogue():
    global FONT_COLOR
    run = True
    while run:
        FONT_COLOR=(255,255,255)
        SCREEN.fill((0, 0, 0))
        font = pygame.font.Font("freesansbold.ttf", 18)

        # text = font.render("""The World is getting invaded by alien. 
        #                       You are the only one to defeat them. Please help us protect the World!
        #                       Be careful of meteor, comet and aliens don't get touch by them.
        #                       You can shoot them if they come close.""", True, FONT_COLOR)
        # skip = font.render("""Press Enter to Skip""", True, FONT_COLOR)
        # textRect = text.get_rect()
        # textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(font.render("The World is getting invaded by alien.", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 - 60))
        SCREEN.blit(font.render("You are the only one to defeat them. Please help us protect the World!", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 - 30))
        SCREEN.blit(font.render("Be careful of meteor, comet and aliens don't get touch by them.", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2))
        SCREEN.blit(font.render("You can shoot them if they come close. Collect 1000 points to proceed to next level", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 + 30))
        SCREEN.blit(font.render("Press Any Key to Continue", True, FONT_COLOR), (SCREEN_WIDTH // 3 - 100, SCREEN_HEIGHT // 2 + 60))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_l1()



t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
