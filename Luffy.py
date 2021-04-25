import pygame
from math import *
import os
from settings import *
from sprites import *

class Luffy(character):
    def __init__(self,screen,x,y):
        super().__init__(x,y,screen)
        self.name = 'luffy'
        self.setUpSprites('AllSprites' + os.sep + 'luffy')
        self.image = self.walkRight[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)

    def playVideo(self):
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

    '''def loadMusic(self, path):
        self.gomu = pygame.mixer.Sound(path + os.sep + 'gomu.wav')
        self.bazuka = pygame.mixer.Sound(path + os.sep + 'bazuka.wav')
        self.yali = pygame.mixer.Sound(path + os.sep + 'yali.wav')
        self.olialialia = pygame.mixer.Sound(path + os.sep + 'olialialia.wav')
        self.gatling = pygame.mixer.Sound(path + os.sep + 'gatling.wav')'''

    def update(self):
        keys = pygame.key.get_pressed()
        self.updateDead()
        if self.dead == True:
            self.ifDead()
            self.rect.x += self.vx
            self.rect.y += self.vy
            self.health = 0
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

    def draw(self):
        if self.image == self.rightAttackWJ[4] or self.image == self.rightAttackWJ[5]:
            self.screen.blit(self.image, (self.rect.x, self.rect.y - self.image.get_height()//2))
        elif self.image == self.leftAttackWJ[4] or self.image == self.leftAttackWJ[5]:
            self.screen.blit(self.image, (self.rect.x - self.image.get_width()//2, self.rect.y - self.image.get_height()//2))
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (0,0))
        # health num
        text = 'Player1 Health:' + str(int(self.health))
        drawText(self.screen,text,WHITE,50,0)
        #health bar
        if self.dead == False:
            width = self.health * 3 / 2
            self.healthbar = pygame.Surface((width,25))
            self.healthbar.fill(RED)
            self.screen.blit(self.healthbar, (60,25))
        #energy bar
        if self.energy == 150: color = ORANGE
        elif self.energy >= 100: color = YELLOW
        elif self.energy >= 50: color = GREEN
        else: color = BLUE
        self.energybar = pygame.Surface((self.energy,10))
        self.energybar.fill(color)
        self.screen.blit(self.energybar,(60,55))

    def updateWalking(self,keys):
        super().updateWalking(keys, pygame.K_a, pygame.K_d)

    def updateJumping(self,keys):
        super().updateJumping(keys, pygame.K_k, pygame.K_s)

    def updateDefending(self,keys):
        super().updateDefending(keys, pygame.K_s)

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not self.isHit:
            if keys[pygame.K_s] and keys[pygame.K_j] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_w] and keys[pygame.K_j] and not(self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_j] and not(self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_i] and self.energy >= 50 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

    def ifAttackingSJ(self):
        fpsPerSprite = FPS // len(self.rightAttackSJ) + 1
        if not(self.isAttackingJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI) and self.isAttackingSJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.2
            self.attackMove = 2
            self.energy += 0.2
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
        if self.attackCountSJ//fpsPerSprite >= len(self.rightAttackSJ):
            self.attackCountSJ = 0
            self.isAttackingSJ = False
            self.isAttacking = False
            self.paused = True
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

class Luffy_1(Luffy):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)

class Luffy_2(Luffy):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)

    def draw(self):
        if self.image == self.rightAttackWJ[4] or self.image == self.rightAttackWJ[5]:
            self.screen.blit(self.image, (self.rect.x, self.rect.y - self.image.get_height()//2))
        elif self.image == self.leftAttackWJ[4] or self.image == self.leftAttackWJ[5]:
            self.screen.blit(self.image, (self.rect.x - self.image.get_width()//2, self.rect.y - self.image.get_height()//2))
        else:
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

    def updateWalking(self,keys):
        self.walk(keys, pygame.K_LEFT, pygame.K_RIGHT)

    def updateDefending(self,keys):
        self.defend(keys, pygame.K_DOWN)

    def updateJumping(self,keys):
        self.jump(keys, pygame.K_PAGEDOWN, pygame.K_DOWN)

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not self.isHit:
            if keys[pygame.K_DOWN] and keys[pygame.K_END] and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_UP] and keys[pygame.K_END] and not(self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_END] and not(self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_PAGEUP] and self.energy >= 50 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

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


class LuffyGear2(character):
    def __init__(self,screen,x,y):
        super().__init__(x,y,screen)
        self.name = 'Luffy Gear 2 and 3'
        self.setUpSprites('AllSprites' + os.sep + 'luffy_gear2')
        self.rangedAttack = pygame.image.load('AllSprites' + os.sep + 'luffy_gear2' + os.sep + 'Attacks' + os.sep + 'projectile' + os.sep + '0.png')
        self.rangedWidth = self.rangedAttack.get_width()
        self.image = self.walkRight[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
        self.ultCount = 0
        self.jClickCountMax = 1
        self.attackMove = 0
        self.attackMoveY = 0
        self.deathvideo = cv2.VideoCapture('Luffy+Crocodile.mp4')

    def playVideo(self):
        '''cap = deathvideo
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
        cv2.destroyAllWindows()'''
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        self.updateDead()
        if self.dead == True:
            #if self.videoPlayed == False:
                #self.playVideo()
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

    def draw(self):
        if self.image in [self.rightAttackI[20],self.rightAttackI[21],self.rightAttackI[22],self.rightAttackI[23],self.leftAttackI[20],self.leftAttackI[21],self.leftAttackI[22],self.leftAttackI[23]]:
            self.screen.blit(self.image, (self.rect.x, self.rect.y + self.height - self.image.get_height()))
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (0,0))
        text = 'Player1 Health:' + str(int(self.health))
        drawText(self.screen,text,WHITE,50,0)
        if self.dead == False:
            width = self.health * 3 / 2
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

    def ifAttackingWJ(self):
        fpsPerSprite = (FPS // len(self.rightAttackWJ) + 1)
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingI or self.isAttackingWI) and self.isAttackingWJ:
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

    def updateWalking(self,keys):
        super().updateWalking(keys, pygame.K_a, pygame.K_d)

    def updateJumping(self,keys):
        super().updateJumping(keys, pygame.K_k, pygame.K_s)

    def updateDefending(self,keys):
        super().updateDefending(keys, pygame.K_s)

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

    def ifAttackingJ(self):
        if self.jClickCount == 0:
            tempR = self.rightAttackJ[:5]
            tempL = self.leftAttackJ[:5]
        elif self.jClickCount == 1:
            tempR = self.rightAttackJ[:11]
            tempL = self.leftAttackJ[:11]
        fpsPerSprite = (FPS // len(self.rightAttackJ[:4]) + 1)//3
        if not(self.isAttackingSJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI or self.isAttackingWI) and self.isAttackingJ:
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

    def ifAttackingSJ(self):
        fpsPerSprite = FPS // len(self.rightAttackSJ) + 1
        if not(self.isAttackingJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI or self.isAttackingWI) and self.isAttackingSJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.2
            self.attackMove = 2
            self.energy += 0.2
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
        if self.attackCountSJ//fpsPerSprite >= len(self.rightAttackSJ):
            self.attackCountSJ = 0
            self.isAttackingSJ = False
            self.isAttacking = False
            self.paused = True
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

class LuffyGear2_1(LuffyGear2):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)

class LuffyGear2_2(LuffyGear2):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)

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

    def draw(self):
        if self.image in [self.rightAttackI[20],self.rightAttackI[21],self.rightAttackI[22],self.rightAttackI[23],self.leftAttackI[20],self.leftAttackI[21],self.leftAttackI[22],self.leftAttackI[23]]:
            self.screen.blit(self.image, (self.rect.x, self.rect.y + self.height - self.image.get_height()))
        else:
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

    def updateWalking(self,keys):
        self.walk(keys, pygame.K_LEFT, pygame.K_RIGHT)

    def updateDefending(self,keys):
        self.defend(keys, pygame.K_DOWN)

    def updateJumping(self,keys):
        self.jump(keys, pygame.K_PAGEDOWN, pygame.K_DOWN)

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

class LuffyArmament(character):
    def __init__(self,screen,x,y):
        super().__init__(x,y,screen)
        self.name = 'Luffy Armament'
        self.setUpSprites('AllSprites' + os.sep + 'luffy_gear2_armament')
        self.rangedAttack = pygame.image.load('AllSprites' + os.sep + 'luffy_gear2_armament' + os.sep + 'Attacks' + os.sep + 'projectile' + os.sep + '0.png')
        self.rangedWidth = self.rangedAttack.get_width()
        self.rightAttackWI = getSprites('AllSprites' + os.sep + 'luffy_gear2_armament' + os.sep + 'Attacks' + os.sep + 'attackWI')
        self.leftAttackWI = getFlippedSprites(self.rightAttackWI)
        self.image = self.walkRight[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
        self.ultCount = 0
        self.jClickCountMax = 1
        self.attackMove = ATTACKMOVE
        self.attackMoveY = 0
        self.deathvideo = cv2.VideoCapture('Luffy+Crocodile.mp4')
        self.iconWI = pygame.image.load('AllSprites' + os.sep + 'luffy_gear2_armament' + os.sep + 'iconWI.jpg')
        self.iconWI = pygame.transform.scale(self.iconWI, (WIDTH, HEIGHT))
        self.ultSound2 = pygame.mixer.Sound('AllSprites' + os.sep + 'luffy_gear2_armament' + os.sep + 'ultSound2.wav')
        self.isTransforming = False
        self.transformed = False
        self.transformCount = 0
        self.transformation = getSprites('AllSprites' + os.sep + 'luffy_gear2_armament' + os.sep + 'transform')

    def playVideo(self):
        '''cap = deathvideo
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
        cv2.destroyAllWindows()'''
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        self.updateDead()
        if self.dead == True:
            #if self.videoPlayed == False:
                #self.playVideo()
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
        elif self.isTransforming:
            self.ifTransforming()
        elif self.paused == False:
            self.updateWalking(keys)
            self.ifWalking()
            self.updateJumping(keys)
            self.updateAttack(keys)
            self.ifAttackingJ()
            self.ifAttackingSJ()
            self.ifAttackingWJ()
            self.ifAttackingWI()
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

    def draw(self):
        #if self.image in [self.rightAttackI[20],self.rightAttackI[21],self.rightAttackI[22],self.rightAttackI[23],self.leftAttackI[20],self.leftAttackI[21],self.leftAttackI[22],self.leftAttackI[23]]:
        #    self.screen.blit(self.image, (self.rect.x, self.rect.y + self.height - self.image.get_height()))
        #else:
        if self.image in [self.rightAttackWI[4],self.rightAttackWI[5],self.rightAttackWI[6],self.rightAttackWI[7],self.leftAttackWI[4],self.leftAttackWI[5],self.leftAttackWI[6],self.leftAttackWI[7]]:
            self.screen.blit(self.image, (self.rect.x + self.width//2 - self.image.get_width()//2, self.rect.y + self.height - self.image.get_height()))
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (0,0))
        text = 'Player1 Health:' + str(int(self.health))
        drawText(self.screen,text,WHITE,50,0)
        if self.dead == False:
            width = self.health * 3 / 2
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

    def ifAttackingWJ(self):
        fpsPerSprite = (FPS // len(self.rightAttackWJ) + 1)
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingI or self.isAttackingWI) and self.isAttackingWJ:
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

    def updateWalking(self,keys):
        super().updateWalking(keys, pygame.K_a, pygame.K_d)

    def updateJumping(self,keys):
        super().updateJumping(keys, pygame.K_k, pygame.K_s)

    def updateDefending(self,keys):
        super().updateDefending(keys, pygame.K_s)

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not(self.isHit):
            if keys[pygame.K_o] and self.energy == 150:
                self.isTransforming = True
            elif keys[pygame.K_s] and keys[pygame.K_j] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_w] and keys[pygame.K_j] and not(self.isAttackingWI or self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_j] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_u] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ):
                self.isAttackingU = True
            elif keys[pygame.K_i] and keys[pygame.K_w] and self.energy >= 75 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingWI = True
            elif keys[pygame.K_i] and self.energy >= 50 and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

    def ifTransforming(self):
        fpsPerSprite = (FPS // len(self.transformation) + 1) * 2
        if self.isTransforming:
            self.image = self.transformation[self.transformCount // fpsPerSprite]
            self.transformCount += 1
        if self.transformCount//fpsPerSprite >= len(self.transformation):
            self.transformCount = 0
            self.transformed = True

    def ifAttackingJ(self):
        if self.jClickCount == 0:
            tempR = self.rightAttackJ[:5]
            tempL = self.leftAttackJ[:5]
        elif self.jClickCount == 1:
            tempR = self.rightAttackJ[:11]
            tempL = self.leftAttackJ[:11]
        fpsPerSprite = (FPS // len(self.rightAttackJ[:4]) + 1)//3
        if not(self.isAttackingSJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI or self.isAttackingWI) and self.isAttackingJ:
            self.isAttacking = True
            self.isDefending = False
            self.energy += 0.1
            if self.facingRight:
                self.rect.x += ATTACKMOVE
                self.image = tempR[self.attackCountJ//fpsPerSprite]
                self.attackCountJ += 1
            else:
                self.rect.x -= ATTACKMOVE
                self.image = tempL[self.attackCountJ//fpsPerSprite]
                self.attackCountJ += 1
        if self.attackCountJ//fpsPerSprite >= len(tempR):
            self.attackCountJ = 0
            self.jClickCount = 0
            self.isAttackingJ = False
            self.isAttacking = False
            self.paused = True

    def ifAttackingSJ(self):
        fpsPerSprite = FPS // len(self.rightAttackSJ) + 1
        if not(self.isAttackingJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI or self.isAttackingWI) and self.isAttackingSJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.2
            self.attackMove = 2
            self.energy += 0.2
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
        if self.attackCountSJ//fpsPerSprite >= len(self.rightAttackSJ):
            self.attackCountSJ = 0
            self.isAttackingSJ = False
            self.isAttacking = False
            self.paused = True
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

    def ifAttackingI(self):
        fpsPerSprite = (FPS // len(self.rightAttackI) + 1) * 2
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingWJ or self.isAttackingWI) and self.isAttackingI and self.energy >= 50:
            if self.attackCountI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            if self.facingRight:
                self.image = self.rightAttackI[self.attackCountI//fpsPerSprite]
                if self.rightAttackI.index(self.image) in [0,1,2,3,4]:
                    self.dmg = 0
                    self.attackMove = 0
                else:
                    self.dmg = 0.2
                    self.attackMove = 2
                self.attackCountI += 1
                self.rect.x += self.attackMove
            else:
                self.image = self.leftAttackI[self.attackCountI//fpsPerSprite]
                if self.leftAttackI.index(self.image) in [0,1,2,3,4]:
                    self.dmg = 0
                    self.attackMove = 0
                else:
                    self.dmg = 0.2
                    self.attackMove = 2
                self.rect.x -= self.attackMove
                self.attackCountI += 1
        if self.attackCountI//fpsPerSprite >= len(self.rightAttackI):
            self.attackCountI = 0
            self.isAttackingI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 50
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

    def ifAttackingWI(self):
        fpsPerSprite = FPS // len(self.rightAttackWI) + 1
        if not(self.isAttackingJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI or self.isAttackingSJ) and self.isAttackingWI and self.energy >= 75:
            if self.attackCountWI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.attackMove = 0
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackWI[self.attackCountWI//fpsPerSprite]
                self.mask = pygame.mask.from_surface(self.image)
                self.attackCountWI += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackWI[self.attackCountWI//fpsPerSprite]
                self.mask = pygame.mask.from_surface(self.image)
                self.attackCountWI += 1
            if self.image in [self.rightAttackWI[4],self.rightAttackWI[5],self.rightAttackWI[6],self.rightAttackWI[7],self.leftAttackWI[4],self.leftAttackWI[5],self.leftAttackWI[6],self.leftAttackWI[7]]:
                self.dmg = 0.3
            else:
                self.dmg = 0
        if self.attackCountWI//fpsPerSprite >= len(self.rightAttackWI):
            self.attackCountWI = 0
            self.isAttackingWI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 75
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

class LuffyArmament_1(LuffyArmament):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not(self.isHit):
            if keys[pygame.K_s] and keys[pygame.K_j] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_w] and keys[pygame.K_j] and not(self.isAttackingWI or self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_j] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_u] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ):
                self.isAttackingU = True
            elif keys[pygame.K_i] and keys[pygame.K_w] and self.energy >= 75 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingWI = True
            elif keys[pygame.K_i] and self.energy >= 50 and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

class LuffyArmament_2(LuffyArmament):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not(self.isHit):
            if keys[pygame.K_DOWN] and keys[pygame.K_END] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_UP] and keys[pygame.K_END] and not(self.isAttackingWI or self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_END] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_RSHIFT] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ):
                self.isAttackingU = True
            elif keys[pygame.K_PAGEUP] and keys[pygame.K_UP] and self.energy >= 75 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingWI = True
            elif keys[pygame.K_PAGEUP] and self.energy >= 50 and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

    def draw(self):
        if self.image in [self.rightAttackWI[4],self.rightAttackWI[5],self.rightAttackWI[6],self.rightAttackWI[7],self.leftAttackWI[4],self.leftAttackWI[5],self.leftAttackWI[6],self.leftAttackWI[7]]:
            self.screen.blit(self.image, (self.rect.x + self.width//2 - self.image.get_width()//2, self.rect.y + self.height - self.image.get_height()))
        else:
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

    def updateWalking(self,keys):
        self.walk(keys, pygame.K_LEFT, pygame.K_RIGHT)

    def updateDefending(self,keys):
        self.defend(keys, pygame.K_DOWN)

    def updateJumping(self,keys):
        self.jump(keys, pygame.K_PAGEDOWN, pygame.K_DOWN)

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


class LuffyGear4(character):
    def __init__(self,screen,x,y):
        super().__init__(x,y,screen)
        self.name = 'Luffy LuffyGear4'
        self.health = 250
        self.setUpSprites('AllSprites' + os.sep + 'luffy_gear4')
        #self.rangedAttack = pygame.image.load('AllSprites' + os.sep + 'luffy_gear2_armament' + os.sep + 'Attacks' + os.sep + 'projectile' + os.sep + '0.png')
        #self.rangedWidth = self.rangedAttack.get_width()
        self.rightAttackWI = getSprites('AllSprites' + os.sep + 'luffy_gear4' + os.sep + 'Attacks' + os.sep + 'attackWI')
        self.leftAttackWI = getFlippedSprites(self.rightAttackWI)
        self.image = self.walkRight[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
        self.ultCount = 0
        self.jClickCountMax = 2
        self.attackMove = 0
        self.attackMoveY = 0
        self.deathvideo = cv2.VideoCapture('Luffy+Crocodile.mp4')
        self.iconWI = pygame.image.load('AllSprites' + os.sep + 'luffy_gear4' + os.sep + 'iconWI.jpg')
        self.iconWI = pygame.transform.scale(self.iconWI, (WIDTH, HEIGHT))
        self.ultSound2 = pygame.mixer.Sound('AllSprites' + os.sep + 'luffy_gear4' + os.sep + 'ultSound2.wav')
        self.transformSound = pygame.mixer.Sound('AllSprites' + os.sep + 'luffy_gear4' + os.sep + 'transformSound.wav')
        self.transformSound.set_volume(1)
        self.ultSound.set_volume(0.1)
        self.ultSound2.set_volume(0.1)

    def playVideo(self):
        '''cap = deathvideo
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
        cv2.destroyAllWindows()'''
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        self.updateDead()
        if self.dead == True:
            #if self.videoPlayed == False:
                #self.playVideo()
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
            self.updateWalking(keys)
            self.ifWalking()
            self.updateJumping(keys)
            self.updateAttack(keys)
            self.ifAttackingJ()
            self.ifAttackingSJ()
            self.ifAttackingWJ()
            self.ifAttackingI()
            self.ifAttackingWI()
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

    def draw(self):
        if self.image in [self.rightAttackWI[5],self.rightAttackWI[6],self.rightAttackWI[7], self.leftAttackWI[5],self.leftAttackWI[6],self.leftAttackWI[7]]:
            self.screen.blit(self.image, (self.rect.x + self.width//2 - self.image.get_width()//2, self.rect.y + self.height - self.image.get_height()))
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (0,0))
        text = 'Player1 Health:' + str(int(self.health))
        drawText(self.screen,text,WHITE,50,0)
        if self.dead == False:
            width = self.health * 3 / 2 * 100 / 250
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

    def ifAttackingWJ(self):
        fpsPerSprite = (FPS // len(self.rightAttackWJ) + 1)
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingI) and self.isAttackingWJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.4
            self.attackMove = 0
            self.attackMoveY = -4
            self.energy += 0.3
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
        super().updateWalking(keys, pygame.K_a, pygame.K_d)

    def updateJumping(self,keys):
        super().updateJumping(keys, pygame.K_k, pygame.K_s)

    def updateDefending(self,keys):
        super().updateDefending(keys, pygame.K_s)

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not(self.isHit):
            if keys[pygame.K_s] and keys[pygame.K_j] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_w] and keys[pygame.K_j] and not(self.isAttackingWI or self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_j] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_i] and keys[pygame.K_w] and self.energy >= 75 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingWI = True
            elif keys[pygame.K_i] and self.energy >= 50 and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

    def ifAttackingJ(self):
        if self.jClickCount == 0:
            tempR = self.rightAttackJ[:7]
            tempL = self.leftAttackJ[:7]
        elif self.jClickCount == 1:
            tempR = self.rightAttackJ[:12]
            tempL = self.leftAttackJ[:12]
        elif self.jClickCount == 2:
            tempR = self.rightAttackJ
            tempL = self.leftAttackJ
        fpsPerSprite = (FPS // len(self.rightAttackJ[:4]) + 1) // 2
        if self.isAttackingJ:
            self.isAttacking = True
            self.isDefending = False
            self.energy += 0.15
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

    def ifAttackingSJ(self):
        fpsPerSprite = FPS // len(self.rightAttackSJ) + 1
        if not(self.isAttackingJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI) and self.isAttackingSJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.4


            self.attackMove = 2
            self.energy += 0.3
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
        if self.attackCountSJ//fpsPerSprite >= len(self.rightAttackSJ):
            self.attackCountSJ = 0
            self.isAttackingSJ = False
            self.isAttacking = False
            self.paused = True
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

    def ifAttackingU(self):
        pass

    def ifAttackingI(self):
        fpsPerSprite = (FPS // len(self.rightAttackI) + 1) * 2
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingWJ or self.isAttackingWI) and self.isAttackingI and self.energy >= 50:
            if self.attackCountI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.attackMove = 0
            if self.facingRight:
                self.image = self.leftAttackI[self.attackCountI//fpsPerSprite]
                if self.leftAttackI.index(self.image) in [0,5]:
                    self.dmg = 0
                else:
                    self.dmg = 0.5
                self.attackCountI += 1
                self.rect.x += self.attackMove
            else:
                self.image = self.rightAttackI[self.attackCountI//fpsPerSprite]
                if self.rightAttackI.index(self.image) in [0,5]:
                    self.dmg = 0
                else:
                    self.dmg = 0.3
                self.rect.x -= self.attackMove
                self.attackCountI += 1
        if self.attackCountI//fpsPerSprite >= len(self.rightAttackI):
            self.attackCountI = 0
            self.isAttackingI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 50
            self.dmg = DMG
            self.attackMove = ATTACKMOVE
            self.facingRight = not self.facingRight
            self.facingLeft = not self.facingLeft

    def ifAttackingWI(self):
        fpsPerSprite = FPS // len(self.rightAttackWI) + 1
        if not(self.isAttackingJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI or self.isAttackingSJ) and self.isAttackingWI and self.energy >= 75:
            if self.attackCountWI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.attackMove = 0
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackWI[self.attackCountWI//fpsPerSprite]
                self.mask = pygame.mask.from_surface(self.image)
                self.attackCountWI += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackWI[self.attackCountWI//fpsPerSprite]
                self.mask = pygame.mask.from_surface(self.image)
                self.attackCountWI += 1
            if self.image in [self.rightAttackWI[5],self.rightAttackWI[6],self.rightAttackWI[7],self.leftAttackWI[5],self.leftAttackWI[6],self.leftAttackWI[7]]:
                self.dmg = 0.5
            else:
                self.dmg = 0
        if self.attackCountWI//fpsPerSprite >= len(self.rightAttackWI):
            self.attackCountWI = 0
            self.isAttackingWI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 75
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

    def setUpSprites(self,path):
        self.icon = pygame.image.load(path + os.sep + 'icon.png')
        self.icon = pygame.transform.scale(self.icon, (50, 50))
        self.walkRight = getSprites(path + os.sep + 'walking')
        self.walkLeft = getFlippedSprites(self.walkRight)
        self.rightStanding = pygame.image.load(path + os.sep + 'standing.png')
        self.leftStanding = getFlippedSprites(self.rightStanding)
        self.rightDefense = pygame.image.load(path + os.sep + 'defending.png')
        self.leftDefense = getFlippedSprites(self.rightDefense)
        self.rightHit = pygame.image.load(path + os.sep + 'hit.png')
        self.leftHit = getFlippedSprites(self.rightHit)
        self.rightAttackJ = getSprites(path + os.sep + 'Attacks' + os.sep + 'attackJ')
        self.leftAttackJ = getFlippedSprites(self.rightAttackJ)
        self.rightAttackSJ = getSprites(path + os.sep + 'Attacks' + os.sep + 'attackSJ')
        self.leftAttackSJ = getFlippedSprites(self.rightAttackSJ)
        self.rightAttackWJ = getSprites(path + os.sep + 'Attacks' + os.sep + 'attackWJ')
        self.leftAttackWJ = getFlippedSprites(self.rightAttackWJ)
        #self.rightAttackU = getSprites(path + os.sep + 'Attacks' + os.sep + 'attackU')
        #self.leftAttackU = getFlippedSprites(self.rightAttackU)
        self.rightAttackI = getSprites(path + os.sep + 'Attacks' + os.sep + 'attackI')
        self.leftAttackI = getFlippedSprites(self.rightAttackI)
        self.rightDying = pygame.image.load(path + os.sep + 'dying.png')
        self.leftDying = getFlippedSprites(self.rightDying)
        self.rightDead = pygame.image.load(path + os.sep + 'dead.png')
        self.leftDead = getFlippedSprites(self.rightDead)
        self.iconI = pygame.image.load(path + os.sep + 'iconI.png')
        self.iconI = pygame.transform.scale(self.iconI, (WIDTH, HEIGHT))
        self.ultSound = pygame.mixer.Sound(path + os.sep + 'ultSound.wav')

class LuffyGear4_1(LuffyGear4):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)
        self.health = 100

    def ifAttackingWJ(self):
        fpsPerSprite = (FPS // len(self.rightAttackWJ) + 1)
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingI) and self.isAttackingWJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.2
            self.attackMove = 0
            self.attackMoveY = -4
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

    def ifAttackingJ(self):
        if self.jClickCount == 0:
            tempR = self.rightAttackJ[:7]
            tempL = self.leftAttackJ[:7]
        elif self.jClickCount == 1:
            tempR = self.rightAttackJ[:12]
            tempL = self.leftAttackJ[:12]
        elif self.jClickCount == 2:
            tempR = self.rightAttackJ
            tempL = self.leftAttackJ
        fpsPerSprite = (FPS // len(self.rightAttackJ[:4]) + 1) // 2
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

    def ifAttackingSJ(self):
        fpsPerSprite = FPS // len(self.rightAttackSJ) + 1
        if not(self.isAttackingJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI) and self.isAttackingSJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.2
            self.attackMove = 2
            self.energy += 0.2
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
        if self.attackCountSJ//fpsPerSprite >= len(self.rightAttackSJ):
            self.attackCountSJ = 0
            self.isAttackingSJ = False
            self.isAttacking = False
            self.paused = True
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

    def ifAttackingU(self):
        pass

    def ifAttackingI(self):
        fpsPerSprite = (FPS // len(self.rightAttackI) + 1) * 2
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingWJ or self.isAttackingWI) and self.isAttackingI and self.energy >= 50:
            if self.attackCountI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.attackMove = 0
            if self.facingRight:
                self.image = self.leftAttackI[self.attackCountI//fpsPerSprite]
                if self.leftAttackI.index(self.image) in [0,5]:
                    self.dmg = 0
                else:
                    self.dmg = 0.3
                self.attackCountI += 1
                self.rect.x += self.attackMove
            else:
                self.image = self.rightAttackI[self.attackCountI//fpsPerSprite]
                if self.rightAttackI.index(self.image) in [0,5]:
                    self.dmg = 0
                else:
                    self.dmg = 0.3
                self.rect.x -= self.attackMove
                self.attackCountI += 1
        if self.attackCountI//fpsPerSprite >= len(self.rightAttackI):
            self.attackCountI = 0
            self.isAttackingI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 50
            self.dmg = DMG
            self.attackMove = ATTACKMOVE
            self.facingRight = not self.facingRight
            self.facingLeft = not self.facingLeft

    def ifAttackingWI(self):
        fpsPerSprite = FPS // len(self.rightAttackWI) + 1
        if not(self.isAttackingJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI or self.isAttackingSJ) and self.isAttackingWI and self.energy >= 75:
            if self.attackCountWI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.attackMove = 0
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackWI[self.attackCountWI//fpsPerSprite]
                self.mask = pygame.mask.from_surface(self.image)
                self.attackCountWI += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackWI[self.attackCountWI//fpsPerSprite]
                self.mask = pygame.mask.from_surface(self.image)
                self.attackCountWI += 1
            if self.image in [self.rightAttackWI[5],self.rightAttackWI[6],self.rightAttackWI[7],self.leftAttackWI[5],self.leftAttackWI[6],self.leftAttackWI[7]]:
                self.dmg = 0.5
            else:
                self.dmg = 0
        if self.attackCountWI//fpsPerSprite >= len(self.rightAttackWI):
            self.attackCountWI = 0
            self.isAttackingWI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 75
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

    def draw(self):
        if self.image in [self.rightAttackWI[5],self.rightAttackWI[6],self.rightAttackWI[7], self.leftAttackWI[5],self.leftAttackWI[6],self.leftAttackWI[7]]:
            self.screen.blit(self.image, (self.rect.x + self.width//2 - self.image.get_width()//2, self.rect.y + self.height - self.image.get_height()))
        else:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.screen.blit(self.icon, (0,0))
        text = 'Player1 Health:' + str(int(self.health))
        drawText(self.screen,text,WHITE,50,0)
        if self.dead == False:
            width = self.health * 3 / 2
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

class LuffyGear4_2(LuffyGear4):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)
        self.health = 100

    def ifAttackingWJ(self):
        fpsPerSprite = (FPS // len(self.rightAttackWJ) + 1)
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingI) and self.isAttackingWJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.2
            self.attackMove = 0
            self.attackMoveY = -4
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

    def ifAttackingJ(self):
        if self.jClickCount == 0:
            tempR = self.rightAttackJ[:7]
            tempL = self.leftAttackJ[:7]
        elif self.jClickCount == 1:
            tempR = self.rightAttackJ[:12]
            tempL = self.leftAttackJ[:12]
        elif self.jClickCount == 2:
            tempR = self.rightAttackJ
            tempL = self.leftAttackJ
        fpsPerSprite = (FPS // len(self.rightAttackJ[:4]) + 1) // 2
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

    def ifAttackingSJ(self):
        fpsPerSprite = FPS // len(self.rightAttackSJ) + 1
        if not(self.isAttackingJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI) and self.isAttackingSJ:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.2
            self.attackMove = 2
            self.energy += 0.2
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackSJ[self.attackCountSJ//fpsPerSprite]
                self.attackCountSJ += 1
        if self.attackCountSJ//fpsPerSprite >= len(self.rightAttackSJ):
            self.attackCountSJ = 0
            self.isAttackingSJ = False
            self.isAttacking = False
            self.paused = True
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

    def ifAttackingU(self):
        pass

    def ifAttackingI(self):
        fpsPerSprite = (FPS // len(self.rightAttackI) + 1) * 2
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingWJ or self.isAttackingWI) and self.isAttackingI and self.energy >= 50:
            if self.attackCountI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.attackMove = 0
            if self.facingRight:
                self.image = self.leftAttackI[self.attackCountI//fpsPerSprite]
                if self.leftAttackI.index(self.image) in [0,5]:
                    self.dmg = 0
                else:
                    self.dmg = 0.3
                self.attackCountI += 1
                self.rect.x += self.attackMove
            else:
                self.image = self.rightAttackI[self.attackCountI//fpsPerSprite]
                if self.rightAttackI.index(self.image) in [0,5]:
                    self.dmg = 0
                else:
                    self.dmg = 0.3
                self.rect.x -= self.attackMove
                self.attackCountI += 1
        if self.attackCountI//fpsPerSprite >= len(self.rightAttackI):
            self.attackCountI = 0
            self.isAttackingI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 50
            self.dmg = DMG
            self.attackMove = ATTACKMOVE
            self.facingRight = not self.facingRight
            self.facingLeft = not self.facingLeft

    def ifAttackingWI(self):
        fpsPerSprite = FPS // len(self.rightAttackWI) + 1
        if not(self.isAttackingJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI or self.isAttackingSJ) and self.isAttackingWI and self.energy >= 75:
            if self.attackCountWI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.attackMove = 0
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackWI[self.attackCountWI//fpsPerSprite]
                self.mask = pygame.mask.from_surface(self.image)
                self.attackCountWI += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackWI[self.attackCountWI//fpsPerSprite]
                self.mask = pygame.mask.from_surface(self.image)
                self.attackCountWI += 1
            if self.image in [self.rightAttackWI[5],self.rightAttackWI[6],self.rightAttackWI[7],self.leftAttackWI[5],self.leftAttackWI[6],self.leftAttackWI[7]]:
                self.dmg = 0.5
            else:
                self.dmg = 0
        if self.attackCountWI//fpsPerSprite >= len(self.rightAttackWI):
            self.attackCountWI = 0
            self.isAttackingWI = False
            self.isAttacking = False
            self.paused = True
            self.energy -= 75
            self.dmg = DMG
            self.attackMove = ATTACKMOVE

    def updateAttack(self,keys):
        if self.vx == 0 and self.vy == 0 and not(self.isHit):
            if keys[pygame.K_DOWN] and keys[pygame.K_END] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingSJ = True
            elif keys[pygame.K_UP] and keys[pygame.K_END] and not(self.isAttackingWI or self.isAttackingSJ or self.isAttackingJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingWJ = True
            elif keys[pygame.K_END] and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingSJ or self.isAttackingI or self.isAttackingU):
                self.isAttackingJ = True
            elif keys[pygame.K_PAGEUP] and keys[pygame.K_UP] and self.energy >= 75 and not(self.isAttackingWJ or self.isAttackingJ or self.isAttackingI or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingWI = True
            elif keys[pygame.K_PAGEUP] and self.energy >= 50 and not(self.isAttackingWI or self.isAttackingWJ or self.isAttackingJ or self.isAttackingSJ or self.isAttackingU):
                self.isAttackingI = True

    def draw(self):
        if self.image in [self.rightAttackWI[5],self.rightAttackWI[6],self.rightAttackWI[7], self.leftAttackWI[5],self.leftAttackWI[6],self.leftAttackWI[7]]:
            self.screen.blit(self.image, (self.rect.x + self.width//2 - self.image.get_width()//2, self.rect.y + self.height - self.image.get_height()))
        else:
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

    def updateWalking(self,keys):
        self.walk(keys, pygame.K_LEFT, pygame.K_RIGHT)

    def updateDefending(self,keys):
        self.defend(keys, pygame.K_DOWN)

    def updateJumping(self,keys):
        self.jump(keys, pygame.K_PAGEDOWN, pygame.K_DOWN)

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

