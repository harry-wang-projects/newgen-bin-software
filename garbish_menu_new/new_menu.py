import pygame
import sys
from os import path
import os 
import time
from random import random
from camera_run_temp import get_pic, verify_classes#, get_barcode
from pygame._sdl2 import touch
from screeninfo import get_monitors
from barcode_get import get_barcode
from garbage_list import trash_list
# from hardware_commands import get_weight, unlock

if len(sys.argv)!=2:
    print("invalid argument count.")
    pygame.quit()
    sys.exit()
trash_type=sys.argv[1]

for m in get_monitors():
    screen_height=m.height
    screen_width=m.width
# screen_height=480
# screen_width=720
print(screen_height,screen_width)

pygame.init()

#since 1200 x 720 was the starting screen resolution, adjustments must be made accordingly.
hm = screen_height/720
wm = screen_width/1200 #height and width multiplier
print(wm," ",hm)
xlname = pygame.font.Font("Somatic-Rounded.otf",int(135*wm))
lname = pygame.font.Font("Somatic-Rounded.otf",int(115*wm))
name = pygame.font.Font("Somatic-Rounded.otf",int(110*wm))
xxsname = pygame.font.Font("Somatic-Rounded.otf",int(20*wm))
xsname = pygame.font.Font("Somatic-Rounded.otf",int(30*wm))
sname = pygame.font.Font("Somatic-Rounded.otf",int(60*wm))
mname = pygame.font.Font("Somatic-Rounded.otf",int(80*wm))
msname = pygame.font.Font("Somatic-Rounded.otf",int(60*wm))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
class Menu(): #creates a menu with 3 buttons and the title on the top.
    def __init__(self,text1,text1center,small_title,big_title,font=name,font_render=xlname,font_2=sname,font_render_2=mname,text1color=(255,255,255),text2=None,text2center=None,text2color=(255,255,255),text3=None,text3center=None,text3color=(255,255,255),title="JCSE Recycling",student_id=None,cycle=False,animation=None): #spinner_chance adds up to 1, its a list.
        self.width = screen_width
        self.height = screen_height
        self.screen=screen
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = font
        self.font_render = font_render
        self.st=small_title
        self.bt=big_title
        self.student_id=student_id
        if not student_id==None:
            self.font_render_2 = font_render_2
            self.font_2=font_2
            self.student_id_text=str(student_id)
            self.student_id_rect = self.font_render_2.render(self.student_id_text, True, BLACK, None).get_rect(center=(1000*wm,650*hm)) #(620,400,120,50)
        self.textboxrect = pygame.Rect(50*wm, 30*hm,self.width-(100)*wm, 250*hm)
        self.touchquitrect=pygame.Rect(10,10,100,300*hm)
        self.touchquitcount=0

        self.text1_text = text1
        self.text1_color=text1color
        self.text1_rect = self.font_render.render(self.text1_text, True, BLACK, None).get_rect(center=(text1center))
        self.text2_text = text2
        self.text3_text = text3
        if not self.text2_text==None:
            self.text2_color=text2color
            self.text2_rect = self.font_render.render(self.text2_text, True, BLACK, None).get_rect(center=(text2center))
        if not self.text3_text==None:
            self.text3_color=text3color
            self.text3_rect = self.font_render.render(self.text3_text, True, BLACK, None).get_rect(center=(text3center))
        self.cycle=cycle 
        self.start_time = pygame.time.get_ticks()
        if self.cycle:
            self.cycle_time=10 #sec
        self.mouse_pos = None
        self.keep_looping = True
        self.message = ""
        self.button = 0
        self.button_cooldown = 3
        self.current_frame=0
        self.next_frame=True
        self.animation=animation
        self.max_frame=max_frames[animation-1]

    # def barcode(self):
    #     id_card=""
    #     for i in range(7):
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #             if event.type == pygame.KEYDOWN:
    #                 key=pygame.key.get_pressed()
    #                 if key[pygame.K_0]:
    #                     id_card=id_card+str(0)
    #                 if key[pygame.K_1]:
    #                     id_card=id_card+str(1)
    #                 if key[pygame.K_2]:
    #                     id_card=id_card+str(2)
    #                 if key[pygame.K_3]:
    #                     id_card=id_card+str(3)
    #                 if key[pygame.K_4]:
    #                     id_card=id_card+str(4)
    #                 if key[pygame.K_5]:
    #                     id_card=id_card+str(5)
    #                 if key[pygame.K_6]:
    #                     id_card=id_card+str(6)
    #                 if key[pygame.K_7]:
    #                     id_card=id_card+str(7)
    #                 if key[pygame.K_8]:
    #                     id_card=id_card+str(8)
    #                 if key[pygame.K_9]:
    #                     id_card=id_card+str(9)
    #                 if key[pygame.K_RETURN]:
    #                     return id_card
    #     if len(id_card)==7:  
    #         try:
    #             id_card = int(id_card)
    #             if not id_card==None:
    #                 return id_card
    #         except TypeError:
    #             print("typeerror")
    #     return "unsuccess"


    def events(self):
        current_time = pygame.time.get_ticks()
        if touch_available:
            self.finger_data = touch.get_finger(0)
        for event in pygame.event.get():
            if touch_available and self.finger_data['pressure']>=0.1:
                self.screen_touch=True
            if event.type == pygame.QUIT:
                self.keep_looping = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()
            if current_time-self.start_time%0.025<=0.005:
                print("next")
                self.next_frame=True #change to only current frame
            if self.cycle and current_time-self.start_time%1<=0.005:
                self.cycle_time=self.cycle_time-1
            if self.cycle and self.cycle_time<=0:
                self.keep_looping=False
            

    def draw_text_button(self,text, myrect, font, font_color=(0,0,0), background_color=(255,255,255), use_inner=False):
        inner_area = pygame.Rect((-22, -8, myrect[2], myrect[3]))
        pygame.draw.rect(self.screen, background_color, myrect,border_radius=20)
        txt_surface = font.render(text, True, font_color)
        if use_inner == True:
            self.screen.blit(txt_surface, myrect, inner_area)
        else:
            self.screen.blit(txt_surface, myrect)
    
    def animation_detect(self):
        print("true")
        print(self.animation)
        if self.animation!=None:
            if self.animation==1:
                print("1 animation")
                self.screen.blit(river1[self.current_frame],(0,0))
            if self.animation==2:
                self.screen.blit(river2[self.current_frame],(0,0))
            if self.animation==3:
                self.screen.blit(forest[self.current_frame],(0,0))
        
    
    def draw(self):
        self.screen.blit(background, (0, 0))
        self.animation_detect()
        if self.next_frame:
            print("true animation")
            self.animation_detect()
            if not self.current_frame>=self.max_frame:
                print("add frame")
                self.current_frame+=1
            else:
                print("frame reset")
                self.current_frame=0
            self.next_frame=False
        pygame.draw.rect(self.screen, (214,240,232), self.textboxrect, border_radius=30)
        text = msname.render(self.st, True, BLACK, None)
        textRect = text.get_rect(center=(self.width/2,self.height/2))
        textRect.center = (((self.width/2),90*hm))
        self.screen.blit(text, textRect)
        text2 = name.render(self.bt, True, BLACK, None)
        textRect2 = text2.get_rect()
        textRect2.center = ((self.width/2,180*hm))
        if not self.student_id==None:
            self.draw_text_button(self.student_id_text, self.student_id_rect, self.font_2,use_inner=True,background_color=(255,255,255))
        self.screen.blit(text2, textRect2)
        self.draw_text_button(self.text1_text, self.text1_rect, self.font,use_inner=True,background_color=self.text1_color)
        if self.text2_text!=None:
            self.draw_text_button(self.text2_text, self.text2_rect, self.font, use_inner=True,background_color=self.text2_color)
        if self.text3_text!=None:
            self.draw_text_button(self.text3_text, self.text3_rect, self.font, use_inner=True,background_color=self.text3_color)
            
        if not self.mouse_pos == None:
            if self.touchquitrect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.touchquitcount+=1
            if self.text1_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.message = self.text1_text
            if not self.text2_text==None and self.text2_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.message = self.text2_text
            if not self.text3_text==None and self.text3_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.message = self.text3_text
            self.mouse_pos = None
            if len(self.message) > 0 and self.message!="Scanning":
                self.keep_looping = False
        if touch_available and self.screen_touch:
            if self.text1_rect.collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
                self.message = self.text1_text
            if not self.text2_text==None and self.text2_rect.collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
                self.message = self.text2_text
            if not self.text3_text==None and self.text3_rect.collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
                self.message = self.text3_text
            self.mouse_pos = None
            if len(self.message) > 0:
                self.keep_looping = False
            if self.touchquitrect.collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
                self.touchquitcount+=1
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.events()
            self.draw()
            if self.touchquitcount==10:
                pygame.quit()
                sys.exit()
            if self.student_id==None:
                pass
                # id_card = get_barcode()
                # if not id_card==None and id_card!="unsuccess":
                #     self.keep_looping=False
                #     return id_card
        print(self.message,"Success")
        return self.message

class pages():        
    def __init__(self):
        if path.exists('save.txt'): 
            self.first_save=False
        else:
            with open('save.txt','a') as success:
                L = ["Success:0\n", "Fail:0\n", "Formatting: Success, Trash type (if available), student id and time:\n\n"] 
                success.writelines(L)
            self.first_save=True
        self.reward=[]
            
    def cycle(self):
        while True:
            messages={
                "waste":"2800 Kg",
                "tree":"382",
                "co2":"18982"
            }
            for i in range(1,4):
                print(i)
                start = pygame.time.get_ticks()
                barcode = Menu("Scanning",(850*wm,460*hm),"Place your id under the camera","Please Standby",text1color=(97,255,77),cycle=True,animation=i)
                id_card = barcode.main()
                end = pygame.time.get_ticks()
                print("start-end",end-start)
                print(id_card, "id card")
                try:
                    id_card = int(id_card)
                    if not id_card==None:
                        return id_card
                except TypeError and ValueError:
                    print("typeerror")
                    pass
        
        
    def page(self):
        id_card = self.cycle()
        uncotaminated = Menu(" Yes ",(650*wm,460*hm),"Is your trash","Uncontaminated?",text1color=(97,255,77),text2=" No ",text2center=(1000*wm, 460*hm),text2color=(255,59,59),student_id=id_card)
        uncotaminated = uncotaminated.main()
        if uncotaminated != " Yes ": 
            self.fail()
            return ["Fail",trash_type.replace(" ",""),id_card]
        page4 = Menu(" Yes ",(650*wm,460*hm),"Place trash on tray for identification","Loading...",text1color=(97,255,77),student_id=id_card)
        uncotaminated = page4.main()
        
        page6 = Menu("Exit ",(650*wm,460*hm),"Your trash is being consumed","Please stand by...",text1color=(97,255,77),text2="Spin",text2center=(1000*wm, 460*hm),text2color=(246, 142, 51),student_id=id_card)
        finish = page6.main()
        if finish=="Exit ":
            return ["Success",trash_type.replace(" ",""),id_card]
        return ["Success",trash_type.replace(" ",""),id_card]
        
    def unknown_material(self,id_card):   
        unknown = Menu(" Okay",(850*wm,460*hm),"Your trash can not be identified (Or not metal, plastic or paper)","Please try again!",text1color=(97,255,77),student_id=id_card)
        unknown.main() 
        
    def incorrect_material(self,id_card):
        incorrect = Menu(" Okay",(850*wm,460*hm),"You chose the wrong type!","Please be more careful.",text1color=(97,255,77),student_id=id_card)
        incorrect.main() 
        
    def fail(self):
        fail = Menu(" Okay",(850*wm,460*hm),"Your trash is not suitable for recycling","Please try again!",text1color=(97,255,77))
        fail.main()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
    def main(self):
        while True:
            temp = self.page()
            with open('save.txt','r') as save:
                lines = save.readlines()
            numsuccess = int(lines[0].replace("Success:",""))
            numfailure = int(lines[1].replace("Fail:",""))
            if temp[0]=="Success":
                numsuccess+=1
            else:
                numfailure+=1
            lines[0]="Success:"+str(numsuccess)+"\n"
            lines[1]="Fail:"+str(numfailure)+"\n"
            with open('save.txt','w') as success:
                success.writelines(lines)
                if not len(temp)==1:
                    success.write(temp[0]+" "+temp[1]+" "+temp[2]+" "+str(time.ctime())+"\n")
                else:
                    success.write(temp[0]+" "+str(time.ctime())+"\n")
                
touch_available=False
background = pygame.transform.scale(pygame.image.load("background.jpg"), (screen_width,screen_height))
river1 = []
max_frames=[]
max_frame=0
for count in range(len(os.listdir("river1"))):
    river1.append(pygame.transform.scale(pygame.image.load(f"river1/{count+1}.png"),(screen_width,screen_height)))
    max_frame=count
max_frames.append(max_frame)
    
river2 = []
for count in range(len(os.listdir("river2"))):
    river2.append(pygame.transform.scale(pygame.image.load(f"river2/{count+1}.png"),(screen_width,screen_height)))
    max_frame=count
max_frames.append(max_frame)

forest = []
for count in range(len(os.listdir("forest"))):
    forest.append(pygame.transform.scale(pygame.image.load(f"forest/{count+1}.png"),(screen_width,screen_height)))
    max_frame=count
max_frames.append(max_frame)

print(max_frames)
screen = pygame.display.set_mode((screen_width, screen_height),flags=pygame.FULLSCREEN)
# screen = pygame.display.set_mode((screen_width, screen_height))
page = pages()
page.main()
