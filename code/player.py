import pygame
import pyscroll
import math
from pyscroll.orthographic import BufferedRenderer

from animation import SpriteAnimé



class Entité(SpriteAnimé):
    def __init__(self, nom, x, y, vitesse, health):
        # On crée la classe "Joueur" qui hérite de la super-classe "Sprite" de Pygame.
        super().__init__(nom)#Image du sprite
        self.image = self.get_image(0,0) # on injecte l'image
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() # On définit la "hitbox" du joueur en fonction de la taille de l'image
        self.position = [x,y] # Position du joueur sur la carte
        self.vitesse = vitesse # Vitesse du joueur
        self.feet = pygame.Rect(0,0, self.rect.width * 0.5, 1) # On place les pieds du joueur qui vont etre les facteurs de collisions pour plus de réalisme
        self.old_pos = self.position.copy() # On enregistre la position du joueur pour l'y faire revenir en cas de collision
        self.health = health 
        

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
plus = 40    
class Joueur(Entité):
    def __init__(self):
        super().__init__("Chevalier Rose", 0, 0, 1, 3)

    
    


class Monstre(Entité):
    def __init__(self, nom, x, y, joueur, health):
        super().__init__(nom, x, y, 0.45, health)

        self.joueur = joueur
    def move(self):
        presse = pygame.key.get_pressed()
        if self.position[0]<self.joueur.position[0]:
            self.move_side(1)
        elif self.position[0]>self.joueur.position[0]:
            self.move_side(-1)
        if self.position[1]>self.joueur.position[1]:
            self.move_high(-1)
        elif self.position[1]<self.joueur.position[1]:
            self.move_high(1)

class Weapon:
    def __init__(self, pivot, name, surface, monstres, joueur):
        self.pivot = pivot
        self.surface = surface
        self.monstres = monstres
        self.image_orig = pygame.transform.rotate(pygame.image.load(f"graphiques/{name}.png"), -90)
        self.image_orig =  pygame.transform.scale(self.image_orig,(self.image_orig.get_width()*2,self.image_orig.get_height()*2))
        self.gim = self.get_image(0,0)
        self.gim.set_colorkey([0,0,0])
        self.rect = self.gim.get_rect()
        self.plus = 40
        self.joueur = joueur
        self.position = [self.joueur.position[0], self.joueur.position[1]]

    
    def get_image(self, x, y):
        # Fonction pour injecter l'image a des coordonnées données
        image = pygame.Surface([self.image_orig.get_width(), self.image_orig.get_height()])
        image.blit(self.image_orig,(0,0),(x,y,self.image_orig.get_width(),self.image_orig.get_height()))
        return image
        


    def rotate_pivot(self, image, angle, pivot, origine):
        surf = pygame.transform.rotate(image, angle)

        offset = pivot + (origine - pivot).rotate(-angle)
        rect = surf.get_rect(center = offset)
        return surf, rect
    
    def basic(self):
        image = self.image_orig
        pos = self.pivot + (self.plus,0)
        rect = image.get_rect(center = pos)

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_offset = mouse_pos - self.pivot

        angle = -math.degrees(math.atan2(mouse_offset.y, mouse_offset.x))
        image, rect = self.rotate_pivot(self.image_orig, angle, self.pivot, pos)
        self.surface.blit(image, rect)

    def attaque(self):
        global clock
        global cooldown_tracker
        cooldown_tracker += 1
        if cooldown_tracker > 100:
            cooldown_tracker = 0

        left, middle, right = pygame.mouse.get_pressed()
        if left and cooldown_tracker > 0 and cooldown_tracker < 9:
            self.plus = 60
            for i in self.monstres:
                if self.rect.colliderect(i.rect) and type(i) is Monstre:
                    i.health -= 1
                    if i.health <= 0:
                        self.monstres.remove(i)
        else:
            self.plus = 40
        
    def update(self):
        self.position = [self.joueur.position[0], self.joueur.position[1]]
        self.rect.center = self.position
        self.attaque()
        self.basic()
        
        
clock = pygame.time.Clock()
cooldown_tracker = 0