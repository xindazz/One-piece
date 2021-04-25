import pygame
from math import *
import os
from settings import *
from sprites import *

class Doflamingo(character):
    def __init__(self,screen,x,y):
        super().__init__(x,y,screen)
        self.name = 'Doflamingo'
        self.health = 150
        self.setUpSprites('AllSprites' + os.sep + 'doflamingo')
        self.facingLeft = True
        self.facingRight = False
        self.rangedAttack = pygame.Surface((50,3))
        self.rangedAttack.fill(WHITE)
        self.rangedWidth = self.rangedAttack.get_width()
        self.image = self.walkLeft[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
        self.jClickCountMax = 2

    def playVideo(self):
        pygame.mixer.music.load('Luffy+Doffy1.mp3')
        pygame.mixer.music.play()
        cap = cv2.VideoCapture('Luffy+Doffy1.mp4')
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
            self.ifFlyingAway()
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
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (WIDTH-50,0))
        text = 'Enemy Health:' + str(int(self.health))
        width = self.health * 3/2 * 100 / 150
        if width <= 0: width = 0
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

    def updateWalking(self,keys):
        super().updateWalking(keys, pygame.K_LEFT, pygame.K_RIGHT)

    def updateDefending(self,keys):
        super().updateDefending(keys, pygame.K_DOWN)

    def updateJumping(self,keys):
        super().updateJumping(keys, pygame.K_PAGEDOWN, pygame.K_DOWN)

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not self.isHit:
            if keys[pygame.K_DOWN] and keys[pygame.K_END] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_UP] and keys[pygame.K_END] and not(self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_END] and not(self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_RSHIFT] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ):
                self.isAttackingU = True
            elif keys[pygame.K_PAGEUP] and self.energy >= 50 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

    def ifAttackingWJ(self):
        fpsPerSprite = (FPS // len(self.rightAttackWJ) + 1) //3 *2
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingI) and self.isAttackingWJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.2
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
        '''else:
            self.dmg = DMG
            self.attackMove = 0
            self.attackMoveY = 0'''
        if self.attackCountWJ//fpsPerSprite >= len(self.rightAttackWJ):
            self.attackCountWJ = 0
            self.isAttackingWJ = False
            self.isAttacking = False
            self.paused = True
            self.dmg = DMG
            self.attackMove = 0
            self.attackMoveY = 0

    def ifAttackingJ(self):
        if self.jClickCount == 0:
            tempR = self.rightAttackJ[:6]
            tempL = self.leftAttackJ[:6]
        elif self.jClickCount == 1:
            tempR = self.rightAttackJ[:11]
            tempL = self.leftAttackJ[:11]
        elif self.jClickCount == 2:
            tempR = self.rightAttackJ[:17]
            tempL = self.leftAttackJ[:17]
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
        fpsPerSprite = (FPS // len(self.rightAttackI) + 1) * 2
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
        else:
            self.dmg = DMG
            self.attackMove = ATTACKMOVE
        if self.attackCountI//fpsPerSprite >= len(self.rightAttackI):
            self.attackCountI = 0
            self.isAttackingI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 50

class DoflamingoAwakened(Doflamingo):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)
        self.health = 250
        self.energy = 150
        self.leftAttackSI = getSprites('AllSprites' + os.sep + 'doflamingo' + os.sep + 'Attacks' + os.sep + 'attackSI')
        self.rightAttackSI = getFlippedSprites(self.leftAttackSI)
        self.attackCountSI = 0
        self.isAttackingSI = False
        self.godThread = pygame.image.load('AllSprites' + os.sep + 'doflamingo' + os.sep + '0.png')
        self.godThread = pygame.transform.scale(self.godThread, (200,100))
        self.finalCount = 0
        self.ultSound2 = pygame.mixer.Sound('AllSprites' + os.sep + 'doflamingo' + os.sep + 'ultSound2.wav')
        self.ultSound2.set_volume(0.3)
        self.iconSI = pygame.image.load('AllSprites' + os.sep + 'doflamingo' + os.sep + 'iconSI.png')
        self.iconSI = pygame.transform.scale(self.iconSI, (WIDTH, HEIGHT))

    def playVideo(self):
        pygame.mixer.music.load('Luffy+Doffy2.mp3')
        pygame.mixer.music.play()
        cap = cv2.VideoCapture('Luffy+Doffy2.mp4')
        videoCount = 0
        while True:
            ret, frame = cap.read()
            cv2.imshow('frame',frame)
            frame = cv2.resize(frame,(500,500),interpolation = cv2.INTER_AREA)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
            videoCount += 1
            if videoCount > 1000:
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
            #self.updateAttack(keys)
            self.ifAttackingJ()
            self.ifAttackingSJ()
            self.ifAttackingWJ()
            self.ifAttackingI()
            self.ifAttackingSI()
            self.ifAttackingU()
            self.ifAttacking()
            #self.updateDefending(keys)
            self.ifDefending()
            self.ifHit()
            self.ifStanding()
            self.updateEnergy()
            self.ifFlyingAway()
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
            if keys[pygame.K_DOWN] and keys[pygame.K_END] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_UP] and keys[pygame.K_END] and not(self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_END] and not(self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_RSHIFT] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ):
                self.isAttackingU = True
            elif keys[pygame.K_DOWN] and keys[pygame.K_PAGEUP] and self.energy >= 150:
                self.isAttackingSI = True
            elif keys[pygame.K_PAGEUP] and self.energy >= 50 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

    def draw(self):
        if self.isAttackingSI:
            self.screen.blit(self.image, (self.rect.x + self.width//2 - self.image.get_width()//2, self.rect.y + self.height - self.image.get_height()))
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (WIDTH-50,0))
        text = 'Enemy Health:' + str(int(self.health))
        width = self.health * 3/2 * 100 / 250
        if width <= 0: width = 0
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

    def ifAttackingSI(self):
        fpsPerSprite = (FPS // len(self.rightAttackSI) + 1)
        if self.isAttackingSI and self.energy >= 150:
            if self.attackCountSI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0
            self.attackMove = 0
            index = self.attackCountSI//fpsPerSprite
            if index >= len(self.rightAttackSI):
                index = len(self.rightAttackSI) - 1
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackSI[index]
                self.attackCountSI += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackSI[index]
                self.attackCountSI += 1
        if self.finalCount >= FPS * 2:
            self.attackCountSI = 0
            self.isAttackingSI = False
            self.isAttacking = False
            self.finalCount = 0
            self.paused = True
            self.energy -= 150
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

class Doflamingo_1(Doflamingo):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)
        self.health = 100

    def playVideo(self):
        pass

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
            self.ifFlyingAway()
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


class Doflamingo_2(Doflamingo):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)
        self.health = 100

    def playVideo(self):
        pass

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
            self.ifFlyingAway()
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
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (WIDTH-50,0))
        text = 'Player2 Health:' + str(int(self.health))
        width = self.health * 3/2
        if width <= 0: width = 0
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

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not self.isHit:
            if keys[pygame.K_DOWN] and keys[pygame.K_END] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_UP] and keys[pygame.K_END] and not(self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_END] and not(self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_RSHIFT] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ):
                self.isAttackingU = True
            elif keys[pygame.K_PAGEUP] and self.energy >= 50 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True
