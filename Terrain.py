import pygame as pg
from perlin_noise import PerlinNoise
import random
noise = PerlinNoise(octaves=1, seed=random.randint(0, 1000))
back_noise = PerlinNoise(octaves = 2, seed=random.randint(0, 100))
RES = WIDTH, HEIGHT = 1200, 600
SKY_COLOR = (175, 255, 255)
pg.init()
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()
FPS = 60
carry_state_ground = False
carry_state_mountain = False
ground_fps, mountain_fps = 80,10
cooldown_time_ground_seconds = 1/ground_fps
cooldown_time_mountain_seconds = 1/mountain_fps
noise_x = 0
back_noise_x = 0
noise_step = 0.01
back_noise_step = 0.005
MIN_HEIGHT = 0.05*HEIGHT
MAX_HEIGHT = 0.95*HEIGHT
max_circle_radius = 3
grass_width = 2
grass_height = 15
snow_height = 30
percent_of_height_as_ground = 0.7
percent_of_height_as_back_ground = 0.3
min_snow_height_percent_wrt_screen_Height = 0.2
lineWidth = 2
mountainLineWidth = 2
lineList = []
mountainLineList = []
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)              
mountainColor = (120, 120, 120)   
snow_cap_color = (245, 245, 245)  

sky_image = pg.image.load(r'C:\Users\USER\projects\Ray_Tracing\cloud.jpeg')
sky_image = pg.transform.scale(sky_image, (WIDTH, HEIGHT)).convert()
class lineClass:
    def __init__(self, height, xIndex, color, isMain, lineWidth, is_snow_mountain) -> None:
        self.isMain = isMain
        self.height = height
        self.xIndex = xIndex
        self.lineWidth = lineWidth
        self.xPos = self.xIndex*lineWidth    
        self.color = color
        self.is_snow = is_snow_mountain
    def moveLine(self):
        self.xIndex -= 1
        self.xPos = self.xIndex*lineWidth
    def drawLine(self):
        pg.draw.line(screen, self.color, (self.xPos, HEIGHT),
                     (self.xPos, self.height), self.lineWidth)
        if self.isMain:
            circle_radius = random.uniform(0, max_circle_radius)
            pg.draw.circle(screen, BROWN, (self.xPos, self.height), circle_radius)
            pg.draw.line(screen, GREEN, (self.xPos, self.height), 
                        (self.xPos, self.height - grass_height), grass_width)
        if self.is_snow:
            pg.draw.line(screen, snow_cap_color, (self.xPos, self.height + snow_height), (self.xPos, self.height), self.lineWidth)
        
lineList.append(lineClass(HEIGHT//2, 0, BROWN, True, lineWidth, False))
while len(lineList) <= WIDTH//lineWidth : 
    height_noise = noise(noise_x)
    noise_x+=noise_step
    new_height = percent_of_height_as_ground * HEIGHT + height_noise * HEIGHT *(1-percent_of_height_as_ground)
    lineList.append(lineClass(new_height, len(lineList), BROWN, True, lineWidth, False))
while len(mountainLineList) <= WIDTH//mountainLineWidth:
    back_height_noise = back_noise(back_noise_x)
    back_noise_x += back_noise_step
    new_back_height = percent_of_height_as_back_ground * HEIGHT + back_height_noise * HEIGHT *(1-percent_of_height_as_back_ground)
    snow_mountain = new_back_height <= min_snow_height_percent_wrt_screen_Height*HEIGHT
    if not snow_mountain : mountainLineList.append(lineClass(new_back_height, len(mountainLineList), mountainColor, False, mountainLineWidth, False))
    else : mountainLineList.append(lineClass(new_back_height, len(mountainLineList), mountainColor, False, mountainLineWidth, True))
last_ground_tick_seconds = pg.time.get_ticks()/1000
last_mountain_tick_seconds = pg.time.get_ticks()/1000
while True:
    screen.blit(sky_image, (0,0))
    for event in  pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    

    current_time_seconds = pg.time.get_ticks() / 1000
    if current_time_seconds - last_ground_tick_seconds >= cooldown_time_ground_seconds:
        lineList.remove(lineList[0])
        height_noise = noise(noise_x)
        noise_x+=noise_step
        new_height = percent_of_height_as_ground * HEIGHT + height_noise * HEIGHT *(1-percent_of_height_as_ground)
        new_height = max(MIN_HEIGHT, min(MAX_HEIGHT, new_height))
        #min(max(ground_level, min(min_height, lineList[-1].height + (slope*lineWidth))), max_height)
        lineList.append(lineClass(new_height, len(lineList), BROWN, True, lineWidth, False))
        last_ground_tick_seconds = current_time_seconds
        carry_state_ground = True

    if current_time_seconds - last_mountain_tick_seconds >= cooldown_time_mountain_seconds:
        mountainLineList.remove(mountainLineList[0])
        back_height_noise = back_noise(back_noise_x)
        back_noise_x += back_noise_step
        new_back_height = percent_of_height_as_back_ground * HEIGHT + back_height_noise * HEIGHT *(1-percent_of_height_as_back_ground)
        new_back_height = min(MAX_HEIGHT, max(MIN_HEIGHT, new_back_height))
        snow_mountain = new_back_height <= min_snow_height_percent_wrt_screen_Height*HEIGHT
        if not snow_mountain : mountainLineList.append(lineClass(new_back_height, len(mountainLineList), mountainColor, False, mountainLineWidth, False))
        else : mountainLineList.append(lineClass(new_back_height, len(mountainLineList), mountainColor, False, mountainLineWidth, True))
        last_mountain_tick_seconds = current_time_seconds
        carry_state_mountain = True

    if carry_state_mountain:
        for line in mountainLineList:
            line.moveLine()
        carry_state_mountain = False 
    for line in mountainLineList:
        line.drawLine()
    if carry_state_ground :
        for line in lineList:
            line.moveLine()
        carry_state_ground = False
    for line in lineList:
        line.drawLine()
       
    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'FPS : {clock.get_fps():.0f}')
