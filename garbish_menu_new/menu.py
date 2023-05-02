import pygame
import sys
from os import path
import os 
import time
from random import random
from camera_run import get_pic#, get_barcode
import tensorflow as tf
from pygame._sdl2 import touch
from screeninfo import get_monitors
for m in get_monitors():
    screen_height=m.height
    screen_width=m.width
# screen_height=480
# screen_width=720
print(screen_height,screen_width)
model = tf.keras.models.load_model("./tiny_good_model1.model")

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
    def __init__(self,text1,text1center,small_title,big_title,font=name,font_render=xlname,font_2=sname,font_render_2=mname,text1color=(255,255,255),text2=None,text2center=None,text2color=(255,255,255),text3=None,text3center=None,text3color=(255,255,255),title="JCSE Recycling",spinner=False,spinner_rewards=None,spinner_chance=None,spinner_reward_page=False,spinner_reward_=None,student_id=None): #spinner_chance adds up to 1, its a list.
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
        #spinner
        self.spinner=spinner
        self.spinner_large_rect=(self.width*0.075,145*hm,1000*wm,350*hm)
        if self.spinner:
            self.spinner_rewards=spinner_rewards
            self.spinner_chance=spinner_chance
            self.spinner_rect=[]
            temp = 0 #previous x
            for i in range(len(self.spinner_chance)):
                self.spinner_rect.append((self.width*0.075+temp,145*hm,(self.spinner_chance[i]*1000+1)*wm,350*hm))
                temp+=(self.spinner_chance[i]*1000)*wm
        #spinner reward page
        self.spinner_reward_page=spinner_reward_page
        if self.spinner_reward_page:
            self.spinner_reward_rect=(self.width*0.35,145*hm,self.width*0.3,350*hm)
            self.spinner_reward=spinner_reward_
            self.current_frame=0
            self.current_frame2=0
            self.next_frame=False
            self.next_frame2=False
            pygame.time.set_timer(1,25)
            pygame.time.set_timer(2,40)

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
        self.mouse_pos = None
        self.keep_looping = True
        self.message = ""
        self.button = 0
        self.button_cooldown = 3

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
            elif self.spinner_reward_page and event.type==1:
                self.next_frame=True
            elif self.spinner_reward_page and event.type==2:
                self.next_frame2=True

    def draw_text_button(self,text, myrect, font, font_color=(0,0,0), background_color=(255,255,255), use_inner=False):
        inner_area = pygame.Rect((-22, -8, myrect[2], myrect[3]))
        pygame.draw.rect(self.screen, background_color, myrect,border_radius=20)
        txt_surface = font.render(text, True, font_color)
        if use_inner == True:
            self.screen.blit(txt_surface, myrect, inner_area)
        else:
            self.screen.blit(txt_surface, myrect)
    
    def draw(self):
        self.screen.blit(background, (0, 0))
        if self.spinner or self.spinner_reward_page:
            self.textboxrect = pygame.Rect(25*wm, 30*hm,self.width-(50)*wm, 125*hm)
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
        if not self.spinner and not self.spinner_reward_page:
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
            if len(self.message) > 0:
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
                
        if self.spinner:
            temp=0
            begin_color=(160,210,160)
            ending_color=(0,110,0)
            past_mid=0
            value_change=((begin_color[0]-ending_color[0])/len(self.spinner_chance),(begin_color[1]-ending_color[1])/len(self.spinner_chance),(begin_color[2]-ending_color[2])/len(self.spinner_chance))
            for i in range(len(self.spinner_chance)):
                if len(self.spinner_chance)/2<=i:
                    past_mid+=1
                    pygame.draw.rect(self.screen,(begin_color[0]-value_change[0]*(i-past_mid)+value_change[0]*past_mid,begin_color[1]-value_change[1]*(i-past_mid)+value_change[1]*past_mid,begin_color[2]-value_change[2]*(i-past_mid)+value_change[2]*past_mid),self.spinner_rect[i])
                else:
                    pygame.draw.rect(self.screen,(begin_color[0]-value_change[0]*i,begin_color[1]-value_change[1]*i,begin_color[2]-value_change[2]*i,),self.spinner_rect[i])
                text = xxsname.render(self.spinner_rewards[i], True, BLACK, None)
                textRect = text.get_rect(center=(self.width*0.075+temp+(self.spinner_chance[i]*500)*wm,320*hm))
                self.screen.blit(text, textRect)
                temp+=(self.spinner_chance[i]*1000)*wm
            # for i in range(len(self.spinner_chance)):
            #     pygame.draw.rect(self.screen,(0,0,0),self.spinner_rect[i],width=2)
            pygame.draw.rect(self.screen,(0,0,0),self.spinner_large_rect,width=2)
        if self.spinner_reward_page:
            pygame.draw.rect(self.screen,(160,210,160),self.spinner_reward_rect)
            pygame.draw.rect(self.screen,(0,0,0),self.spinner_reward_rect,width=3)
            text = xxsname.render(self.spinner_reward, True, BLACK, None)
            textRect = text.get_rect(center=(self.width/2,320*hm))
            self.screen.blit(text, textRect)
            self.screen.blit(confetti_gif[self.current_frame],(0,0))
            if self.spinner_reward=="25 G-Coin":
                self.screen.blit(confetti_gif2[self.current_frame2],(0,0))
            if self.next_frame:
                if not self.current_frame>=max_frame:
                    self.current_frame+=1
                else:
                    self.current_frame=0
                self.next_frame=False
            if self.next_frame2:
                if not self.current_frame2>=max_frame2:
                    self.current_frame2+=1
                else:
                    self.current_frame2=0
                self.next_frame2=False
        # if self.spinner or self.spinner_reward_page:
        #     pygame.draw.polygon(self.screen,(250,225,0),[(self.width/2-50,self.spinner_large_rect[1]-10),(self.width/2,self.spinner_large_rect[1]+50),(self.width/2+50,self.spinner_large_rect[1]-10)])
        #     pygame.draw.polygon(self.screen,(250,225,0),[(self.width/2-50,self.spinner_large_rect[1]+self.spinner_large_rect[3]+10),(self.width/2,self.spinner_large_rect[1]+self.spinner_large_rect[3]-50),(self.width/2+50,self.spinner_large_rect[1]+self.spinner_large_rect[3]+10)])
        #     #borders
        #     pygame.draw.polygon(self.screen,(0,0,0),[(self.width/2-50,self.spinner_large_rect[1]-10),(self.width/2,self.spinner_large_rect[1]+50),(self.width/2+50,self.spinner_large_rect[1]-10)],width=3)
        #     pygame.draw.polygon(self.screen,(0,0,0),[(self.width/2-50,self.spinner_large_rect[1]+self.spinner_large_rect[3]+10),(self.width/2,self.spinner_large_rect[1]+self.spinner_large_rect[3]-50),(self.width/2+50,self.spinner_large_rect[1]+self.spinner_large_rect[3]+10)],width=3)
        if not self.spinner and not self.spinner_reward_page:
            self.screen.blit(fairy, (15*hm, self.height*0.4))
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.events()
            self.draw()
            if self.touchquitcount==10:
                pygame.quit()
                sys.exit()
        return self.message

class pages():        
    def __init__(self):
        if path.exists('save.txt'): 
            self.first_save=False
        else:
            with open('save.txt','a') as success:
                L = ["Success:0\n", "Fail:0\n", "Formatting: Success, Material (if available), student id and time:\n\n"] 
                success.writelines(L)
            self.first_save=True
        self.reward=[]
            
        
    def page(self):
        #(850,460) for 1280
        # while True:
        page1 = Menu(" Begin",(850*wm,460*hm),"Welcome, please click Begin to","Scan your ID",text1color=(97,255,77))
        message = page1.main()
        id_card="0012113"
        # while True:
        #     barcode = Menu("Scanning",(850*wm,460*hm),"Place your id under the camera","Please standby (Click Scanning to continue)",text1color=(97,255,77))
        #     barcode.main()
        #     id_card = get_barcode()
        #     if not id_card==None:
        #         break
        #(650,460) (1050, 460)
        page2 = Menu(" Yes ",(650*wm,460*hm),"Is your trash wholly composed of","Metal, Plastic, Paper?",text1color=(97,255,77),text2=" No ",text2center=(1000*wm,460*hm),text2color=(255,59,59),student_id=id_card)
        recycle_check = page2.main()
        if recycle_check != " Yes ": 
            self.fail()
            return ["Fail"]
        page3 = Menu("         Metal   ",(850*wm,355*hm),"Please select","Metal, Plastic, Paper",font=mname,font_render=lname,text1color=(39,39,39),text2="        Plastic  ",text2center=(850*wm,499*hm),text2color=(90,90,90),text3="         Paper  ",text3center=(850*wm,645*hm),text3color=(172,172,172))
        material = page3.main()
        material = material.replace(" ","")
        pic_check = get_pic(model)
        same_material=False
        print(pic_check)
        if pic_check==material:
            print("unlock")
            #unlcok
            same_material=True
        material_types=['metal', 'paper', 'plastic']
        material_other=True
        if not same_material:
            for i in range(3):
                if pic_check==material_types[i]:
                    material=material_types[i]
                    self.incorrect_material(id_card=id_card)
                    break
            if material_other:
                self.unknown_material(id_card=id_card)
                return ["Fail"]
        #get_weight - regurns wieght in kg
        #lock(), unlock() - physical stuff
        page4 = Menu(" Yes ",(650*wm,460*hm),"Is your trash","Uncontaminated?",text1color=(97,255,77),text2=" No ",text2center=(1000*wm, 460*hm),text2color=(255,59,59),student_id=id_card)
        uncotaminated = page4.main()
        if uncotaminated != " Yes ": 
            self.fail()
            return ["Fail",material.replace(" ",""),id_card]
        page5 = Menu(" Yes ",(650*wm,460*hm),"Your trash is suitable for recycling","Confirm?",text1color=(97,255,77),text2=" No ",text2center=(1000*wm, 460*hm),text2color=(255,59,59),student_id=id_card)
        confirmation = page5.main()
        if confirmation != " Yes ": 
            self.fail()
            return ["Fail",material.replace(" ",""),id_card]
        page6 = Menu("Exit ",(650*wm,460*hm),"Your trash is being consumed","Please stand by...",text1color=(97,255,77),text2="Spin",text2center=(1000*wm, 460*hm),text2color=(246, 142, 51),student_id=id_card)
        finish = page6.main()
        if finish=="Exit ":
            return ["Success",material.replace(" ",""),id_card]
        self.spinner(material,id_card)
        return ["Success",material.replace(" ",""),id_card]
        
    def spinner(self,material,id_card):
        page7 = Menu("Exit ",(250*wm,600*hm),"Spend 1 R Buck to draw a random reward?","Placeholder",text1color=(97,255,77),text2="Spin",text2center=(1000*wm, 600*hm),text2color=(246, 142, 51),spinner=True,spinner_rewards=["1 G-Coin","5 G-Coin","25 G-Coin","5 G-Coin","1 G-Coin"],spinner_chance=[0.30,0.15,0.10,0.15,0.30])
        ifspin = page7.main()
        if ifspin=="Exit ":
            return ["Success",material.replace(" ",""),id_card]
        temp = random()
        if temp>=0.98:
            reward="25 G-Coin"
        elif temp>=0.7:
            reward="5 G-Coin"
        else:
            reward="1 G-Coin"
        #need to store this in the database. 
        self.reward.append(reward)
        self.spin(reward,material,id_card)
        return ["Success",material.replace(" ",""),reward,id_card]
        
    def spin(self,reward,material,id_card):
        spin = Menu("Exit ",(250*wm,600*hm),"Your reward:","Placeholder",text1color=(97,255,77),text2="Spin",text2center=(1000*wm, 600*hm),text2color=(246, 142, 51),spinner_reward_page=True,spinner_reward_=reward)
        check = spin.main()
        if check=="Spin":
            item = self.spinner(material,id_card) #could extract data from here through returns
        
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
                
touch_available=True
try:
    deviceid = touch.get_device(0)
except:
    touch_available = False
#720, 480
#1280,720
# screen_width=720
# screen_height=480
# screen_width=1280 #0.5625
# screen_height=720 #0.6667
background = pygame.transform.scale(pygame.image.load("background.jpg"), (screen_width,screen_height))
# fairy = pygame.image.load("recyclefairy.png")
fairy = pygame.transform.scale(pygame.image.load("recyclefairy.png"),(500*wm,500*wm))
confetti_gif=[]
confetti_gif2=[]
for count in range(len(os.listdir("reward_confetti"))):
    confetti_gif.append(pygame.transform.scale(pygame.image.load(f"reward_confetti/{count+1}.png"),(screen_width,screen_height)))
    max_frame=count
for count in range(len(os.listdir("confetti2"))):
    confetti_gif2.append(pygame.transform.scale(pygame.image.load(f"confetti2/{count+1}.png"),(screen_width,screen_height)))
    max_frame2=count
# screen = pygame.display.set_mode((screen_width, screen_height),flags=pygame.FULLSCREEN)
screen = pygame.display.set_mode((screen_width, screen_height))
page = pages()
page.main()