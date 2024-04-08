import pygame
import pyscroll
import math
from pyscroll.orthographic import BufferedRenderer
from random import randint

from animation import SpriteAnimé

def checkForInput(position, rect):
        if position[0] in range(rect.left, rect.right) and position[1] in range(rect.top, rect.bottom):
            return True
        return False
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("graphiques/menu/font.ttf", size)
last_attack_time = 0
attack_cooldown = 500
class Entité(SpriteAnimé):
    def __init__(self, nom, x, y, vitesse, health, damage):
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
        self.damage = damage

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
    def __init__(self, choix_joueur, vitesse, health, damage):
        super().__init__(f'{choix_joueur}', 0,0, vitesse, health, damage)
        self.max_health = health
        self.health = self.max_health
        self.abso = 0
        self.xbool = False

        self.inventory = ['','','']
        self.coin_list = []
        self.coins = 0
        self.filled_slots = 0
        self.current_slot = 0
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

        #pour changer de slot d'inventaire
        if presse[pygame.K_1]:
            self.current_slot = 0
        elif presse[pygame.K_2]:
            self.current_slot = 1
        elif presse[pygame.K_3]:
            self.current_slot = 2
        

    def show_life(self, surface):
        img_plein = pygame.transform.scale(pygame.image.load('graphiques/autres/plein.png'), (45,42))
        img_moitie = pygame.transform.scale(pygame.image.load('graphiques/autres/moitie.png'), (45,42))
        img_moitie_abso = pygame.transform.scale(pygame.image.load('graphiques/autres/moitie_abso.png'), (45,42))
        img_plein_abso = pygame.transform.scale(pygame.image.load('graphiques/autres/full_abso.png'), (45,42))
        img_vide = pygame.transform.scale(pygame.image.load('graphiques/autres/vide.png'), (45,42))
        
        vide = 0
        x = 50
        if self.health % 2 != 0:
            plein = (self.health - 1) / 2
            moitié = 1
        else:
            plein = self.health/2
            moitié = 0
        if self.abso % 2 != 0:
            plein_abso = (self.abso - 1) / 2
            moitié_abso = 1
        else:
            plein_abso = self.abso/2
            moitié_abso = 0
        if self.max_health - self.health >= 2: 
            if (self.max_health - self.health) % 2 == 0:
                vide = ((self.max_health - self.health)/2)
            elif (self.max_health - self.health) % 2 != 0:
                vide = ((self.max_health - self.health-1)/2)
        for i in range(int(plein)):
            surface.blit(img_plein,(x,935,30,28))
            x += 50
        if moitié == 1:
            surface.blit(img_moitie,(x,935,30,28))
            x += 50
        for i in range(int(vide)):
            surface.blit(img_vide,(x,935,30,28))
            x += 50
        for i in range(int(plein_abso)):
            surface.blit(img_plein_abso,(x,935,30,28))
            x+=50
        if moitié_abso == 1:
            surface.blit(img_moitie_abso,(x,935,30,28))
            x+=50
            

    def fill_inventory(self, map_manager, i):
        if self.non_filled_slots != []:
            slot_to_fill = self.non_filled_slots[0]
            self.inventory[slot_to_fill] = i
            map_manager.items().remove(i)

    def update_inventory(self):
        self.non_filled_slots = []
        index = 0
        for i in self.inventory:
            if i == '':
                self.non_filled_slots.append(index)
            index+=1
        

    def use_item(self, monstre):
        left, middle, right = pygame.mouse.get_pressed()
        if self.inventory != []:
            item = self.inventory[self.current_slot]
            if right:
                if item != '':
                    if item.type == 'heal':
                        if self.health != self.max_health:
                            if self.health + item.level > self.max_health:
                                self.health = self.max_health
                                self.inventory[self.current_slot] = ''
                            else:
                                self.health += item.level
                                self.inventory[self.current_slot] = ''
                    if item.type == 'abso':
                        if self.abso < 4:
                            self.abso = 4
                            self.inventory[self.current_slot] = ''
                    if item.type == 'bombe':
                        for i in monstre:
                            if isinstance(i, Monstre):
                                if abs(self.position[0] - i.position[0]) < 400 and abs(self.position[1] - i.position[1]) < 400:
                                    i.health = 0
                                    monstre.remove(i)
                                    del(i)

                        self.inventory[self.current_slot] = ''
                    
                    


class Monstre(Entité):
    def __init__(self, nom, x, y, joueur, health, damage, speed):
        super().__init__(nom, x, y, 0.30, health, damage)

        self.joueur = joueur
        self.max_health = health
        self.last_attack_time = 0
        self.attack_cooldown = 700
        self.damage = damage
        self.speed = speed
    def move(self):
        presse = pygame.key.get_pressed()
        if abs(self.joueur.position[0] - self.position[0]) > 200 or abs(self.joueur.position[1] - self.position[1]) > 200:
            self.position = self.old_pos
        elif abs(self.joueur.position[0] - self.position[0]) < 200 and abs(self.joueur.position[1] - self.position[1]) < 200:
            if self.position[0]<self.joueur.position[0]:
                self.move_side(self.speed)
            elif self.position[0]>self.joueur.position[0]:
                self.move_side(-self.speed)
            if self.position[1]>self.joueur.position[1]:
                self.move_high(-self.speed)
            elif self.position[1]<self.joueur.position[1]:
                self.move_high(self.speed)

    def show_life(self, surface, position, vie):
        life = pygame.Rect(position[0]-20, position[1]-25, (32*vie)/self.max_health, 4)
        dead = pygame.Rect(position[0]-20, position[1]-25, (32*self.max_health)/self.max_health, 4)
        
        color1 = (0,255,0)
        color2 = (255,0,0)
        pygame.draw.rect(surface, color2, dead)
        pygame.draw.rect(surface, color1, life)

    def attaque(self):

        current_time = pygame.time.get_ticks()
        if self.rect.colliderect(self.joueur.rect):
            if current_time - self.last_attack_time > self.attack_cooldown:
                if self.joueur.abso != 0:
                    self.joueur.abso -= self.damage
                    self.last_attack_time = current_time
                else:    
                    self.joueur.health -= self.damage
                    self.last_attack_time = current_time

    def drop(self):
        x = randint(3,10)
        for i in range(x):
            self.joueur.coin_list.append(Item('coin0', 'coin', 1, self.joueur, self.position[0], self.position[1], 12, 12, 
                                              [randint(round(self.position[0]-20), round(self.position[0]+20)), randint(round(self.position[1]-20), round(self.position[1]+20))], 0))        

class Weapon:
    def __init__(self, pivot, name, surface, monstres, joueur):
        self.pivot = pivot
        self.surface = surface
        self.monstres = monstres
        self.image_orig = pygame.transform.rotate(pygame.image.load(f"graphiques/Armes/{name}.png"), -90)
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
                rect[2] = 35
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
            for i in self.monstres:
                if rect.colliderect(i.rect) and isinstance(i, Monstre):
                    
                    i.health -= self.joueur.damage
                    if i.health <= 0:
                        self.monstres.remove(i)
                        del(i)

            # Mettre à jour le temps de la dernière attaque
            last_attack_time = current_time
        image, rect = self.rotate_pivot(self.image_orig, angle, self.pivot, pos)
        self.surface.blit(image, rect)
        # Vérifier si le bouton gauche de la souris est enfoncé et si le cooldown est terminé
        
    def update(self):
        self.position = [self.joueur.position[0], self.joueur.position[1]]
        self.rect.center = self.position
        self.basic()
        
class Item:
    def __init__(self, name, type, level, joueur, x, y, width, height, to_pos, prix):
        self.name = name
        self.prix = prix
        self.quantity = 0
        self.type = type
        self.level = level
        self.joueur = joueur
        self.position = [x,y]
        self.image = pygame.transform.scale((pygame.image.load(f'graphiques/Items/{self.name}.png')), (width, height))
        self.gim = self.get_image(0,0)
        self.rect = self.gim.get_rect()
        self.rect[0], self.rect[1] = self.position[0], self.position[1]
        self.to_pos = to_pos
        
			
    def get_image(self, x, y):
        # Fonction pour injecter l'image a des coordonnées données
        img = pygame.Surface([self.image.get_width(), self.image.get_height()])
        img.blit(self.image,(0,0),(x,y,self.image.get_width(),self.image.get_height()))
        img.set_colorkey([0,0,0])
        return img


    
class Shop:
    def __init__(self, screen, items, joueur):
        self.screen = screen
        self.joueur = joueur
        self.items = [
            Item('potion_heal1', 'heal', 1, self.joueur, 0, 0, 60, 66, (0,0), 100),
            Item('potion_abso1', 'abso', 1, self.joueur, 0, 0, 60, 66, (0,0), 110),
            Item('potion_heal', 'heal', 2, self.joueur, 0, 0, 60, 66, (0,0), 180),
            Item('potion_abso', 'abso', 2, self.joueur, 0, 0, 60, 66, (0,0), 190),
            Item('bombe1', 'bombe', 2, self.joueur, 0, 0, 60, 66, (0,0), 300),

        ]
        self.width = 800
        self.height = 500
        self.on = False
        self.last_activation = 0
        self.current = 3

    def update(self):
        nb3 = 0
        nb4 = 0
        presse = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if presse[pygame.K_LSHIFT] or presse[pygame.K_ESCAPE]:
            if current_time - self.last_activation > 400:
                if self.on == True:
                    self.on = False
                else:
                    self.on = True
                self.last_activation = current_time
        if self.on:
            surface = pygame.Surface((1000,750))  # the size of your rect
            surface.set_alpha(168)                # alpha level
            surface.fill((0,0,0))           # this fills the entire surface
            self.screen.blit(surface, (250,100))
            logo = pygame.transform.scale(pygame.image.load('graphiques/autres/nom_shop.png'),(84*4, 55*3))
            coin = pygame.transform.scale(pygame.image.load('graphiques/Items/coin0.png'), (14, 14))
            rect = logo.get_rect(center = (500, 200))
            self.screen.blit(logo, rect)
            nb = 0
            nb2 = 0
            left, mid, right = pygame.mouse.get_pressed()
            for i in self.items:
                prix = str(i.prix)
                if nb % 2 == 0 and nb != 0:
                    nb2 += 1
                    nb = 0
                
                txt = get_font(10).render(i.name, True, "White")
                rect = txt.get_rect(center=(880+250*nb,310+200*nb2))
                self.screen.blit(txt, rect)
                self.screen.blit(i.gim, pygame.Rect(850+250*nb,220+200*nb2, i.rect[2], i.rect[3]))
                self.screen.blit(coin, coin.get_rect(center = (887+250*nb,340+200*nb2)))
                txt = get_font(9).render(prix, True, "White")
                rect = txt.get_rect(center=(860+250*nb,340+200*nb2))
                self.screen.blit(txt, rect)
                rect = pygame.Rect(800+250*nb,180+200*nb2, 160, 180)
                if checkForInput(pygame.mouse.get_pos(), rect):
                    if left:
                        self.current = self.items.index(i)
                        it = self.items[self.current]
                        if self.joueur.coins >= it.prix:

                            if self.joueur.non_filled_slots != []:
                                slot_to_fill = self.joueur.non_filled_slots[0]
                                self.joueur.inventory[slot_to_fill] = Item(it.name, it.type, it.level, it.joueur, it.position[0], it.position[1], 20, 22, it.to_pos, it.prix)
                                self.joueur.coins -= it.prix
                nb+=1
            if self.current % 2 == 0:
                nb3 = 0
                nb4 = self.current/2
            else:
                nb3 = 1
                nb4 = (self.current-1)/2
            current_rect = pygame.Rect(800+250*nb3,180+200*nb4, 160, 180)
            pygame.draw.rect(self.screen, '#ffffff', current_rect, 2)

class Tresor:
    def __init__(self, x, y, joueur):
        self.position = [x,y]
        self.opened = False
        self.joueur = joueur
        self.image = pygame.transform.scale((pygame.image.load(f'graphiques/Items/tresor.png')), (48, 42))
        self.gim = self.get_image(0,0)
        self.rect = self.gim.get_rect()
        self.rect[0], self.rect[1] = self.position[0], self.position[1]
    
    def basic(self, screen, map_manager):  
        presse = pygame.key.get_pressed()
        pos = map_manager.map_layer().translate_point(self.position)
        screen.blit(self.image, (pos[0], pos[1], 48,42))
        if self.opened == False:
            if self.rect.colliderect(self.joueur.rect):
                txt = get_font(15).render('press F to open', True, "White")
                rect = txt.get_rect(center=(770,800))
                screen.blit(txt, rect)
                if presse[pygame.K_f]:
                    x = randint(10,30)
                    for i in range(x):
                        self.joueur.coin_list.append(Item('coin0', 'coin', 1, self.joueur, self.position[0], self.position[1], 12, 12, 
                                                        [randint(round(self.position[0]-35), round(self.position[0]+35)), randint(round(self.position[1]-35), round(self.position[1]+35))], 0))
                    self.opened = True
                    self.image = pygame.transform.scale((pygame.image.load(f'graphiques/Items/tresor_opened.png')), (48, 42))
    
    def get_image(self, x, y):
        # Fonction pour injecter l'image a des coordonnées données
        img = pygame.Surface([self.image.get_width(), self.image.get_height()])
        img.blit(self.image,(0,0),(x,y,self.image.get_width(),self.image.get_height()))
        img.set_colorkey([0,0,0])
        return img