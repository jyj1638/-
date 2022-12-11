import pygame
from pygame import mixer
from pygame.mixer import music
import random
from time import sleep
pygame.mixer.init()

#초기설정
WHITE= (255,255,255)
RED= (255,0,0)
YELLOW=(255,255,0)

pad_width=1024
pad_height=512
background_width=1024

penguin_width=70
penguin_height=70

present_width=110
present_height=67

eagle_width=70 
eagle_height=70
fireball_width=130
fireball_height=60


def textObj(text, font):
    textSurface=font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def dispMessage(text):
    global gamepad
    
    largeText=pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect=textObj(text, largeText)
    TextRect.center=((pad_width/2),(pad_height/2))
    gamepad.blit(TextSurf,TextRect)
    pygame.display.update()
    sleep(2)
    pygame.mixer.music.unpause()
    runGame()

def crash():
    global gamepad
    global gameover_sound
    
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(gameover_sound)
    dispMessage('Game Over')

    
def drawObject(obj,x,y):
    global gamepad
    gamepad.blit(obj,(x,y))

def runGame():
    global gamepad, penguin, clock, background1, background2
    global present, fires, bullet, boom, fireball_height, fireball_width,score
    global shot_sound, complete_sound, gameover_sound
    
    isShotpresent =False
    boom_count=0
    score=0
    
    bullet_xy=[]
    
    #팽귄 좌표
    x=pad_width*0.05
    y=pad_height*0.8
    y_change=0
    
    background1_x=0
    background2_x=background_width
    
    present_x=pad_width
    present_y=random.randrange(0,pad_height)
    
    #장애물 좌표
    fire_x=pad_width
    fire_y=random.randrange(0,pad_height)
    random.shuffle(fires)
    fire=fires[0]
    
  
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed=True
                
            if event.type == pygame.KEYDOWN: #키 누를때
                if event.key == pygame.K_UP:  #위 방향키
                    y_change=-5 
                elif event.key == pygame.K_DOWN: #아래 방향키
                    y_change=5
                
                elif event.key == pygame.K_LCTRL: #컨트롤 키
                    pygame.mixer.Sound.play(shot_sound)
                    bullet_x=x+penguin_width  #눈뭉치 발사 위치 
                    bullet_y=y+penguin_height/2
                    bullet_xy.append([bullet_x,bullet_y])
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change=0
        
        #배경화면
        background1_x-=2
        background2_x-=2
        
        if background1_x == -background_width:
            background1_x=background_width
            
        if background2_x == -background_width:
            background2_x=background_width
        
        drawObject(background1, background1_x,0)
        drawObject(background2, background2_x,0)
        
        #펭귄이 화면밖으로 못나가게하기
        y += y_change
        if y < 0:
            y=0
        elif y > pad_height-penguin_height:
            y=pad_height-penguin_height
        
        #선물 생성위치
        present_x-=7
        if present_x <= 0:
            present_x=pad_width
            present_y=random.randrange(0,pad_height)
        
        #독수리,불꽃이 다가옴
        if fire[1]==None:
            fire_x-=30
        else:
            fire_x-=15
            
        if fire_x <=0:
            fire_x=pad_width
            fire_y=random.randrange(250,pad_height)
            random.shuffle(fires)
            fire=fires[0]
            
        #눈뭉치가 날라감
        if len(bullet_xy)!=0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0]=bxy[0]
                
                if bxy[0]>present_x:
                    if bxy[1]>present_y and bxy[1]<present_y+present_height:
                        bullet_xy.remove(bxy)
                        isShotpresent=True  #선물을 맞추면 10점 획득
                        score += 10
                         
                    if bxy[0] >= pad_width:
                        try:
                            bullet_xy.remove(bxy)
                        except:
                            pass
                        
         #점수                   
        score_font=pygame.font.Font(None, 50)
        score_image=score_font.render("score{}".format(score),True,RED)
        gamepad.blit(score_image,(850,30))
        
            
        if x + penguin_width >present_x: #선물이 펭귄을 지나갈때
            #선물이 펭귄과 부딪혔을때
            if(y>present_y and y<present_y+present_height)or\
            (y+penguin_height> present_y and y+penguin_height < present_y+present_height): 
                crash()
                
                
        if fire[1]!= None:
            if fire[0]==0: #독수리
                fireball_width=eagle_width
                fireball_height=eagle_height
            elif fire[0]==1: #불꽃
                fireball_width=fireball_width
                fireball_height=fireball_height
            
            if x+ penguin_width > fire_x:
                #독수리,불꽃에 부딪혔을때
                if(y>fire_y and y<fire_y+fireball_height)or\
                (y+penguin_height>fire_y and penguin_height<fire_y+fireball_height):
                    crash()
                    
        drawObject(penguin,x,y)
        
        #선물을 획득했을때(효과)
        if len(bullet_xy) !=0:
            for bx,by in bullet_xy:
                drawObject(bullet,bx,by)
        if not isShotpresent:
            drawObject(present,present_x,present_y)
        else:
            drawObject(boom,present_x,present_y)
            boom_count += 1
            if boom_count>15:
                boom_count=0
                present_x=pad_width
                present_y=random.randrange(0,pad_height-present_height)
                isShotpresent=False
        
        if fire[1] != None:
            drawObject(fire[1],fire_x,fire_y)
            
        pygame.display.update()
        clock.tick(60)
        
        #100점 달성시 미션 컴플리트트
        if score >= 100:
            pygame.mixer.music.pause()
            complete_sound.play()
            dispMessage('Mission Complete')
            
    
    pygame.quit()
    quit()
    
def initGame():
    global gamepad, penguin, clock, background1, background2
    global present, fires, bullet, boom
    global gameover_sound, complete_sound
    
    fires=[]
    
    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    
    #이미지 파일
    pygame.display.set_caption("PENGUIN'S ADVENTURE")
    penguin=pygame.image.load('penguin.png')
    background1=pygame.image.load('snowbackground.png')
    background2=pygame.image.load('snowbackground2.png')
    present=pygame.image.load('present.png')
    
    fires.append((0,pygame.image.load('eagle.png')))
    fires.append((1,pygame.image.load('fireball3.png')))
    boom=pygame.image.load('spark.png')
    
    for i in range(3):
        fires.append((i+2,None))
    
    bullet=pygame.image.load('snowbullet.png')
    
    clock=pygame.time.Clock()
    runGame()
 
#음성 파일   
global shot_sound, complete_sound, gameover_sound
shot_sound = pygame.mixer.Sound('shoot.wav')
complete_sound = pygame.mixer.Sound('missioncomplete.wav')
gameover_sound = pygame.mixer.Sound('gameover.wav')
    
pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.play(-1)

if __name__ == '__main__':
    initGame()