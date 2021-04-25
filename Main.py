'''
Citations:
    Idea originated from the One Piece anime and Super Smash Bros game
    Main framework and organization reference:
        https://qwewy.gitbooks.io/pygame-module-manual/chapter1/framework.html
        https://www.youtube.com/watch?v=i6xMBig-pP4&t=3s
        https://www.youtube.com/watch?v=uWvb3QzA48c
    Sprite animation reference:
        https://www.youtube.com/watch?v=UdsNBIzsmlI&t=852s
    Source of sprites and sound effects:
        https://www.spritedatabase.net
    Sources of videos in game:
        https://www.youtube.com/watch?v=gKZRqe0Iyww
        https://www.youtube.com/watch?v=EXWpjE4nv9I&t=3s
        https://www.youtube.com/watch?v=5YuTINXqy1w
    Text display reference:
        https://pythonprogramming.net/displaying-text-pygame-screen/
    Open CV load video reference:
        https://pythonprogramming.net/loading-video-python-opencv-tutorial/
    Music mixer reference:
        https://www.pygame.org/docs/ref/music.html
    Reading and Writing from text files:
        https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
'''

import pygame
import os
from math import *
from settings import *
from sprites import *
from Luffy import *
from Doflamingo import *
from Enemies import *

import cv2
import numpy as np

class Game(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.startScreen = pygame.image.load('AllSprites' + os.sep + 'startScreen.png')
        self.startScreen = pygame.transform.scale(self.startScreen, (WIDTH, HEIGHT))
        self.loadingScreen = getSprites('AllSprites' + os.sep + 'loadingScreen')
        temp = []
        for ocean in self.loadingScreen:
            temp += [pygame.transform.scale(ocean, (WIDTH, HEIGHT))]
        self.loadingScreen = temp
        self.loadingCount = 0
        self.ship = pygame.image.load('AllSprites' + os.sep + 'ship.png')
        self.ship = pygame.transform.scale(self.ship, (80,80))
        self.ship = getFlippedSprites(self.ship)
        self.shipRect = self.ship.get_rect()
        self.shipRect.x, self.shipRect.y = 0, 250
        self.journey, self.multiplayer = False, False
        self.color1 = YELLOW
        self.color2 = WHITE
        self.clock = pygame.time.Clock()
        self.running = True
        self._keys = {}
        self.crocUlt = getSprites('AllSprites' + os.sep + 'crocodile' + os.sep + 'ult')
        self.bg1 = pygame.image.load('AllSprites' + os.sep + 'bg1.png')
        self.bg2 = pygame.image.load('AllSprites' + os.sep + 'bg2.png')
        self.bg3 = pygame.image.load('AllSprites' + os.sep + 'bg3.png')
        self.bg4 = pygame.image.load('AllSprites' + os.sep + 'bg4.png')
        for bg in [self.bg1, self.bg2, self.bg3, self.bg4]:
            bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        self.playingGame1 = False
        self.playingGame2 = False
        self.playingGame3 = False
        self.learning = True
        self.player1Selected, self.player2Selected = False, False
        self.allIcons = getSprites('AllSprites' + os.sep + 'icons')
        self.iconLength = WIDTH // len(self.allIcons)
        temp = []
        for icon in self.allIcons:
            temp += [pygame.transform.scale(icon, (self.iconLength, self.iconLength))]
        self.allIcons = temp
        self.player1Highlight = [True] + [False] * (len(self.allIcons)-1)
        self.player2Highlight = [False] * (len(self.allIcons)-1) + [True]
        self.pointer2 = pygame.image.load('AllSprites' + os.sep + 'pointer1.png')
        self.pointer1 = pygame.image.load('AllSprites' + os.sep + 'pointer2.png')
        self.pointer2 = pygame.transform.scale(self.pointer2, (self.iconLength, self.iconLength))
        self.pointer1 = pygame.transform.scale(self.pointer1, (self.iconLength//2, self.iconLength//2))
        self.playing1v1 = False
        self.selectingMaps = False
        self.mapHighlight = [[True, False],
                             [False, False]]
        self.mapGrid = [([False] * 10) for row in range(10)]
        self.gridLength = 50
        self.ownPlatform = pygame.image.load('AllSprites' + os.sep + 'p1.jpg')
        self.emptyGrid = pygame.image.load('AllSprites' + os.sep + 'grid.png')
        self.emptyGrid = pygame.transform.scale(self.emptyGrid, (50,50))
        self.customizing = False
        self.platformDrawn = False
        self.godThreads = pygame.sprite.Group()
        self.hintCount = 0
        self.endScreen = pygame.image.load('AllSprites' + os.sep + 'endScreen.png')
        self.endScreen = pygame.transform.scale(self.endScreen, (WIDTH,HEIGHT))
        self.congrats = pygame.image.load('AllSprites' + os.sep + 'congrats.png')
        self.congrats = pygame.transform.scale(self.congrats, (300,100))
        self.myScores = [0,0,0]
        f=open("scoreboard.txt", "r")
        contents = f.read()
        scores = []
        for score in contents.split(','):
            scores += [int(score)]
        self.scoreBoard = scores

    def game1(self):
        time1 = pygame.time.get_ticks()
        self.musicPlayed = False
        self.allSprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.strings = pygame.sprite.Group()
        self.enelDragon = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.player1 = Luffy(self.screen,0,0)
        self.allSprites.add(self.player1)
        self.players.add(self.player1)
        self.player2 = Crocodile(self.screen, 400, 0)
        #self.player2 = Doflamingo(self.screen,400,300)
        self.allSprites.add(self.player2)
        self.players.add(self.player2)
        platform1 = pygame.image.load('AllSprites' + os.sep + 'platform1.jpg')
        p1 = Platform(self.screen, platform1, (0,HEIGHT-40),WIDTH,40)
        p2 = Platform(self.screen, platform1, (WIDTH//7*2,HEIGHT-260),WIDTH//7*3,30)
        p3, p4 = Platform(self.screen, platform1, (0,HEIGHT-150),WIDTH//6,35), Platform(self.screen, platform1, (WIDTH//6*5,HEIGHT-150),WIDTH//6,35)
        for p in [p1,p2,p3,p4]:
            self.allSprites.add(p)
            self.platforms.add(p)
        self.player1Group = pygame.sprite.Group()
        self.player1Group.add(self.player1)
        self.player2Group = pygame.sprite.Group()
        self.player2Group.add(self.player2)
        pygame.mixer.music.load('AllSprites' + os.sep + 'fightMusic.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        self.run()
        time2 = pygame.time.get_ticks()
        time = int(time2 - time1)
        self.myScores[0] = time

    def game2(self):
        time1 = pygame.time.get_ticks()
        self.musicPlayed = False
        self.allSprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.strings = pygame.sprite.Group()
        self.enelDragon = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.player1 = LuffyGear2(self.screen,0,0)
        #self.player1 = LuffyArmament(self.screen,0,400)
        self.allSprites.add(self.player1)
        self.players.add(self.player1)
        self.player2 = Enel(self.screen,400,0)
        self.allSprites.add(self.player2)
        self.players.add(self.player2)
        platform1 = pygame.image.load('AllSprites' + os.sep + 'platform3.jpg')
        p1 = Platform(self.screen, platform1, (0,HEIGHT-40),WIDTH,40)
        p2 = Platform(self.screen, platform1, (WIDTH//7*2,HEIGHT-260),WIDTH//7*3,35)
        p3, p4 = Platform(self.screen, platform1, (0,HEIGHT-150),WIDTH//6,30), Platform(self.screen, platform1, (WIDTH//6*5,HEIGHT-370),WIDTH//6,30)
        for p in [p1,p2,p3,p4]:
            self.allSprites.add(p)
            self.platforms.add(p)
        self.player1Group = pygame.sprite.Group()
        self.player1Group.add(self.player1)
        self.player2Group = pygame.sprite.Group()
        self.player2Group.add(self.player2)
        pygame.mixer.music.load('AllSprites' + os.sep + 'fightMusic.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        self.run()
        time2 = pygame.time.get_ticks()
        time = int(time2 - time1)
        self.myScores[1] = time

    def game3(self):
        time1 = pygame.time.get_ticks()
        self.musicPlayed = False
        self.allSprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.strings = pygame.sprite.Group()
        self.enelDragon = pygame.sprite.Group()
        self.godThreads = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.player1 = LuffyArmament(self.screen,0,0)
        #self.player1 = LuffyGear4(self.screen, 0, 300)
        self.allSprites.add(self.player1)
        self.players.add(self.player1)
        #self.player2 = Crocodile(self.screen, 400, 300)
        self.player2 = Doflamingo(self.screen,400,0)
        self.allSprites.add(self.player2)
        self.players.add(self.player2)
        platform1 = pygame.image.load('AllSprites' + os.sep + 'platform2.jpg')
        p1 = Platform(self.screen, platform1, (0,HEIGHT-40),WIDTH,60)
        p2 = Platform(self.screen, platform1, (WIDTH//7*2,HEIGHT-150),WIDTH//7*3,35)
        p3, p4 = Platform(self.screen, platform1, (0,HEIGHT-260),WIDTH//6,30), Platform(self.screen, platform1, (WIDTH//6*5,HEIGHT-260),WIDTH//6,30)
        for p in [p1,p2,p3,p4]:
            self.allSprites.add(p)
            self.platforms.add(p)
        self.player1Group = pygame.sprite.Group()
        self.player1Group.add(self.player1)
        self.player2Group = pygame.sprite.Group()
        self.player2Group.add(self.player2)
        pygame.mixer.music.load('AllSprites' + os.sep + 'fightMusic.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        self.run()
        time2= pygame.time.get_ticks()
        time = int(time2 - time1)
        self.myScores[2] = time

    def run(self):
        self.playing = True
        self.platformDrawn = False
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update()

    #test player platform collision
    def update(self):
        # player stop at boundary
        for player in self.players:
            if player.rect.x < 0:
                player.rect.x = 0
            elif player.rect.x + player.image.get_width() > WIDTH:
                player.rect.x = WIDTH - player.image.get_width()
            if player.rect.y + player.image.get_height() > HEIGHT:
                player.rect.y = HEIGHT - player.image.get_height()

        # platform collision
        for player in self.players:
            collision = False
            if player.dead:
                for platform in self.platforms:
                    if (platform.rect.y <= player.rect.y + player.image.get_height() <= platform.rect.y + platform.height) and platform.rect.x <= player.rect.x + player.image.get_width() and player.rect.x <= platform.rect.x + platform.width:
                        if player.isFalling:
                            player.rect.y = platform.rect.y - player.image.get_height()
                            player.vy = 0
                            player.airBorne = False
                            collision = True
                        break
                if collision == False:
                    player.vy += GRAVITY
            else:
                for platform in self.platforms:
                    if platform.rect.y <= player.rect.y + player.height <= platform.rect.y + platform.height and platform.rect.x <= player.rect.x + player.image.get_width() and player.rect.x <= platform.rect.x + platform.width:
                        if player.isFalling:
                            player.rect.y = platform.rect.y - player.height
                            player.vy = 0
                            player.airBorne = False
                            player.inJump = False
                            collision = True
                        break
                if collision == False:
                    player.vy += GRAVITY

        #test player player collision
        self.testPlayerPlayerCollision(self.player1,self.player2,self.player1Group, self.player2Group)

        '''if pygame.sprite.spritecollide(self.player1, self.player2Group, False) and pygame.sprite.spritecollide(self.player1, self.player2Group, False, pygame.sprite.collide_mask):
            if self.player1.isAttacking and self.player2.isAttacking:
                if self.player1.dmg < self.player2.dmg:
                    self.player1.isAttacking = False
                    self.playerHit(self.player2,self.player1)
                elif self.player1.dmg > self.player2.dmg:
                    self.player2.isAttacking = False
                    self.playerHit(self.player2,self.player1)
                else:
                    self.player1.isAttacking = False
                    self.player2.isAttacking = False
            elif self.player1.isAttacking:
                self.playerHit(self.player1,self.player2)
            elif self.player2.isAttacking:
                self.playerHit(self.player2,self.player1)
            else:
                self.player1.isHit = False
                self.player2.isHit = False
        else:
            self.player1.isHit = False
            self.player2.isHit = False'''

        # LuffyArmament attackWI actions
        if isinstance(self.player1, LuffyArmament) and self.player1.isAttackingWI:
            self.LuffyArmamentAttackWI(self.player1, self.player2)
        if isinstance(self.player2, LuffyArmament) and self.player2.isAttackingWI:
            self.LuffyArmamentAttackWI(self.player2, self.player1)

        #LuffyGear4 attackI actions
        if isinstance(self.player1, LuffyGear4) and self.player1.isAttackingI:
            self.player1.rect.y = self.player2.rect.y + self.player2.height - self.player1.height
            if self.player1.image == self.player1.rightAttackI[0] or self.player1.image == self.player1.leftAttackI[0]:
                if self.player1.facingRight:
                    self.player1.rect.x = self.player2.rect.x + self.player2.width
                    self.player2.facingRight = True
                    self.player2.facingLeft = False
                else:
                    self.player1.rect.x = self.player2.rect.x
                    self.player2.facingRight = False
                    self.player2.facingLeft = True
            elif self.player1.image == self.player1.rightAttackI[3] or self.player1.image == self.player1.leftAttackI[3]:
                halfHeight = self.player1.image.get_height() // 2
                if (self.player2.rect.y - halfHeight <= self.player1.rect.y <= self.player2.rect.y + halfHeight):
                    self.player2.isHit = True
                    self.player2.flyingAway = True
        if isinstance(self.player2, LuffyGear4) and self.player2.isAttackingI:
            self.player2.rect.y = self.player1.rect.y + self.player1.height - self.player2.height
            if self.player2.image == self.player2.rightAttackI[0] or self.player2.image == self.player2.leftAttackI[0]:
                if self.player2.facingRight:
                    self.player2.rect.x = self.player1.rect.x + self.player1.width
                    self.player1.facingRight = True
                    self.player1.facingLeft = False
                else:
                    self.player2.rect.x = self.player1.rect.x
                    self.player1.facingRight = False
                    self.player1.facingLeft = True
            elif self.player2.image == self.player2.rightAttackI[3] or self.player2.image == self.player2.leftAttackI[3]:
                halfHeight = self.player2.image.get_height() // 2
                if (self.player1.rect.y - halfHeight <= self.player2.rect.y <= self.player1.rect.y + halfHeight):
                    self.player1.isHit = True
                    self.player1.flyingAway = True

        #LuffyGear4 attackWI actions
        if isinstance(self.player1, LuffyGear4) and self.player1.isAttackingWI:
            self.LuffyGear4AttackWI(self.player1, self.player2)
            '''if self.player1.image == self.player1.rightAttackWI[0] or self.player1.image == self.player1.leftAttackWI[0]:
                self.player1.rect.x = self.player2.rect.x
                self.player1.rect.y = self.player2.rect.y - 100
            if self.player1.facingRight:
                if 5 <= self.player1.rightAttackWI.index(self.player1.image) <= 7:
                    halfWidth = self.player1.image.get_width() // 2
                    if (self.player2.rect.x - halfWidth <= self.player1.rect.x <= self.player2.rect.x + halfWidth):
                        if self.player2.isDefending:
                            self.player2.health -= self.player1.dmg * 0.5
                        else:
                            self.player2.isHit = True
                            self.player2.health -= self.player1.dmg
                            self.player2.isKnockedBack = True
            else:
                if 5 <= self.player1.leftAttackWI.index(self.player1.image) <= 7:
                    halfWidth = self.player1.image.get_width() // 2
                    if (self.player2.rect.x - halfWidth <= self.player1.rect.x <= self.player2.rect.x + halfWidth):
                        if self.player2.isDefending:
                            self.player2.health -= self.player1.dmg * 0.5
                        else:
                            self.player2.isHit = True
                            self.player2.health -= self.player1.dmg
                            self.player2.isKnockedBack = True'''
        if isinstance(self.player2, LuffyGear4) and self.player2.isAttackingWI:
             self.LuffyGear4AttackWI(self.player2, self.player1)

        # Doffy attackI actions
        if isinstance(self.player2, Doflamingo) and self.player2.isAttackingI:
            self.DoffyAttackI(self.player1, self.player2)
            '''if self.player2.attackCountI == 1:
                string1posX, string1posY = self.getRectCenter(self.player1)
                self.string1 = DoffyString(self.screen, (string1posX,string1posY), 70, WHITE)
                string2posY = string1posY - self.player1.height // 3
                string3posY = string1posY + self.player1.height // 3
                self.string2 = DoffyString(self.screen, (string1posX,string2posY), 70, WHITE)
                self.string3 = DoffyString(self.screen, (string1posX,string3posY), 70, WHITE)
                player2posX, player2posY = self.getRectCenter(self.player2)
                dx, dy = string1posX - player2posX, string1posY - player2posY
                if dx == 0: dx += 0.00001
                self.string1.angle = -atan(dy/dx)
                dx, dy = string1posX - player2posX, string2posY - player2posY
                if dx == 0: dx += 0.00001
                self.string2.angle = -atan(dy/dx)
                dx, dy = string1posX - player2posX, string3posY - player2posY
                if dx == 0: dx += 0.00001
                self.string3.angle = -atan(dy/dx)
                if self.player2.rect.x <= self.player1.rect.x:
                    self.string1.neg = 1
                    self.string2.neg = 1
                    self.string3.neg = 1
                else:
                    self.string1.neg = -1
                    self.string2.neg = -1
                    self.string3.neg = -1
                self.allSprites.add(self.string1)
                self.strings.add(self.string1)
                self.allSprites.add(self.string2)
                self.strings.add(self.string2)
                self.allSprites.add(self.string3)
                self.strings.add(self.string3)
            elif self.player2.image == self.player2.rightAttackI[4] or self.player2.image == self.player2.leftAttackI[4]:
                for string in self.strings:
                    string.dx = -5 * cos(string.angle) * string.neg
                    string.dy = 5 * sin(string.angle) * string.neg
            elif self.player2.image == self.player2.rightAttackI[8] or self.player2.image == self.player2.leftAttackI[8]:
                for string in self.strings:
                    string.kill()
            elif self.player2.attackCountI > 1:
                if self.string1.neg == 1:
                    if self.string1.startX <= self.player2.rect.x:
                        for string in self.strings:
                            string.kill()
                else:
                    if self.string1.startX >= self.player2.rect.x:
                        for string in self.strings:
                            string.kill()
            if self.player2.attackCountI > 1:
                if self.string1.neg == 1:
                    if self.string1.startX <= self.player1.rect.x + self.player1.width and self.string1.endX >= self.player1.rect.x:
                        if self.string1.endY <= self.player1.rect.y + self.player1.height and self.string1.startY >= self.player1.rect.y:
                            projectileHit(self.player1, self.string1)
                        else:
                            self.player1.isHit = False
                else:
                    if self.string1.endX <= self.player1.rect.x + self.player1.width and self.string1.startX >= self.player1.rect.x:
                        if self.string1.endY <= self.player1.rect.y + self.player1.height and self.string1.startY >= self.player1.rect.y:
                            projectileHit(self.player1, self.string1)
                        else:
                            self.player1.isHit = False'''
        if isinstance(self.player1, Doflamingo) and self.player1.isAttackingI:
            self.DoffyAttackI(self.player2, self.player1)

        # Doffy attackSI actions
        if isinstance(self.player2, DoflamingoAwakened) and self.player2.isAttackingSI and self.player2.attackCountSI >= 10:
            if self.player2.facingLeft and self.player2.finalCount <= FPS * 2:
                x = WIDTH
                if self.player2.finalCount % 30 == 0:
                    for i in range(8):
                        string = Projectile(self.screen, (x,i*50), self.player2.godThread, 0.15)
                        string.dx = -10
                        self.allSprites.add(string)
                        self.godThreads.add(string)
                self.player2.finalCount += 1
            elif self.player2.facingRight and self.player2.finalCount <= FPS * 2:
                x = -100
                if self.player2.finalCount % 30 == 0:
                    for i in range(8):
                        string = Projectile(self.screen, (x,i*50), self.player2.godThread, 0.15)
                        string.dx = 10
                        self.allSprites.add(string)
                        self.godThreads.add(string)
                self.player2.finalCount += 1
        for s in self.godThreads:
            strings = pygame.sprite.Group()
            strings.add(s)
            if pygame.sprite.spritecollide(self.player1, strings, False):
                if self.player1.isDefending:
                    self.player1.health -= s.dmg * 0.5
                    self.player1.energy += 2
                else:
                    self.player1.health -= s.dmg
                    self.player1.isHit = True
                    self.player1.energy += 4

        # Crocodile attackI actions
        if isinstance(self.player2, Crocodile) and self.player2.isAttackingI:
            self.CrocAttackI(self.player1, self.player2)
            '''self.player2.vy = 1
            if self.player2.attackCountI == 1:
                self.player2.rect.x = self.player1.rect.x
                self.player2.rect.y = self.player1.rect.y - ABOVEDIS
            elif (self.player2.image == self.player2.rightAttackI[4] or self.player2.image == self.player2.leftAttackI[4]) and pygame.sprite.spritecollide(self.player1, self.player2Group, False) and pygame.sprite.spritecollide(self.player1, self.player2Group, False, pygame.sprite.collide_mask):
                self.player2.hitUlt = True
                self.player1.isHit = True
                self.crocUltImage = self.crocUlt[0]
                self.crocUltImageX, self.crocUltImageY = self.player1.rect.x + self.player1.width//2 - self.crocUltImage.get_width()//2, self.player1.rect.y + self.player1.height//2 - self.crocUltImage.get_height()//2
            if self.player2.hitUlt == True:
                fpsPerSprite = FPS // len(self.crocUlt) + 1
                self.crocUltImage = self.crocUlt[self.player2.ultCount // fpsPerSprite]
                self.player2.ultCount += 1
                self.player2.attackCountI = len(self.player2.rightAttackI) * ((FPS // len(self.player2.rightAttackI) + 1)//3*2) - 2
                self.player2.rect.y = self.crocUltImageY - self.player2.image.get_height()
                self.player2.vy = 0
                if self.player1.isDefending:
                    self.player1.health -= 0.25
                else:
                    self.player1.isHit = True
                    self.player1.health -= 0.5
                if self.player2.ultCount//fpsPerSprite >= len(self.crocUlt):
                    self.player2.hitUlt = False
                    self.player1.isHit = False
                    self.player2.isAttackingI = False
                    self.player2.isAttacking = False
                    self.player2.attackCountI = 0
                    self.player2.paused = True
                    self.player2.ultCount = 0
                    self.player2.energy -= 50'''
        if isinstance(self.player1, Crocodile) and self.player1.isAttackingI:
            self.CrocAttackI(self.player2, self.player1)

        # Enel attackI actions
        if isinstance(self.player2, Enel) and self.player2.isAttackingI:
            self.EnelAttackI(self.player1, self.player2)
            '''if self.player2.image in [self.player2.rightAttackI[4],self.player2.rightAttackI[5],self.player2.leftAttackI[4],self.player2.leftAttackI[5]]:
                self.dmg = 0.5
                self.attackMove = 1
            else:
                self.dmg = 0
                self.attackMove = 0
            if self.player2.image in [self.player2.rightAttackI[6],self.player2.leftAttackI[6]]:
                x = self.player2.rect.x + self.player2.image.get_width()//2
                y = self.player2.rect.y + self.player2.height // 3
                if self.player2.facingRight:
                    self.dragon = EnelDragon(self.screen, (x,y), self.player2.rightUltImage, 0.5)
                    self.dragon.rect.x -= self.dragon.width // 4
                    self.dragon.dx = 5
                else:
                    self.dragon = EnelDragon(self.screen, (x,y), self.player2.leftUltImage, 0.5)
                    self.dragon.rect.x -= self.dragon.width // 4 * 3
                    self.dragon.dx = -5
                self.allSprites.add(self.dragon)
                self.enelDragon.add(self.dragon)'''
        if isinstance(self.player1, Enel) and self.player1.isAttackingI:
            self.EnelAttackI(self.player2, self.player1)

        # Enel dragon collide
        for player in self.players:
            if not isinstance(player, Enel):
                if pygame.sprite.spritecollide(player, self.enelDragon, False) and pygame.sprite.spritecollide(player, self.enelDragon, False, pygame.sprite.collide_mask):
                    if player.isDefending:
                        player.health -= self.dragon.dmg * 0.5
                    else:
                        player.health -= self.dragon.dmg
                        player.isHit = True

        # attackU actions
        for player in self.players:
            if player.isAttackingU and player.projInAir == False:
                if isinstance(player, Doflamingo):
                    y = player.rect.y + player.height//2
                else:
                    y = player.rect.y
                if player.facingRight:
                    self.bullet = Projectile(self.screen, (player.rect.x+player.width, y), player.rangedAttack, 10)
                    self.bullet.dx = 10
                else:
                    self.bullet = Projectile(self.screen, (player.rect.x - player.rangedWidth, y), player.rangedAttack, 10)
                    self.bullet.dx = -10
                self.projectiles.add(self.bullet)
                self.allSprites.add(self.bullet)
                player.projInAir = True

            if pygame.sprite.spritecollide(player, self.projectiles, False):# and pygame.sprite.spritecollide(player, self.projectiles, False, pygame.sprite.collide_mask):
                if player.isDefending:
                    player.health -= self.bullet.dmg * 0.5
                    player.energy += 2
                else:
                    player.health -= self.bullet.dmg
                    player.isHit = True
                    player.energy += 4
                self.bullet.kill()

        if len(self.projectiles) == 2: #may need more change
            proj = []
            for p in self.projectiles:
                proj += [p]
            projGroup = pygame.sprite.Group()
            projGroup.add(proj[1])
            if pygame.sprite.spritecollide(proj[0], projGroup, False):
                proj[0].kill()
                proj[1].kill()

        for bullet in self.projectiles:
            if bullet.rect.x + bullet.width < 0:
                bullet.kill()
            elif bullet.rect.x > WIDTH:
                bullet.kill()

        #knockback
        for player in self.players:
            if player.isKnockedBack:
                player.knockBack()

        if self.journey:
            self.AI(self.player1, self.player2)

        # luffy transformation
        if isinstance(self.player1, LuffyArmament) and self.player1.transformed:
            x, y = self.player1.rect.x, self.player1.rect.y
            self.player1.kill()
            self.player1 = LuffyGear4(self.screen,x,y)
            self.allSprites.add(self.player1)
            self.players.add(self.player1)
            self.player1Group.add(self.player1)
            self.player1.transformSound.play()
        if isinstance(self.player2, LuffyArmament) and self.player2.transformed:
            x, y = self.player2.rect.x, self.player2.rect.y
            self.player2.kill()
            self.player2 = LuffyGear4(self.screen,x,y)
            self.allSprites.add(self.player1)
            self.players.add(self.player1)
            self.player1Group.add(self.player1)
            self.player2.transformSound.play()

        # doffy awakening
        if isinstance(self.player2, Doflamingo) and not(isinstance(self.player2, DoflamingoAwakened)) and self.player2.dyingCount >= DYINGCOUNT // 2:
            x, y = self.player2.rect.x, self.player2.rect.y
            self.player2.kill()
            self.player2 = DoflamingoAwakened(self.screen, x, y)
            self.allSprites.add(self.player2)
            self.players.add(self.player2)
            self.player2Group.add(self.player2)

        for sprite in self.allSprites:
            sprite.update()
            if sprite in self.players:
                sprite.ifJumpingDown(self.platforms)

    def LuffyArmamentAttackWI(self, player1, player2):
        if player1.image in player1.rightAttackWI or player1.image in player1.leftAttackWI:
            if player1.image == player1.rightAttackWI[1] or player1.image == player1.leftAttackWI[1]:
                player1.rect.x = player2.rect.x
                player1.rect.y = player2.rect.y - 50
                #if player1.image in [player1.rightAttackWI[4],player1.rightAttackWI[5],player1.rightAttackWI[6],player1.rightAttackWI[7],player1.leftAttackWI[4],player1.leftAttackWI[5],player1.leftAttackWI[6],player1.leftAttackWI[7]]:
            else:
                halfWidth = player1.image.get_width() // 2
                if (player2.rect.x - halfWidth <= player1.rect.x <= player2.rect.x + halfWidth):
                    if player2.isDefending:
                        player2.health -= player1.dmg * 0.51
                    else:
                        player2.isHit = True
                        player2.health -= player1.dmg
                        player2.isKnockedBack = True

    def LuffyGear4AttackWI(self, player1, player2):
        if player1.image in player1.rightAttackWI or player1.image in player1.leftAttackWI:
            if player1.image == player1.rightAttackWI[0] or player1.image == player1.leftAttackWI[0]:
                player1.rect.x = player2.rect.x
                player1.rect.y = player2.rect.y - 100
                #if player1.image in [player1.rightAttackWI[5],player1.rightAttackWI[6],player1.rightAttackWI[7],player1.leftAttackWI[5],player1.leftAttackWI[6],player1.leftAttackWI[7]]:
            else:
                halfWidth = player1.image.get_width() // 2
                if (player2.rect.x - halfWidth <= player1.rect.x <= player2.rect.x + halfWidth):
                    if player2.isDefending:
                        player2.health -= player1.dmg * 0.5
                    else:
                        player2.isHit = True
                        player2.health -= player1.dmg
                        player2.isKnockedBack = True

    def DoffyAttackI(self, player1, player2):
        if player2.attackCountI == 1:
            string1posX, string1posY = self.getRectCenter(player1)
            self.string1 = DoffyString(self.screen, (string1posX,string1posY), 70, WHITE)
            string2posY = string1posY - player1.height // 3
            string3posY = string1posY + player1.height // 3
            self.string2 = DoffyString(self.screen, (string1posX,string2posY), 70, WHITE)
            self.string3 = DoffyString(self.screen, (string1posX,string3posY), 70, WHITE)
            player2posX, player2posY = self.getRectCenter(player2)
            dx, dy = string1posX - player2posX, string1posY - player2posY
            if dx == 0: dx += 0.00001
            self.string1.angle = -atan(dy/dx)
            dx, dy = string1posX - player2posX, string2posY - player2posY
            if dx == 0: dx += 0.00001
            self.string2.angle = -atan(dy/dx)
            dx, dy = string1posX - player2posX, string3posY - player2posY
            if dx == 0: dx += 0.00001
            self.string3.angle = -atan(dy/dx)
            if player2.rect.x <= player1.rect.x:
                self.string1.neg = 1
                self.string2.neg = 1
                self.string3.neg = 1
            else:
                self.string1.neg = -1
                self.string2.neg = -1
                self.string3.neg = -1
            self.allSprites.add(self.string1)
            self.strings.add(self.string1)
            self.allSprites.add(self.string2)
            self.strings.add(self.string2)
            self.allSprites.add(self.string3)
            self.strings.add(self.string3)
        elif player2.image == player2.rightAttackI[4] or player2.image == player2.leftAttackI[4]:
            for string in self.strings:
                string.dx = -5 * cos(string.angle) * string.neg
                string.dy = 5 * sin(string.angle) * string.neg
        elif player2.image == player2.rightAttackI[8] or player2.image == player2.leftAttackI[8]:
            for string in self.strings:
                string.kill()
        elif player2.attackCountI > 1:
            if self.string1.neg == 1:
                if self.string1.startX <= player2.rect.x:
                    for string in self.strings:
                        string.kill()
            else:
                if self.string1.startX >= player2.rect.x:
                    for string in self.strings:
                        string.kill()
        if player2.attackCountI > 1:
            if self.string1.neg == 1:
                if self.string1.startX <= player1.rect.x + player1.width and self.string1.endX >= player1.rect.x:
                    if self.string1.endY <= player1.rect.y + player1.height and self.string1.startY >= player1.rect.y:
                        projectileHit(player1, self.string1)
                    else:
                        player1.isHit = False
            else:
                if self.string1.endX <= player1.rect.x + player1.width and self.string1.startX >= player1.rect.x:
                    if self.string1.endY <= player1.rect.y + player1.height and self.string1.startY >= player1.rect.y:
                        projectileHit(player1, self.string1)
                    else:
                        player1.isHit = False

    def CrocAttackI(self, player1, player2):
        player2.vy = 1
        if player2.attackCountI == 1:
            player2.rect.x = player1.rect.x
            player2.rect.y = player1.rect.y - ABOVEDIS
        elif (player2.image == player2.rightAttackI[4] or player2.image == player2.leftAttackI[4]) and pygame.sprite.spritecollide(player1, self.player2Group, False) and pygame.sprite.spritecollide(player1, self.player2Group, False, pygame.sprite.collide_mask):
            player2.hitUlt = True
            player1.isHit = True
            self.crocUltImage = self.crocUlt[0]
            self.crocUltImageX, self.crocUltImageY = player1.rect.x + player1.width//2 - self.crocUltImage.get_width()//2, player1.rect.y + player1.height//2 - self.crocUltImage.get_height()//2
        if player2.hitUlt == True:
            fpsPerSprite = FPS // len(self.crocUlt) + 1
            self.crocUltImage = self.crocUlt[player2.ultCount // fpsPerSprite]
            player2.ultCount += 1
            player2.attackCountI = len(player2.rightAttackI) * ((FPS // len(player2.rightAttackI) + 1)//3*2) - 2
            player2.rect.y = self.crocUltImageY - player2.image.get_height()
            player2.vy = 0
            if player1.isDefending:
                player1.health -= 0.25
            else:
                player1.isHit = True
                player1.health -= 0.5
            if player2.ultCount//fpsPerSprite >= len(self.crocUlt):
                player2.hitUlt = False
                player1.isHit = False
                player2.isAttackingI = False
                player2.isAttacking = False
                player2.attackCountI = 0
                player2.paused = True
                player2.ultCount = 0
                player2.energy -= 50

    def EnelAttackI(self, player1, player2):
        if player2.image in [player2.rightAttackI[4],player2.rightAttackI[5],player2.leftAttackI[4],player2.leftAttackI[5]]:
            player2.dmg = 0.5
            attackMove = 1
        else:
            player2.dmg = 0
            player2.attackMove = 0
        if player2.image in [player2.rightAttackI[6],player2.leftAttackI[6]]:
            x = player2.rect.x + player2.image.get_width()//2
            y = player2.rect.y + player2.height // 3
            if player2.facingRight:
                self.dragon = EnelDragon(self.screen, (x,y), player2.rightUltImage, 0.5)
                self.dragon.rect.x -= self.dragon.width // 4
                self.dragon.dx = 5
            else:
                self.dragon = EnelDragon(self.screen, (x,y), player2.leftUltImage, 0.5)
                self.dragon.rect.x -= self.dragon.width // 4 * 3
                self.dragon.dx = -5
            self.allSprites.add(self.dragon)
            self.enelDragon.add(self.dragon)

    def getRectCenter(self, player):
        x = player.rect.x + player.width // 2
        y = player.rect.y + player.height // 2
        return x,y

    def testPlayerPlayerCollision(self, player1, player2, player1Group, player2Group):
        if pygame.sprite.spritecollide(player1, player2Group, False) and maskCollision(player1, player2):
        #(pygame.sprite.spritecollide(player1, player2Group, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(player2, player1Group, False, pygame.sprite.collide_mask)):
            if player1.isAttacking and player2.isAttacking:
                if player1.dmg < player2.dmg:
                    self.stopAllAttacks(self.player1)
                    playerHit(player2,player1)
                elif player1.dmg > player2.dmg:
                    self.stopAllAttacks(self.player2)
                    playerHit(player1,player2)
                else:
                    player1.isAttacking = False
                    player2.isAttacking = False
            elif player1.isAttacking:
                playerHit(player1,player2)
            elif player2.isAttacking:
                playerHit(player2,player1)
            else:
                player1.isHit = False
                player2.isHit = False
        else:
            player1.isHit = False
            player2.isHit = False

    # updates hit and receives dmg
    '''def playerHit(self,player1,player2):
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
            if player1.facingRight:
                player2.facingLeft = True
                player2.facingRight = False
                player2.rect.x += player1.attackMove
            else:
                player2.facingLeft = False
                player2.facingRight = True
                player2.rect.x -= player1.attackMove
            player2.rect.y += player1.attackMoveY'''

    def stopAllAttacks(self, player):
        player.isAttacking = False
        player.isAttackingJ = False
        player.isAttackingSJ = False
        player.isAttackingWJ = False
        player.isAttackingI = False

    def keyPressed(self, keyCode, modifier):
        if self.player1.isAttackingJ and keyCode == pygame.K_j:
            self.player1.jClickCount += 1
            if self.player1.jClickCount > self.player1.jClickCountMax:
                self.player1.jClickCount = self.player1.jClickCountMax
        if self.player2.isAttackingJ and keyCode == pygame.K_END:
            self.player2.jClickCount += 1
            if self.player2.jClickCount > self.player2.jClickCountMax:
                self.player2.jClickCount = self.player2.jClickCountMax
        if self.journey:
            if self.player2.dyingCount > DYINGCOUNT and keyCode == pygame.K_RETURN:
                if self.playingGame1:
                    self.playingGame1 = False
                    self.playingGame2 = True
                    self.playing = False
                elif self.playingGame2:
                    self.playingGame2 = False
                    self.playingGame3 = True
                    self.playing = False
                elif self.playingGame3:
                    self.playingGame3 = False
                    self.playing = False
            elif self.player1.dyingCount > DYINGCOUNT and keyCode == pygame.K_RETURN:
                self.playing = False
        elif self.multiplayer:
            if keyCode == pygame.K_RETURN and (self.player2.dyingCount > DYINGCOUNT or self.player1.dyingCount > DYINGCOUNT):
                self.playing = False
                self.player1Selected, self.player2Selected = False, False
            elif self.customizing:
                if keyCode == pygame.K_1:
                    self.ownPlatform = pygame.image.load('AllSprites' + os.sep + 'p1.jpg')
                elif keyCode == pygame.K_2:
                    self.ownPlatform = pygame.image.load('AllSprites' + os.sep + 'p2.jpg')
                elif keyCode == pygame.K_3:
                    self.ownPlatform = pygame.image.load('AllSprites' + os.sep + 'p3.jpg')
                elif keyCode == pygame.K_4:
                    self.ownPlatform = pygame.image.load('AllSprites' + os.sep + 'p4.jpg')

    def keyReleased(self, keyCode, modifier):
        if self.multiplayer and not(self.player1Selected or self.player2Selected):
            if self.player1Selected == False:
                if keyCode == pygame.K_a:
                    index = self.player1Highlight.index(True)
                    if index == 0:
                        newIndex = len(self.allIcons) - 1
                    else:
                        newIndex = index - 1
                    self.player1Highlight[index] = False
                    self.player1Highlight[newIndex] = True
                elif keyCode == pygame.K_d:
                    index = self.player1Highlight.index(True)
                    if index == len(self.allIcons) - 1:
                        newIndex = 0
                    else:
                        newIndex = index + 1
                    self.player1Highlight[index] = False
                    self.player1Highlight[newIndex] = True
            if self.player2Selected == False:
                if keyCode == pygame.K_LEFT:
                    index = self.player2Highlight.index(True)
                    if index == 0:
                        newIndex = len(self.allIcons) - 1
                    else:
                        newIndex = index - 1
                    self.player2Highlight[index] = False
                    self.player2Highlight[newIndex] = True
                elif keyCode == pygame.K_RIGHT:
                    index = self.player2Highlight.index(True)
                    if index == len(self.allIcons) - 1:
                        newIndex = 0
                    else:
                        newIndex = index + 1
                    self.player2Highlight[index] = False
                    self.player2Highlight[newIndex] = True
        if self.multiplayer and self.selectingMaps:
            currRow, currCol = 0, 0
            for i in range(2):
                for j in range(2):
                    if self.mapHighlight[i][j] == True:
                        currRow = i
                        currCol = j
                        break
            newRow, newCol = currRow, currCol
            if keyCode == pygame.K_a:
                if currCol == 0:
                    newCol = 1
                else:
                    newCol = currCol - 1
            elif keyCode == pygame.K_d:
                if currCol == 1:
                    newCol = 0
                else:
                    newCol = currCol + 1
            if keyCode == pygame.K_w:
                if currRow == 0:
                    newRow = 1
                else:
                    newRow = currRow - 1
            elif keyCode == pygame.K_s:
                if currRow == 1:
                    newRow = 0
                else:
                    newRow = currRow + 1
            self.mapHighlight[currRow][currCol] = False
            self.mapHighlight[newRow][newCol] = True

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def mousePressed(self, x, y):
        if self.multiplayer and self.customizing:
            for r in range(len(self.mapGrid)):
                for c in range(len(self.mapGrid[0])):
                    if (r*50 <= x < (r+1)*50) and (c*50 <= y < (c+1)*50):
                        if self.mapGrid[r][c] == False:
                            self.mapGrid[r][c] = True
                        else:
                            self.mapGrid[r][c] = False
                        break

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing and self.journey:
                    self.playing = False
                    self.playingGame1 = False
                    self.playingGame2 = False
                    self.playingGame3 = False
                elif self.playing and self.multiplayer:
                    self.playing = False
                    self.playing1v1 = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._keys[event.key] = True
                self.keyPressed(event.key, event.mod)
            elif event.type == pygame.KEYUP:
                self._keys[event.key] = False
                self.keyReleased(event.key, event.mod)

    def draw(self):
        self.screen.fill((0,0,0))
        if self.journey:
            if isinstance(self.player2, Crocodile):
                self.screen.blit(self.bg1, (0,0))
            elif isinstance(self.player2, Doflamingo):
                self.screen.blit(self.bg2, (0,0))
            elif isinstance(self.player2, Enel):
                self.screen.blit(self.bg3, (0,0))
        elif self.multiplayer:
            self.screen.blit(self.battleField, (0,0))
        for p in self.platforms:
            p.draw()
        for s in self.godThreads:
            s.draw()
        for d in self.enelDragon:
            d.draw()
        for sprite in self.players:
            sprite.draw()
        for s in self.strings:
            s.draw()
        for proj in self.projectiles:
            proj.draw()
        for player in self.players:
            if isinstance(player, Crocodile) and player.hitUlt:
                self.screen.blit(self.crocUltImage, (self.crocUltImageX, self.crocUltImageY))
        #dying text
        if self.journey:
            if self.player2.dyingCount > DYINGCOUNT:
                text = 'YOU WIN! PRESS ENTER TO CONTINUE'
                self.message_display(text,WIDTH//2,HEIGHT//2,25,BLACK)
                if self.musicPlayed == False:
                    pygame.mixer.music.load('AllSprites' + os.sep + 'victory.mp3')
                    pygame.mixer.music.play()
                    self.musicPlayed = True
            elif self.player1.dyingCount > DYINGCOUNT:
                text = 'YOU LOSE! PRESS ENTER TO RESTART'
                self.message_display(text,WIDTH//2,HEIGHT//2,25,BLACK)
                if self.musicPlayed == False:
                    pygame.mixer.music.load('AllSprites' + os.sep + 'death.mp3')
                    pygame.mixer.music.play()
                    self.musicPlayed = True
            elif isinstance(self.player2, DoflamingoAwakened) and self.hintCount <= FPS * 5:
                text = 'The Enemy has Awakened. Hint: Press O at Full Energy'
                if self.hintCount % 20 <= 10:
                    self.message_display(text,WIDTH//2,HEIGHT//2,15,BLACK)
                self.hintCount += 1
        elif self.multiplayer:
            if self.player2.dyingCount > DYINGCOUNT:
                text = 'Player1 WINS! PRESS ENTER TO RESTART'
                self.message_display(text,WIDTH//2,HEIGHT//2,20,BLACK)
                if self.musicPlayed == False:
                    pygame.mixer.music.load('AllSprites' + os.sep + 'victory.mp3')
                    pygame.mixer.music.play()
                    self.musicPlayed = True
            elif self.player1.dyingCount > DYINGCOUNT:
                text = 'Player2 WINS! PRESS ENTER TO RESTART'
                self.message_display(text,WIDTH//2,HEIGHT//2,20,BLACK)
                if self.musicPlayed == False:
                    pygame.mixer.music.load('AllSprites' + os.sep + 'victory.mp3')
                    pygame.mixer.music.play()
                    self.musicPlayed = True

        #ult icon
        for player in self.players:
            if player.ultPause:
                if player.isAttackingI:
                    self.screen.blit(player.iconI, (0,0))
                    player.ultSound.play()
                elif player.isAttackingWI:
                    self.screen.blit(player.iconWI, (0,0))
                    player.ultSound2.play()
                elif player.isAttackingSI:
                    self.screen.blit(player.iconSI, (0,0))
                    player.ultSound2.play()
        pygame.display.flip()

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, x, y, size, color):
        largeText = pygame.font.Font('freesansbold.ttf', size)
        TextSurf, TextRect = self.text_objects(text, largeText, color)
        TextRect.center = (x,y)
        self.screen.blit(TextSurf, TextRect)

    def AI(self,player1, player2):
        if not(player2.isDefending or player2.isAttacking or player2.isHit or player2.airBorne) and not(player1.dead or player2.dead or player2.paused):
            if isinstance(player2, DoflamingoAwakened):
                if player2.energy >= 150:
                    player2.isAttackingSI = True
                else:
                    if player1.rect.x - player2.rect.x < 0:
                        player2.facingLeft = True
                        player2.facingRight = False
                    else:
                        player2.facingLeft = False
                        player2.facingRight = True
                    if player1.rect.x - player2.rect.x <= -150:
                        player2.vx = -player2.speed
                        player2.isWalking = True
                    elif player1.rect.x - player2.rect.x >= 150:
                        player2.vx = player2.speed
                        player2.isWalking = True
                    else:
                        player2.isWalking = False
                        player2.vx = 0
                        player2.walkCount = 0
                        if abs(player1.rect.x - player2.rect.x) <= 150 and abs(player1.rect.y - player2.rect.y) <= 50:
                            r = random.choice([True, False])
                            if r:
                                player2.isAttackingSJ = True
                            else:
                                player2.isAttackingJ = True
                                player2.jClickCount = player2.jClickCountMax
                        elif abs(player1.rect.x - player2.rect.x) <= 50 and abs(player1.rect.y - player2.rect.y) <= 50:
                            player2.isAttackingJ = True
                    if player1.isAttackingU and player2.airBorne == False and abs(player1.rect.y - player2.rect.y) <= 50 and ((player2.facingLeft and player1.rect.x - player2.rect.x < -200) or (player2.facingRight and player1.rect.x - player2.rect.x >= 200)):
                        player2.vy = -6
                        player2.airBorne = True

            else:
                if player1.rect.x - player2.rect.x < 0:
                    player2.facingLeft = True
                    player2.facingRight = False
                else:
                    player2.facingLeft = False
                    player2.facingRight = True
                if player2.energy < 50:
                    if player1.rect.x - player2.rect.x <= -150:
                        player2.vx = -player2.speed
                        player2.isWalking = True
                    elif player1.rect.x - player2.rect.x >= 150:
                        player2.vx = player2.speed
                        player2.isWalking = True
                    else:
                        player2.isWalking = False
                        player2.vx = 0
                        player2.walkCount = 0
                        if abs(player1.rect.x - player2.rect.x) <= 150 and abs(player1.rect.y - player2.rect.y) <= 50:
                            r = random.choice([True, False])
                            if r:
                                player2.isAttackingSJ = True
                            else:
                                player2.isAttackingJ = True
                                player2.jClickCount = player2.jClickCountMax
                        elif abs(player1.rect.x - player2.rect.x) <= 50 and abs(player1.rect.y - player2.rect.y) <= 50:
                            player2.isAttackingJ = True
                elif player2.energy >= 50:
                    player2.isWalking = False
                    if isinstance(player2, Enel):
                        if abs(player1.rect.y - player2.rect.y) <= 50:
                            player2.isAttackingI = True
                    else:
                        player2.isAttackingI = True
                if player1.isAttackingU and player2.airBorne == False and abs(player1.rect.y - player2.rect.y) <= 50 and ((player2.facingLeft and player1.rect.x - player2.rect.x < -200) or (player2.facingRight and player1.rect.x - player2.rect.x >= 200)):
                    player2.vy = -6
                    player2.airBorne = True

        if player1.isAttacking and abs(player1.rect.x - player2.rect.x) <= 50 and not(player2.inDefence or player2.isHit):
            r = random.choice([True, False])
            if r:
                player2.isDefending = True
                player2.inDefence = True
            else:
                player2.inDefence = True
        if player2.inDefence and player1.isAttacking == False:
            player2.inDefence = False
            player2.isDefending = False

        self.findPlatform(player1, player2)

    def findPlatform(self, player1, player2):
        if not(player2.isDefending or player2.isAttacking or player2.isHit) and player1.dead == False and player2.dead == False:
            if player2.rect.y - player1.rect.y >= 50:
                r = False
                if abs(player1.rect.x - player2.rect.x) <= 150 and player2.rect.y - player1.rect.y <= 150:
                    r = random.choice([True,False])
                    if r:
                        player2.isAttackingWJ = True
                if r == False:
                    jumped = False
                    for p in self.platforms:
                        if p.rect.x <= player2.rect.x <= p.rect.x + p.width and 0 <= player2.rect.y - p.rect.y <= 150 and player2.airBorne == False:
                            player2.vy = -6
                            player2.airBorne = True
                            jumped = True
                            break
                    if jumped == False:
                        if player1.rect.x - player2.rect.x < 0:
                            player2.vx = -player2.speed
                            player2.isWalking = True
                        elif player1.rect.x - player2.rect.x >= 0:
                            player2.vx = player2.speed
                            player2.isWalking = True
            elif player1.rect.y - player2.rect.y >= 50 and not (player2.airBorne or player2.isAttacking or player2.isHit):
                player2.isJumpingDown = True

    def gameStartScreen(self):
        self.playing = True
        pygame.mixer.music.load('AllSprites' + os.sep + 'startMusic.mp3')
        pygame.mixer.music.play(-1)
        while self.playing and not(self.journey or self.multiplayer):
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.playing:
                        self.playing = False
            self.screen.blit(self.startScreen, (0,0))
            text = 'One Piece Journey'
            self.message_display(text,WIDTH//2,HEIGHT//2,50,BLACK)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] and self.color1 == YELLOW:
                self.color1 = WHITE
                self.color2 = YELLOW
            elif keys[pygame.K_UP] and self.color1 == WHITE:
                self.color1 = YELLOW
                self.color2 = WHITE
            text1 = "Go On Luffy's Journey"
            text2 = 'Multiplayer Battleground'
            self.message_display(text1, WIDTH//2, HEIGHT//6*4,30,self.color1)
            self.message_display(text2, WIDTH//2, HEIGHT//6*5,30,self.color2)
            if keys[pygame.K_RETURN] and self.color1 == YELLOW:
                self.journey = True
            elif keys[pygame.K_RETURN] and self.color2 == YELLOW:
                self.multiplayer = True
            pygame.display.flip()

    def instructions(self):
        self.playing = True
        while self.playing and self.learning:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.playing:
                        self.playing = False
            self.screen.fill(WHITE)
            self.message_display('Instructions (Press J to Continue)',WIDTH//2,HEIGHT//8,30,BLACK)
            self.message_display('Left and Right: A and D',WIDTH//2,HEIGHT//8*2,20,BLACK)
            self.message_display('Normal attack: J',WIDTH//2,HEIGHT//8*3,20,BLACK)
            self.message_display('Jump: K',WIDTH//2,HEIGHT//8*4,20,BLACK)
            self.message_display('Defend: S',WIDTH//2,HEIGHT//8*5,20,BLACK)
            self.message_display('Special Ability: I',WIDTH//2,HEIGHT//8*6,20,BLACK)
            self.message_display('Try out combinations of keys for more moves!',WIDTH//2,HEIGHT//8*7,20,BLACK)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_j]:
                self.learning = False
            pygame.display.flip()

    def shipSailing(self):
        self.playing = True
        self.loading = True
        self.shipRect.x = 0
        pygame.mixer.music.load('AllSprites' + os.sep + 'loadingMusic.mp3')
        pygame.mixer.music.play(-1)
        while self.playing and self.loading:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.playing:
                        self.playing = False
            self.screen.fill(BLACK)
            fpsPerSprite = (FPS // len(self.loadingScreen) + 1) * 4
            self.oceanView = self.loadingScreen[self.loadingCount // fpsPerSprite]
            self.screen.blit(self.oceanView, (0,0))
            self.message_display('Sailing to next island...',WIDTH//2,HEIGHT//7,30,BLACK)
            self.screen.blit(self.ship, (self.shipRect.x, self.shipRect.y))
            self.loadingCount += 1
            if self.loadingCount // fpsPerSprite >= len(self.loadingScreen):
                self.loadingCount = 0
            self.shipRect.x += 2
            if self.shipRect.x + self.ship.get_width() > WIDTH:
                self.loading = False
            pygame.display.flip()

    def playerSelection(self):
        self.playing = True
        while self.playing and not(self.player1Selected and self.player2Selected):
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
            self.screen.fill(BLACK)
            for i in range(len(self.allIcons)):
                self.screen.blit(self.allIcons[i],(i*self.iconLength, HEIGHT/2 - self.iconLength/2))
            keys = pygame.key.get_pressed()
            for i in range(len(self.player1Highlight)):
                if self.player1Highlight[i]:
                    self.screen.blit(self.pointer1, ((i+0.5)*self.iconLength - self.pointer1.get_width()/2, HEIGHT/2 - self.iconLength/2 - self.pointer1.get_height()))
            for i in range(len(self.player2Highlight)):
                if self.player2Highlight[i]:
                    self.screen.blit(self.pointer2, ((i+0.5)*self.iconLength - self.pointer2.get_width()/2, HEIGHT/2 - self.iconLength/2 + self.pointer2.get_height()))

            if keys[pygame.K_j]:
                self.player1Num = self.player1Highlight.index(True)
                self.player1Selected = True
            elif keys[pygame.K_k]:
                self.player1Selected = False
            if keys[pygame.K_END]:
                self.player2Num = self.player2Highlight.index(True)
                self.player2Selected = True
            elif keys[pygame.K_PAGEDOWN]:
                self.player2Selected = False

            pygame.display.flip()

    def mapSelection(self):
        self.playing = True
        self.selectingMaps = True
        while self.playing and self.selectingMaps:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
            desert = pygame.transform.scale(self.bg1, (WIDTH//2,HEIGHT//2))
            skyIsland = pygame.transform.scale(self.bg3, (WIDTH//2,HEIGHT//2))
            dressrosa = pygame.transform.scale(self.bg2, (WIDTH//2,HEIGHT//2))
            customize = pygame.transform.scale(self.bg4, (WIDTH//2,HEIGHT//2))
            self.screen.blit(desert, (0,0))
            self.screen.blit(skyIsland, (WIDTH//2,0))
            self.screen.blit(dressrosa, (0,HEIGHT//2))
            self.screen.blit(customize, (WIDTH//2,HEIGHT//2))
            if self.mapHighlight[0][0] == True:
                self.message_display('Alabasta', WIDTH//4, HEIGHT//4, 40, YELLOW)
            elif self.mapHighlight[0][1] == True:
                self.message_display('Skypiea', WIDTH//4*3, HEIGHT//4, 40, YELLOW)
            elif self.mapHighlight[1][0] == True:
                self.message_display('Dressrosa', WIDTH//4, HEIGHT//4*3, 40, YELLOW)
            elif self.mapHighlight[1][1] == True:
                self.message_display('Custimize Your Own', WIDTH//4*3, HEIGHT//4*3, 25, YELLOW)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_j]:
                self.selectingMaps = False
            pygame.display.flip()

    def initializePlayer1(self, pos):
        x,y = pos
        if self.player1Num == 0:
            self.player1 = Luffy_1(self.screen,x,y)
        elif self.player1Num == 1:
            self.player1 = LuffyGear2_1(self.screen,x,y)
        elif self.player1Num == 2:
            self.player1 = LuffyArmament_1(self.screen,x,y)
        elif self.player1Num == 3:
            self.player1 = Crocodile_1(self.screen,x,y)
        elif self.player1Num == 4:
            self.player1 = Enel_1(self.screen,x,y)
        elif self.player1Num == 5:
            self.player1 = Doflamingo_1(self.screen,x,y)
        elif self.player1Num == 6:
            self.player1 = LuffyGear4_1(self.screen,x,y)

    def initializePlayer2(self, pos):
        x,y = pos
        if self.player2Num == 0:
            self.player2 = Luffy_2(self.screen,x,y)
        elif self.player2Num == 1:
            self.player2 = LuffyGear2_2(self.screen,x,y)
        elif self.player2Num == 2:
            self.player2 = LuffyArmament_2(self.screen,x,y)
        elif self.player2Num == 3:
            self.player2 = Crocodile_2(self.screen,x,y)
        elif self.player2Num == 4:
            self.player2 = Enel_2(self.screen,x,y)
        elif self.player2Num == 5:
            self.player2 = Doflamingo_2(self.screen,x,y)
            #self.player2 = DoflamingoAwakened(self.screen,x,y)
        elif self.player2Num == 6:
            self.player2 = LuffyGear4_2(self.screen,x,y)

    def initializeMap(self):
        if self.mapHighlight[0][0] == True:
            self.battleField = self.bg1
            self.platforms = pygame.sprite.Group()
            platform1 = pygame.image.load('AllSprites' + os.sep + 'platform1.jpg')
            p1 = Platform(self.screen, platform1, (0,HEIGHT-40),WIDTH,40)
            p2 = Platform(self.screen, platform1, (WIDTH//7*2,HEIGHT-260),WIDTH//7*3,30)
            p3, p4 = Platform(self.screen, platform1, (0,HEIGHT-150),WIDTH//6,35), Platform(self.screen, platform1, (WIDTH//6*5,HEIGHT-150),WIDTH//6,35)
            for p in [p1,p2,p3,p4]:
                self.platforms.add(p)
        elif self.mapHighlight[0][1] == True:
            self.battleField = self.bg3
            self.platforms = pygame.sprite.Group()
            platform1 = pygame.image.load('AllSprites' + os.sep + 'platform3.jpg')
            p1 = Platform(self.screen, platform1, (0,HEIGHT-40),WIDTH,40)
            p2 = Platform(self.screen, platform1, (WIDTH//7*2,HEIGHT-260),WIDTH//7*3,35)
            p3, p4 = Platform(self.screen, platform1, (0,HEIGHT-150),WIDTH//6,30), Platform(self.screen, platform1, (WIDTH//6*5,HEIGHT-370),WIDTH//6,30)
            for p in [p1,p2,p3,p4]:
                self.platforms.add(p)
        elif self.mapHighlight[1][0] == True:
            self.battleField = self.bg2
            self.platforms = pygame.sprite.Group()
            platform1 = pygame.image.load('AllSprites' + os.sep + 'platform2.jpg')
            p1 = Platform(self.screen, platform1, (0,HEIGHT-40),WIDTH,60)
            p2 = Platform(self.screen, platform1, (WIDTH//7*2,HEIGHT-150),WIDTH//7*3,35)
            p3, p4 = Platform(self.screen, platform1, (0,HEIGHT-260),WIDTH//6,30), Platform(self.screen, platform1, (WIDTH//6*5,HEIGHT-260),WIDTH//6,30)
            for p in [p1,p2,p3,p4]:
                self.platforms.add(p)
        elif self.mapHighlight[1][1] == True:
            self.customizeOwnMap()

    def customizeOwnMap(self):
        self.playing = True
        self.customizing = True
        self.battleField = self.bg4
        self.platforms = pygame.sprite.Group()
        base = Platform(self.screen, self.ownPlatform, (-50,HEIGHT-50), WIDTH+100, 50)
        self.platforms.add(base)
        while self.playing and self.customizing:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = False
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
            self.screen.blit(self.bg4, (0,0))
            block = pygame.transform.scale(self.ownPlatform, (50,50))
            for r in range(len(self.mapGrid)):
                for c in range(len(self.mapGrid[0])):
                    if self.mapGrid[r][c]:
                        self.screen.blit(block, (r*50, c*50))
                        #p = Platform(self.screen, self.ownPlatform, (r*50, c*50),50,50)
                        #self.platforms.add(p)
                    else:
                        self.screen.blit(self.emptyGrid, (r*50, c*50))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.customizing = False
            pygame.display.flip()

    def player1v1(self):
        self.musicPlayed = False
        self.allSprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.strings = pygame.sprite.Group()
        self.enelDragon = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.initializePlayer1((0,0))
        self.initializePlayer2((400,0))
        self.allSprites.add(self.player1)
        self.players.add(self.player1)
        self.allSprites.add(self.player2)
        self.players.add(self.player2)
        self.initializeMap()
        for r in range(len(self.mapGrid)):
            for c in range(len(self.mapGrid[0])):
                if self.mapGrid[r][c]:
                    p = Platform(self.screen, self.ownPlatform, (r*50, c*50),50,50)
                    self.platforms.add(p)
        for p in self.platforms:
            self.allSprites.add(p)
        self.player1Group = pygame.sprite.Group()
        self.player1Group.add(self.player1)
        self.player2Group = pygame.sprite.Group()
        self.player2Group.add(self.player2)
        pygame.mixer.music.load('AllSprites' + os.sep + 'fightMusic.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        self.run()

    def gameOverScreen(self):
        self.playing = True
        pygame.mixer.music.load('AllSprites' + os.sep + 'congratsMusic.mp3')
        pygame.mixer.music.play(-1)
        while self.playing:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
            self.screen.blit(self.endScreen, (0,0))
            self.screen.blit(self.congrats, (WIDTH//2 - 150, HEIGHT//10))
            self.message_display('Game1 Shortest Time: ' + str(int(self.scoreBoard[0]/1000)) + ' Your Time: ' + str(int(self.myScores[0]/1000)), WIDTH//2, HEIGHT//11*6, 15, YELLOW)
            self.message_display('Game2 Shortest Time: ' + str(int(self.scoreBoard[1]/1000)) + ' Your Time: ' + str(int(self.myScores[1]/1000)), WIDTH//2, HEIGHT//11*8, 15, YELLOW)
            self.message_display('Game3 Shortest Time: ' + str(int(self.scoreBoard[2]/1000)) + ' Your Time: ' + str(int(self.myScores[2]/1000)), WIDTH//2, HEIGHT//11*10, 15, YELLOW)
            pygame.display.flip()
        f=open("scoreboard.txt", "w")
        for i in range(3):
            if self.myScores[i] != 0 and self.myScores[i] < self.scoreBoard[i]:
                self.scoreBoard[i] = self.myScores[i]
        f.write(str(self.scoreBoard[0]) + ',' + str(self.scoreBoard[1]) + ',' + str(self.scoreBoard[2]))

g = Game()
g.gameStartScreen()
if g.journey:
    while g.running:
        g._keys = dict()
        g.instructions()
        g.shipSailing()
        g.playingGame1 = True
        while g.playingGame1:
            g.game1()
        g.shipSailing()
        while g.playingGame2:
            g.game2()
        g.shipSailing()
        g.playingGame3 = True
        while g.playingGame3:
            g.game3()
        g.gameOverScreen()
        break
elif g.multiplayer:
    while g.running:
        g._keys = dict()
        g.playing1v1 = True
        while g.playing1v1:
            g.playerSelection()
            g.mapSelection()
            g.player1v1()
        break
pygame.quit()
