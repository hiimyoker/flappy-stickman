# pygame, sysというライブラリを使用する
from threading import Thread
from tkinter import CENTER, Variable
import pygame,sys
import numpy as np
import sounddevice as sd
import random

test = 0
screen_width = 250
screen_height = 500
clock = pygame.time.Clock() # FPS設定

#　バックグラウンドを設定する変数
screen = pygame.display.set_mode((screen_width,screen_height))
background = pygame.image.load('assets/background-night.png')
background = pygame.transform.scale(background, (screen_width,screen_height))

#　floorを設定する変数
floor = pygame.image.load('assets/floor.png') 
floor = pygame.transform.scale(floor, (screen_width*1.5,screen_height*0.25))
floor_X_pos = 0

#birdを作る変数
bird = pygame.image.load('assets/yellowbird-midflap.png') 
bird = pygame.transform.scale(bird, (screen_width*0.15,screen_height*0.05))
bird_rect = bird.get_rect(center = (screen_width*0.25,screen_height*0.5) )

#pipe を作る変数
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale(pipe_surface,(screen_width*0.2,screen_height*0.5))
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe,1000)
pipe_list = []
random_pipe = [0.4,0.5,0.6,0.7]
game_active = True
# 重力設定
gravity = screen_height/1000
global bird_movement
bird_movement = 0
#System 設定
pygame.font.init();
game_font = pygame.font.Font('04B_19.TTF',int(screen_height*0.05))
score = 0
high_score = 0
#score 処理
def score_display(game_active):
    if game_active == 'in_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (screen_width*0.5,screen_height*0.1))
        screen.blit(score_surface,score_rect)
    else:
        high_score_surface = game_font.render('HIGH SCORE ' + str(int(high_score)),True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (screen_width*0.5,screen_height*0.73))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score;
    return high_score;
# floor  を描く関数
def draw_floor():
    screen.blit(floor,(floor_X_pos,screen_height*0.8))
    screen.blit(floor,(floor_X_pos+screen_width*1.5,0.8*screen_height))

#pipe を作る関数
def creat_pipe():
    random_pipe_pos = screen_height*random.choice(random_pipe) 
    bottom_pipe = pipe_surface.get_rect(midtop = (screen_width*1.2,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (screen_width*1.2,random_pipe_pos-screen_height*0.8))
    return bottom_pipe,top_pipe
#pipe を動かせる関数
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= screen_width*0.006
    return pipes
#pipeを描く関数
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height*0.9:
            screen.blit(pipe_surface,pipe)
        else :
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
#接触を確認する関数
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    return True
        
        
#音声認識
def audio():
    # Variable
    global duration
    duration = 1000   #in seconds
    # subfunc
    def audio_callback(indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        global test
        test = int(volume_norm)

    stream = sd.InputStream(callback=audio_callback)
    with stream:
        sd.sleep(duration * 1000)

# Thread
thread_audio = Thread(target = audio)
thread_audio.start()

# def main_game():
while 1:
    # To exit game
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) :
            pygame.quit()
            sys.exit()
    # bird fly
        #by key
        if (event.type == pygame.KEYDOWN):
            if game_active:
                print("by key")
                bird_movement = 0
                bird_movement = -screen_height/70
            else:
                game_active = True
                pipe_list.clear()
                score = 0;
                bird_movement = 0
                bird_rect.center = (screen_width*0.25,screen_height*0.5)
    #pipe spawn
        if event.type == spawn_pipe:
            pipe_list.extend(creat_pipe())
        
    #by voice
    if(test>=30):
        print(test)
        print("by voice")
        bird_movement = 0
        bird_movement = -screen_height/70

    #background を描く
    screen.blit(background,(0,0))
    bird_movement += gravity
    bird_rect.centery += bird_movement
    if game_active:
         #bird を描く
        if (bird_rect.centery >0.75*screen_height):
            bird_rect.centery = 0.75*screen_height
        if (bird_rect.centery <-0.1*screen_height):
            bird_rect.centery = -0.1*screen_height
        screen.blit(bird,bird_rect)
        game_active =  check_collision(pipe_list)
        #pipeを描く
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 1/60
        score_display('in_game')
    else: 
        high_score = update_score(score,high_score)
        score_display('game_over')
        
        
       
    #floor を描く
    floor_X_pos -= 1
    draw_floor()
    if floor_X_pos <= -1.5*screen_width:
        floor_X_pos = 0;
    pygame.display.update()
    clock.tick(60)

        
