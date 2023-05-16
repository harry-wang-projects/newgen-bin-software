import pygame
import sys

def get_barcode():
    id_card=""
    while not len(id_card)==7:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key=pygame.key.get_pressed()
                if key[pygame.K_0]:
                    id_card=id_card+str(0)
                if key[pygame.K_1]:
                    id_card=id_card+str(1)
                if key[pygame.K_2]:
                    id_card=id_card+str(2)
                if key[pygame.K_3]:
                    id_card=id_card+str(3)
                if key[pygame.K_4]:
                    id_card=id_card+str(4)
                if key[pygame.K_5]:
                    id_card=id_card+str(5)
                if key[pygame.K_6]:
                    id_card=id_card+str(6)
                if key[pygame.K_7]:
                    id_card=id_card+str(7)
                if key[pygame.K_8]:
                    id_card=id_card+str(8)
                if key[pygame.K_9]:
                    id_card=id_card+str(9)
                if key[pygame.K_RETURN]:
                    return id_card
                
    return "unsuccess"
