# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading

import pygame

pygame.init()

# Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Runner")

Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

RUNNING = [
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile008.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile009.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile010.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile011.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile012.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile013.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile014.png")),
    pygame.image.load(os.path.join("assets/Soldier/r_run", "tile015.png")),
]
DEAD = [pygame.image.load(os.path.join("assets/Soldier/r_dead", "tile007.png"))]
JUMPING = [pygame.image.load(os.path.join("assets/Soldier/r_run", "tile012.png"))]
DUCKING = [
    pygame.image.load(os.path.join("assets/Soldier/r_duck", "tile004.png"))
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Other", "desert_rock1.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Other", "middle_lane_rock1_1.png")),
    pygame.image.load(os.path.join("assets/Other", "middle_lane_rock1_2.png")),
    pygame.image.load(os.path.join("assets/Other", "middle_lane_rock1_3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "tile000.png")),
    pygame.image.load(os.path.join("assets/Bird", "tile001.png")),
    pygame.image.load(os.path.join("assets/Bird", "tile002.png")),
    pygame.image.load(os.path.join("assets/Bird", "tile003.png")),
    pygame.image.load(os.path.join("assets/Bird", "tile004.png")),
    pygame.image.load(os.path.join("assets/Bird", "tile005.png")),
]

SHOOT = pygame.image.load(os.path.join("assets/Soldier/r_shoot", "tile007.png"))

CLOUD = pygame.image.load(os.path.join("assets/Other", "cloud_shape3_1.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

BULLET = pygame.image.load(os.path.join("assets/Other", "bullet_image.png"))

FONT_COLOR=(0,0,0)

fireballs=[]
bullet_items = []
fireball_count = 3

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

class Dinosaur:

    X_POS = 80
    Y_POS = 330
    Y_POS_DUCK = 370
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DEAD
        self.shoot_img = SHOOT

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.dino_dead = False
        self.dino_shoot = False

        self.step_index = 0
        self.jump_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.hitbox = self.dino_rect.inflate(-20, -10)

    def update(self, userInput):

        self.hitbox = self.dino_rect.inflate(-90, 20)

        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_dead:
            self.dead()
        if self.dino_shoot:
            self.shoot()

        if self.step_index >= 8:
            self.step_index = 0

        if (userInput[pygame.K_UP]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        elif self.dino_dead:
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = False
            self.dino_dead = True
            
    def duck(self):
        self.image = self.duck_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img[self.jump_index]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
    
    def dead(self):
        self.image = self.dead_img[0]
    
    def shoot(self):
        self.image = self.shoot_img


    def draw(self, SCREEN):
        # pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2) #debug hitbox
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class BulletItem:
    def __init__(self):
        self.image = pygame.image.load(os.path.join("assets/Other", "bullet_image.png"))  # Replace with your item image path
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, 350)  # Random height

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            # Remove the item if it goes off the screen
            bullet_items.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def main():
    global fireballs, fireball_count, death_count
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False

    def display_bullet_count():
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render(f'Bullets: {fireball_count}', True, FONT_COLOR)
        text_rect = text.get_rect(topleft=(10, 10))  # Position at top-left corner
        SCREEN.blit(text, text_rect)

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        current_time = datetime.datetime.now().hour
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]  
            highscore = max(score_ints)
            if points > highscore:
                highscore=points 
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and fireball_count > 0:
                    player.shoot()
                    fireballs.append(Fireball(150, 340))
                    fireball_count -= 1
        # Add bullet items to the game
        if random.randint(0, 15) == 5:  # Adjust the frequency as needed
            bullet_items.append(BulletItem())

        # Update and draw bullet items
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            item.update()
            item.draw(SCREEN)

        # Check for collisions with bullet items
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            if player.dino_rect.colliderect(item.rect):
                fireball_count += 1  # Increase bullet count
                bullet_items.remove(item)  # Remove the collected item

        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.hitbox.colliderect(obstacle.rect) and not player.dino_dead:
                death_count += 1
                player.dino_dead = True  # Set the dinosaur as dead
                player.dead()  # Call the dead method to handle the death event
                break 
            for fireball in fireballs:
                if fireball.collides_with(obstacle):  # You'll need to implement this method
                    obstacles.remove(obstacle)
                    fireballs.remove(fireball)
                    break
        
        fireballs = [fireball for fireball in fireballs if fireball.x < SCREEN_WIDTH]

        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            SCREEN.fill((255, 255, 255))
        else:
            SCREEN.fill((0, 0, 0))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                player.dead()
                if player.dino_dead == True:
                    pygame.time.delay(1000)
                    menu(death_count)

        background()

        for fireball in fireballs:
            fireball.move()
            fireball.draw(SCREEN)
        
        for item in bullet_items[:]:  # Use a slice copy to iterate safely when removing items
            item.draw(SCREEN)
        
        cloud.draw(SCREEN)
        cloud.update()
        display_bullet_count()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    global FONT_COLOR
    run = True
    while run:
        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            FONT_COLOR=(0,0,0)
            SCREEN.fill((255, 255, 255))
        else:
            FONT_COLOR=(255,255,255)
            SCREEN.fill((128, 128, 128))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, FONT_COLOR)
        elif death_count > 0:
            global fireball_count
            fireball_count = 3
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            f = open("score.txt", "a")
            f.write(str(points) + "\n")
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
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
