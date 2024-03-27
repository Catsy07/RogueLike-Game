import pygame
import pyscroll
import math
from pyscroll.orthographic import BufferedRenderer

from animation import SpriteAnimé


last_attack_time = 0
attack_cooldown = 500
class Entité(SpriteAnimé):
    def __init__(self, nom, x, y, vitesse, health):
        # On crée la classe "Joueur" qui hérite de la super-classe "Sprite" de Pygame.
        super().__init__(nom)#Image du sprite
        self.image = self.get_image(0,0) # on injecte l'image
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() # On définit la "hitbox" du joueur en fonction de la taille de l'image
        self.rect[1] += 20
        self.rect[3] -=10
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
    
    def draw_rect(self, surface):
        # Dessiner le rectangle de collision sur la surface spécifiée
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
plus = 40    
class Joueur(Entité):
    def __init__(self):
        super().__init__("Chevalier Rose", 0, 0, 1, 3)
    
        self.health = 6
        
        self.xbool = False

    def presse(self):
    #Cette fonction va servir a récupérer les touches pressées par le joueur sur le clavier ou la souris
        presse = pygame.key.get_pressed()
        
        # Mouvements du joueur avec ZSQD ou les fleches
        if presse[pygame.K_UP] or presse[pygame.K_z]:
            self.move_high(-1)
            self.change_animation('run',self.xbool)
        elif presse[pygame.K_DOWN] or presse[pygame.K_s]:
            self.move_high(1)
            self.change_animation('run',self.xbool)
        elif presse[pygame.K_LEFT] or presse[pygame.K_q]:
            self.move_side(-1)
            self.xbool = True
            self.change_animation('run',self.xbool)
        elif presse[pygame.K_RIGHT] or presse[pygame.K_d]:
            self.move_side(1)
            self.xbool = False
            self.change_animation('run',self.xbool)
        else:
            
            self.change_animation('idle',self.xbool)

    
    


class Monstre(Entité):
    def __init__(self, nom, x, y, joueur, health):
        super().__init__(nom, x, y, 0.30, health)

        self.joueur = joueur
        self.last_attack_time = 0
    def move(self):
        presse = pygame.key.get_pressed()
        if abs(self.joueur.position[0] - self.position[0]) > 100 or abs(self.joueur.position[1] - self.position[1]) > 100:
            self.position = self.old_pos
        elif abs(self.joueur.position[0] - self.position[0]) < 100 and abs(self.joueur.position[1] - self.position[1]) < 100:
            if self.position[0]<self.joueur.position[0]:
                self.move_side(1)
            elif self.position[0]>self.joueur.position[0]:
                self.move_side(-1)
            if self.position[1]>self.joueur.position[1]:
                self.move_high(-1)
            elif self.position[1]<self.joueur.position[1]:
                self.move_high(1)

    def show_life(self, surface):
        i = 0
        life = pygame.Rect(self.position[0], self.position[1]+20, 16, 3)
        color = (0,255,0)
        pygame.draw.rect(surface, color, life)
        while i < 1000:
            i+=1

    def attaque(self):
        global attack_cooldown
        current_time = pygame.time.get_ticks()
        if self.rect.colliderect(self.joueur.rect):
            if current_time - self.last_attack_time > attack_cooldown:
                print(f'la vie du joueur est a {self.joueur.health} pv')
                self.joueur.health -= 1
                self.last_attack_time = current_time

            

class Weapon:
    def __init__(self, pivot, name, surface, monstres, joueur):
        self.pivot = pivot
        self.surface = surface
        self.monstres = monstres
        self.image_orig = pygame.transform.rotate(pygame.image.load(f"graphiques/{name}.png"), -90)
        self.image_orig =  pygame.transform.scale(self.image_orig,(self.image_orig.get_width()*2,self.image_orig.get_height()*2.5))
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
        global last_attack_time
        global attack_cooldown
        left, middle, right = pygame.mouse.get_pressed()
        current_time = pygame.time.get_ticks()

        image = self.image_orig
        if left and current_time - last_attack_time > attack_cooldown:
            self.plus = 65
        else:
            self.plus = 40
        pos = self.pivot + (self.plus,0)
        rect = image.get_rect(center = pos)

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_offset = mouse_pos - self.pivot
        angle = -math.degrees(math.atan2(mouse_offset.y, mouse_offset.x))
        
        if left and current_time - last_attack_time > attack_cooldown:
            new_angle = 0
            if angle < 0:
                new_angle = angle + 360               
            else:
                new_angle = angle  
            rect = pygame.Rect(0,0,20,25)
            if (new_angle >= 0 and new_angle < 22.5) or (new_angle > 337.5 and new_angle < 360):
                rect.midleft = self.joueur.position
            elif (new_angle >= 22.5 and new_angle < 67.5):
                rect.bottomleft = self.joueur.position
            elif (new_angle >= 67.5 and new_angle < 112.5):
                rect.midbottom = self.joueur.position
            elif (new_angle >= 112.5 and new_angle < 157.5):
                rect.bottomright = self.joueur.position
            elif (new_angle >= 157.5 and new_angle < 202.5):
                rect.midright = self.joueur.position
            elif (new_angle >= 202.5 and new_angle < 247.5):
                rect.topright = self.joueur.position
            elif (new_angle >= 247.5 and new_angle < 292.5):
                rect.midtop = self.joueur.position
            elif (new_angle >= 292.5 and new_angle < 337.5):
                rect.topleft = self.joueur.position
            
            pygame.draw.rect(self.surface, (0,255,0), rect, 2)
            for i in self.monstres:
                if rect.colliderect(i.rect) and isinstance(i, Monstre):
                    
                    i.health -= 1
                    i.show_life(self.surface)
                    if i.health <= 0:
                        self.monstres.remove(i)
                        i.rect.center = (0,0)

            # Mettre à jour le temps de la dernière attaque
            last_attack_time = current_time
        image, rect = self.rotate_pivot(self.image_orig, angle, self.pivot, pos)
        self.surface.blit(image, rect)
        # Vérifier si le bouton gauche de la souris est enfoncé et si le cooldown est terminé
        

        
        
        
    def update(self):
        self.position = [self.joueur.position[0], self.joueur.position[1]]
        self.rect.center = self.position
        self.basic()
        

  # Cooldown en millisecondes (par exemple, 500ms)