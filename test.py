import cv2
import numpy as np
import pygame
from pygame.locals import *

pygame.init()
display = pygame.display.set_mode((1920,1080))

im = cv2.imread("A9em5.png", cv2.IMREAD_UNCHANGED)

w,h,c = im.shape


# im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
np.set_printoptions(threshold=np.inf)
print(im.shape)
print(np.max(im))
# im = np.sum(im, axis = 2)
# print(im)

im = im.astype(np.uint8)

print(im)

alpha = pygame.image.frombuffer(im, im.shape[1::-1], "RGBA").convert_alpha()
alpha = pygame.transform.scale(alpha, (1920,1080))

background = pygame.image.load("leaves.png").convert_alpha()

background = pygame.transform.scale(background,(1920,1080))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # draw
    display.fill(Color(0, 0, 0))
    masked = background.copy()
    masked.blit(alpha, (0, 0), None, pygame.BLEND_RGBA_MULT)
    display.blit(masked, (0, 0))
    pygame.display.flip()