import pygame
import pyscroll
import math
from pyscroll.orthographic import BufferedRenderer

from animation import SpriteAnimé

def rotate_pivot(image, angle, pivot, origine):
    surf = pygame.transform.rotate(image, angle)

    offset = pivot + (origine - pivot).rotate(-angle)
    rect = surf.get_rect(center = offset)
    return surf, rect

class Entité(SpriteAnimé):
    def __init__(self, nom, x, y, vitesse):
        # On crée la classe "Joueur" qui hérite de la super-classe "Sprite" de Pygame.
        super().__init__(nom)#Image du sprite
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
        self.rect.center = self.position
        self.feet.midbottom = self.rect.midbottom
        

    def get_image(self, x, y):
        # Fonction pour injecter l'image a des coordonnées données
        image = pygame.Surface([16,32])
        image.blit(self.sprite_sheet,(0,0),(x,y,16,32))
        return image
    
class Joueur(Entité):
    def __init__(self):
        super().__init__("Chevalier Rose", 0, 0, 1)
        
    def attaque(self, pivot, name, surface):
        left, middle, right = pygame.mouse.get_pressed()
        
        if left:
            plus = 60
        else:
            plus = 40
        pos = pivot + (plus,0)
        image_orig =  pygame.transform.rotate(pygame.image.load(f"graphiques/{name}.png"), -90)
        image_orig =  pygame.transform.scale(image_orig,(image_orig.get_width()*2,image_orig.get_height()*2))
        image = image_orig
        rect = image.get_rect(center = pos)

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_offset = mouse_pos - pivot

        angle = -math.degrees(math.atan2(mouse_offset.y, mouse_offset.x))
        image, rect = rotate_pivot(image_orig, angle, pivot, pos)
        surface.blit(image, rect)


class Monstre(Entité):
    def __init__(self):
        super().__init__("")


