import os, pygame, sys
from pygame.locals import *

WIDTH, HEIGHT = 800, 600
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT),RESIZABLE)

pygame.display.set_caption('Battle Ship!')
title_font = pygame.font.Font('freesansbold.ttf', 64)
menu_font = pygame.font.Font('freesansbold.ttf', 32)

title_surf = title_font.render('BATTLE SHIP!', True, (255,165,0))
pvc_surf = menu_font.render('PLAYER VS COMPUTER', True, (255,255,255))
pvp_surf = menu_font.render('PLAYER VS PLAYER', True, (255,255,255))
quit_surf = menu_font.render('QUIT', True, (255,255,255))

title = title_surf.get_rect()
pvc = pvc_surf.get_rect()
pvp = pvp_surf.get_rect()
quit_ = quit_surf.get_rect()

title.center = (WIDTH/2,HEIGHT/4)
pvc.center = (WIDTH/2,(HEIGHT/2)+(HEIGHT/20)+3)
pvp.center = (WIDTH/2,(HEIGHT/2)+(4*HEIGHT/18))
quit_ = (3*WIDTH/7+9,(HEIGHT/2)+(7*HEIGHT/20)+3)

while True: 
    display.blit(title_surf, title)
    display.blit(pvc_surf, pvc)
    display.blit(pvp_surf, pvp)
    display.blit(quit_surf, quit_)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
