import pygame as pg

RES = WIDTH, HEIGHT = 1200, 600
pixelSide = 10
numX, numY = WIDTH//pixelSide, HEIGHT//pixelSide
SKY_COLOR = (175, 255, 255)
pg.init()
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()
FPS = 60
Aqua  = ( 0, 255, 255)
Black = ( 0, 0, 0)
Blue =  ( 0, 0, 255)
Fuchsia =  (255, 0, 255)
Gray =  (128, 128, 128)
Green  = ( 0, 128, 0)
Lime  = ( 0, 255, 0)
Maroon =  (128, 0, 0)
Navy_Blue =  ( 0, 0, 128)
Olive =  (128, 128, 0)
Purple =  (128, 0, 128)
Red  = (255, 0, 0)
Silver  = (192, 192, 192)
Teal  = ( 0, 128, 128)
White =  (255, 255, 255)
Yellow  = (255, 255, 0)

pixelList = []

class pixelClass:
    def __init__(self, pos, color) -> None:
        self.pos = self.x, self.y = pos
        self.color = color
    def drawPixel(self):
        pg.draw.rect(screen, self.color, (self.pos[0]*pixelSide, self.pos[1]*pixelSide, pixelSide, pixelSide))

for i in range(numX):
    for j in range(numY):
        pixelList.append(pixelClass((i,j), SKY_COLOR))

while True:
    for event in  pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = [event.pos[0]//pixelSide, event.pos[1]//pixelSide]
            pixelList.remove(pixelList[pos[0]+pos[1]])
            pixelList.append(pixelClass(pos, 'Red'))
    for pixel in pixelList:
        pixel.drawPixel()
    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'FPS : {clock.get_fps():.0f}')