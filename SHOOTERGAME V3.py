import pygame
import os
import time
import random
from pygame import mixer

pygame.mixer.init()
pygame.font.init()

WIDTH,HEIGHT = 800,600
pygame.display.set_caption(("ALIEN WARS"))
WIN=pygame.display.set_mode((WIDTH,HEIGHT))


#PLAYER PLANES
planemultiplier =   0.81
HERO_PLANE2= pygame.image.load(os.path.join("PNG ALIEN","HEROPLANE2.png")).convert_alpha()
HERO_PLANE_WIDTH = HERO_PLANE2.get_width()*planemultiplier
HERO_PLANE_HEIGHT = HERO_PLANE2.get_height()*planemultiplier
HERO_PLANE_2A = pygame.transform.scale(HERO_PLANE2, (HERO_PLANE_WIDTH,HERO_PLANE_HEIGHT))

#ENEMY PLANES

#FLASHPLANE
flashmultiplier = 0.475
FLASHPLANE=pygame.image.load(os.path.join("PNG ALIEN","FLASHPLANE.png")).convert_alpha()
FLASHPLANE_WIDTH = FLASHPLANE.get_width()*flashmultiplier
FLASHPLANE_HEIGHT = FLASHPLANE.get_height()*flashmultiplier
FLASHPLANEA = pygame.transform.scale(FLASHPLANE, (FLASHPLANE_WIDTH,FLASHPLANE_HEIGHT))


#LASER PLANE
lasermultiplier = 0.6
LASERPLANE=pygame.image.load(os.path.join("PNG ALIEN","LASERPLANE.png")).convert_alpha()
LASERPLANE_WIDTH = LASERPLANE.get_width()*lasermultiplier
LASERPLANE_HEIGHT = LASERPLANE.get_height()*lasermultiplier
LASERPLANEA = pygame.transform.scale(LASERPLANE, (LASERPLANE_WIDTH,LASERPLANE_HEIGHT))




#SHOOTER PLANE
shootermultiplier = 0.5
SHOOTERPLANE=pygame.image.load(os.path.join("PNG ALIEN","SHOOTERPLANE.png")).convert_alpha()
SHOOTERPLANE_WIDTH = SHOOTERPLANE.get_width()*shootermultiplier
SHOOTERPLANE_HEIGHT = SHOOTERPLANE.get_height()*shootermultiplier
SHOOTERPLANEA = pygame.transform.scale(SHOOTERPLANE, (SHOOTERPLANE_WIDTH,SHOOTERPLANE_HEIGHT))


#LASERS
#PLAYER BULLET
pbmultiplier = 0.5
PLAYER_BULLET=pygame.image.load(os.path.join("PNG ALIEN","PLAYERBULLET.png")).convert_alpha()
PLAYER_BULLET_WIDTH = PLAYER_BULLET.get_width() * pbmultiplier
PLAYER_BULLET_HEIGHT = PLAYER_BULLET.get_height() * pbmultiplier
PLAYER_BULLETA = pygame.transform.scale(PLAYER_BULLET, (PLAYER_BULLET_WIDTH,PLAYER_BULLET_HEIGHT))


#SHOOTER BULLET
sbmultiplier = 0.5
SHOOTER_BULLET=pygame.image.load(os.path.join("PNG ALIEN","SHOOTERBULLET.png")).convert_alpha()
SHOOTER_BULLET_WIDTH = SHOOTER_BULLET.get_width() * sbmultiplier
SHOOTER_BULLET_HEIGHT = SHOOTER_BULLET.get_height() * sbmultiplier
SHOOTER_BULLETA = pygame.transform.scale(SHOOTER_BULLET, (SHOOTER_BULLET_WIDTH,SHOOTER_BULLET_HEIGHT))


#LASER BULLET
lbmultiplier = 0.5
LASER_BULLET=pygame.image.load(os.path.join("PNG ALIEN","LASERBULLET.png")).convert_alpha()
LASER_BULLET_WIDTH = LASER_BULLET.get_width() * lbmultiplier
LASER_BULLET_HEIGHT = LASER_BULLET.get_height() * lbmultiplier
LASER_BULLETA = pygame.transform.scale(LASER_BULLET, (LASER_BULLET_WIDTH,LASER_BULLET_HEIGHT))

#FLASH BULLET
fbmultiplier = 0.5
FLASH_BULLET=pygame.image.load(os.path.join("PNG ALIEN","FLASHBULLET.png")).convert_alpha()
FLASH_BULLET_WIDTH = FLASH_BULLET.get_width() * fbmultiplier
FLASH_BULLET_HEIGHT = FLASH_BULLET.get_height() * fbmultiplier
FLASH_BULLETA = pygame.transform.scale(FLASH_BULLET, (FLASH_BULLET_WIDTH,FLASH_BULLET_HEIGHT))

#BACKGROUND
BG = pygame.transform.scale(pygame.image.load(os.path.join("PNG ALIEN","SPACE.png")),(WIDTH,HEIGHT))
# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
    def move(self,vel):
        self.y +=vel
    def off_screen(self,height):
        return not (self.y <= height)
    def collision(self,obj):
        return collide(self,obj)


class Ship:
    COOLDOWN = 7
    def __init__(self,x,y,health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self,window):
        window.blit(self.ship_img, (self.x , self.y))
        for laser in self.lasers:
            laser.draw(window)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter >0:
            self.cool_down_counter += 1


class Player(Ship):
    def __init__(self,x,y, score = 0, health = 50):
        super().__init__(x,y,health)
        self.ship_img = HERO_PLANE_2A
        self.laser_img = PLAYER_BULLETA
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score=0

    def shoot(self):
        if self.cool_down_counter ==0:
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play()
            laser = Laser(self.x +  HERO_PLANE_2A.get_width()/2 - 4,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if  laser.collision(obj):
                        if obj.health != 0 :
                            obj.health -= 50
                            bullet_sound = mixer.Sound('hit.wav')
                            bullet_sound.play()

                        else:
                            objs.remove(obj)
                            self.score +=1
                            bullet_sound = mixer.Sound('Big.wav')
                            bullet_sound.play()

                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)


    def healthbar(self,window):
        pygame.draw.rect(window, (10,10,10), (self.x -2 ,self.y + self.ship_img.get_height() + 10,self.ship_img.get_width()+4,10))
        pygame.draw.rect(window, (100, 100, 100),(self.x, self.y + 2 + self.ship_img.get_height() + 10, self.ship_img.get_width(), 6))
        pygame.draw.rect(window, (255, 69, 0), (self.x, self.y + 2 + self.ship_img.get_height() + 10,self.ship_img.get_width() * (self.health / self.max_health), 6))

class Enemy(Ship):

    IDENTITY_MAP = {
                        "SHOOTER": (SHOOTERPLANEA,SHOOTER_BULLETA),
                        "FLASH": (FLASHPLANEA,FLASH_BULLETA),
                        "LASER": (LASERPLANEA,LASER_BULLETA)
                    }

    def __init__(self,x,y,identity,vel=0, x_diff=0 , y_diff=0 ,player_health_reduce=0,highscore=None, health = None):

        super().__init__(x,y,health)
        with open("highscore.txt",'r') as f:
            self.highscore = f.read()
            self.highscore = int(self.highscore)


        self.ship_img, self.laser_img = self.IDENTITY_MAP[identity]
        self.mask = pygame.mask.from_surface(self.ship_img)
        if identity == 'SHOOTER':
            self.x_diff=self.IDENTITY_MAP[identity][0].get_width() / 2 - 8
            self.y_diff= 55
            self.vel=2.75
            self.player_health_reduce = 5
            self.health=150
        if identity == 'FLASH':
            self.x_diff=self.IDENTITY_MAP[identity][0].get_width() / 2 - 8
            self.y_diff= 55
            self.vel=3.75
            self.player_health_reduce = 3
            self.health=100
        if identity == 'LASER':
            self.x_diff=self.IDENTITY_MAP[identity][0].get_width() / 2 - 23.5
            self.y_diff = 100
            self.vel=1.75
            self.player_health_reduce = 7
            self.health = 400


    def shoot(self):
        if self.cool_down_counter ==0:
            bullet_Sound = mixer.Sound('laser Blasts.wav')
            bullet_Sound.play()
            laser = Laser(self.x + self.x_diff,self.y + self.y_diff,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1



    def move(self):
        self.y  += self.vel


    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                if obj.health > 0:
                    #print(obj.score)
                    obj.health -= self.player_health_reduce
                    bullet_Sound = mixer.Sound('hit.wav')
                    bullet_Sound.play()
                    self.lasers.remove(laser)




                if obj.score > self.highscore:
                    print(obj.score)
                    with open("highscore.txt", "w") as f:
                        f.write(str(obj.score))





def collide(obj1, obj2):
    #difference of top left co ordintes
    diff_x  = obj2.x - obj1.x
    diff_y  = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (diff_x , diff_y)) != None #and health = 0
    """initially overlap is none . the function checks whether the overlap has occured based on the common number of pixels intersecting"""



def main():

    run= True
    FPS = 60
    level = 0
    lives = 10
    lost_count=0
    lost = False

    enemies = []
    wave_length = 1


    player_vel = 7.5
    laser_vel = 5
    player = Player(335,400)

    lost_font = pygame.font.SysFont("comicsans", 50)
    main_font = pygame.font.SysFont("comicsans", 20)
    highscore_font = pygame.font.SysFont("comicsans", 26)
    score = pygame.font.SysFont("comicsans", 25)

    clock = pygame.time.Clock()

    def redraw_window():
            WIN.blit(BG, (0,0))
            #draw text
            lives_label = main_font.render(f"LIVES : {lives}",1 ,(255,255,255))
            level_label = main_font.render(f"SCORE : {player.score}",1 ,(255,255,255))

            WIN.blit(lives_label, (10,10))
            WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))


            for enemy in enemies:
                enemy.draw(WIN)
            player.draw(WIN)
            if lost:
                lost_label = lost_font.render("YOU LOST !!", 1 ,(255,0,0))
                WIN.blit(lost_label,(WIDTH/2 - lost_label.get_width()/2,HEIGHT/2 - 100))
                with open ("highscore.txt","r") as f:
                    highscore_label=highscore_font.render(f"HIGHSCORE: {f.read()}",1,(255,255,255))
                    WIN.blit(highscore_label,(WIDTH/2 - highscore_label.get_width()/2 - 20,HEIGHT/2))

                score_lable=score.render(f"CURRENT SCORE: {player.score}",1,(255,255,255))
                WIN.blit(score_lable,(WIDTH/2 - score_lable.get_width()/2 - 10,HEIGHT/2 + 50))
            pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()

        #LOST DISPLAY
        if lives <= 0 or player.health <= 0 :
            lost = True
            lost_count +=1
        if lost:
            if lost_count >  FPS * 3:
                break
            else:
                continue

        #ENEMY SPAWN
        if len(enemies) == 0:
            level += 1
            if(not wave_length>8):
                wave_length += 1 #n of enemies
            for i in range(1,wave_length):
                IDEN = random.choice(['SHOOTER','FLASH','LASER','SHOOTER','FLASH'])
                enemy = Enemy(random.randrange(50, int(WIDTH - LASERPLANEA.get_width())), random.randrange(-700,-250), IDEN)
                enemies.append(enemy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False
        #KEY PRESSED CHECK
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  and player.x - player_vel >0:
            player.x -= player_vel*1.5
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH  :
            player.x += player_vel*1.5
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel*1.5
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 20 < HEIGHT  :
            player.y += player_vel*1.5
        if keys[pygame.K_SPACE]:
            player.shoot()



        #ENEMY MOVEMENT AND ENEMY LASER CONTROL
        for enemy in enemies[:]:
            enemy.move()

            enemy.move_lasers(laser_vel,player)
            #probability of enemy shooting plane
            if random.randrange(0,3*FPS) == 1:
                    enemy.shoot()
            if collide(enemy, player):
                player.health -= 10/FPS
                #enemies.remove(enemy)
            if enemy.y  >HEIGHT:
                lives -=1
                enemies.remove(enemy)


        #PLAYER LASER CONTROL
        player.move_lasers(-laser_vel*2.5,enemies)


def main_menu():
        title_font = pygame.font.SysFont("comicsans",35)
        run = True
        while run:
            WIN.blit(BG,(0,0))
            title_label = title_font.render("PRESS ANY KEY TO BEGIN...",1,(255,255,255))
            WIN.blit(title_label,(WIDTH/2 - title_label.get_width()/2,300))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    main()
        pygame.quit()

main_menu()
