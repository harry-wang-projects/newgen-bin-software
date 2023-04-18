import pygame
import sys
from os import path
import os 
import time
from random import random
# from pygame._sdl2 import touch
pygame.init()

xlname = pygame.font.Font("Somatic-Rounded.otf",150)
lname = pygame.font.Font("Somatic-Rounded.otf",115)
name = pygame.font.Font("Somatic-Rounded.otf",110)
xxsname = pygame.font.Font("Somatic-Rounded.otf",20)
xsname = pygame.font.Font("Somatic-Rounded.otf",30)
sname = pygame.font.Font("Somatic-Rounded.otf",50)
mname = pygame.font.Font("Somatic-Rounded.otf",80)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
class Menu(): #creates a menu with 3 buttons and the title on the top.
    def __init__(self,text1,text1center,small_title,big_title,font=name,font_render=xlname,text1color=(255,255,255),text2=None,text2center=None,text2color=(255,255,255),text3=None,text3center=None,text3color=(255,255,255),title="JCSE Recycling",screen_width=1280,screen_height=720,spinner=False,spinner_rewards=None,spinner_chance=None,spinner_reward_page=False,spinner_reward_=None): #spinner_chance adds up to 1, its a list.
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((self.width, self.height),flags=pygame.FULLSCREEN)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = font
        self.font_render = font_render
        # self.change = pygame.mixer.Sound('confirm.wav')
        self.st=small_title
        self.bt=big_title
        self.textboxrect = pygame.Rect(75, 30,self.width-150, 250)
        #spinner
        self.spinner=spinner
        self.spinner_large_rect=(130,145,1000,350)
        if self.spinner:
            self.spinner_rewards=spinner_rewards
            self.spinner_chance=spinner_chance
            self.spinner_rect=[]
            temp = 0 #previous x
            for i in range(len(self.spinner_chance)):
                self.spinner_rect.append((130+temp,145,self.spinner_chance[i]*1000,350))
                temp+=self.spinner_chance[i]*1000
        #spinner reward page
        self.spinner_reward_page=spinner_reward_page
        if self.spinner_reward_page:
            self.spinner_reward_rect=(self.width/2-200,145,400,350)
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
        key = pygame.key.get_pressed()
        # if touch_available:
        #     self.finger_data = touch.get_finger(0)
        for event in pygame.event.get():
            # if touch_available and self.finger_data['pressure']>=0.1:
            #     self.screen_touch=True
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
        inner_area = pygame.Rect((-28, -15, myrect[2], myrect[3]))
        pygame.draw.rect(self.screen, background_color, myrect,border_radius=20)
        txt_surface = font.render(text, True, font_color)
        if use_inner == True:
            self.screen.blit(txt_surface, myrect, inner_area)
        else:
            self.screen.blit(txt_surface, myrect)
    
    def draw(self):
        self.screen.blit(background, (0, 0))
        if self.spinner or self.spinner_reward_page:
            self.textboxrect = pygame.Rect(75, 30,self.width-150, 100)
        pygame.draw.rect(self.screen, (214,240,232), self.textboxrect, border_radius=30)
        text = sname.render(self.st, True, BLACK, None)
        textRect = text.get_rect(center=(self.width/2,self.height/2))
        textRect.center = ((self.width/2,80))
        self.screen.blit(text, textRect)
        text2 = name.render(self.bt, True, BLACK, None)
        textRect2 = text2.get_rect()
        textRect2.center = ((self.width/2,180))
        if not self.spinner and not self.spinner_reward_page:
            self.screen.blit(text2, textRect2)
        self.draw_text_button(self.text1_text, self.text1_rect, self.font,use_inner=True,background_color=self.text1_color)
        if self.text2_text!=None:
            self.draw_text_button(self.text2_text, self.text2_rect, self.font, use_inner=True,background_color=self.text2_color)
        if self.text3_text!=None:
            self.draw_text_button(self.text3_text, self.text3_rect, self.font, use_inner=True,background_color=self.text3_color)
            
        if not self.mouse_pos == None:
            if self.text1_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.message = self.text1_text
            if not self.text2_text==None and self.text2_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.message = self.text2_text
            if not self.text3_text==None and self.text3_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])==1:
                self.message = self.text3_text
            self.mouse_pos = None
            if len(self.message) > 0:
                self.keep_looping = False
        # if touch_available and self.screen_touch:
        #     if self.text1_rect.collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
        #         self.message = self.text1_text
        #     if not self.text2_text==None and self.text2_rect.collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
        #         self.message = self.text2_text
        #     if not self.text3_text==None and self.text3_rect.collidepoint(self.finger_data['x'],self.finger_data['y'])==1:
        #         self.message = self.text3_text
        #     self.mouse_pos = None
        #     if len(self.message) > 0:
        #         self.keep_looping = False
                
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
                textRect = text.get_rect(center=(130+temp+self.spinner_chance[i]*500,320))
                self.screen.blit(text, textRect)
                temp+=self.spinner_chance[i]*1000
            for i in range(len(self.spinner_chance)):
                pygame.draw.rect(self.screen,(0,0,0),self.spinner_rect[i],width=1)
            pygame.draw.rect(self.screen,(0,0,0),self.spinner_large_rect,width=3)
        if self.spinner_reward_page:
            pygame.draw.rect(self.screen,(160,210,160),self.spinner_reward_rect)
            pygame.draw.rect(self.screen,(0,0,0),self.spinner_reward_rect,width=3)
            text = xxsname.render(self.spinner_reward, True, BLACK, None)
            textRect = text.get_rect(center=(self.width/2,320))
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
            
            
        if self.spinner or self.spinner_reward_page:
            pygame.draw.polygon(self.screen,(250,225,0),[(self.width/2-50,self.spinner_large_rect[1]-10),(self.width/2,self.spinner_large_rect[1]+50),(self.width/2+50,self.spinner_large_rect[1]-10)])
            pygame.draw.polygon(self.screen,(250,225,0),[(self.width/2-50,self.spinner_large_rect[1]+self.spinner_large_rect[3]+10),(self.width/2,self.spinner_large_rect[1]+self.spinner_large_rect[3]-50),(self.width/2+50,self.spinner_large_rect[1]+self.spinner_large_rect[3]+10)])
            #borders
            pygame.draw.polygon(self.screen,(0,0,0),[(self.width/2-50,self.spinner_large_rect[1]-10),(self.width/2,self.spinner_large_rect[1]+50),(self.width/2+50,self.spinner_large_rect[1]-10)],width=3)
            pygame.draw.polygon(self.screen,(0,0,0),[(self.width/2-50,self.spinner_large_rect[1]+self.spinner_large_rect[3]+10),(self.width/2,self.spinner_large_rect[1]+self.spinner_large_rect[3]-50),(self.width/2+50,self.spinner_large_rect[1]+self.spinner_large_rect[3]+10)],width=3)
        if not self.spinner and not self.spinner_reward_page:
            self.screen.blit(fairy, (10, 225))
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.events()
            self.draw()
        return self.message

class pages():        
    def __init__(self):
        if path.exists('save.txt'): 
            self.first_save=False
        else:
            with open('save.txt','a') as success:
                L = ["Success:0\n", "Fail:0\n", "Formatting: Success, Material (if available) and time:\n\n"] 
                success.writelines(L)
            self.first_save=True
        self.reward=[]
            
        
    def page(self):
        page1 = Menu("  Begin",(850,460),"Welcome, please click Begin to","Scan your ID",text1color=(97,255,77))
        message = page1.main()
        #need to add a section that scans ur id. 
        page2 = Menu(" Yes ",(650,460),"Is your trash wholly composed of","Metal, Plastic, Paper?",text1color=(97,255,77),text2="  No ",text2center=(1050, 460),text2color=(255,59,59))
        recycle_check = page2.main()
        if recycle_check != " Yes ": 
            self.fail()
            return ["Fail"]
        page3 = Menu("         Metal   ",(850,355),"Please select","Metal, Plastic, Paper",font=mname,font_render=lname,text1color=(39,39,39),text2="        Plastic  ",text2center=(850,499),text2color=(90,90,90),text3="         Paper  ",text3center=(850,645),text3color=(172,172,172))
        material = page3.main()
        page4 = Menu(" Yes ",(650,460),"Is your trash","Uncontaminated?",text1color=(97,255,77),text2="  No ",text2center=(1050, 460),text2color=(255,59,59))
        uncotaminated = page4.main()
        if uncotaminated != " Yes ": 
            self.fail()
            return ["Fail",material.replace(" ","")]
        page5 = Menu(" Yes ",(650,460),"Your trash is suitable for recycling","Confirm?",text1color=(97,255,77),text2="  No ",text2center=(1050, 460),text2color=(255,59,59))
        confirmation = page5.main()
        if confirmation != " Yes ": 
            self.fail()
            return ["Fail",material.replace(" ","")]
        page6 = Menu(" Exit",(650,460),"Your trash is being consumed","Please stand by...",text1color=(97,255,77),text2=" Spin",text2center=(1050, 460),text2color=(246, 142, 51))
        finish = page6.main()
        if finish==" Exit":
            return ["Success",material.replace(" ","")]
        self.spinner(material)
        
    def spinner(self,material):
        page7 = Menu(" Exit",(250,600),"Spend 1 R Buck to draw a random reward?","Placeholder",text1color=(97,255,77),text2=" Spin",text2center=(1050, 600),text2color=(246, 142, 51),spinner=True,spinner_rewards=["1 G-Coin","5 G-Coin","25 G-Coin","5 G-Coin","1 G-Coin"],spinner_chance=[0.30,0.15,0.10,0.15,0.30])
        ifspin = page7.main()
        if ifspin==" Exit":
            return ["Success",material.replace(" ","")]
        temp = random()
        if temp>=0.98:
            reward="25 G-Coin"
        elif temp>=0.7:
            reward="5 G-Coin"
        else:
            reward="1 G-Coin"
        #need to store this in the database. 
        self.reward.append(reward)
        self.spin(reward,material)
        return ["Success",material.replace(" ",""),reward]
        
    def spin(self,reward,material):
        spin = Menu(" Exit",(250,600),"Your reward:","Placeholder",text1color=(97,255,77),text2=" Spin",text2center=(1050, 600),text2color=(246, 142, 51),spinner_reward_page=True,spinner_reward_=reward)
        check = spin.main()
        if check==" Spin":
            item = self.spinner(material) #could extract data from here through returns
            
        
    def fail(self):
        fail = Menu("  Okay",(850,460),"Your trash is not suitable for recycling","Please try again!",text1color=(97,255,77))
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
                    success.write(temp[0]+" "+temp[1]+" "+str(time.ctime())+"\n")
                else:
                    success.write(temp[0]+" "+str(time.ctime())+"\n")
                
# touch_available=True
# try:
#     deviceid = touch.get_device(0)
# except:
#     touch_available = False
screen_width=1024
screen_height=600
background = pygame.transform.scale(pygame.image.load("background.jpg"), (screen_width,screen_height))
fairy = pygame.image.load("recyclefairy.png")
confetti_gif=[]
confetti_gif2=[]
for count in range(len(os.listdir("reward_confetti"))):
    confetti_gif.append(pygame.transform.scale(pygame.image.load(f"reward_confetti/{count+1}.png"),(screen_width,screen_height)))
    max_frame=count
for count in range(len(os.listdir("confetti2"))):
    confetti_gif2.append(pygame.transform.scale(pygame.image.load(f"confetti2/{count+1}.png"),(screen_width,screen_height)))
    max_frame2=count
page = pages()
page.main()