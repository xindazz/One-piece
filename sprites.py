import pygame
from math import *
import os
from settings import *

class character(pygame.sprite.Sprite):
    def __init__(self,x,y,screen):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'My name'
        self.screen = screen
        self.image = pygame.Surface((30,30))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)
        self.vx = 0
        self.vy = 0
        self.speed = 1
        self.dmg = 0.1
        self.health = 100
        self.isWalking = False
        self.isFalling = False
        self.airBorne = False
        self.isDefending = False
        self.facingLeft = False
        self.facingRight = True
        self.walkCount = 0
        self.isAttacking = False
        self.isAttackingJ = False
        self.isAttackingSJ = False
        self.isAttackingWJ = False
        self.isAttackingU = False
        self.isAttackingI = False
        self.isAttackingWI = False
        self.attackCountJ = 0
        self.jClickCount = 0
        self.jClickCountMax = 0
        self.attackCountSJ = 0
        self.attackCountWJ = 0
        self.attackCountU = 0
        self.attackCountI = 0
        self.attackCountWI = 0
        self.isHit = False
        self.defendRatio = 0.5
        self.attackMove = 0
        self.attackMoveY = 0
        self.paused = False
        self.pauseCount = 0
        self.dead = False
        self.dyingCount = 0
        self.energy = 0
        self.fallingCount = 0
        self.isKnockedBack = False
        self.projInAir = False
        self.hitUlt = False
        self.videoPlayed = False
        self.ultPause = False
        self.ultPauseCount = 0
        self.inDefence = False
        self.inJump = False
        self.defenceCount = 0
        self.isJumpingDown = False
        self.soundCount = 0
        self.flyingAway = False
        self.isAttackingSI = False

    #def __eq__(self, other):
    #    return isinstance(self,other) and self.name == other.name

    def update(self):
        pass

    def updateWalking(self, keys, leftKey, rightKey):
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

    def updateJumping(self,keys,jumpKey,downKey):
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

    def updateDefending(self,keys,defendKey):
        if self.vx == 0 and self.vy == 0 and not (self.isAttacking or self.isHit) and keys[defendKey]:
            self.isDefending = True
        else:
            self.isDefending = False

    def ifStanding(self):
        if not(self.isWalking or self.isDefending or self.isAttacking or self.isHit):
            if self.facingRight:
                self.image = self.rightStanding
            else:
                self.image = self.leftStanding

    def ifWalking(self):
        fpsPerSprite = FPS // len(self.walkRight) + 1
        if self.walkCount + 1 >= FPS:
            self.walkCount = 0
        if self.isWalking:
            if self.vx > 0:
                self.image = self.walkRight[self.walkCount//fpsPerSprite]
                self.walkCount += 1
            else:
                self.image = self.walkLeft[self.walkCount//fpsPerSprite]
                self.walkCount += 1

    def ifDefending(self):
        if self.isDefending:
            if self.facingRight:
                self.image = self.rightDefense
            else:
                self.image = self.leftDefense
        elif not(self.isAttacking or self.isHit or self.isWalking):
            if self.facingRight:
                self.image = self.rightStanding
            else:
                self.image = self.leftStanding

    def ifHit(self):
        if self.isHit:
            self.vx = 0
            if self.energy < 150:
                self.energy += 0.2
            self.isAttacking = False
            if self.isDefending == False:
                if self.facingRight:
                    self.image = self.rightHit
                else:
                    self.image = self.leftHit
                self.paused = True

    '''def attackMotion(self, move, left, right, count, timeRatio, newDmg, newAttackMove):
        print('firstcount:',count)
        fpsPerSprite = (FPS // len(right) + 1)*timeRatio
        if move:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = newDmg
            self.attackMove = newAttackMove
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = right[count//fpsPerSprite]
                count += 1
                print('count:',count)
            else:
                self.rect.x -= self.attackMove
                self.image = left[count//fpsPerSprite]
                count += 1
        else:
            self.dmg = DMG
            self.attackMove = ATTACKMOVE
        if count//fpsPerSprite >= len(right):
            count = 0
            move = False
            isAttacking = False
        print('recount:',count)'''

    def ifAttackingJ(self):
        fpsPerSprite = (FPS // len(self.rightAttackJ) + 1)//2
        if not(self.isAttackingSJ or self.isAttackingWJ or self.isAttackingU or self.isAttackingI) and self.isAttackingJ:
            self.isAttacking = True
            self.isDefending = False
            self.energy += 0.1
            if self.facingRight:
                self.rect.x += 1
                self.image = self.rightAttackJ[self.attackCountJ//fpsPerSprite]
                self.attackCountJ += 1
            else:
                self.rect.x -= 1
                self.image = self.leftAttackJ[self.attackCountJ//fpsPerSprite]
                self.attackCountJ += 1
        if self.attackCountJ//fpsPerSprite >= len(self.rightAttackJ):
            self.attackCountJ = 0
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

    def ifAttackingWJ(self):
        fpsPerSprite = (FPS // len(self.rightAttackWJ) + 1)//2
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
        if self.attackCountWJ//fpsPerSprite >= len(self.rightAttackWJ):
            self.attackCountWJ = 0
            self.isAttackingWJ = False
            self.isAttacking = False
            self.paused = True
            self.dmg = DMG
            self.attackMove = 0
            self.attackMoveY = 0

    def ifAttackingU(self):
        fpsPerSprite = (FPS // len(self.rightAttackU) + 1)//2
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingWJ or self.isAttackingI or self.isAttackingWI) and self.isAttackingU:
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0
            self.attackMove = 0
            self.attackMoveY = 0
            self.energy += 0.1
            if self.facingRight:
                self.rect.x += self.attackMove
                self.image = self.rightAttackU[self.attackCountU//fpsPerSprite]
                self.attackCountU += 1
            else:
                self.rect.x -= self.attackMove
                self.image = self.leftAttackU[self.attackCountU//fpsPerSprite]
                self.attackCountU += 1
            if self.attackCountU == 2:
                self.projInAir = True
        if self.attackCountU//fpsPerSprite >= len(self.rightAttackU):
            self.attackCountU = 0
            self.isAttackingU = False
            self.isAttacking = False
            self.paused = True
            self.projInAir = False
            self.dmg = DMG
            self.attackMove = 0
            self.attackMoveY = 0

    def ifAttackingI(self):
        #self.attackMotion(self.isAttackingI, self.leftAttackI, self.rightAttackI, self.attackCountI, 2, 0.5, 2)
        fpsPerSprite = (FPS // len(self.rightAttackI) + 1) * 2
        if not(self.isAttackingJ or self.isAttackingSJ or self.isAttackingU or self.isAttackingWJ or self.isAttackingWI) and self.isAttackingI and self.energy >= 50:
            if self.attackCountI == 0:
                self.ultPause = True
            self.isAttacking = True
            self.isDefending = False
            self.dmg = 0.2
            self.attackMove = 2
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

    def ifAttacking(self):
        if self.isAttacking == False:
            self.isAttackingI = False
            self.isAttackingJ = False

    def updateDead(self):
        if self.health <= 0:
            self.dead = True

    def ifDead(self):
        self.dyingCount += 1
        if self.dyingCount <= DYINGCOUNT:
            if self.facingRight:
                self.vx = -1
                self.image = self.rightDying
            else:
                self.vx = 1
                self.image = self.leftDying
        else:
            self.vx = 0
            if self.facingRight:
                self.image = self.rightDead
            else:
                self.image = self.leftDead

    def updateEnergy(self):
        if self.energy >= 150:
            self.energy = 150

    def knockBack(self):
        self.paused = True
        if self.facingLeft:
            self.vx = 2
            self.image = self.leftHit
            self.fallingCount += 1
            self.health -= 0.2
        else:
            self.vx = -2
            self.image = self.rightHit
            self.fallingCount += 1
            self.health -= 0.2
        if self.fallingCount >= FPS//2:
            self.vx = 0
            self.fallingCount = 0
            self.paused = False
            self.isKnockedBack = False

    def ifJumpingDown(self, platList):
        if self.isJumpingDown:
            for p in platList:
                if p.rect.y > self.rect.y + self.image.get_height() + 51:
                    self.rect.y += p.height
                    break
            self.isJumpingDown = False

    def ifFlyingAway(self):
        if self.flyingAway:
            self.isHit = True
            if self.facingRight:
                dx = 5
            else:
                dx = -5
            self.rect.x += dx
            if self.rect.x <= 0 or self.rect.x + self.width >= WIDTH:
                self.health -= 10
                self.isHit = False
                self.flyingAway = False

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
        self.rightAttackU = getSprites(path + os.sep + 'Attacks' + os.sep + 'attackU')
        self.leftAttackU = getFlippedSprites(self.rightAttackU)
        self.rightAttackI = getSprites(path + os.sep + 'Attacks' + os.sep + 'attackI')
        self.leftAttackI = getFlippedSprites(self.rightAttackI)
        self.rightDying = pygame.image.load(path + os.sep + 'dying.png')
        self.leftDying = getFlippedSprites(self.rightDying)
        self.rightDead = pygame.image.load(path + os.sep + 'dead.png')
        self.leftDead = getFlippedSprites(self.rightDead)
        self.iconI = pygame.image.load(path + os.sep + 'iconI.png')
        self.iconI = pygame.transform.scale(self.iconI, (WIDTH, HEIGHT))
        self.ultSound = pygame.mixer.Sound(path + os.sep + 'ultSound.wav')
        self.ultSound.set_volume(0.5)

# gets sprites from a given folder
def getSprites(path):
    lst = []
    result = []
    for filename in os.listdir(path):
        lst += [filename]
        #lst += [pygame.image.load(path + os.sep + filename)]
    lst = sorted(lst,key=lambda x: int(os.path.splitext(x)[0]))
    for filename in lst:
        result += [pygame.image.load(path + os.sep + filename)]
    return result

def getFlippedSprites(lst):
    if not isinstance(lst, list):
        return pygame.transform.flip(lst, True, False)
    result = []
    for image in lst:
        result += [pygame.transform.flip(image, True, False)]
    return result

def getScaledSprites(path):
    lst = []
    for filename in os.listdir(path):
        lst += [pygame.transform.scale(pygame.image.load(path + os.sep + filename), (62,91))]
    return lst

class Platform(pygame.sprite.Sprite):
    def __init__(self,screen,image,pos,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = image
        self.image = pygame.transform.scale(self.image, (w,h))
        #self.image = pygame.Surface((w,h))
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.width, self.height = self.image.get_width(), self.image.get_height()

    def draw(self):
        self.screen.blit(self.image,(self.rect.x,self.rect.y))

class DoffyString(pygame.sprite.Sprite):
    def __init__(self,screen,pos,len,color):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.startX, self.startY = pos
        self.len = len
        self.angle = 0
        self.color = color
        self.neg = 1
        self.endX = self.startX + self.len * cos(self.angle) * self.neg
        self.endY = self.startY - self.len * sin(self.angle) * self.neg
        self.dx, self.dy = 0, 0
        self.width = 2
        self.dmg = 0.2

    def update(self):
        self.startX += self.dx
        self.startY += self.dy
        self.endX = self.startX + self.len * cos(self.angle) * self.neg
        self.endY = self.startY - self.len * sin(self.angle) * self.neg

    def draw(self):
        self.image = pygame.draw.line(self.screen, self.color, (self.startX, self.startY), (self.endX, self.endY), self.width)

class Projectile(pygame.sprite.Sprite):
    def __init__(self,screen,pos,image,dmg):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'bulletString'
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.dmg = dmg
        self.dx, self.dy = 0,0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

class EnelDragon(pygame.sprite.Sprite):
    def __init__(self,screen,pos,image,dmg):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'EnelDragon'
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.dmg = dmg
        self.dx, self.dy = 0,0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

