import random
import pygame
import math
from sys import exit

pygame.init()

screen_width = 1600
screen_height = 900

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

all_sprites = pygame.sprite.Group()
non_player_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
exps = pygame.sprite.Group()
enemies = pygame.sprite.Group()
weapons = pygame.sprite.Group()
equipments = pygame.sprite.Group()
font = pygame.font.SysFont('pixel_font.otf', 30, bold=True)
sfont = pygame.font.SysFont('pixel_font.otf', 10, bold=True)
time_text = font.render("00:00", True, RED)
time_text_rect = time_text.get_rect(center=(screen_width/2 + 10,100))
bg = pygame.image.load("BG_gameplay.png")
bg = pygame.transform.scale(bg, (screen_width,screen_height))
pause_icon = pygame.image.load("pause-icon.png")
pause_icon = pygame.transform.scale(pause_icon,(50,50))
tier1_enemy_image = pygame.image.load("Blightbun.PNG")
tier1_enemy_image = pygame.transform.scale(tier1_enemy_image,(100,100))
tier1_enemy_image_hit = pygame.image.load("W_Blightbun.png")
tier1_enemy_image_hit = pygame.transform.scale(tier1_enemy_image_hit,(100,100))
hit_Tuta = pygame.image.load("R_Tuta_.png")
hit_Tuta = pygame.transform.scale(hit_Tuta,(150,150))
Tuta = pygame.image.load("Tuta.png")
Tuta = pygame.transform.scale(Tuta,(150,150))
overhead = pygame.Surface((screen_width,150))
exp_bar = pygame.Surface((screen_width-400,20))
exp_bar_rect = exp_bar.get_rect(center = (screen_width//2,40))
MightCarrot_image = pygame.image.load("MightCarrot.png")
MightCarrot_image = pygame.transform.scale(MightCarrot_image,(30,30))
RedMushroom_image = pygame.image.load("RedMushroom.png")
RedMushroom_image = pygame.transform.scale(RedMushroom_image,(30,30))
QuickCarrot_image = pygame.image.load("QuickCarrot.png")
QuickCarrot_image = pygame.transform.scale(QuickCarrot_image,(30,30))
HardCarrot_image = pygame.image.load("HardCarrot.png")
HardCarrot_image = pygame.transform.scale(HardCarrot_image,(30,30))
CarrotBasket_image = pygame.image.load("CarrotBasket.png")
CarrotBasket_image = pygame.transform.scale(CarrotBasket_image,(30,30))
LightCarrot_image = pygame.image.load("LightCarrot.png")
LightCarrot_image = pygame.transform.scale(LightCarrot_image,(30,30))
HealthCarrot_image = pygame.image.load("HealthCarrot.png")
HealthCarrot_image = pygame.transform.scale(HealthCarrot_image,(30,30))
TastyCarrot_image = pygame.image.load("TastyCarrot.png")
TastyCarrot_image = pygame.transform.scale(TastyCarrot_image,(30,30))
kill_count = 0
minutes = 0
seconds = 0



def main(start_time):
    screen = pygame.display.set_mode((screen_width,screen_height))
    global minutes, seconds, kill_count
    clock = pygame.time.Clock()
    player = Player("Tuta")
    lv_box = LVBox(player)

    all_sprites.add(player)

    def main_logic():
        global seconds, kill_count
        running = True
        pause = False
        
        time_paused = 0
        pause_start_time = 0

        #starting weapon
        if player.name == "Tuta":
            force_field = Force_Field(player.rect.centerx,player.rect.centery,player,start_time)
            weapons.add(force_field)
            player.weapons.append(force_field)

        #background pos
        bg_x = 0
        bg_y = 0

        while running:
            current_time = pygame.time.get_ticks() - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.go_left()
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.go_right()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.go_up()
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        player.go_down()

                    if event.key == pygame.K_ESCAPE and not pause:
                        pause_start_time = pygame.time.get_ticks()
                        running = paused()
                        time_paused += pygame.time.get_ticks() - pause_start_time                 

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a :
                        if player.changex < 0:
                            player.stopx()
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if player.changex > 0:
                            player.stopx()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if player.changey < 0 :
                            player.stopy()
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if player.changey > 0:
                            player.stopy()

                

            # Update background position based on player's movement
            bg_x -= player.changex
            bg_y -= player.changey

            # Reset the background position to create a continuous scrolling effect
            if bg_x <= -screen_width:
                bg_x = 0
            if bg_y <= -screen_height:
                bg_y = 0
            if bg_x >= screen_width:
                bg_x = 0
            if bg_y >= screen_height:
                bg_y = 0

            # Draw the background
            screen.blit(bg, (bg_x, bg_y))
            screen.blit(bg, (bg_x - screen_width, bg_y))
            screen.blit(bg, (bg_x + screen_width, bg_y))
            screen.blit(bg, (bg_x, bg_y - screen_height))
            screen.blit(bg, (bg_x, bg_y + screen_height))
            screen.blit(bg, (bg_x - screen_width, bg_y - screen_height))
            screen.blit(bg, (bg_x + screen_width, bg_y - screen_height))
            screen.blit(bg, (bg_x - screen_width, bg_y + screen_height))
            screen.blit(bg, (bg_x + screen_width, bg_y + screen_height))

            #game times
            minutes, seconds = game_time(time_paused,current_time)
            if minutes == 5:
                running = False

            #enemies spawn
            if minutes <= 1:
                while len(enemies) <= 50:
                    enemy = tier_1()
                    enemy.rect.centerx = random.randrange(-300, screen_width + 300)
                    enemy.rect.centery = random.randrange(-300, screen_height + 300)
                    if enemy.rect.centerx not in range(-100,screen_width+100) or enemy.rect.centery not in range(-100,screen_height+100):
                        enemies.add(enemy)
                        non_player_sprites.add(enemy)
                        all_sprites.add(enemy)
            elif 2 > minutes >= 1:
                while len(enemies) <= 80:
                    enemy = tier_1()
                    enemy.rect.centerx = random.randrange(-300, screen_width + 300)
                    enemy.rect.centery = random.randrange(-300, screen_height + 300)
                    if enemy.rect.centerx not in range(-100,screen_width+100) or enemy.rect.centery not in range(-100,screen_height+100):
                        enemies.add(enemy)
                        non_player_sprites.add(enemy)
                        all_sprites.add(enemy)
            elif 3 > minutes >= 2:
                while len(enemies) <= 110:
                    enemy = tier_1()
                    enemy.rect.centerx = random.randrange(-300, screen_width + 300)
                    enemy.rect.centery = random.randrange(-300, screen_height + 300)
                    if enemy.rect.centerx not in range(-100,screen_width+100) or enemy.rect.centery not in range(-100,screen_height+100):
                        enemies.add(enemy)
                        non_player_sprites.add(enemy)
                        all_sprites.add(enemy)
            elif 4> minutes >= 3:
                while len(enemies) <= 140:
                    enemy = tier_1()
                    enemy.rect.centerx = random.randrange(-300, screen_width + 300)
                    enemy.rect.centery = random.randrange(-300, screen_height + 300)
                    if enemy.rect.centerx not in range(-100,screen_width+100) or enemy.rect.centery not in range(-100,screen_height+100):
                        enemies.add(enemy)
                        non_player_sprites.add(enemy)
                        all_sprites.add(enemy)
            elif 5> minutes >= 4:
                while len(enemies) <= 250:
                    enemy = tier_1()
                    enemy.rect.centerx = random.randrange(-300, screen_width + 300)
                    enemy.rect.centery = random.randrange(-300, screen_height + 300)
                    if enemy.rect.centerx not in range(-100,screen_width+100) or enemy.rect.centery not in range(-100,screen_height+100):
                        enemies.add(enemy)
                        non_player_sprites.add(enemy)
                        all_sprites.add(enemy)

            #enemy and enemy collision           
            for enemy in enemies:
                enemy_and_enemy_collision(enemy, enemies)
        
            #enemy and player collision
            enemy_and_player_collision(player,enemies)

            #enemy and bullet collision
            for enemy in enemies:
                for bullet in bullets:
                    enemy_and_bullet_collision(enemy, bullet)

            #enemy and FF collision + damage inflict
            if current_time - force_field.last_shot >= force_field.cooldown:
                enemy_and_force_field_collision(force_field,enemies)
                force_field.last_shot = current_time
                
            #world shift
            world_shift()

            #move towards player
            towards_player()

            #force field update
            if force_field in player.weapons:
                force_field.update(player.rect.centerx,player.rect.centery,player)

            #draw
            clock.tick(60)
            weapons.draw(screen)
            all_sprites.draw(screen)
            all_sprites.update(player)

            #overhead black bar
            overhead.fill(BLACK)
            screen.blit(overhead,(0,0))
            
            #exp bar
            if player.EXP != 0:
                exp_bar = pygame.Surface(((player.EXP/player.EXPthreshold)*1200,20))
                exp_bar.fill(BLUE) 
                screen.blit(exp_bar,exp_bar_rect)

            #LV text
            lv_text = font.render(f"LV {player.LV}", True, WHITE)
            screen.blit(lv_text,(exp_bar_rect.x-100,exp_bar_rect.y-7+10))

            #kill count text
            kill_text = font.render(f"Kill: {kill_count}", True, WHITE)
            screen.blit(kill_text,(exp_bar_rect.x-100,exp_bar_rect.y+57))

            #player killed
            if player.HP <= 0:
                running = False

            #time
            game_time(time_paused,current_time)

            #lvup box
            if player.LVUP == True:
                pause_start_time = pygame.time.get_ticks()
                screen.blit(lv_box.image, (screen_width // 2 - lv_box.rect.width // 2, screen_height // 2 - lv_box.rect.height // 2 +50))
                lv_box.random_equip()
                equip1image = pygame.transform.scale(lv_box.equip1.image,(100,100))
                equip2image = pygame.transform.scale(lv_box.equip2.image,(100,100))
                equip3image = pygame.transform.scale(lv_box.equip3.image,(100,100))
                eq1_text = font.render(f"{lv_box.equip1.name}", True, WHITE)
                eq2_text = font.render(f"{lv_box.equip2.name}", True, WHITE)
                eq3_text = font.render(f"{lv_box.equip3.name}", True, WHITE)
                screen.blit(equip1image, (lv_box.rect.x+20, lv_box.rect.centery - 200))
                screen.blit(equip2image, (lv_box.rect.x+20, lv_box.rect.centery))
                screen.blit(equip3image, (lv_box.rect.x+20, lv_box.rect.centery + 200))
                screen.blit(eq1_text, (lv_box.rect.x+200, lv_box.rect.centery - 200))
                screen.blit(eq2_text, (lv_box.rect.x+200, lv_box.rect.centery))
                screen.blit(eq3_text, (lv_box.rect.x+200, lv_box.rect.centery + 200))
                running = paused()
                lv_box.update(player)
                time_paused += pygame.time.get_ticks() - pause_start_time 
            
            #equipments show
            changex = 0
            for equipment in player.equipments:
                eq_text = sfont.render(f"{equipment.LV}", True, WHITE)
                screen.blit(equipment.image,(1300+changex,100))
                screen.blit(eq_text,(1307+changex,130))
                changex += 50

            #update display
            pygame.display.flip()
        return kill_count,minutes,seconds,player.LV

        

    def world_shift():
            #right
            if player.rect.centerx > screen_width//2 :
                diff = player.rect.centerx - screen_width//2
                player.rect.centerx = screen_width//2
                for sprite in non_player_sprites:
                    sprite.rect.centerx += -diff

            #left
            if player.rect.centerx < screen_width//2 :
                diff = (screen_width//2 ) - player.rect.centerx
                player.rect.centerx = screen_width//2 
                for sprite in non_player_sprites:
                    sprite.rect.centerx += diff

            #up
            if player.rect.centery < screen_height//2:
                diff = screen_height//2 - player.rect.centery
                player.rect.centery = screen_height//2
                for sprite in non_player_sprites:
                    sprite.rect.centery += diff

            #down
            if player.rect.centery > screen_height//2:
                diff = player.rect.centery - screen_height//2
                player.rect.centery = screen_height//2
                for sprite in non_player_sprites:
                    sprite.rect.centery += -diff

    def towards_player():
        for enemy in enemies:
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            distance = math.sqrt(dx**2 + dy**2)

            if distance != 0:
                dx /= distance
                dy /= distance

            enemy.rect.centerx += dx * enemy.MVMSPD 
            enemy.rect.centery += dy * enemy.MVMSPD 

    def enemy_and_enemy_collision(enemy, enemies):
        enemy_hit_list = pygame.sprite.spritecollide(enemy, enemies, False, pygame.sprite.collide_mask)
        for enemy2 in enemy_hit_list:

            dx = enemy2.rect.centerx - enemy.rect.centerx
            dy = enemy2.rect.centery - enemy.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                nx = dx / distance
                ny = dy / distance

                overlap = 2 * enemy.image.get_width() - distance

                enemy.rect.x -= nx * overlap /16
                enemy.rect.y -= ny * overlap /16
                enemy2.rect.x += nx * overlap /16
                enemy2.rect.y += ny * overlap /16

    def enemy_and_player_collision(player, enemies):
        enemy_hit_list = pygame.sprite.spritecollide(player,enemies,False,pygame.sprite.collide_mask)
        for enemy in enemy_hit_list:
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                nx = dx / distance
                ny = dy / distance

                overlap = 2 * player.image.get_width() - distance

                enemy.rect.x -= nx * overlap /8
                enemy.rect.y -= ny * overlap /8
            if player.DEF < enemy.ATK:
                player.HP -= (enemy.ATK - player.DEF)
            else:
                player.HP -= 1
            player.hit_flash()
            print(player.HP)
    
    def enemy_and_bullet_collision(enemy, bullet):
        dx = bullet.rect.x - enemy.rect.x
        dy = bullet.rect.y - enemy.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        if pygame.sprite.collide_rect(bullet, enemy) == True:
            if distance != 0:
                nx = dx / distance
                ny = dy / distance

                overlap = 2 * bullet.image.get_width() - distance

                enemy.rect.x += nx * overlap 
                enemy.rect.y += ny * overlap 

    def enemy_and_force_field_collision(force_field, enemies):   
        enemy_hit_list = pygame.sprite.spritecollide(force_field, enemies, False, pygame.sprite.collide_mask)
        for enemy in enemy_hit_list:
            dx = force_field.rect.centerx - enemy.rect.centerx
            dy = force_field.rect.centery - enemy.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                nx = dx / distance
                ny = dy / distance

                overlap = 2 * enemy.image.get_width() - distance

                enemy.rect.centerx -= nx * overlap /16
                enemy.rect.centery -= ny * overlap /16
            enemy.HP -= (player.ATK*force_field.ATK) - enemy.DEF
            damage = int((player.ATK*force_field.ATK) - enemy.DEF)
            enemy.hit_flash()
            damage_text = DamageText(str(damage), enemy.rect.centerx,enemy.rect.top)
            all_sprites.add(damage_text)
            non_player_sprites.add(damage_text)
            
    def game_time(time_lag,real_current_time):
        current_time = ((real_current_time-time_lag) // 1000)
        minutes = current_time // 60
        seconds = current_time % 60
        time_text = font.render(f"{minutes:02}:{seconds:02}", True, RED)
        screen.blit(time_text, time_text_rect)
        return minutes,seconds

    def paused():
        pause = True
        while pause:
            screen.blit(pause_icon,(screen_width-100,200))
            pygame.display.update()
            player.stopx()
            player.stopy()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = True
                        pause = False
                        return running

                    running, pause = equip_add(event)
                    return running
                if event.type == pygame.QUIT:
                    running = False
                    return running

    def equip_add(event):
        if player.LVUP == True:
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                if event.key == pygame.K_1:
                    if lv_box.equip1 not in player.equipments:
                        player.equipments.append(lv_box.equip1)
                        print(lv_box.equip1.LV)
                    else:
                        lv_box.equip1.LV += 1
                        print(lv_box.equip1,lv_box.equip1.LV)
                    pause = False
                    running = True
                    print(player.equipments)
                    equipments.add(lv_box.equip1)
                    lv_box.equip1.update(player)
                elif event.key == pygame.K_2:
                    if lv_box.equip2 not in player.equipments:
                        player.equipments.append(lv_box.equip2)
                        print(lv_box.equip2,lv_box.equip2.LV)
                    else:
                        lv_box.equip2.LV += 1
                        print(lv_box.equip2,lv_box.equip2.LV)
                    pause = False
                    running = True
                    print(player.equipments)
                    equipments.add(lv_box.equip2)
                    lv_box.equip2.update(player)
                elif event.key == pygame.K_3:
                    if lv_box.equip3 not in player.equipments:
                        player.equipments.append(lv_box.equip3)
                        print(lv_box.equip3,lv_box.equip3.LV)
                    else:
                        lv_box.equip3.LV += 1
                        print(lv_box.equip3,lv_box.equip3.LV)
                    pause = False
                    running = True
                    print(player.equipments)
                    equipments.add(lv_box.equip3)
                    lv_box.equip3.update(player)

                player.LVUP = False
            pause = False 
            running = True
            return running,pause
        return True, True

    #main logic run
    kill_counts,minutes,seconds,lvl = main_logic()
    all_sprites.empty()
    non_player_sprites.empty()
    bullets.empty()
    exps.empty()
    enemies.empty()
    weapons.empty()
    equipments.empty()
    kill_count = 0
    return kill_counts,minutes,seconds,lvl

class DamageText(pygame.sprite.Sprite):
    def __init__(self, text, x,y, duration=300):
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        self.duration = duration  # Duration in milliseconds
        self.time_created = pygame.time.get_ticks()  # Timestamp of when the text was created
        self.image = font.render(self.text, True, RED)
        self.rect = self.image.get_rect(center=(x,y))
    
    def update(self,player):
        # Remove the text after the specified duration has passed
        if pygame.time.get_ticks() - self.time_created >= self.duration:
            self.kill()        

class LVBox(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.equipment_list = [MightCarrot(),RedMushroom(),QuickCarrot(),HardCarrot(),CarrotBasket(),LightCarrot(),HealthCarrot(),TastyCarrot()]
        self.image = pygame.Surface((1000,600))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center = (screen_width//2,screen_height//2))

    def random_equip(self):
        self.equip1 = random.choice(self.equipment_list)
        self.equipment_list.remove(self.equip1)
        self.equip2 = random.choice(self.equipment_list)
        self.equipment_list.remove(self.equip2)
        self.equip3 = random.choice(self.equipment_list)
        self.equipment_list.remove(self.equip3)

        self.equipment_list.append(self.equip1)
        self.equipment_list.append(self.equip2)    
        self.equipment_list.append(self.equip3)

    def update(self,player):
        if len(player.equipments) == 6:
            self.equipment_list = player.equipments

class Equipment(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

class MightCarrot(Equipment):
    def __init__(self):
        super().__init__()
        self.LV = 1
        self.name = "MightCarrot"
        self.image = MightCarrot_image
        self.rect = self.image.get_rect()

    def update(self,player):
        self.plus = player.ATK*1.2
        if self in player.equipments:
            player.ATK = self.plus

class RedMushroom(Equipment):
    def __init__(self):
        super().__init__()
        self.LV = 1
        self.name = "RedMushroom"
        self.image = RedMushroom_image
        self.rect = self.image.get_rect()

    def update(self,player):
        self.plus = player.AREA+(0.05*self.LV)
        if self in player.equipments:
            player.AREA = self.plus

class QuickCarrot(Equipment):
    def __init__(self):
        super().__init__()
        self.LV = 1
        self.name = "QuickCarrot"
        self.image = QuickCarrot_image
        self.rect = self.image.get_rect()

    def update(self,player):
        self.plus = player.PSPD*1.1*self.LV
        if self in player.equipments:
            player.PSPD = self.plus

class HardCarrot(Equipment):
    def __init__(self):
        super().__init__()
        self.LV = 1
        self.name = "HardCarrot"
        self.image = HardCarrot_image
        self.rect = self.image.get_rect()

    def update(self,player):
        self.plus = player.DEF*1.1*self.LV
        if self in player.equipments:
            player.DEF = self.plus

class CarrotBasket(Equipment):
    def __init__(self):
        super().__init__()
        self.LV = 1
        self.name = "CarrotBasket"
        self.image = CarrotBasket_image
        self.rect = self.image.get_rect()

    def update(self,player):
        self.plus = player.ATKSPD*1.1*self.LV
        if self in player.equipments:
            player.ATKSPD = self.plus

class LightCarrot(Equipment):
    def __init__(self):
        super().__init__()
        self.LV = 1
        self.name = "LightCarrot"
        self.image = LightCarrot_image
        self.rect = self.image.get_rect()

    def update(self,player):
        self.plus = player.MVMSPD + self.LV
        if self in player.equipments:
            player.MVMSPD = self.plus

class HealthCarrot(Equipment):
    def __init__(self):
        super().__init__()
        self.LV = 1
        self.name = "HealthCarrot"
        self.image = HealthCarrot_image
        self.rect = self.image.get_rect()

    def update(self,player):
        self.plus = player.HP*1.2*self.LV
        if self in player.equipments:
            player.MAXHP = self.plus

class TastyCarrot(Equipment):
    def __init__(self):
        super().__init__()
        self.LV = 1
        self.REGEN = 0
        self.name = "TastyCarrot"
        self.image = TastyCarrot_image
        self.rect = self.image.get_rect()

    def update(self,player):
        self.REGEN = self.LV *0.005 *player.MAXHP
        if self in player.equipments:
            start_regen = pygame.time.get_ticks()
            if pygame.time.get_ticks() - start_regen == 1000:
                player.HP += self.REGEN

class Player(pygame.sprite.Sprite):
    #base chara
    def __init__(self,name):
        super().__init__()
        self.name = name
        if self.name == "Tuta":
            self.image = Tuta
            
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center= (screen_width//2,screen_height//2)) 

        #movement
        self.changex = 0
        self.changey = 0

        #basic stats (subject to change)
        self.MAXHP = 100
        self.HP = self.MAXHP
        self.ATK = 10
        self.DEF = 5
        self.ATKSPD = 1
        self.MVMSPD = 1
        self.LV = 1
        self.AREA = 1
        self.PSPD = 1
        self.EXPthreshold = (((self.LV**2)-self.LV)/2) + 5
        self.EXP = 0

        #attack related
        self.cooldown = self.ATKSPD * 500
        self.last_shot = pygame.time.get_ticks()

        #list
        self.weapons = []
        self.equipments = []

        #misc
        self.LVUP = False
        self.flash = False
        self.kill_count = 0

    def update(self,player):
        #collecting exps
        exp_drops_get = pygame.sprite.spritecollide(self, exps, True)
        for exp in exp_drops_get:
            self.EXP += exp.EXP

        #level up
        if self.EXP >= self.EXPthreshold:
            self.LV += 1
            self.EXPthreshold = (((self.LV**2)-self.LV)/2) + 5
            self.EXP = 0
            print("LV UP!")
            self.LVUP = True

        #left right
        self.rect.x += self.changex

        #up down
        self.rect.y += self.changey

        #hit flash
        if self.flash and pygame.time.get_ticks() -self.hit_time >= 150:
            self.image = Tuta
            self.flash = False

    def attack(self,player):
        for weapon in self.weapons:
            weapon.attack(player)
        
    def hit_flash(self):
        self.hit_time = pygame.time.get_ticks()
        self.image = hit_Tuta
        self.flash = True

    #movement
    def go_left(self):
        self.changex = -(2+self.MVMSPD)
    
    def go_right(self):
        self.changex = (2+self.MVMSPD)

    def go_up(self):
        self.changey = -(2+self.MVMSPD)
    
    def go_down(self):
        self.changey = (2+self.MVMSPD)

    def stopx(self):
        self.changex = 0

    def stopy(self):
        self.changey = 0   

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.pierce = 2

        if direction == "up":
            self.vel = (0, -5)
        elif direction == "down":
            self.vel = (0, 5)
        elif direction == "left":
            self.vel = (-5,0)
        elif direction == "right":
            self.vel = (5,0)
        elif direction == "topright":
            self.vel = (3,-3)
        elif direction == "topleft":
            self.vel = (-3,-3)
        elif direction == "botright":
            self.vel = (3,3)
        elif direction == "botleft":
            self.vel = (-3,3)
    
    def update(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

        #collision
        enemy_hit_list = pygame.sprite.spritecollide(self, enemies, False)
        for hit_enemy in enemy_hit_list:
            hit_enemy.HP -= Player().ATK

        #pierce
        if self.pierce <= 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def reset_pos_too_up(self):
        self.rect.centery = screen_height + 100
        self.rect.centerx = random.randrange(-100,screen_width+100)
    
    def reset_pos_too_down(self):
        self.rect.centery = -100
        self.rect.centerx = random.randrange(-100,screen_width+100)

    def reset_pos_too_right(self):
        self.rect.centery = random.randrange(-100,screen_height+100)
        self.rect.centerx = -100

    def reset_pos_too_left(self):
        self.rect.centery = random.randrange(-100,screen_height+100)
        self.rect.centerx = screen_width + 100

class exp_drops(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

class tier_1_exp(exp_drops):
    def __init__(self):
        super().__init__()
        self.EXP = 1
        self.image = pygame.Surface((3,3))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

class tier_1(Enemy):
    def __init__(self):
        super().__init__()
        self.image = tier1_enemy_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.flash = False

        #stats
        self.HP = 50
        self.ATK = 10
        self.DEF = 5
        self.MVMSPD = 1

    def update(self,player):
        global kill_count
        bullet_hit_list = pygame.sprite.spritecollide(self, bullets, False)
        for bullet in bullet_hit_list:
            bullet.pierce -= 1

        if self.HP <= 0:
            kill_count += 1
            self.kill()
            exp = tier_1_exp()
            exp.rect.center = self.rect.center
            exps.add(exp)
            non_player_sprites.add(exp)
            all_sprites.add(exp)

        if self.flash and pygame.time.get_ticks() -self.hit_time >= 150:
            self.image = tier1_enemy_image
            self.flash = False

        if self.rect.y > screen_height + self.rect.height + 300: #too far down
            self.reset_pos_too_down()
        if self.rect.y < -(300 + self.rect.height): #too far up
            self.reset_pos_too_up()
        if self.rect.x > screen_width + self.rect.width + 300: #too far right
            self.reset_pos_too_right()
        if self.rect.x < -300 -self.rect.width: #too far left
            self.reset_pos_too_left()

    def hit_flash(self):
        self.hit_time = pygame.time.get_ticks()
        self.image = tier1_enemy_image_hit
        self.flash = True
        
class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()        

class Force_Field(Weapon):
    def __init__(self,x,y,player,start_time):
        super().__init__()
        self.ATK = 0.8
        self.LV = 1
        self.pierce = 0
        self.cooldown = 550
        self.area = 300*player.AREA
        self.last_shot = pygame.time.get_ticks() - start_time
        self.image = pygame.image.load("ForceField.PNG").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.area,self.area))
        self.rect = self.image.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self,x,y,player):
        self.area = 300*player.AREA
        self.image = pygame.transform.scale(self.image,(self.area,self.area))
        self.rect = self.image.get_rect(center=(x,y))
        self.rect.center = (x+7,y+15) # modified so it could be in center
        self.mask = pygame.mask.from_surface(self.image)

    def attack(self):
        if self not in weapons:
            weapons.add(self)       
        enemy_hit_list = pygame.sprite.spritecollide(self, enemies, False)
        for hit_enemy in enemy_hit_list:
            hit_enemy.HP -= (Player().ATK*self.ATK)


if __name__ == "__main__":
    main()