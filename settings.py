# Game settings
import pygame
import random

WIDTH = 500
HEIGHT = 500
GRAVITY = 0.2
TITLE = 'One Piece Jounry'
FPS = 80

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
ORANGE = (255,165,0)
BLACK = (0,0,0)
ABOVEDIS = 90

#basic character settings
DMG = 0.1
ATTACKMOVE = 1
PAUSECOUNT = 20
DYINGCOUNT = FPS // 2
ULTPAUSE = 50

def drawText(screen,text,color,x,y):
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    textsurface = myfont.render(text, False, color)
    screen.blit(textsurface,(x,y))


from Enemies import *
from Doflamingo import *
from Luffy import *
from sprites import *

def playerHit(player1,player2):
    if player2.dead == False:
        if player2.isDefending:
            player2.health -= player1.dmg * player2.defendRatio
        else:
            player2.health -= player1.dmg
            if player1.dmg != 0:
                player2.isHit = True
        # if player2 back to player1, player2 is turned
        if isinstance(player1, Crocodile) and player2.isDefending == False and player1.jClickCount == 1 and (player1.image == player1.rightAttackJ[8] or player1.image == player1.leftAttackJ[8]):
            player2.isKnockedBack = True
        elif isinstance(player1, Doflamingo) and player2.isDefending == False and player1.jClickCount == 2 and (player1.image == player1.rightAttackJ[16] or player1.image == player1.leftAttackJ[16]):
            player2.isKnockedBack = True
        elif (isinstance(player1, LuffyGear2) or isinstance(player1, LuffyArmament)) and player2.isDefending == False and player1.jClickCount == 1 and (player1.image == player1.rightAttackJ[10] or player1.image == player1.leftAttackJ[10]):
            player2.isKnockedBack = True
        if player1.facingRight:
            player2.facingLeft = True
            player2.facingRight = False
            player2.rect.x += player1.attackMove
        else:
            player2.facingLeft = False
            player2.facingRight = True
            player2.rect.x -= player1.attackMove
        player2.rect.y += player1.attackMoveY
        if isinstance(player1, Enel) and player1.isAttackingWJ:
            player2.isKnockedBack = True

def maskCollision(player1,player2):
    player1.mask = pygame.mask.from_surface(player1.image)
    player2.mask = pygame.mask.from_surface(player2.image)
    ox = player2.image.get_rect().center[0] - player1.image.get_rect().center[0]
    oy = player2.image.get_rect().center[1] - player1.image.get_rect().center[1]
    return player1.mask.overlap(player2.mask, (ox, oy))

def projectileHit(player, proj):
    if player.dead == False:
        if player.isDefending:
            player.health -= proj.dmg * player.defendRatio
        else:
            player.health -= proj.dmg
            player.isHit = True










