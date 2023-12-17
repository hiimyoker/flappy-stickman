from ctypes.wintypes import RGB
from lib2to3.pgen2.token import STRING
from pickle import FALSE
from posixpath import split
from tokenize import Name
from turtle import _Screen
from itertools import cycle 
import pygame
import sys 
import random 
from pygame.locals import *
import time 
from threading import Thread
from tkinter import StringVar, Variable
import pygame,sys
import numpy as np
import sounddevice as sd
import tkinter as tk
pygame.init()
#Create a displace surface object
DISPLAYSURF = pygame.display.set_mode((500,500))
x,y=DISPLAYSURF.get_size()
backgroundImg =pygame.image.load("MAINMENU.png")
inGameBackground =pygame.image.load("INGAME.png")
pygame.display.flip()
mainLoop = True
flag=-1
pygame.display.set_caption('Show Text')
font = pygame.font.Font('freesansbold.ttf', 32)
global loaded
loaded=False
loadedN=False

def MainMenu():
    global flag
    if flag==-1:
        if loaded!=True:
            loadScore()
        if loadedN!=True:
            loadScoreName()
    if flag==0:
        DISPLAYSURF.blit(inGameBackground,(0,0))
    if(pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0]>=12 and pygame.mouse.get_pos()[1]>=175 and pygame.mouse.get_pos()[0]<=194 and pygame.mouse.get_pos()[1]<=258):
        flag=1
        global t
        t=time.time()
    if(pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0]>=304 and pygame.mouse.get_pos()[1]>=175 and pygame.mouse.get_pos()[0]<=491 and pygame.mouse.get_pos()[1]<=258):
        flag =2
    if(pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0]>=167 and pygame.mouse.get_pos()[1]>=333 and pygame.mouse.get_pos()[0]<=335 and pygame.mouse.get_pos()[1]<=377):
        flag =3
    if(pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0]>=167 and pygame.mouse.get_pos()[1]>=409 and pygame.mouse.get_pos()[0]<=335 and pygame.mouse.get_pos()[1]<=456):
        flag =4
    else :
        DISPLAYSURF.blit(backgroundImg, (0,0))
def voiceRecMode():
    DISPLAYSURF.blit(inGameBackground,(0,0))
    inGametime()
    DISPLAYSURF.blit(timerr, timerRect)
    if (event.type == KEYDOWN):
       if (event.key == K_ESCAPE):
           backToMainMenu()
def keyMode():
    print("keyMode is now on")
    DISPLAYSURF.blit(inGameBackground, (0,0))
    if (event.type == KEYDOWN):
       if (event.key == K_ESCAPE):
           backToMainMenu()
def highScoreMode():
    print ("highscore mode is now on")
    if (event.type == KEYDOWN):
       if (event.key == K_ESCAPE):
           backToMainMenu()
def helpMode():
    print("helpMode is now on")
    if (event.type == KEYDOWN):
       if (event.key == K_ESCAPE):
           backToMainMenu()
score=[]

def backToMainMenu():
    score.append(tm)
    
    global scores
    highscore = open('highscore.txt','w')
    for i in range(len(score)):
        if(i!=len(score)-1):
            highscore.write(str(score[i])+'i')
        else:
            highscore.write(str(score[i]))
    highscore.close()
    print(score)
    saveScoreName()
    global flag
    flag =0
    
    
def loadScore():
    global score
    scores=score
    load=open('highscore.txt','r')
    for line in load:
        scores=line.split('i')
    for i in range(len(scores)):
        score.append(int(scores[i]))
    print(score) 
    global loaded
    loaded=True
def saveScoreName():
    scorename.append("guest")
    highscorename = open('highscorename.txt','w')
    for i in range(len(scorename)):
        if(i!=len(scorename)-1):
            highscorename.write(scorename[i]+',')
        else:
            highscorename.write(scorename[i])
    highscorename.close()
    print(scorename)

scorename=[]
def loadScoreName():
    loadname=open('highscorename.txt','r')
    Names=scorename
    for line in loadname:
        Names=line.split(',')
    for i in range(len(Names)):
        scorename.append(Names[i])
    print(scorename) 
    global loadedN
    loadedN=True
def inGametime():
    global t
    global timerr
    global timerRect
    global tm
    tm=int(time.time()-t)
    timerr = font.render(str(tm), True, RGB(50,100,100))
    timerRect = timerr.get_rect()
    timerRect.center = (x // 2, y // 10)
    print(int(time.time()-t))


while mainLoop:
    if (flag==0 or flag==-1):
        MainMenu()
    if (flag==1):
        voiceRecMode()
    if (flag==2):
        keyMode()
    if (flag==3):
        highScoreMode()
    if(flag==4):
        helpMode()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                    mainLoop = False
        
    pygame.display.update()
    
# pygame.quit()
