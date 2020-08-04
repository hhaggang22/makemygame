import pygame, sys, random
from pygame.locals import QUIT, KEYDOWN,\
     K_LEFT, K_RIGHT, Rect
import gettext
import math
from pygame.locals import*
import threading
import time

pygame.init() #오류 많아서 잡으려고 초기화 
screen = pygame.display.set_mode((849,600)) #윈도우의 크기 셋팅
pygame.display.set_caption('다비의 상큼이 피하기 대모험') #caption
pygame.display.set_icon(pygame.image.load('연희쓰.png')) #caption 앞의 이미지
fps_clock = pygame.time.Clock()
clock = pygame.time.Clock()				     
dabi = pygame.image.load("그림1.png")			     #이미지 불러오기
ground = pygame.image.load("배경.png")
detail = pygame.image.load("폭탄.png")

BLACK=(0, 0, 0)
WHITE=(200, 200, 200)
YELLOW=(250, 250, 20)
BLUE=(20, 20, 250)

game_over = False


class Fruits:
    def __init__(self):
        grape = "grape.png"
        peach = "peach.png"
        watermelon = "watermelon.png"
        pineapple = "pineapple.png"
        fruits = (grape, peach, watermelon, pineapple)
        self.random_fruit = random.choice(fruits)
        self.oh = pygame.image.load(self.random_fruit)
        self.x = random.randint(0,500)
        self.y = -3
    
    def move(self, n):
        self.y += n

    def draw(self):
        screen.blit(self.oh, (self.x, self.y))

    def get_score(self):
        if self.random_fruit == "grape.png":
            return 3
        elif self.random_fruit == "peach.png":
            return 2
        elif self.random_fruit == "watermelon.png":
            return 2
        else:
            return 1

class Bombs:
    def __init__(self):
        img = "bomb.png"
        self.bomb = pygame.image.load(img)
        self.x = random.randint(0, 500)
        self.y = -3
    
    def move_bomb(self, n):
        self.y += n

    def draw_bomb(self):
        screen.blit(self.bomb, (self.x, self.y))

class startTimer:
    def __init__(self):
        self.tn = 0

    def start(self):
        self.tn += 1
        self.timer = threading.Timer(1, self.start)
        self.timer.start()

    def get_time(self):
        return self.tn

    def stop(self):
        self.timer.cancel()
        
        
def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

def printdetail(ground, detail ,x, y):
    d = 130 
    while d != 0:
        clock.tick(60)
        screen.blit(ground, (0, 0))		
        screen.blit(detail, (x, y))
        d -= 1
        pygame.display.update()

def printmessage(msg):
    d = 130
    while d != 0:
        clock.tick(60)
        draw_text(msg,pygame.font.Font('NanumGothic.ttf', 100), screen,
        400, 250, BLACK)
        d -= 1
        pygame.display.update()
       
def game_loop4():
    pygame.mixer.music.load('game.wav')
    collide_sound = pygame.mixer.Sound('collide.wav')
    bomb_sound = pygame.mixer.Sound('bomb.wav')
    pygame.mixer.music.play(-1)
    global game_over
    game_over = False
    pos_x = 250						# 좌표 지정
    pos_y = 412
    count = 0
    A = 1
    level = 1
    sysfont = pygame.font.SysFont(None, 72)
    time = 0
    fruitdrops = []
    bombdrops = []
    bombcount = 0

    printdetail(ground, detail, 120, 180)

    timer4 = startTimer()
    timer4.start()
    
    while 1:
        if game_over==True:
            pygame.mixer.music.stop()
            collide_sound.stop()
            bomb_sound.stop()
            break
        
        clock.tick(60)			# 레벨 만들기 (5초가 지날때 마다 카운트 상향)
    
        if level == 1:
            A = 30
        elif level == 2:
            A = 20
        elif level == 3:
            A = 15
        
        if time*1.5% A==0:
            fruitdrops.append(Fruits())

        if time*1.5 % A == 0: #폭탄 많이 나오게
            bombdrops.append(Bombs())

        screen.blit(ground, (0, 0))		# 배경 이미지 출력
        screen.blit(dabi, (pos_x, pos_y))	# 주인공 이미지 출력

        for fruitdrop in fruitdrops:		
            fruitdrop.move(11)
            fruitdrop.draw()

        for bombdrop in bombdrops:
            bombdrop.move_bomb(11)
            bombdrop.draw_bomb()
        
        for event in pygame.event.get():	
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key_event = pygame.key.get_pressed() 
        if key_event[pygame.K_LEFT]:
            if pos_x > 0:			
                pos_x -= 10
                dabi

        if key_event[pygame.K_RIGHT]:
            if 958 > pos_x:
                pos_x += 10
                dabi
        

        time+=1
    
        if count == 15:
             level = 2
        elif count == 25:
            level = 3

    
    #아래 4줄: (200,50)에다가 Score 출력
        message1 = sysfont.render("Score is {}".format(count), True, (255,255,0))	# 카운트당 스코어가 오르게하고 화면에 스코어 메세지를 출력하게 함
        message1_rect = message1.get_rect()
        message1_rect.center = (200,50)
        screen.blit(message1, message1_rect)	# 스코어 메세지 출력
        message2 = sysfont.render("Time: {}".format(timer4.get_time()), True, (255,0,0))	# 카운트당 스코어가 오르게하고 화면에 스코어 메세지를 출력하게 함
        message2_rect = message2.get_rect()
        message2_rect.center = (200,100)
        screen.blit(message2, message2_rect)	# 스코어 메세지 출력

        if bombcount >= 3:
            draw_text("Game Over!",pygame.font.Font('NanumGothic.ttf', 100), screen,
                   400, 250, BLACK)
            game_over = True
            timer.stop()
   
        if timer4.get_time() >= 30:
            if count < 100:
                draw_text("Game Over!",pygame.font.Font('NanumGothic.ttf', 100), screen,
                   400, 250, BLACK)
                game_over = True
                timer4.stop()
            else:
                printmessage("Success!")
                game_over = True
        
            
        for e in fruitdrops:
            if pos_x - 70 < e.x < pos_x + 70:
                if pos_y + 10 < e.y+10 < pos_y + 30:
                    collide_sound.play()
                    fruitdrops.remove(e)
                    count = count + e.get_score()
                
            elif e.y >= 600:
                fruitdrops.remove(e)

        for e in bombdrops:
            if pos_x - 70 < e.x < pos_x + 70:
                if pos_y + 10 < e.y+10 < pos_y + 30:
                    bomb_sound.play()
                    bombdrops.remove(e)
                    bombcount += 1
                
            elif e.y >= 600:
                bombdrops.remove(e)

        pygame.display.update() # 위에 사항들을 디스플레이에 계속 업데이트

def game_loop3():
    pygame.mixer.music.load('game.wav')
    collide_sound = pygame.mixer.Sound('collide.wav')
    bomb_sound = pygame.mixer.Sound('bomb.wav')
    pygame.mixer.music.play(-1)
    global game_over
    game_over = False
    pos_x = 250						# 좌표 지정
    pos_y = 412
    count = 0
    A = 1
    level = 1
    sysfont = pygame.font.SysFont(None, 72)
    time = 0
    fruitdrops = []
    bombdrops = []
    bombcount = 0

    printdetail(ground, detail, 120, 180)

    timer3 = startTimer()
    timer3.start()
    
    while 1:
        if game_over==True:
            pygame.mixer.music.stop()
            collide_sound.stop()
            break
    
        clock.tick(60)			# 레벨 만들기 (5초가 지날때 마다 카운트 상향)
    
        if level == 1:
            A = 30
        elif level == 2:
            A = 20
        elif level == 3:
            A = 15
        
        if time % A==0:
            fruitdrops.append(Fruits())

        if time*0.7 % A == 0: #폭탄 가끔 나오게
            bombdrops.append(Bombs())

        screen.blit(ground, (0, 0))		# 배경 이미지 출력
        screen.blit(dabi, (pos_x, pos_y))	# 주인공 이미지 출력

        for fruitdrop in fruitdrops:		
            fruitdrop.move(7)
            fruitdrop.draw()
            
        for bombdrop in bombdrops:
            bombdrop.move_bomb(7)
            bombdrop.draw_bomb()
        
        for event in pygame.event.get():	
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key_event = pygame.key.get_pressed() 
        if key_event[pygame.K_LEFT]:
            if pos_x > 0:			
                pos_x -= 10
                dabi

        if key_event[pygame.K_RIGHT]:
            if 958 > pos_x:
                pos_x += 10
                dabi
        

        time+=1
    
        if count == 15:
             level = 2
        elif count == 25:
            level = 3

    
    #아래 4줄: (200,50)에다가 Score 출력
        message1 = sysfont.render("Score is {}".format(count), True, (255,255,0))	# 카운트당 스코어가 오르게하고 화면에 스코어 메세지를 출력하게 함
        message1_rect = message1.get_rect()
        message1_rect.center = (200,50)
        screen.blit(message1, message1_rect)	# 스코어 메세지 출력
        message2 = sysfont.render("Time: {}".format(timer3.get_time()), True, (255,0,0))	# 카운트당 스코어가 오르게하고 화면에 스코어 메세지를 출력하게 함
        message2_rect = message2.get_rect()
        message2_rect.center = (200,100)
        screen.blit(message2, message2_rect)	# 스코어 메세지 출력      

        if bombcount>= 3:
            draw_text("Game Over!",pygame.font.Font('NanumGothic.ttf', 100), screen,
                   400, 250, BLACK)
            game_over = True
            timer.stop()
            
        if timer3.get_time() >= 25:
            if count < 60:
                draw_text("Game Over!",pygame.font.Font('NanumGothic.ttf', 100), screen,
                   400, 250, BLACK)
                game_over = True
                timer3.stop()
            else:
                printmessage("Success!")
                game_over = True
                game_loop4()
        
            
        for e in fruitdrops:
            if pos_x - 70 < e.x < pos_x + 70:
                if pos_y + 10 < e.y+10 < pos_y + 30:
                    collide_sound.play()
                    fruitdrops.remove(e)
                    count = count + e.get_score()
                
            elif e.y >= 600:
                fruitdrops.remove(e)

        for e in bombdrops:
            if pos_x - 70 < e.x < pos_x + 70:
                if pos_y + 10 < e.y+10 < pos_y + 30:
                    bomb_sound.play()
                    bombdrops.remove(e)
                    bombcount += 1
                
            elif e.y >= 600:
                bombdrops.remove(e)

        pygame.display.update() # 위에 사항들을 디스플레이에 계속 업데이트

def game_loop2():
    pygame.mixer.music.load('game.wav')
    collide_sound = pygame.mixer.Sound('collide.wav')
    bomb_sound = pygame.mixer.Sound('bomb.wav')
    pygame.mixer.music.play(-1)
    global game_over
    global tn2
    tn2 = 0
    game_over = False					     
    pos_x = 250						# 좌표 지정
    pos_y = 412
    count = 0
    A = 1
    level = 1
    sysfont = pygame.font.SysFont(None, 72)
    time = 0
    fruitdrops = []

    screen.blit(ground, (0, 0))

    printmessage("Level 2")

    timer2 = startTimer()
    timer2.start()
    
    while 1:
        if game_over==True:
            pygame.mixer.music.stop()
            collide_sound.stop()
            break
    
        clock.tick(60)			# 레벨 만들기 (5초가 지날때 마다 카운트 상향)
    
        if level == 1:
            A = 30
        elif level == 2:
            A = 20
        elif level == 3:
            A = 15
        
        if time % A==0:
            fruitdrops.append(Fruits())

        screen.blit(ground, (0, 0))		# 배경 이미지 출력
        screen.blit(dabi, (pos_x, pos_y))	# 주인공 이미지 출력

        for fruitdrop in fruitdrops:		
            fruitdrop.move(6)
            fruitdrop.draw()
        
        for event in pygame.event.get():	
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key_event = pygame.key.get_pressed() 
        if key_event[pygame.K_LEFT]:
            if pos_x > 0:			
                pos_x -= 10
                dabi

        if key_event[pygame.K_RIGHT]:
            if 958 > pos_x:
                pos_x += 10
                dabi
        

        time+=1
    
        if count == 10:
             level = 2
        elif count == 20:
            level = 3

    
    #아래 4줄: (200,50)에다가 Score 출력
        message1 = sysfont.render("Score is {}".format(count), True, (255,255,0))	# 카운트당 스코어가 오르게하고 화면에 스코어 메세지를 출력하게 함
        message1_rect = message1.get_rect()
        message1_rect.center = (200,50)
        screen.blit(message1, message1_rect)	# 스코어 메세지 출력
        message2 = sysfont.render("Time: {}".format(timer2.get_time()), True, (255,0,0))	# 카운트당 스코어가 오르게하고 화면에 스코어 메세지를 출력하게 함
        message2_rect = message2.get_rect()
        message2_rect.center = (200,100)
        screen.blit(message2, message2_rect)	# 스코어 메세지 출력      
                
        if timer2.get_time() >= 20:
            if count < 40:
                draw_text("Game Over!",pygame.font.Font('NanumGothic.ttf', 100), screen,
                   400, 250, BLACK)
                game_over = True
                timer2.stop()
            else:
                printmessage("Success!")
                timer2.stop()
                game_over = True
                game_loop3()
        
            
        for e in fruitdrops:
            if pos_x - 70 < e.x < pos_x + 70:
                if pos_y + 10 < e.y+10 < pos_y + 30:
                    collide_sound.play()
                    fruitdrops.remove(e)
                    count = count + e.get_score()
                
            elif e.y >= 600:
                fruitdrops.remove(e)

        pygame.display.update() # 위에 사항들을 디스플레이에 계속 업데이트
            
def game_loop1():
    pygame.mixer.music.load('game.wav')
    collide_sound = pygame.mixer.Sound('collide.wav')
    bomb_sound = pygame.mixer.Sound('bomb.wav')
    pygame.mixer.music.play(-1)
    global game_over
    game_over = False					     
    pos_x = 250						# 좌표 지정
    pos_y = 412
    count = 0
    A = 1
    level = 1
    sysfont = pygame.font.SysFont(None, 72)
    time = 0
    fruitdrops = []

    screen.blit(ground, (0, 0))

    printmessage("Level 1")
    
    timer = startTimer()
    timer.start()
    
    while 1:
        if game_over==True:
            pygame.mixer.music.stop()
            collide_sound.stop()
            break
    
        clock.tick(60)			# 레벨 만들기 (5초가 지날때 마다 카운트 상향)
    
        if level == 1:
            A = 40
        elif level == 2:
            A = 25
        elif level == 3:
            A = 15

        if time % A==0:
            fruitdrops.append(Fruits())
            
        screen.blit(ground, (0, 0))		# 배경 이미지 출력
        screen.blit(dabi, (pos_x, pos_y))	# 주인공 이미지 출력

        for fruitdrop in fruitdrops:		
            fruitdrop.move(4)
            fruitdrop.draw()
        
        for event in pygame.event.get():	
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key_event = pygame.key.get_pressed() 
        if key_event[pygame.K_LEFT]:
            if pos_x > 0:			
                pos_x -= 10
                dabi

        if key_event[pygame.K_RIGHT]:
            if 958 > pos_x:
                pos_x += 10
                dabi
        
        time+=1
    
        if count == 12:
             level = 2
        elif count == 20:
            level = 3

    
    #아래 4줄: (200,50)에다가 Score 출력
        message1 = sysfont.render("Score is {}".format(count), True, (255,255,0))	# 카운트당 스코어가 오르게하고 화면에 스코어 메세지를 출력하게 함
        message1_rect = message1.get_rect()
        message1_rect.center = (200,50)
        screen.blit(message1, message1_rect)	# 스코어 메세지 출력
        message2 = sysfont.render("Time: {}".format(timer.get_time()), True, (255,0,0))	# 카운트당 스코어가 오르게하고 화면에 스코어 메세지를 출력하게 함
        message2_rect = message2.get_rect()
        message2_rect.center = (200,100)
        screen.blit(message2, message2_rect)	# 스코어 메세지 출력      

        if timer.get_time() >= 15:
            if count < 30:
                draw_text("Game Over!",pygame.font.Font('NanumGothic.ttf', 100), screen,
                   400, 250, BLACK)
                game_over = True
                timer.stop()
            else:
                printmessage("Success!")
                timer.stop()
                game_over = True
                game_loop2()
            
        for e in fruitdrops:
            if pos_x - 70 < e.x < pos_x + 70:
                if pos_y + 10 < e.y+10 < pos_y + 30:
                    collide_sound.play()
                    fruitdrops.remove(e)
                    count = count + e.get_score()
                
            elif e.y >= 600:
                fruitdrops.remove(e)

        pygame.display.update() # 위 사항들을 디스플레이에 계속 업데이트     




def game_screen():
    pygame.init()
    pygame.mixer.init()
    
    start_image = pygame.image.load('beforegame.png')
    screen.blit(start_image, [0, 0])

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return 'quit'
            elif event.key == pygame.K_s:
                return 'play'
        if event.type == pygame.MOUSEBUTTONDOWN:
            return 'play'
        if event.type == QUIT:
            return 'quit'

    return 'game_screen'


def main_loop():
    pygame.mixer.music.load('before_gamestart.wav')
    pygame.mixer.music.play(-1)
    
    action = 'game_screen'

    while action !='quit':
        if action == 'game_screen':
            action = game_screen()
        elif action == 'play':
            pygame.mixer.music.stop()
            action = game_loop1()

    pygame.quit()

main_loop()
