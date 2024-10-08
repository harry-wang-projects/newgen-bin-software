import pygame
import sys
from os import path
import os 
import time
from random import random
from camera_run import get_pic, verify_classes#, get_barcode
from pygame._sdl2 import touch
from screeninfo import get_monitors
# from barcode_get import get_barcode
from garbage_list import trash_list, plastic_mass, plastic_count, get_trash_stats
from hardware_commands import get_weight, unlock
from send_api import send_to_server, id_default, password_default
from wait_change import wait_action, get_action

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
xxlname = pygame.font.Font("Somatic-Rounded.otf",int(150*wm))
xlname = pygame.font.Font("Somatic-Rounded.otf",int(135*wm))
lname = pygame.font.Font("Somatic-Rounded.otf",int(115*wm))
name = pygame.font.Font("Somatic-Rounded.otf",int(110*wm))
xxsname = pygame.font.Font("Somatic-Rounded.otf",int(20*wm))
xsname = pygame.font.Font("Somatic-Rounded.otf",int(30*wm))
sname = pygame.font.Font("Somatic-Rounded.otf",int(60*wm))
mname = pygame.font.Font("Somatic-Rounded.otf",int(80*wm))
msname = pygame.font.Font("Somatic-Rounded.otf",int(60*wm))
cname=pygame.font.Font("Somatic-Rounded.otf",int(25*wm))
underline = pygame.font.SysFont("arial",int(80*wm))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
class Menu(): #creates a menu with 3 buttons and the title on the top.
    def __init__(self,text1,text1center,small_title,big_title,font=name,font_render=xlname,font_2=sname,font_render_2=mname,text1color=(255,255,255),text2=None,text2center=None,text2color=(255,255,255),text3=None,text3center=None,text3color=(255,255,255),title="Recycle Royale Bin UI",student_id=None,cycle=False,animation=None,get_id=None,timer=None,exit_=True): #spinner_chance adds up to 1, its a list.
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
            self.student_id_rect = self.font_render_2.render(self.student_id_text, True, BLACK, None).get_rect(center=(1000*wm,600*hm)) #(620,400,120,50)
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
        # if self.cycle:
        #     self.cycle_time=10000 #msec
        #     self.animation=animation
        #     self.max_frame=max_frames[animation-1]
        self.mouse_pos = None
        self.keep_looping = True
        self.message = ""
        self.button = 0
        self.button_cooldown = 3
        # self.current_frame=0
        # self.next_frame=True
        self.detect_id_card = "" #barcode
        self.key_id_card = "" #keyboard
        self.credit = "Made by Edwin Fang & Harry Wang"
        self.credit_font = cname.render(self.credit, True, WHITE, None)
        self.credit_rect = self.credit_font.get_rect(center=(self.width/2,self.height*0.925))
        self.exit_=exit_
        
        self.timer=timer
        self.get_id = get_id
        if self.get_id:
            self.key_board_large_rect = pygame.rect.Rect(self.width*0.075+(self.width/10)*3,self.height*0.4,(self.width/10)*3,(self.height*0.12)) 
            self.key_board_rect = []
            self.key_board_font = []
            self.key_board_font_rect = []
            self.key_board_result = ""
            self.key_board_underline = "_______"
            self.key_board_underline_rect = pygame.rect.Rect(self.width*0.083+(self.width/10)*3,self.height*0.4,self.width*0.08,self.height*0.08)
            self.key_board_underline_font = underline.render(self.key_board_underline,True,BLACK,None)
            
            self.key_zero_font = mname.render(" 0 ",True,BLACK,None)
            w,h = mname.size(" 0 ") #width and height of font
            self.key_zero = self.key_zero_font.get_rect(center=(self.width*0.055+(self.width/10)*2-w/2,self.height*0.9-h/2))
            
            self.key_del_font = mname.render(" x ",True,BLACK,None)
            w,h = mname.size(" x ") #width and height of font
            self.key_del = self.key_del_font.get_rect(center=(self.width*0.05+(self.width/10)-w/2,self.height*0.9-h/2))
            
            self.key_enter_font = mname.render("ok",True,BLACK,None)
            w,h = mname.size("ok") #width and height of font
            self.key_enter = self.key_enter_font.get_rect(center=(self.width*0.05+(self.width/10)*3-w/2,self.height*0.9-h/2))
            self.enter=False
            actual = 1
            for i in range(3):
                temp = []
                temp1 = []
                temp2 = []
                for y in range(3):
                    item = pygame.rect.Rect(self.width*0.075+(self.width/10)*y,self.height*0.7+(self.height*0.12)*i,self.width*0.08,self.height*0.08) #not needed i think
                    item1 = mname.render(" "+str(actual)+" ",True,BLACK, None)
                    if actual==1:
                        item1 = mname.render(" "+str(actual)+"  ",True,BLACK, None)
                    item2 = item1.get_rect(center=(self.width*0.075+(self.width/10)*y+self.width*0.04,self.height*0.425+(self.height*0.125)*i+self.height*0.04))
                    actual+=1
                    temp.append(item)
                    temp1.append(item1)
                    temp2.append(item2)
                self.key_board_rect.append(temp)
                self.key_board_font.append(temp1)
                self.key_board_font_rect.append(temp2)

    def barcode(self,event):
        if self.get_id:
            if event == pygame.KEYDOWN:
                key=pygame.key.get_pressed()
                if key[pygame.K_0]:
                    self.detect_id_card=str(self.detect_id_card)+str(0)
                if key[pygame.K_1]:
                    self.detect_id_card=str(self.detect_id_card)+str(1)
                if key[pygame.K_2]:
                    self.detect_id_card=str(self.detect_id_card)+str(2)
                if key[pygame.K_3]:
                    self.detect_id_card=str(self.detect_id_card)+str(3)
                if key[pygame.K_4]:
                    self.detect_id_card=str(self.detect_id_card)+str(4)
                if key[pygame.K_5]:
                    self.detect_id_card=str(self.detect_id_card)+str(5)
                if key[pygame.K_6]:
                    self.detect_id_card=str(self.detect_id_card)+str(6)
                if key[pygame.K_7]:
                    self.detect_id_card=str(self.detect_id_card)+str(7)
                if key[pygame.K_8]:
                    self.detect_id_card=str(self.detect_id_card)+str(8)
                if key[pygame.K_9]:
                    self.detect_id_card=str(self.detect_id_card)+str(9)
                if key[pygame.K_RETURN]:
                    return self.detect_id_card
            if len(str(self.detect_id_card))==7:  
                try:
                    #self.detect_id_card = int(self.detect_id_card)
                    if not self.detect_id_card==None:
                        return self.detect_id_card
                except TypeError:
                    print("typeerror")
            return "unsuccess"

    def events(self):
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
            self.barcode(event.type)

    def draw_text_button(self,text, myrect, font, font_color=(0,0,0), background_color=(255,255,255), use_inner=False):
        inner_area = pygame.Rect((-22, -8, myrect[2], myrect[3]))
        pygame.draw.rect(self.screen, background_color, myrect,border_radius=20)
        txt_surface = font.render(text, True, font_color)
        if use_inner == True:
            self.screen.blit(txt_surface, myrect, inner_area)
        else:
            self.screen.blit(txt_surface, myrect)
    
    # def animation_detect(self):
        # if self.cycle:
        #     if self.animation==1:
        #         self.screen.blit(river1[self.current_frame],(0,0))
            # if self.animation==2:
            #     self.screen.blit(river2[self.current_frame],(0,0))
            # if self.animation==3:
            #     self.screen.blit(forest[self.current_frame],(0,0))
        
    
    def draw(self):
        self.screen.blit(background, (0, 0))
        # self.animation_detect()
        # if self.cycle:
        #     if self.next_frame:
        #         if not self.current_frame>=self.max_frame:
        #             self.current_frame+=1
        #         else:
        #             self.current_frame=0
        #         self.next_frame=False
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
        
        if self.get_id:
            pygame.draw.rect(self.screen, (240,240,240), self.key_board_large_rect, border_radius=10)
            for i in range(3):
                for x in range(3):
                    pygame.draw.rect(self.screen, (230,230,230), self.key_board_font_rect[i][x], border_radius=10)
                    self.screen.blit(self.key_board_font[i][x],self.key_board_font_rect[i][x])
            self.screen.blit(self.key_board_underline_font,self.key_board_underline_rect)
            temp = mname.render(self.key_id_card,True,BLACK,None)
            self.screen.blit(temp,self.key_board_underline_rect)
            pygame.draw.rect(self.screen, (230,230,230), self.key_enter, border_radius=10)
            self.screen.blit(self.key_enter_font,self.key_enter)
            pygame.draw.rect(self.screen, (230,230,230), self.key_del, border_radius=10)
            self.screen.blit(self.key_del_font,self.key_del)
            pygame.draw.rect(self.screen, (230,230,230), self.key_zero, border_radius=10)
            self.screen.blit(self.key_zero_font,self.key_zero)
        else:
            self.screen.blit(fairy, (15*hm, self.height*0.4))
            
        if not self.mouse_pos == None:
            if self.get_id:
                actual=1
                for i in range(3):
                    for x in range(3):
                        if self.key_board_font_rect[i][x].collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                            if not len(self.key_id_card)>=7:
                                self.key_id_card=str(self.key_id_card)+str(actual)
                        actual=actual+1
                if self.key_enter.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                    #self.enter = True
                    actual = 0
                    self.key_id_card = ""
                if self.key_del.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                    if len(self.key_id_card)>=1:
                        temp1 = len(self.key_id_card) #index
                        self.key_id_card = self.key_id_card[:temp1-1]
                if self.key_zero.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                    if not len(self.key_id_card)>=7:
                        self.key_id_card=str(self.key_id_card)+'0'
            if self.touchquitrect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.touchquitcount+=1
            if self.text1_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.message = self.text1_text
                self.enter = True
            if not self.text2_text==None and self.text2_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.message = self.text2_text
            if not self.text3_text==None and self.text3_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.message = self.text3_text
            self.mouse_pos = None
            if len(self.message) > 0 and self.message!="Scanning" and self.message!=" 5R ":
                self.keep_looping = False
        if touch_available and self.screen_touch:
            if self.get_id:
                actual=1
                for i in range(3):
                    for x in range(3):
                        if self.key_board_font_rect[i][x].collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
                            if not len(self.key_id_card)>=7:
                                self.key_id_card=str(self.key_id_card)+str(actual)
                        actual=actual+1
                if self.key_enter.collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
                    self.enter = True
                if self.key_del.collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
                    if len(self.key_id_card)>=1:
                        temp1 = len(self.key_id_card) #index
                        self.key_id_card = self.key_id_card[:temp1-1]

                if self.key_zero.collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
                    if not len(self.key_id_card)>=7:
                        self.key_id_card=str(self.key_id_card) + '0'
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
        self.screen.blit(self.credit_font, self.credit_rect)
            
        pygame.display.flip()

    def main(self, wait_unlock):
        while self.keep_looping:
            self.events()
            self.draw()
            # print(self.key_id_card,"id")
            if self.touchquitcount==10:
                pygame.quit()
                sys.exit()
            if wait_unlock == True:
                if get_action() == True:
                    print("sleep 0.5")
                    time.sleep(0.5)
                    return self.message
            if self.get_id:
                if len(str(self.detect_id_card))==7:
                    self.detect_id_card = str(self.detect_id_card)
                    self.keep_looping=False
                    return self.detect_id_card
                if self.enter:
                    if len(str(self.key_id_card))==7:
                        self.key_id_card = str(self.key_id_card)
                        self.keep_looping=False
                        return self.key_id_card
                    self.enter=False
            current_time = pygame.time.get_ticks()
            if self.exit_ and (current_time-self.start_time)>=15000:
                return "exit"
            if self.timer !=None:
                print(current_time-self.start_time)
                if (current_time-self.start_time)>=self.timer:
                    return "timer"
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
            start = pygame.time.get_ticks()
            idle = Menu("Continue",(850*wm,460*hm), "Number of Bottles Recycled:", str(get_trash_stats()), font=xlname,font_render=xxlname, text1color=(97,255,77),exit_=False)
            #id_card = '0012113'
            msg = idle.main(True)
            return 
        
    def page(self):#use weight to detect change and when change move to page4
        get_trash_stats()
        temp = self.cycle()
        page3 = Menu("  Go! ",(800*wm,460*hm),"Place Item on Tray","Plastic Only",text1color=(97,255,77))
        loading = page3.main(False) 
        if loading=="exit":
            print("exit")
            return "exit"
        page4 = Menu("  Ok  ",(800*wm,460*hm),"Camera Scanning Item","Loading...",text1color=(97,255,77))
        print("harry123", trash_type)
        loading = page4.draw()
        if loading=="exit":
            print("exit")
            return "exit"
        temp, got_img = verify_classes(trash_type, True)
        #temp=True
        if not temp:
            self.fail()
            return ["Fail",trash_type]
        material_num = 0
        for i in range(3):
            if trash_type==trash_list[i + 1].name:
                material_num = i + 1
                break
        weight_inrange = True
        val = get_weight()
        print("type: ", type(val))
        print("weight of the thing:", val)
        print("minweight:", trash_list[material_num].min_weight)
        print("maxweight:", trash_list[material_num].max_weight)
        if val > trash_list[material_num].min_weight and val < trash_list[material_num].max_weight:
            weight_inrange = True
        else:
            weight_inrange = False
            self.too_heavy()
            return ["Fail",trash_type]
        page5 = Menu(" Unlocking",(800*wm,460*hm),"Place trash on tray for identification","Trash is Acceptable",text1color=(97,255,77))
        unlocking = page5.draw()
        unlock()

        page6 = Menu(" Exit ",(650*wm,460*hm),"Your trash is being consumed","Recieve Your Reward?",text1color=(97,255,77),text2="ID ",text2center=(1000*wm, 460*hm),text2color=(97,255,77))
        finish = page6.main(False)
        if finish=="Exit ":
            return ["Success",trash_type,val]
        if finish == "ID ":
            id_card = self.get_id()
            send_to_server(id_default, password_default, id_card, 1, got_img, val, 1) 
        return ["Success",trash_type,val,""]
        
    def fail(self):
        fail = Menu(" Okay",(800*wm,460*hm),"Your trash is not suitable for recycling","Please try again!",text1color=(97,255,77))
        fail.main(False)
        
    def too_heavy(self):
        fail = Menu(" Okay",(800*wm,460*hm),"Your trash is contaminated","Please try again!",text1color=(97,255,77))
        fail.main(False)
        
    def get_id(self):
        get_id = Menu(" 5R ",(850*wm,460*hm),"Type in or scan your ID Card","Your Reward:",text1color=(97,255,77),get_id=True)
        id_card = get_id.main(False)
        print(id_card, "id_card in get_id")
        return id_card
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
    def main(self):
        while True:
            temp = self.page()
            #send to api thing here. Format = "Success, trash_type, val, id_card" or "Fail, trash_type, id_card"
            
            # with open('save.txt','r') as save:
            #     lines = save.readlines()
            # numsuccess = int(lines[0].replace("Success:",""))
            # numfailure = int(lines[1].replace("Fail:",""))
            # if temp[0]=="Success":
            #     numsuccess+=1
            # else:
            #     numfailure+=1
            # lines[0]="Success:"+str(numsuccess)+"\n"
            # lines[1]="Fail:"+str(numfailure)+"\n"
            # with open('save.txt','w') as success:
            #     success.writelines(lines)
            #     if not len(temp)==1:
            #         success.write(temp[0]+" "+temp[1]+" "+temp[2]+" "+str(time.ctime())+"\n")
            #     else:
            #         success.write(temp[0]+" "+str(time.ctime())+"\n")
            
                
fairy = pygame.transform.scale(pygame.image.load("recyclefairy.png"),(500*wm,500*wm))
touch_available=False
background = pygame.transform.scale(pygame.image.load("background.jpg"), (screen_width,screen_height))
river1 = []
# max_frames=[]
# max_frame=0
# for count in range(len(os.listdir("river1"))):
#     river1.append(pygame.transform.scale(pygame.image.load(f"river1/{count+1}.jpeg"),(screen_width,screen_height)))
#     max_frame=count
# max_frames.append(max_frame)
    
# river2 = []
# for count in range(len(os.listdir("river2"))):
#     river2.append(pygame.transform.scale(pygame.image.load(f"river2/{count+1}.jpeg"),(screen_width,screen_height)))
#     max_frame=count
# max_frames.append(max_frame)

# forest = []
# for count in range(len(os.listdir("forest"))):
#     forest.append(pygame.transform.scale(pygame.image.load(f"forest/{count+1}.jpeg"),(screen_width,screen_height)))
#     max_frame=count
# max_frames.append(max_frame)

# print(max_frames)
screen = pygame.display.set_mode((screen_width, screen_height),flags=pygame.FULLSCREEN)
# screen = pygame.display.set_mode((screen_width, screen_height))
page = pages()
page.main()
