import pygame
import math
import random
from moviepy.editor import VideoFileClip
from roguelike import main

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Project B.")

start_img = pygame.image.load('btn/start_btn.png').convert_alpha()
start_img = pygame.transform.scale(start_img, (start_img.get_size()[0],start_img.get_size()[1]))
exit_img = pygame.image.load('btn/exit_btn.png').convert_alpha()
exit_img = pygame.transform.scale(exit_img, (exit_img.get_size()[0]*2,exit_img.get_size()[1]*2))
next_img = pygame.image.load('btn/next_btn.png').convert_alpha()
next_img = pygame.transform.scale(next_img, (next_img.get_size()[0]*2,next_img.get_size()[1]*2))
back_img = pygame.image.load('btn/back_btn.png').convert_alpha()
back_img = pygame.transform.scale(back_img, (back_img.get_size()[0]*2,back_img.get_size()[1]*2))
storage_img = pygame.image.load('btn/storage_btn.png').convert_alpha()
storage_img = pygame.transform.scale(storage_img, (storage_img.get_size()[0]*2,storage_img.get_size()[1]*2))
bunx1 = pygame.image.load('btn/bunx1.png').convert_alpha()
bunx1 = pygame.transform.scale(bunx1, (bunx1.get_size()[0]*2,bunx1.get_size()[1]*2))
bunx10 = pygame.image.load('btn/bunx10.png').convert_alpha()
bunx10 = pygame.transform.scale(bunx10, (bunx10.get_size()[0]*2,bunx10.get_size()[1]*2))
cash_img = pygame.image.load('btn/cash_blank.png').convert_alpha()
cash_img = pygame.transform.scale(cash_img,(cash_img.get_size()[0]//2,cash_img.get_size()[1]//2))
money = pygame.image.load('btn/money_carrot.png').convert_alpha()
money = pygame.transform.scale(money, (WIDTH//4, HEIGHT//2))
play = pygame.image.load('btn/play_btn.png').convert_alpha()
play = pygame.transform.scale(play, (play.get_size()[0]*4 , play.get_size()[1]*4))

background = pygame.image.load("background/backgroud.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background2 = pygame.image.load("background/rate.png")
background2 = pygame.transform.scale(background2, (background2.get_size()[0]*2,background2.get_size()[1]*2))
roll_bg1 = pygame.image.load("background/origin.png")
roll_bg1 = pygame.transform.scale(roll_bg1, (WIDTH, HEIGHT))
roll_bg2 = pygame.image.load('background/tuta.png')
roll_bg2 = pygame.transform.scale(roll_bg2, (WIDTH, HEIGHT))
topup_bg = pygame.image.load('background/topup.png')
topup_bg = pygame.transform.scale(topup_bg, (WIDTH, HEIGHT))
over_bg = pygame.image.load('background/game_over.png')
over_bg = pygame.transform.scale(over_bg, (WIDTH,HEIGHT))
go_gacha_bg = pygame.image.load('background/go_gacha.png')
go_gacha_bg = pygame.transform.scale(go_gacha_bg, (WIDTH,HEIGHT))

def gacha_animation(video_path):
    clip = VideoFileClip(video_path).resize((WIDTH, HEIGHT))
    clip.preview()

music_files = {
    "main_menu": "sound/menu_bmg.ogg",
    'Gacha_Information':"sound/menu_bmg.ogg",
    "gacha_game": "sound/gacha.mp3",
    'gacha_origin': 'sound/gacha.mp3',
    'display_storage' : "sound/menu_bmg.ogg",
    'topup' : "sound/menu_bmg.ogg",
}

character_images = {
    "Pure Salt": pygame.image.load(r"crt/salt.png"),
    "Whizdy": pygame.image.load(r"crt//Whizdy.png"),
    "Marinelle": pygame.image.load(r"crt/Marinelle.png"),
    "Komomo": pygame.image.load(r"crt/Komomo.png"),
    "Baby": pygame.image.load(r"crt/Baby.png"),
    "Rocky": pygame.image.load(r"crt/Rocky.png"),
    "Carra": pygame.image.load(r"crt/Carra.png"),
    'Tuta': pygame.image.load(r'crt/Tuta.png')
}

roll_count, roll_countA = 0, 0
roll_count_origin, roll_countA_origin = 0, 0
spark_count = 0
storage = {}
last10 = []  
level_list = []
item_level = None
current_image = None
current_character_name = ""
current_page = "main_menu"
current_music = None
current_result_index = 0  
circle_center = (112*(WIDTH/800), 310*(HEIGHT/450))
circle_radius = 60*(HEIGHT/450)
circle_topup_center = (197,55)
circle_topup_radius = 15
topup_rect = pygame.Rect(circle_topup_center[0] - circle_topup_radius, circle_topup_center[1] - circle_topup_radius, circle_topup_radius*2, circle_topup_radius*2)
invisible_rect = pygame.Rect(WIDTH/(21.621), HEIGHT/(3.4615), 185*(WIDTH/800), 38*(HEIGHT/450))
bunbun_gem = 0
scroll_offset = 0
page_stack = []
input_text = ""
input_box = pygame.Rect(160, 245, 800, 75)
active = False
typing = False
code = None
enter_rect = pygame.Rect(980, 245, 450, 80)
sell_rect = pygame.Rect(150, 355, 530, 425)
baby_rect = pygame.Rect(900, 355, 530, 425)
skip_rect = pygame.Rect(1350, 30, 400, 100)
back_menu_rect = pygame.Rect(1250, 810, 800, 800)
kill_count = 0
playtime = 0
reward = 0
lvl = 0
stop_bmg = False
click_sound = pygame.mixer.Sound('sound/click.ogg')
click_sound.set_volume(0.3)
game_over_ogg = pygame.mixer.Sound('sound/game_over.ogg')
game_start_sound = pygame.mixer.Sound('sound/game_start.ogg')
golden_sound = pygame.mixer.Sound('sound/golden.ogg')
purple_sound = pygame.mixer.Sound('sound/purple.ogg')


gacha_tuta = {
    "salt": ["Pure Salt"],
    "A": ["Whizdy", "Marinelle", "Komomo"],
    "S": ['Tuta','Carra','Rocky','Baby']
}

gacha_origins = {
    "salt": ["Pure Salt"],
    "A": ["Whizdy", "Marinelle", "Komomo"],
    "S": ['Carra','Rocky','Baby']
}

bw_character_images = {
    "Pure Salt": pygame.image.load(r"crt/bw_Salt.png"),
    "Whizdy": pygame.image.load(r"crt/bw_ Whizdy.png"),
    "Marinelle": pygame.image.load(r"crt/bw_ Marinelle.png"),
    "Komomo": pygame.image.load(r"crt/bw_ Komomo.png"),
    "Baby": pygame.image.load(r"crt/bw_Baby.png"),
    "Rocky": pygame.image.load(r"crt/bw_ Carra.png"),
    "Carra": pygame.image.load(r"crt/bw_ Rocky.png"),
    'Tuta': pygame.image.load(r'crt/bw_tuta.png')
}

def get_probabilities(roll_):
    roll_count = roll_
    if roll_count >= 180:
        return {"salt": 0.76, "A": 0.08, "S": 0.16}
    elif roll_count >= 150:
        return {"salt": 0.84, "A": 0.08, "S": 0.08}
    elif roll_count >= 100:
        return {"salt": 0.90, "A": 0.08, "S": 0.02}
    else:
        return {"salt": 0.91, "A": 0.08, "S": 0.01}

def roll_gacha(prob, roll_count, roll_countA, gacha_chest):
    roll = random.random()
    gacha_items = gacha_chest
    if roll_countA % 9 == 0 and roll_countA >= 1:
        return "A", random.choice(gacha_items["A"])
    if roll_count % 200 == 0 and roll_count >= 1:
        return "S", random.choice(gacha_items["S"])
    if roll < prob["S"]:
        return "S", random.choice(gacha_items["S"])
    elif roll < prob["S"] + prob["A"]:
        return "A", random.choice(gacha_items["A"])
    else:
        return "salt", random.choice(gacha_items["salt"])

class ButtonImage:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                click_sound.play()
                return True
        return False

start_button = ButtonImage(start_img, 1130, 610)
exit_button = ButtonImage(exit_img, WIDTH-200, 20)
next_button = ButtonImage(next_img,WIDTH-200, HEIGHT-100)
back_button = ButtonImage(back_img,WIDTH-200, 20)
storage_button = ButtonImage(storage_img, 70, HEIGHT-140)
bun1_button = ButtonImage(bunx1, WIDTH//2+249, HEIGHT-140)
bunx10_button = ButtonImage(bunx10, WIDTH-347, HEIGHT-140)
play_button = ButtonImage(play,WIDTH // 2 - 200, HEIGHT // 2 - 80)

def paitermtangna(events) :
    global current_page, bunbun_gem, page_stack, current_color, color_active, color_inactive, input_text, input_box, event, active, code, enter_rect, typing, bunbun_plus
    screen.blit(topup_bg,(0,0))
    back_button.draw(screen)
    screen.blit(cash_img, (50, 30))
    draw_text(f'{bunbun_gem}', 98, 38,color=(20,63,37), size=40)

    for event in events:
        if back_button.is_clicked(event) :
            current_page = page_stack.pop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
        if event.type == pygame.KEYDOWN and active == True :
            typing = True
            if event.key == pygame.K_RETURN :
                click_sound.play()
                code = input_text
                input_text = "" 
                active = False
                typing = False
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode.upper()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and active == True :
                if enter_rect.collidepoint(event.pos) :
                    click_sound.play()
                    code = input_text
                    input_text = "" 
                    active = False
                    typing = False
        if code == 'PLEASEGIVEATOUS' :
            bunbun_plus = 16000
            bunbun_gem += 16000
            code = None
            current_page = 'topup_result'
        else :
            if code != None :
                bunbun_plus = 0
                bunbun_gem += 0
                code = None
                current_page = 'topup_result'
        if active == False :
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                if sell_rect.collidepoint(event.pos) :
                    click_sound.play()
                    bunbun_plus = 20
                    bunbun_gem += 20
                    current_page = 'topup_result'
                elif baby_rect.collidepoint(event.pos) :
                    click_sound.play()
                    bunbun_plus = random.randint(1, 2000)
                    bunbun_gem += bunbun_plus
                    current_page = 'topup_result'

    if active == True :
        if typing == False :
            pygame.draw.rect(screen,(255,255,255),(170, 260, 5, 50))


    font = pygame.font.Font('pixel_font.otf', 72)
    text_surface = font.render(input_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

def display_storage(events):
    global current_page, scroll_offset, bunbun_gem, page_stack, event
    if 'display_storage' not in page_stack:
        page_stack.append('display_storage')
    screen.fill((77, 63, 37))
    back_button.draw(screen)
    screen.blit(cash_img, (50, 30))
    draw_text(f'{bunbun_gem}', 98, 38,color=(20,63,37), size=40)
    draw_text("Character Storage", WIDTH // 2 - 160, 40,size=48) 
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            distance = math.sqrt((mouse_x - circle_topup_center[0])**2 + (mouse_y - circle_topup_center[1])**2)
            if distance <= circle_topup_radius:
                click_sound.play()
                current_page = 'topup'

    items_per_column = 5 
    x_positions = [WIDTH // 2 - 180, WIDTH // 2 + 20]

    y_offset = -scroll_offset  

    for i, character in enumerate(bw_character_images.keys()):
        col = i // items_per_column
        row = i % items_per_column
        x = x_positions[col]+ col * 320 - 220
        y = 120 + row * 160 + y_offset

        count = storage.get(character, 0)
        image = character_images.get(character) if count > 0 else bw_character_images.get(character)

        if 0 <= y < HEIGHT - 120:  
            draw_text(f"{character} : {count}", x + 120, y+40,size=48)
            if image:
                character_image = pygame.transform.scale(image, (120, 120))
                screen.blit(character_image, (x, y))

    for event in events :
        if back_button.is_clicked(event):
            page_stack.pop()
            current_page = page_stack[-1]

def draw_text(text, x, y, color=(255, 255, 255), size=24):
    font = pygame.font.Font('pixel_font.otf', size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def termtang_result(events) :
    global current_page, page_stack, bunbun_plus
    screen.fill((47, 33, 7))
    if bunbun_plus == 16000 :
        text = 'Give A to us, pleaseeeee'
    elif bunbun_plus == 20 :
        text = 'You must really love your friend'
    elif bunbun_plus == 0 :
        text = 'What kind of code is that?'
    else :
        if bunbun_plus < 500 :
            text = 'Baby does not like you much'
        elif bunbun_plus < 1000 :
            text = 'Baby is not in a good mood'
        elif bunbun_plus < 1500 :
            text = 'Baby is in a good mood'
        elif bunbun_plus <= 2000 :
            text = 'OMG! Baby likes you a lot'

    screen.blit(money,(WIDTH//2-500,250))
    draw_text(f'You got {bunbun_plus} Bunbungems!', 800,400,color=(255, 215, 0),size=48)
    draw_text(text, 800,450,size=48)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            current_page = 'topup'


def Gacha_Information():
    global current_page, page_stack, bunbun_gem
    page_stack.append('Gacha_Information')
    screen.fill((77, 63, 37))
    screen.blit(background2, (WIDTH // 4 - 100, HEIGHT // 4 - 180))
    screen.blit(cash_img, (50, 30))
    draw_text(f'{bunbun_gem}', 98, 38,color=(20,63,37), size=40)
    next_button.draw(screen)
    back_button.draw(screen)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            distance = math.sqrt((mouse_x - circle_topup_center[0])**2 + (mouse_y - circle_topup_center[1])**2)
            if distance <= circle_topup_radius:
                click_sound.play()
                current_page = 'topup'


def gacha_game(events):
    global current_page, roll_count, roll_countA, current_image, current_character_name, last10, current_result_index, spark_count, bunbun_gem, page_stack, event, item_level, level_list, stop_bmg
    page_stack.append('gacha_game')
    screen.blit(roll_bg2, (0, 0))
    screen.blit(cash_img, (50, 30))
    draw_text(f'{bunbun_gem}', 98, 38,color=(20,63,37), size=40)
    bun1_button.draw(screen)
    bunx10_button.draw(screen)
    storage_button.draw(screen)
    back_button.draw(screen)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            distance = math.sqrt((mouse_x - circle_topup_center[0])**2 + (mouse_y - circle_topup_center[1])**2)
            if distance <= circle_topup_radius:
                click_sound.play()
                current_page = 'topup'

    if spark_count < 200 :
        draw_text(f'spark in : {spark_count}/200', 124, HEIGHT - 202,color=(255, 255, 255), size=32)
    elif spark_count == 200 :
        draw_text(f'spark now!', 133, HEIGHT - 204,color=(255, 215, 0), size=44)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if invisible_rect.collidepoint(event.pos):
                click_sound.play()
                current_page = 'gacha_origin'
        if spark_count == 200 :
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                distance = math.sqrt((mouse_x - circle_center[0])**2 + (mouse_y - circle_center[1])**2)
                if distance <= circle_radius:
                    click_sound.play()
                    stop_bmg = True
                    last10 = []
                    pygame.mixer.music.stop()
                    golden_sound.play()
                    gacha_animation(r'animation/gold.mp4')
                    result = 'Tuta'
                    storage[result] = storage.get(result, 0) + 1
                    last10.append(result)
                    current_page = "gacha_result"  
                    current_result_index = 0
                    spark_count = 0
                    stop_bmg = False

        if back_button.is_clicked(event):
            current_page = "Gacha_Information"
        elif storage_button.is_clicked(event):
            current_page = "display_storage"
        elif bun1_button.is_clicked(event):
            if bunbun_gem < 160 : 
                current_page = 'topup'

            else :
                stop_bmg = True
                pygame.mixer.music.stop()
                bunbun_gem -= 160
                last10 = []
                prob = get_probabilities(roll_count)
                item_level, result = roll_gacha(prob, roll_count, roll_countA, gacha_tuta)

                if item_level == 'S':
                    golden_sound.play()
                    gacha_animation(r'animation/gold.mp4')
                    roll_count = 0
                elif item_level == 'A':
                    purple_sound.play()
                    gacha_animation(r'animation/purple.mp4')
                    roll_countA = 0
                    roll_count += 1
                else:
                    purple_sound.play()
                    gacha_animation(r'animation/white.mp4')
                    roll_count += 1
                    roll_countA += 1

                storage[result] = storage.get(result, 0) + 1
                last10.append(result)
                stop_bmg = False

                current_page = "gacha_result"  
                current_result_index = 0
                if spark_count < 200 :
                    spark_count += 1

        elif bunx10_button.is_clicked(event):
            if bunbun_gem < 1600 : 
                current_page = 'topup'
            else :
                stop_bmg = True
                pygame.mixer.music.stop()
                bunbun_gem -= 1600
                last10 = []  
                level_list = []
                for x in range(10):
                    prob = get_probabilities(roll_count)
                    item_level, result = roll_gacha(prob, roll_count, roll_countA, gacha_tuta)
                    if item_level == 'S':
                        roll_count = 0
                    elif item_level == 'A':
                        roll_countA = 0
                        roll_count += 1
                    else:
                        roll_count += 1
                        roll_countA += 1
                    storage[result] = storage.get(result, 0) + 1
                    last10.append(result)
                    level_list.append(item_level)
                    if spark_count < 200 :
                        spark_count += 1
                if 'S' in level_list :
                    golden_sound.play()
                    gacha_animation(r'animation/gold.mp4')
                else :
                    purple_sound.play()
                    gacha_animation(r'animation/purple.mp4')

                current_result_index = 0  
                current_page = "gacha_result" 
                stop_bmg = False
    
    if stop_bmg :
        pygame.mixer.music.stop()
    else :
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play(-1, 0.0)


def gacha_origin(events):
    global current_page, roll_count_origin, roll_countA_origin, current_image, current_character_name, last10, current_result_index, page_stack, bunbun_gem, event, item_level, level_list, stop_bmg
    page_stack.append('gacha_origin')
    screen.blit(roll_bg1, (0, 0))
    screen.blit(cash_img, (50, 30))
    draw_text(f'{bunbun_gem}', 98, 38,color=(20,63,37), size=40)
    bun1_button.draw(screen)
    bunx10_button.draw(screen)
    storage_button.draw(screen)
    back_button.draw(screen)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            distance = math.sqrt((mouse_x - circle_topup_center[0])**2 + (mouse_y - circle_topup_center[1])**2)
            if distance <= circle_topup_radius:
                click_sound.play()
                current_page = 'topup'

    for event in events :
        if event.type == pygame.MOUSEBUTTONDOWN:
            if invisible_rect.collidepoint(event.pos):
                click_sound.play()
                current_page = 'gacha_game'
                
        if back_button.is_clicked(event):
            current_page = "Gacha_Information"
        elif storage_button.is_clicked(event):
            current_page = "display_storage"
        elif bun1_button.is_clicked(event):
            if bunbun_gem < 160 : 
                current_page = 'topup'
            else :
                stop_bmg = True
                pygame.mixer.music.stop()
                bunbun_gem -= 160
                last10 = []
                prob = get_probabilities(roll_count_origin)
                item_level, result = roll_gacha(prob, roll_count_origin, roll_countA_origin, gacha_origins)

                if item_level == 'S':
                    golden_sound.play()
                    gacha_animation(r'animation/gold.mp4')
                    roll_count_origin = 0
                elif item_level == 'A':
                    purple_sound.play()
                    gacha_animation(r'animation/purple.mp4')
                    roll_countA_origin = 0
                    roll_count_origin += 1
                else:
                    purple_sound.play()
                    gacha_animation(r'animation/white.mp4')
                    roll_count_origin += 1
                    roll_countA_origin += 1

                storage[result] = storage.get(result, 0) + 1
                last10.append(result)

                current_page = "gacha_result"  
                current_result_index = 0

        elif bunx10_button.is_clicked(event):
            if bunbun_gem < 1600 : 
                current_page = 'topup'
            else :
                stop_bmg = True
                pygame.mixer.music.stop()
                bunbun_gem -= 1600
                last10 = []  
                level_list = []
                for x in range(10):
                    prob = get_probabilities(roll_count_origin)
                    item_level, result = roll_gacha(prob, roll_count_origin, roll_countA_origin, gacha_origins)
                    if item_level == 'S':
                        roll_count_origin = 0
                    elif item_level == 'A':
                        roll_countA_origin = 0
                        roll_count_origin += 1
                    else:
                        roll_count_origin += 1
                        roll_countA_origin += 1
                    storage[result] = storage.get(result, 0) + 1
                    last10.append(result)
                    level_list.append(item_level)
                if 'S' in level_list :
                    golden_sound.play()
                    gacha_animation(r'animation/gold.mp4')
                else :
                    purple_sound.play()
                    gacha_animation(r'animation/purple.mp4')

                current_result_index = 0  
                current_page = "gacha_result" 

    if stop_bmg :
        pygame.mixer.music.stop()
    else :
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play(-1, 0.0)
    

def gacha_result(events):
    global current_page, current_result_index, last10, page_stack, event, item_level, level_list

    screen.fill((77, 63, 37))

    if current_result_index < len(last10):
        character_name = last10[current_result_index]
        pygame.draw.rect(screen, (0, 0, 0), (1080, 735, 800, 80))
        current_image = pygame.transform.scale(character_images[character_name], (WIDTH//4, HEIGHT//2))
        screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
        draw_text(character_name, WIDTH - 480, HEIGHT - 150, size=64)
        if len(last10) > 2 :
            draw_text('SKIP', 1400, 50, size=64)
            draw_text(f'{current_result_index+1} of 10',WIDTH//2-80,700,size=68)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if skip_rect.collidepoint(event.pos):
                    click_sound.play()
                    current_result_index = 9

    else:
        if len(last10) == 10 :
            for i, character_name in enumerate(last10):
                character_img = pygame.transform.scale(character_images[character_name], (WIDTH//8, HEIGHT//4))
                x_pos = 100 + (i % 5) * 300
                y_pos = 100 + (i // 5) * 300
                screen.blit(character_img, (x_pos, y_pos))
                draw_text(character_name, x_pos+20, y_pos + 240, size=48)
        else :
            current_page = page_stack.pop()


    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_result_index < len(last10):
                click_sound.play()
                current_result_index += 1 
            else:
                click_sound.play()
                current_page = page_stack.pop()

def game_over(events) :
    global playtime, kill_count, reward, lvl, current_page
    game_over_ogg.play()
    screen.blit(over_bg,(0,0))
    draw_text(f'level : {lvl}', 150, 300,color=(77, 63, 37),size=48)
    draw_text(f'survive time : {playtime}', 150, 400, color=(77, 63, 37),size=48)
    draw_text(f'kill count : {kill_count}', 150, 500, color=(77, 63, 37),size=48)
    draw_text(f'Bunbungems gained : {reward}', 150, 600, color=(77, 63, 37),size=48)
    for event in events :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if back_menu_rect.collidepoint(event.pos) :
                click_sound.play()
                current_page = 'main_menu'

def go_gacha(events) :
    global current_page, page_stack
    screen.blit(go_gacha_bg, (0,0))

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            current_page = 'gacha_game'


def change_music(page):
    global current_music
    if page == "gacha_result" or page == 'game_over' or page == 'play':
        pygame.mixer.music.stop()
        current_music = None 
    elif page in music_files and current_music != music_files[page]:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_files[page]) 
        pygame.mixer.music.play(-1) 
        current_music = music_files[page]  

change_music(current_page)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    change_music(current_page)
    if current_page == "main_menu":
        screen.blit(background, (0, 0))
        start_button.draw(screen)
        exit_button.draw(screen)
        play_button.draw(screen)
        for event in events:
            if start_button.is_clicked(event):
                current_page = "Gacha_Information"
            elif play_button.is_clicked(event):
                if 'Tuta' in storage :
                    game_start_sound.play()
                    current_page = 'play'
                else :
                    current_page = 'go_gacha'
            elif exit_button.is_clicked(event):
                run = False
    elif current_page == "Gacha_Information":
        Gacha_Information()
        for event in events:
            if next_button.is_clicked(event):
                current_page = "gacha_game"
            elif back_button.is_clicked(event):
                current_page = "main_menu"
    elif current_page == "gacha_game":
        gacha_game(events)
    elif current_page == 'gacha_origin' :
        gacha_origin(events)
    elif current_page == "gacha_result":
        gacha_result(events)
    elif current_page == 'display_storage':
        display_storage(events)
    elif current_page == 'topup':
        paitermtangna(events)
    elif current_page == 'topup_result' :
        termtang_result(events)
    elif current_page == 'play' :
        kill_count,minutes,seconds,lvl = main(start_time=pygame.time.get_ticks())
        playtime = f"{minutes:02}:{seconds:02}"
        reward = kill_count*2
        bunbun_gem += reward
        current_page = 'game_over'
    elif current_page == 'game_over' :
        game_over(events)
    elif current_page == 'go_gacha' :
        go_gacha(events)

    pygame.display.update()

pygame.quit()
