#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from src import Scenes
import sys

pygame.init()
resolution = (1280, 800)
if len(sys.argv) == 3:
	resolution = (int(sys.argv[1]), int(sys.argv[2]))
pygame.display.set_mode(resolution)
pygame.display.set_caption("Cellular Conquest")
Scenes.StartScene()
pygame.quit()
