import pygame
from math import *
import os
from settings import *
from sprites import *

import cv2
import numpy as np

class Crocodile(character):
    def __init__(self,screen,x,y):
        super().__init__(x,y,screen)
        self.name = 'Crocodile'
        self.setUpSprites('AllSprites' + os.sep + 'crocodile')
        self.facingLeft = True
        self.facingRight = False
        self.rangedAttack = pygame.image.load('AllSprites' + os.sep + 'crocodile' + os.sep + 'Attacks' + os.sep + 'projectile' + os.sep + '0.png')
        self.rangedWidth = self.rangedAttack.get_width()
        self.image = self.walkLeft[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
        self.ultCount = 0
        self.jClickCountMax = 1
        self.attackMove = 0
        self.attackMoveY = 0

    def playVideo(self):
        pygame.mixer.music.load('Luffy+Crocodile.mp3')
        pygame.mixer.music.play()
        cap = cv2.VideoCapture('Luffy+Crocodile.mp4')
        videoCount = 0
        while True:
            ret, frame = cap.read()
            cv2.imshow('frame',frame)
            frame = cv2.resize(frame,(500,500),interpolation = cv2.INTER_AREA)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
            videoCount += 1
            if videoCount > 500:
                break
        cap.release()
        cv2.destroyAllWindows()

    def update(self):
        keys = pygame.key.get_pressed()
        self.updateDead()
        if self.dead == True:
            if self.videoPlayed == False:
                self.playVideo()
            self.videoPlayed = True
            self.ifDead()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.isKnockedBack:
            self.ifHit()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.ultPause == True:
            self.ultPauseCount += 1
            if self.ultPauseCount > ULTPAUSE:
                self.ultPause = False
                self.ultPauseCount = 0
        elif self.paused == False:
            #self.updateWalking(keys)
            self.ifWalking()
            self.updateJumping(keys)
            #self.updateJumpingDown(keys)
            #self.updateAttack(keys)
            self.ifAttackingJ()
            self.ifAttackingSJ()
            self.ifAttackingWJ()
            self.ifAttackingI()
            self.ifAttackingU()
            self.ifAttacking()
            #self.updateDefending(keys)
            self.ifDefending()
            self.ifHit()
            self.ifStanding()
            self.updateEnergy()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.paused:
            self.ifStanding()
            self.ifHit()
            self.pauseCount += 1
            if self.pauseCount == PAUSECOUNT:
                self.paused = False
                self.pauseCount = 0
                self.isHit = False
            self.rect.x += self.vx
            self.rect.y += self.vy

    def draw(self):
        if self.image in [self.rightAttackWJ[3], self.rightAttackWJ[4], self.leftAttackWJ[3], self.leftAttackWJ[4]]:
            self.screen.blit(self.image, (self.rect.x, self.rect.y + self.height - self.image.get_height()))
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (WIDTH-50,0))
        text = 'Player1 Health:' + str(int(self.health))
        width = self.health *3/2
        drawText(self.screen,text,WHITE,WIDTH/3*2-50,0)
        if self.dead == False:
            self.healthbar = pygame.Surface((width,25))
            self.healthbar.fill(RED)
            self.screen.blit(self.healthbar, (WIDTH//3*2-50,25))
        if self.energy == 150: color = ORANGE
        elif self.energy >= 100: color = YELLOW
        elif self.energy >= 50: color = GREEN
        else: color = BLUE
        self.energybar = pygame.Surface((self.energy,10))
        self.energybar.fill(color)
        self.screen.blit(self.energybar,(WIDTH//3*2-50,55))

    def ifAttackingWJ(self):
        fpsPerSprite = (FPS // len(self.rightAttackWJ) + 1)
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingI) and self.isAttackingWJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.5
            self.attackMove = 2
            self.attackMoveY = -2
            self.energy += 0.2
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackWJ[self.attackCountWJ//fpsPerSprite]
                self.attackCountWJ += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackWJ[self.attackCountWJ//fpsPerSprite]
                self.attackCountWJ += 1
            self.vy = self.attackMoveY
        if self.attackCountWJ//fpsPerSprite >= len(self.rightAttackWJ):
            self.attackCountWJ = 0
            self.isAttackingWJ = False
            self.isAttacking = False
            self.paused = True
            self.dmg = DMG
            self.attackMove = 0
            self.attackMoveY = 0

    def updateWalking(self,keys):
        super().updateWalking(keys, pygame.K_LEFT, pygame.K_RIGHT)

    def updateDefending(self,keys):
        super().updateDefending(keys, pygame.K_DOWN)

    def updateJumping(self,keys):
        super().updateJumping(keys, pygame.K_PAGEDOWN, pygame.K_DOWN)

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not self.isHit:
            if keys[pygame.K_DOWN] and keys[pygame.K_END]:
                self.isAttackingSJ = True
            elif keys[pygame.K_UP] and keys[pygame.K_END] and self.isAttackingSJ == False:
                self.isAttackingWJ = True
            elif self.isAttackingSJ == False and self.isAttackingWJ == False and keys[pygame.K_END]:
                self.isAttackingJ = True
            elif keys[pygame.K_RSHIFT]:
                self.isAttackingU = True
            elif keys[pygame.K_PAGEUP]:
                self.isAttackingI = True

    def ifAttackingJ(self):
        if self.jClickCount == 0:
            tempR = self.rightAttackJ[:4]
            tempL = self.leftAttackJ[:4]
        elif self.jClickCount == 1:
            tempR = self.rightAttackJ[:9]
            tempL = self.leftAttackJ[:9]
        fpsPerSprite = (FPS // len(self.rightAttackJ[:4]) + 1)//4*3
        if self.isAttackingJ:
            self.isAttacking = True
            self.isDefending = False
            self.energy += 0.1
            if self.facingRight:
                self.rect.x += 1
                self.image = tempR[self.attackCountJ//fpsPerSprite]
                self.attackCountJ += 1
            else:
                self.rect.x -= 1
                self.image = tempL[self.attackCountJ//fpsPerSprite]
                self.attackCountJ += 1
        if self.attackCountJ//fpsPerSprite >= len(tempR):
            self.attackCountJ = 0
            self.jClickCount = 0
            self.isAttackingJ = False
            self.isAttacking = False
            self.paused = True

    def ifAttackingI(self):
        #self.attackMotion(self.isAttackingI, self.leftAttackI, self.rightAttackI, self.attackCountI, 2, 0.5, 2)
        fpsPerSprite = (FPS // len(self.rightAttackI) + 1)//3*2
        if self.isAttackingI and self.energy >=50:
            if self.attackCountI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0
            self.attackMove = 0
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackI[self.attackCountI//fpsPerSprite]
                self.attackCountI += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackI[self.attackCountI//fpsPerSprite]
                self.attackCountI += 1
        if self.attackCountI//fpsPerSprite >= len(self.rightAttackI):
            self.attackCountI = 0
            self.isAttackingI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 50
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

class Crocodile_1(Crocodile):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)

    def update(self):
        keys = pygame.key.get_pressed()
        self.updateDead()
        if self.dead == True:
            #if self.videoPlayed == False:
            #    self.playVideo()
            #self.videoPlayed = True
            self.ifDead()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.isKnockedBack:
            self.ifHit()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.ultPause == True:
            self.ultPauseCount += 1
            if self.ultPauseCount > ULTPAUSE:
                self.ultPause = False
                self.ultPauseCount = 0
        elif self.paused == False:
            self.updateWalking(keys)
            self.ifWalking()
            self.updateJumping(keys)
            self.updateAttack(keys)
            self.ifAttackingJ()
            self.ifAttackingSJ()
            self.ifAttackingWJ()
            self.ifAttackingI()
            self.ifAttackingU()
            self.ifAttacking()
            self.updateDefending(keys)
            self.ifDefending()
            self.ifHit()
            self.ifStanding()
            self.updateEnergy()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.paused:
            self.ifStanding()
            self.ifHit()
            self.pauseCount += 1
            if self.pauseCount == PAUSECOUNT:
                self.paused = False
                self.pauseCount = 0
                self.isHit = False
            self.rect.x += self.vx
            self.rect.y += self.vy

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not self.isHit:
            if keys[pygame.K_s] and keys[pygame.K_j] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_w] and keys[pygame.K_j] and not(self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_j] and not(self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_u] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ):
                self.isAttackingU = True
            elif keys[pygame.K_i] and self.energy >= 50 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

    def draw(self):
        if self.image in [self.rightAttackWJ[3], self.rightAttackWJ[4], self.leftAttackWJ[3], self.leftAttackWJ[4]]:
            self.screen.blit(self.image, (self.rect.x, self.rect.y + self.height - self.image.get_height()))
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (0,0))
        text = 'Player2 Health:' + str(int(self.health))
        width = self.health * 3/2
        if width <= 0: width = 0
        drawText(self.screen,text,WHITE,50,0)
        if self.dead == False:
            self.healthbar = pygame.Surface((width,25))
            self.healthbar.fill(RED)
            self.screen.blit(self.healthbar, (60,25))
        if self.energy == 150: color = ORANGE
        elif self.energy >= 100: color = YELLOW
        elif self.energy >= 50: color = GREEN
        else: color = BLUE
        self.energybar = pygame.Surface((self.energy,10))
        self.energybar.fill(color)
        self.screen.blit(self.energybar,(60,55))

    def updateWalking(self,keys):
        self.walk(keys, pygame.K_a, pygame.K_d)

    def updateJumping(self,keys):
        self.jump(keys, pygame.K_k, pygame.K_s)

    def updateDefending(self,keys):
        self.defend(keys, pygame.K_s)

    def walk(self, keys, leftKey, rightKey):
        if not(self.isAttacking or self.isDefending or self.isHit):
            if keys[leftKey]:
                self.vx = -self.speed
                self.facingLeft = True
                self.facingRight = False
                self.isWalking = True
            elif keys[rightKey]:
                self.vx = self.speed
                self.facingLeft = False
                self.facingRight = True
                self.isWalking = True
            else:
                self.isWalking = False
                self.walkCount = 0
                self.vx = 0

    def jump(self,keys,jumpKey,downKey):
        if not (self.airBorne or self.isAttacking or self.isHit):
            if keys[jumpKey] and keys[downKey]:
                self.isJumpingDown = True
            elif keys[jumpKey]:
                self.vy = -6
                self.airBorne = True
        if self.vy < 0:
            self.isFalling = False
        elif self.vy >= 0:
            self.isFalling = True

    def defend(self,keys,defendKey):
        if self.vx == 0 and self.vy == 0 and not (self.isAttacking or self.isHit) and keys[defendKey]:
            self.isDefending = True
        else:
            self.isDefending = False

class Crocodile_2(Crocodile):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)

    def update(self):
        keys = pygame.key.get_pressed()
        self.updateDead()
        if self.dead == True:
            #if self.videoPlayed == False:
            #    self.playVideo()
            #self.videoPlayed = True
            self.ifDead()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.isKnockedBack:
            self.ifHit()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.ultPause == True:
            self.ultPauseCount += 1
            if self.ultPauseCount > ULTPAUSE:
                self.ultPause = False
                self.ultPauseCount = 0
        elif self.paused == False:
            self.updateWalking(keys)
            self.ifWalking()
            self.updateJumping(keys)
            self.updateAttack(keys)
            self.ifAttackingJ()
            self.ifAttackingSJ()
            self.ifAttackingWJ()
            self.ifAttackingI()
            self.ifAttackingU()
            self.ifAttacking()
            self.updateDefending(keys)
            self.ifDefending()
            self.ifHit()
            self.ifStanding()
            self.updateEnergy()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.paused:
            self.ifStanding()
            self.ifHit()
            self.pauseCount += 1
            if self.pauseCount == PAUSECOUNT:
                self.paused = False
                self.pauseCount = 0
                self.isHit = False
            self.rect.x += self.vx
            self.rect.y += self.vy


class Enel(character):
    def __init__(self,screen,x,y):
        super().__init__(x,y,screen)
        self.name = 'Crocodile'
        self.setUpSprites('AllSprites' + os.sep + 'enel')
        self.facingLeft = True
        self.facingRight = False
        self.rangedAttack = pygame.image.load('AllSprites' + os.sep + 'enel' + os.sep + 'Attacks' + os.sep + 'projectile' + os.sep + '0.png')
        self.rangedWidth = self.rangedAttack.get_width()
        self.image = self.walkLeft[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
        self.ultCount = 0
        self.jClickCountMax = 1
        self.attackMove = 0
        self.attackMoveY = 0
        self.rightUltImage = pygame.image.load('AllSprites' + os.sep + 'enel' + os.sep + 'ultImage.png')
        self.rightUltImage = pygame.transform.scale(self.rightUltImage, (self.rightUltImage.get_width(),40))
        self.leftUltImage = getFlippedSprites(self.rightUltImage)

    def playVideo(self):
        pygame.mixer.music.load('Luffy+Enel.mp3')
        pygame.mixer.music.play()
        cap = cv2.VideoCapture('Luffy+Enel.mp4')
        videoCount = 0
        while True:
            ret, frame = cap.read()
            cv2.imshow('frame',frame)
            frame = cv2.resize(frame,(500,500),interpolation = cv2.INTER_AREA)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
            videoCount += 1
            if videoCount > 550:
                break
        cap.release()
        cv2.destroyAllWindows()

    def update(self):
        keys = pygame.key.get_pressed()
        self.updateDead()
        if self.dead == True:
            if self.videoPlayed == False:
                self.playVideo()
            self.videoPlayed = True
            self.ifDead()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.isKnockedBack:
            self.ifHit()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.ultPause == True:
            self.ultPauseCount += 1
            if self.ultPauseCount > ULTPAUSE:
                self.ultPause = False
                self.ultPauseCount = 0
        elif self.paused == False:
            #self.updateWalking(keys)
            self.ifWalking()
            self.updateJumping(keys)
            #self.updateJumpingDown(keys)
            #self.updateAttack(keys)
            self.ifAttackingJ()
            self.ifAttackingSJ()
            self.ifAttackingWJ()
            self.ifAttackingI()
            self.ifAttackingU()
            self.ifAttacking()
            #self.updateDefending(keys)
            self.ifDefending()
            self.ifHit()
            self.ifStanding()
            self.updateEnergy()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.paused:
            self.ifStanding()
            self.ifHit()
            self.pauseCount += 1
            if self.pauseCount == PAUSECOUNT:
                self.paused = False
                self.pauseCount = 0
                self.isHit = False
            self.rect.x += self.vx
            self.rect.y += self.vy

    def draw(self):
        if self.image in self.rightAttackWJ or self.image in self.leftAttackWJ:
            self.screen.blit(self.image, (self.rect.x + self.width//2 - self.image.get_width()//2, self.rect.y + self.height - self.image.get_height()))
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (WIDTH-50,0))
        text = 'Player1 Health:' + str(int(self.health))
        width = self.health *3/2
        drawText(self.screen,text,WHITE,WIDTH/3*2-50,0)
        if self.dead == False:
            self.healthbar = pygame.Surface((width,25))
            self.healthbar.fill(RED)
            self.screen.blit(self.healthbar, (WIDTH//3*2-50,25))
        if self.energy == 150: color = ORANGE
        elif self.energy >= 100: color = YELLOW
        elif self.energy >= 50: color = GREEN
        else: color = BLUE
        self.energybar = pygame.Surface((self.energy,10))
        self.energybar.fill(color)
        self.screen.blit(self.energybar,(WIDTH//3*2-50,55))

    def ifAttackingWJ(self):
        fpsPerSprite = (FPS // len(self.rightAttackWJ) + 1)
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingI) and self.isAttackingWJ:
            self.isAttacking = True
            self.isDefending = False
            #self.dmg = 0.5
            self.dmg = 10
            self.attackMove = 0
            self.attackMoveY = -150
            self.energy += 0.2
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackWJ[self.attackCountWJ//fpsPerSprite]
                self.attackCountWJ += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackWJ[self.attackCountWJ//fpsPerSprite]
                self.attackCountWJ += 1
        if self.attackCountWJ//fpsPerSprite >= len(self.rightAttackWJ):
            self.attackCountWJ = 0
            self.isAttackingWJ = False
            self.isAttacking = False
            self.paused = True
            self.dmg = DMG
            self.attackMove = 0
            self.attackMoveY = 0

    def updateWalking(self,keys):
        super().updateWalking(keys, pygame.K_LEFT, pygame.K_RIGHT)

    def updateDefending(self,keys):
        super().updateDefending(keys, pygame.K_DOWN)

    def updateJumping(self,keys):
        super().updateJumping(keys, pygame.K_PAGEDOWN, pygame.K_DOWN)

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not self.isHit:
            if keys[pygame.K_DOWN] and keys[pygame.K_END]:
                self.isAttackingSJ = True
            elif keys[pygame.K_UP] and keys[pygame.K_END] and self.isAttackingSJ == False:
                self.isAttackingWJ = True
            elif self.isAttackingSJ == False and self.isAttackingWJ == False and keys[pygame.K_END]:
                self.isAttackingJ = True
            elif keys[pygame.K_RSHIFT]:
                self.isAttackingU = True
            elif keys[pygame.K_PAGEUP]:
                self.isAttackingI = True

    def ifAttackingJ(self):
        if self.jClickCount == 0:
            tempR = self.rightAttackJ[:6]
            tempL = self.leftAttackJ[:6]
        elif self.jClickCount == 1:
            tempR = self.rightAttackJ[:12]
            tempL = self.leftAttackJ[:12]
        fpsPerSprite = (FPS // len(self.rightAttackJ[:6]) + 1)//4*3
        if self.isAttackingJ:
            self.isAttacking = True
            self.isDefending = False
            self.energy += 0.1
            if self.facingRight:
                self.rect.x += 1
                self.image = tempR[self.attackCountJ//fpsPerSprite]
                self.attackCountJ += 1
            else:
                self.rect.x -= 1
                self.image = tempL[self.attackCountJ//fpsPerSprite]
                self.attackCountJ += 1
        if self.attackCountJ//fpsPerSprite >= len(tempR):
            self.attackCountJ = 0
            self.jClickCount = 0
            self.isAttackingJ = False
            self.isAttacking = False
            self.paused = True

    def ifAttackingI(self):
        #self.attackMotion(self.isAttackingI, self.leftAttackI, self.rightAttackI, self.attackCountI, 2, 0.5, 2)
        fpsPerSprite = (FPS // len(self.rightAttackI) + 1)*2
        if self.isAttackingI and self.energy >= 50:
            if self.attackCountI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0
            self.attackMove = 0
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackI[self.attackCountI//fpsPerSprite]
                self.attackCountI += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackI[self.attackCountI//fpsPerSprite]
                self.attackCountI += 1
        if self.attackCountI//fpsPerSprite >= len(self.rightAttackI):
            self.attackCountI = 0
            self.isAttackingI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 50
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

class Enel_1(Enel):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)

    def update(self):
        keys = pygame.key.get_pressed()
        self.updateDead()
        if self.dead == True:
            #if self.videoPlayed == False:
            #    self.playVideo()
            #self.videoPlayed = True
            self.ifDead()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.isKnockedBack:
            self.ifHit()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.ultPause == True:
            self.ultPauseCount += 1
            if self.ultPauseCount > ULTPAUSE:
                self.ultPause = False
                self.ultPauseCount = 0
        elif self.paused == False:
            self.updateWalking(keys)
            self.ifWalking()
            self.updateJumping(keys)
            self.updateAttack(keys)
            self.ifAttackingJ()
            self.ifAttackingSJ()
            self.ifAttackingWJ()
            self.ifAttackingI()
            self.ifAttackingU()
            self.ifAttacking()
            self.updateDefending(keys)
            self.ifDefending()
            self.ifHit()
            self.ifStanding()
            self.updateEnergy()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.paused:
            self.ifStanding()
            self.ifHit()
            self.pauseCount += 1
            if self.pauseCount == PAUSECOUNT:
                self.paused = False
                self.pauseCount = 0
                self.isHit = False
            self.rect.x += self.vx
            self.rect.y += self.vy

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not self.isHit:
            if keys[pygame.K_s] and keys[pygame.K_j] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_w] and keys[pygame.K_j] and not(self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_j] and not(self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_u] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ):
                self.isAttackingU = True
            elif keys[pygame.K_i] and self.energy >= 50 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

    def draw(self):
        if self.image in self.rightAttackWJ or self.image in self.leftAttackWJ:
            self.screen.blit(self.image, (self.rect.x + self.width//2 - self.image.get_width()//2, self.rect.y + self.height - self.image.get_height()))
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (0,0))
        text = 'Player2 Health:' + str(int(self.health))
        width = self.health * 3/2
        if width <= 0: width = 0
        drawText(self.screen,text,WHITE,50,0)
        if self.dead == False:
            self.healthbar = pygame.Surface((width,25))
            self.healthbar.fill(RED)
            self.screen.blit(self.healthbar, (60,25))
        if self.energy == 150: color = ORANGE
        elif self.energy >= 100: color = YELLOW
        elif self.energy >= 50: color = GREEN
        else: color = BLUE
        self.energybar = pygame.Surface((self.energy,10))
        self.energybar.fill(color)
        self.screen.blit(self.energybar,(60,55))

    def updateWalking(self,keys):
        self.walk(keys, pygame.K_a, pygame.K_d)

    def updateJumping(self,keys):
        self.jump(keys, pygame.K_k, pygame.K_s)

    def updateDefending(self,keys):
        self.defend(keys, pygame.K_s)

    def walk(self, keys, leftKey, rightKey):
        if not(self.isAttacking or self.isDefending or self.isHit):
            if keys[leftKey]:
                self.vx = -self.speed
                self.facingLeft = True
                self.facingRight = False
                self.isWalking = True
            elif keys[rightKey]:
                self.vx = self.speed
                self.facingLeft = False
                self.facingRight = True
                self.isWalking = True
            else:
                self.isWalking = False
                self.walkCount = 0
                self.vx = 0

    def jump(self,keys,jumpKey,downKey):
        if not (self.airBorne or self.isAttacking or self.isHit):
            if keys[jumpKey] and keys[downKey]:
                self.isJumpingDown = True
            elif keys[jumpKey]:
                self.vy = -6
                self.airBorne = True
        if self.vy < 0:
            self.isFalling = False
        elif self.vy >= 0:
            self.isFalling = True

    def defend(self,keys,defendKey):
        if self.vx == 0 and self.vy == 0 and not (self.isAttacking or self.isHit) and keys[defendKey]:
            self.isDefending = True
        else:
            self.isDefending = False

class Enel_2(Enel):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)

    def update(self):
        keys = pygame.key.get_pressed()
        self.updateDead()
        if self.dead == True:
            #if self.videoPlayed == False:
            #    self.playVideo()
            #self.videoPlayed = True
            self.ifDead()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.isKnockedBack:
            self.ifHit()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.ultPause == True:
            self.ultPauseCount += 1
            if self.ultPauseCount > ULTPAUSE:
                self.ultPause = False
                self.ultPauseCount = 0
        elif self.paused == False:
            self.updateWalking(keys)
            self.ifWalking()
            self.updateJumping(keys)
            self.updateAttack(keys)
            self.ifAttackingJ()
            self.ifAttackingSJ()
            self.ifAttackingWJ()
            self.ifAttackingI()
            self.ifAttackingU()
            self.ifAttacking()
            self.updateDefending(keys)
            self.ifDefending()
            self.ifHit()
            self.ifStanding()
            self.updateEnergy()
            self.rect.x += self.vx
            self.rect.y += self.vy
        elif self.paused:
            self.ifStanding()
            self.ifHit()
            self.pauseCount += 1
            if self.pauseCount == PAUSECOUNT:
                self.paused = False
                self.pauseCount = 0
                self.isHit = False
            self.rect.x += self.vx
            self.rect.y += self.vy


