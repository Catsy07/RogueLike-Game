import pygame
from time import sleep

class SpriteAnimé(pygame.sprite.Sprite):
    def __init__(self, nom):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'graphiques/sprites/{nom}.png')
        self.index = 0
        self.clock = 0
        self.images = {
            'idle' : self.getimages(0,4,16,self.sprite_sheet.get_height(),0),
            'run' : self.getimages(4,5,16,self.sprite_sheet.get_height(),0)
            }
            
    def change_animation(self,name,xbool):
        self.image = pygame.transform.flip(self.images[name][self.index], xbool, False)
        self.image.set_colorkey(0,0)
        self.clock += 9
        if self.clock >= 80:
            self.index += 1
            if name == 'run':
                if self.index >=4:
                    self.index = 0
            if name == 'idle':
                if self.index >=4:
                    self.index = 0
            self.clock = 0

    def getimage(self,surfacex,surfacey,x,y):
        image = pygame.Surface([surfacex,surfacey])
        image.blit(self.sprite_sheet,(0,0), (x,y, surfacex,surfacey))
        return image
    
    def getimages(self,numero, nombreimages,surfacex,surfacey,y):
        images = []
        
        for i in range(0,nombreimages):
            x = (numero+i)*16
            image = self.getimage(surfacex,surfacey,x,y)
            images.append(image)
        return images