import pygame, random, sys, os, time
from pygame.locals import *
from gameSettings import *


def init():
    pygame.display.set_caption('Fly into space')
    pygame.mouse.set_visible(True)
    font = pygame.font.SysFont(None, 36)
    drawText('Press any key to start new game.', font, windowFrame, (cWinWidth / 4), (cWinHeight / 4))
    pygame.display.update()


def exit1():
    pygame.quit()
    sys.exit()


# let it become a procedure and share the same collections with outside variables
def execCleared():
    recycledArray = []
    explosiveBulletArray = []
    for b in dangerCollections:
        for m in myBulletCollections:
            if m['rect'].colliderect(b['rect']):
                recycledArray.append(b)
                explosiveBulletArray.append(m)
    for e in recycledArray:
        if e in dangerCollections:
            scoreArray[0] += 10
            dangerCollections.remove(e)
            bullet_wav.play()
    for e in explosiveBulletArray:
        if e in myBulletCollections:
            myBulletCollections.remove(e)


# check if our fighters were wounded by opposite attacks
def hasCollision(myBodyShape, dangerCollections):
    for b in dangerCollections:
        if myBodyShape.colliderect(b['rect']):
            return True
    return False


def drawText(text, font, surface, x, y):p
    textobj = font.render(text, 1, cTextColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# move our fighters according to the direction-key states
def moveAdapter():
    if keyStateDict[K_LEFT] and myBodyShape.left > 0:
        myBodyShape.move_ip(-1 * mySpeed, 0)
    if keyStateDict[K_RIGHT] and myBodyShape.right < cWinWidth:
        myBodyShape.move_ip(mySpeed, 0)
    if keyStateDict[K_UP] and myBodyShape.top > 0:
        myBodyShape.move_ip(0, -1 * mySpeed)
    if keyStateDict[K_DOWN] and myBodyShape.bottom < cWinHeight:
        myBodyShape.move_ip(0, mySpeed)


def neatFormationAdjustment():
    for b in dangerCollections:
        b['rect'].move_ip(0, b['speed'])

    for b in dangerCollections[:]:
        if b['rect'].top > cWinHeight:
            dangerCollections.remove(b)

    for b in myBulletCollections:
        b['rect'].move_ip(0, -b['speed'])

    for b in myBulletCollections[:]:
        if b['rect'].bottom < 0:
            myBulletCollections.remove(b)


init()
# whole round fighting (e.g. 5 people will have 5 round fighting in this outer loop)
while (outsideLoopCount > 0):
    # new round fighting
    dangerCollections = []
    myBulletCollections = []

    myBodyShape.topleft = (cWinWidth / 2, cWinHeight - 52)

    # initial status
    keyStateDict = {K_LEFT: False, K_RIGHT: False, K_UP: False, K_DOWN: False}
    dangerCounter = 0
    myBulletCounter = 0

    while True:
        for event in pygame.event.get():

            # check and set the key state params
            if event.type == QUIT:
                exit1()
            if event.type == KEYDOWN:
                for k in keyArray:
                    if event.key == k:
                        keyStateDict[oppositeKeyDict[k]] = False
                        keyStateDict[k] = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    exit1()
                # reset the status as keyup
                for k in keyArray:
                    if event.key == k:
                        keyStateDict[k] = False

        # opposite enemies are adding new attacks
        dangerCounter += 1
        if dangerCounter == cDangerLoopBoundery:
            dangerCounter = 0
            dangerCollectionsize = 1
            newThreat = {'rect': pygame.Rect(random.randint(140, 485), 0 - dangerCollectionsize, 23, 47),
                         'speed': 8,
                         'surface': pygame.transform.scale(random.choice(armory), (23, 47)),
                         }
            dangerCollections.append(newThreat)

        # our fighters will shoot new bullet
        myBulletCounter += 1
        if myBulletCounter == cMyBulletLoopboundery:
            myBulletCounter = 0
            myBulletCollectionSize = 1
            newBullet = {'rect': pygame.Rect(myBodyShape.left, myBodyShape.top - 48, 12, 48),
                         'speed': 8,
                         'surface': pygame.transform.scale(myBullet, (12, 48)),
                         }
            myBulletCollections.append(newBullet)
            # The rule: Each missile/bullet fired consumes 2 credits;
            #   but you can earn 10 credits if you eliminate a threat.
            scoreArray[0] -= 2

        moveAdapter()

        neatFormationAdjustment()

        windowFrame.fill(cBackgroundColor)

        drawText('Score: %s' % (scoreArray[0]), font, windowFrame, 60, 0)
        drawText('Available Fighters: %s' % (outsideLoopCount), font, windowFrame, 60, 40)

        # check if our missiles/bullets eliminate some threats from opposite.
        execCleared()
        windowFrame.blit(myImage, myBodyShape)

        for b in myBulletCollections:
            windowFrame.blit(b['surface'], b['rect'])

        for b in dangerCollections:
            windowFrame.blit(b['surface'], b['rect'])

        pygame.display.update()
        # check if our fighters were wounded/killed by opposite attacks
        if hasCollision(myBodyShape, dangerCollections):
            break

        mainClock.tick(cFrequency)

    outsideLoopCount = outsideLoopCount - 1

    time.sleep(1)
    if (outsideLoopCount == 0):
        drawText('Game over', font, windowFrame, (cWinWidth / 2), (cWinHeight / 2))
        drawText('Press any key to play again.', font, windowFrame, (cWinWidth / 4) - 50, (cWinHeight / 4) + 50)
        pygame.display.update()
        time.sleep(2)
        outsideLoopCount = 5
