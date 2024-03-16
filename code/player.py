import pygame
import pyscroll

from pyscroll.orthographic import BufferedRenderer

from animation import SpriteAnimé

class Entité(SpriteAnimé):
    def __init__(self, nom, x, y, vitesse):
        # On crée la classe "Joueur" qui hérite de la super-classe "Sprite" de Pygame.
        super().__init__(nom)
        self.sprite_sheet = pygame.image.load(f'graphiques/{nom}.png') #Image du sprite
        self.image = self.get_image(0,0) # on injecte l'image
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() # On définit la "hitbox" du joueur en fonction de la taille de l'image
        self.position = [x,y] # Position du joueur sur la carte
        self.vitesse = vitesse # Vitesse du joueur
        self.feet = pygame.Rect(0,0, self.rect.width * 0.5, 1) # On place les pieds du joueur qui vont etre les facteurs de collisions pour plus de réalisme
        self.old_pos = self.position.copy() # On enregistre la position du joueur pour l'y faire revenir en cas de collision

    def save_location(self): 
        # On enregistre la position du joueur pour l'y faire revenir en cas de collision
        self.old_pos = self.position.copy()

    def move_side(self, ex):
        # Déplacement horizontal du joueur (plus pratique que de faire Gauche / Droite on ajoute juste en argument un - ou +(c'est ca ex))
        self.position[0] += ex*self.vitesse
        

    def move_high(self, ex):
        #déplacement Vertical
        self.position[1] += ex*self.vitesse

    def update(self):
        #on dit que la position du joueur correspond au coin en haut a gauche de son "rect" (qui comme dit avant correspond a l'image)
        self.rect.center = self.position       
        self.feet.midbottom = self.rect.midbottom # On dit que les pieds correspondent au bas du rect
    
    def collision(self):
        # en cas de collision, on le faitrevenir a la position qu'on avait sauvergardée grace a "save_location"
        self.position = self.old_pos
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        

    def get_image(self, x, y):
        # Fonction pour injecter l'image a des coordonnées données
        image = pygame.Surface([16,32])
        image.blit(self.sprite_sheet,(0,0),(x,y,16,32))
        return image
    
class Joueur(Entité):
    def __init__(self):
        super().__init__("pumpkin_dude", 0, 0, 1)

    def attaque(self,screen):
        mouse = pygame.mouse.get_pos()
        start = pygame.math.Vector2(self.position[0]*3,self.position[1]*3)
        end = start + (mouse - start).normalize() * 50
        print(f'Player Position = {self.position}, Mouse Position = {mouse}')
        pygame.draw.line(screen, (0,0,255), start, end)
        
        axe = pygame.image.load('graphiques/hache.png')
        return axe, mouse


class Monstre(Entité):
    def __init__(self):
        super().__init__("")

'''class Attaque():
    def __init__(self):
        self.image = pygame.image.load('graphiques/hache.png')
    
    def render(self, screen):
        left, siddle ,right = pygame.mouse.get_pressed()
        if left:
            print('hace')
            pos = pygame.mouse.get_pos()
            screen.blit(self.image,pos)
'''