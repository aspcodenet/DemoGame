
import pygame as pg
import random
import bisect
from pygame.locals import *

screen = pg.display.set_mode((1024, 768))
clock = pg.time.Clock()

allFood = []

class SpriteSheet():
    
    def __init__(self, filename, o_rows, o_cols, rows, cols, p_rows, p_cols):
        self.image = pg.image.load(filename).convert_alpha()
        self.o_rows = o_rows    #Number of rows of options in sprite total
        self.o_cols = o_cols    #Number of cols of options in sprite total
        self.rows = rows        #Number of rows for sprite chosen
        self.cols = cols        #Number of cols for sprite chosen
        self.p_rows = p_rows    #Row number of chosen sprite in sheet
        self.p_cols = p_cols    #Column number of chosen sprite in sheet
        
        self.totalCellCount = cols * rows #Total cells in the specific sprite option chosen
        
        self.option_w = self.image.get_rect().width / self.o_cols #Width of particular option in sheet
        self.option_h = self.image.get_rect().height / self.o_rows #Height of particular option in sheet
        
        self.offset_x = self.option_w * p_cols #Offset the X based on which option in the sheet
        self.offset_y = self.option_h * p_rows #Offset the Y based on which option in the sheet
        
        self.init_rect = pg.Rect(0, 0, self.option_w, self.option_h) #Form initial rectangle (before we break it up into cells)

        self.w = self.cellWidth = self.init_rect.width / cols
        self.h = self.cellHeight = self.init_rect.height / rows
        
        #Get a list of (X,Y) coordinates of each cell in the sprite sheet with associated heights/widths
        #self.cells = list([((index % cols * self.w) + self.offset_x , (index / cols * self.h) + self.offset_y, self.w, self.h) for index in range(self.totalCellCount)])
        #self.cells = list([((index % cols * self.w), (index % rows * self.h), self.w, self.h) for index in range(self.totalCellCount)])
        
        self.cells = []
        myCounter = 0
        
        for ry in range(0, rows):
            for rx in range(0,cols):
                self.cells.append(((myCounter % cols * self.w) + self.offset_x, (ry * self.h) + self.offset_y, self.w, self.h))
                myCounter += 1
                #print(self.cells)
        
    def draw(self, cellIndex = 0, x = 25, y = 25):
        self.rect = pg.Rect(x,y,self.w,self.h) #Form rectangle around cell
        screen.blit(self.image, (x, y), self.cells[cellIndex])
        

class Food(pg.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pg.image.load("worm.png")
        self.surf = pg.Surface((40, 75))
        x = random.randrange(0,screen.get_width()) 
        y = random.randrange(0, screen.get_height())
        self.rect = self.surf.get_rect(center = (x, y))

        
class Fish(SpriteSheet):
    
    rightPos = 6   #Image index to use while moving right
    leftPos = 3    #Image index to use while moving left
    upPos = 9      #Image index to use while moving up
    downPos = 0    #Image index to use while moving down
    
    switchImg = 6  #Switch image after every 'x' moves
    
    def __init__(self, speed, filename, o_rows, o_cols, rows, cols, p_rows, p_cols):
        super().__init__(filename, o_rows, o_cols, rows, cols, p_rows, p_cols)

        self.speed = speed
        self.traveled = 0
        self.counter = 0
        self.direction = 'Left'
        
        #Set current index of sprite - tried to randomize so that all fins weren't doing the same thing
        self.curRightPos = random.randint(Fish.rightPos,8)
        self.curLeftPos = random.randint(Fish.leftPos,5)
        self.curUpPos = random.randint(Fish.upPos,11)
        self.curDownPos = random.randint(Fish.downPos,3)
        

    def moveleft(self):
        self.direction = 'Left'
    def moveright(self):
        self.direction = 'Right'
    def moveup(self):
        self.direction = 'Up'
    def movedown(self):
        self.direction = 'Down'

        
    def move(self):
        self.counter += 1
        #print(self.counter)
        
        #Switch up images
        if self.counter >= Fish.switchImg and self.direction == 'Right':
            if self.curRightPos >= Fish.rightPos + 2:
                self.curRightPos = Fish.rightPos
            else:
                self.curRightPos += 1
                self.counter = 0
        if self.counter >= Fish.switchImg and self.direction == 'Left':
            if self.curLeftPos >= Fish.leftPos + 2:
                self.curLeftPos = Fish.leftPos
            else:
                self.curLeftPos += 1
                self.counter = 0
        if self.counter >= Fish.switchImg and self.direction == 'Up':
            if self.curUpPos >= Fish.upPos + 2:
                self.curUpPos = Fish.upPos
            else:
                self.curUpPos += 1
                self.counter = 0
        if self.counter >= Fish.switchImg and self.direction == 'Down':
            if self.curDownPos >= Fish.downPos + 2:
                self.curDownPos = Fish.downPos
            else:
                self.curDownPos += 1
                self.counter = 0
                
        
        #Move the fish
        #self.draw(self.curRightPos, self.rect.x + self.speed, self.rect.y)
        #self.traveled += self.speed
        
        if self.direction == 'Right':
            self.draw(self.curRightPos, self.rect.x + self.speed, self.rect.y)
            #self.rect.x += self.speed
            self.traveled += self.speed
        elif self.direction == 'Left':
            self.draw(self.curLeftPos, self.rect.x - self.speed, self.rect.y)
            #self.rect.x -= self.speed
            self.traveled -= self.speed
        elif self.direction == 'Up':
            self.draw(self.curUpPos, self.rect.x, self.rect.y - self.speed)
            #self.rect.y -= self.speed
            self.traveled -= self.speed
        else:
            self.draw(self.curDownPos, self.rect.x, self.rect.y + self.speed)
            #self.rect.y += self.speed
            self.traveled += self.speed
            
        #Check if the fish is off the screen
        if self.rect.top > screen.get_height() - self.h:
            self.direction = 'Up'
        elif self.rect.right > screen.get_width():
            self.direction = 'Left'
        elif self.rect.left < 0:
            self.direction = 'Right'
        elif self.rect.top < 0:
            self.direction = 'Down'
            

def main():
    font_small = pg.font.SysFont("Verdana", 20)

    points = 0
    
    fish = Fish(2,"./DolphinSheet1.png",2,4,4,3,random.randint(0,1),random.randint(0,3))
    fish.draw(x = random.randrange(0,screen.get_width()), y = random.randrange(0, screen.get_height()))        

    for n in range(4):
        allFood.append(Food())


    while True:
        event = pg.event.poll()
        if event.type == pg.QUIT:
            return

        for food in allFood:
            if pg.sprite.collide_rect(food, fish):
                points += 10
                allFood.remove(food)


        scores = font_small.render(str(points), True, (255, 255,255))
        screen.blit(scores, (10,10))


        pressed_keys = pg.key.get_pressed()
        if pressed_keys[K_LEFT]:
            fish.moveleft()
        if pressed_keys[K_RIGHT]:
            fish.moveright()
        if pressed_keys[K_UP]:
            fish.moveup()
        if pressed_keys[K_DOWN]:
            fish.movedown()

        
        fish.move()
        for entity in allFood:
                screen.blit(entity.image, entity.rect)

        pg.display.update()
        
        clock.tick(30) #never run more than 30fps
        
        screen.fill((30, 30, 30))
    
if __name__ == "__main__" :
    pg.init()
    main()
    pg.quit()