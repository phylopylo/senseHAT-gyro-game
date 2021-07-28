#!/usr/bin/env python3

from sense_hat import SenseHat
from breadcontrol import Breadboard_control
from typing import Tuple

import pygame
import sys
import os
import time

'''
Variables
'''

worldx = 1200
worldy = 1000
fps = 40
ani = 4
world = pygame.display.set_mode([worldx, worldy])

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

'''
Objects
'''


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('images', 'hero' + str(i) + '.png')).convert()
            img.convert_alpha()  # optimise alpha
            img.set_colorkey(ALPHA)  # set alpha
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x
        self.movey += y

    def update(self):
        """
        Update sprite position
        """

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.images[self.frame//ani]

class Obstacle(pygame.sprite.Sprite): 
    """
    Spawn an obstacle
    """
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('images', 'enemy' + str(i) + '.png')).convert()
            img.convert_alpha()  # optimise alpha
            img.set_colorkey(ALPHA)  # set alpha
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

class Goal(pygame.sprite.Sprite):
    """
    Spawn the Goal
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join('images', 'trophy.png')).convert()
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(ALPHA)  # set alpha
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
'''
Setup
'''

backdrop = pygame.image.load(os.path.join('images', 'stage.jpeg'))
backdrop = pygame.transform.scale(backdrop, (worldx, worldy))
clock = pygame.time.Clock()
pygame.init()
backdropbox = world.get_rect()
main = True

player = Player()  # spawn player
player.rect.x = 0  # go to x
player.rect.y = 0  # go to y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10

obstacle1 = Obstacle()
obstacle1.rect.x = 700
obstacle1.rect.y = 700
obstacle2 = Obstacle()
obstacle2.rect.x = 500
obstacle2.rect.y = 300
obstacle_list = pygame.sprite.Group()
obstacle_list.add(obstacle1)
obstacle_list.add(obstacle2)

trophy = Goal()
trophy.rect.x = 900
trophy.rect.y = 900
trophy_list = pygame.sprite.Group()
trophy_list.add(trophy)

# SenseHAT setup

sense = SenseHat()
sense.set_imu_config(False, True, False)

# Breadboard setup

bread = Breadboard_control(37, 31, 11) # Green LED, Red LED, Button Input

bread.green_toggle()
bread.red_toggle()

time.sleep(0.5)

bread.green_toggle()
bread.red_toggle()

time.sleep(0.5)

bread.green_toggle()
bread.red_toggle()

time.sleep(0.5)

bread.green_toggle()
bread.red_toggle()

while(not bread.is_button()): # Wait for player to start by pressing the button
    time.sleep(0.1)

'''
Main Loop
'''
while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False
    orientation = sense.get_gyroscope()
    roll = orientation["roll"]
    pitch = orientation["pitch"]
    xdir = 0
    ydir = 0
    speed_multiplier = 1
    if roll > 180:
        xdir = -speed_multiplier * ((90 - (roll - 270)) / 10)
        #print("Sending player xdir=" + str(xdir) + " because of roll=" + str(roll))
    else:
        xdir = speed_multiplier * (roll / 10)
        #print("Sending player xdir=" + str(xdir) + " because of roll=" + str(roll))
    if pitch > 180:
        ydir = -speed_multiplier * ((90 - (pitch - 270)) / 10)
    else:
        ydir = speed_multiplier * (pitch / 10)
    if(bread.is_button()):
        player.control(xdir, ydir)
        world.blit(backdrop, backdropbox)
        player.update()
        player_list.draw(world)
        obstacle1.update()
        obstacle_list.draw(world)
        trophy.update()
        trophy_list.draw(world)
        pygame.display.flip()
        clock.tick(fps) 
        player.control(-xdir, -ydir)
    if player.rect.colliderect(obstacle1) or  player.rect.colliderect(obstacle2):
        print("bad guy got you")
        bread.red_toggle()
        time.sleep(5)
        bread.red_toggle()
        exit()
    if player.rect.colliderect(trophy):
        print("You win!")
        bread.green_toggle()
        time.sleep(5)
        bread.green_toggle()
        exit()
