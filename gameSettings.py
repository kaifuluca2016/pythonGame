import pygame
from pygame.locals import *

# constant
cWinWidth = 700
cWinHeight = 650
cTextColor = (0, 0, 255)
cBackgroundColor = (192, 192, 0)
cFrequency = 30

cDangerLoopBoundery = 6
cMyBulletLoopboundery = 9
mySpeed = 6
outsideLoopCount=5
scoreArray = [0]

myImage = pygame.image.load('resources/superboy1.png')
myBullet = pygame.image.load('resources/bullet.png')
arm2 = pygame.image.load('resources/arm2.png')
arm3 = pygame.image.load('resources/arm3.png')
arm4 = pygame.image.load('resources/arm4.png')

myBodyShape = myImage.get_rect()
myBulletRect = myBullet.get_rect()
armory = [arm2,arm3,arm4]

pygame.init()
bullet_wav = pygame.mixer.Sound('resources/bullet.wav')
bullet_wav.set_volume(0.4)
mainClock = pygame.time.Clock()
windowFrame = pygame.display.set_mode((cWinWidth, cWinHeight))
font = pygame.font.SysFont(None, 36)
keyStateDict = {K_LEFT : False, K_RIGHT : False, K_UP : False, K_DOWN: False}
keyArray =[K_LEFT,K_RIGHT,K_UP,K_DOWN]
oppositeKeyDict= {K_LEFT : K_RIGHT, K_RIGHT : K_LEFT, K_UP : K_DOWN, K_DOWN: K_UP}
