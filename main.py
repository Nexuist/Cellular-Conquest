#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from src import Scenes

pygame.init()
resolution = (1280, 800)
pygame.display.set_mode(resolution)
pygame.display.set_caption("Cellular Conquest")
Scenes.StartScene()
pygame.quit()
