import pygame
import pytmx
import pyscroll
from map import MapManager
import math

from player import *


BG = pygame.transform.scale(pygame.image.load("graphiques/menu/Background.png"), (1520, 1024))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("graphiques/menu/font.ttf", size)

class Game:
    def __init__(self):

        # Ici, on définis la taille de la fenetre puis on l'injecte sur l'écran.
        self.screen_width = 1520
        self.screen_height = 1024
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Soul Knight")

        #liste des mobs
        self.mobs = []
        
        self.img_mouse = pygame.image.load("graphiques/menu/mouse.png")
        self.cursor = pygame.image.load("graphiques/autres/cursor.png")
        self.cursor = pygame.transform.scale(self.cursor, (18,18))
        pygame.mouse.set_visible(False)
    
    
    def show_inventory(self):
        pygame.draw.rect(self.screen, "gray", pygame.Rect(660,850, 80*3, 80))
        for i in range(3):
            pygame.draw.rect(self.screen, "#545454", pygame.Rect(660+(80*i),850, 80, 80), 3)
            texte = get_font(10).render(str(i+1), True, "#545454")
            rect = texte.get_rect()
            rect[0], rect[1] = 670+(80*i), 860
            self.screen.blit(texte, rect)
        j = 0
        for i in self.joueur.inventory:   
            if i != '':
                self.screen.blit(i.gim, pygame.Rect(690+(80*j),880, i.rect[2], i.rect[3]))
            j+=1
        pygame.draw.rect(self.screen, "#ffffff", pygame.Rect(657+(80*self.joueur.current_slot),847, 86, 86), 3)
    
    def update_joueur(self):
        if self.joueur.health <= 0:
            self.game_over()
        self.joueur_pos = self.map_manager.map_layer().translate_point(self.joueur.position)
        self.joueur_vect = pygame.Vector2(self.joueur_pos[0],self.joueur_pos[1])
        self.joueur.weapon = Weapon(self.joueur_vect, self.weapon, self.screen, self.map_manager.groupe()._spritelist, self.joueur)
        self.joueur.weapon.update()
        self.joueur.use_item()
        self.joueur.show_life(self.screen)
        self.joueur.update_inventory()
        self.show_inventory()
        pos = pygame.mouse.get_pos()
        self.screen.blit(self.cursor, pos)  


    def update_mobs(self):
        mobs = self.map_manager.mobs()
        for i in mobs:
            if i.health <= 0:
                del(i)
                continue
            i.change_animation('idle', False)
            i.save_location()
            i.move()
            i.attaque()
            i.show_life(self.screen, self.map_manager.map_layer().translate_point(i.position), i.health)

    def update_items(self):
        for i in self.map_manager.items():
            pos = self.map_manager.map_layer().translate_point(i.position)
            self.screen.blit(i.image, (pos[0], pos[1], 20,22))
            if i.rect.colliderect(self.joueur.rect):
                if self.joueur.non_filled_slots != []:
                    slot_to_fill = self.joueur.non_filled_slots[0]
                    self.joueur.inventory[slot_to_fill] = i
                    self.map_manager.items().remove(i)
    def update(self):
        #cette fonction vérifie les parametres du jeu pour gerer les collisions, les interactions, etc...
        self.joueur.presse()
        self.map_manager.update()
        
    def main_menu(self):
        while True:
            self.screen.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("The Dungeon", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(self.screen_width/2, 150))

            PLAY_BUTTON = Button(image=None, pos=(self.screen_width/2, 350), 
                                text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            INFORMATIONS_BUTTON = Button(image=None, pos=(self.screen_width/2, 500), 
                                text_input="INFOS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=None, pos=(self.screen_width/2, 650), 
                                text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, INFORMATIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.interface_c_persos()
                    if INFORMATIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.informations()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        jeu = False
                        pygame.quit()
            
            pos = pygame.mouse.get_pos()
            self.screen.blit(self.cursor, pos)    

            pygame.display.update()
    
    
    def interface_c_persos(self):
        
        while True:
            self.screen.blit(BG, (0, 0))

            CHOIX_MOUSE_POS = pygame.mouse.get_pos()
            
            CHOIX_TEXT = get_font(100).render("The Dungeon", True, "#b68f40")
            CHOIX_RECT = CHOIX_TEXT.get_rect(center=(self.screen_width/2, 150))
            
            chevalier_img = pygame.image.load("graphiques/menu/chevalier_menu.png")
            magicien_img = pygame.image.load("graphiques/menu/magicien_menu.png")
            tank_img = pygame.image.load("graphiques/menu/tank_menu.png")
        
            CHEVALIER_BUTTON = Button(image=None, pos=(self.screen_width/2 - 500, 650), 
                                text_input="Chevalier", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        
            MAGICIEN_BUTTON = Button(image=None, pos=(self.screen_width/2, 650), 
                                    text_input="Magicien", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
            
            TANK_BUTTON = Button(image=None, pos=(self.screen_width/2 + 500, 650), 
                                    text_input="Tank", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
            
            RETURN_BUTTON = Button(image=None, pos=(100, 150), 
                                    text_input="<-", font=get_font(40), base_color="White", hovering_color="Gray")
            
            self.screen.blit(CHOIX_TEXT, CHOIX_RECT)
            self.screen.blit(pygame.transform.scale(chevalier_img, (chevalier_img.get_width() * 10, chevalier_img.get_height() * 10)), (self.screen_width/2 - 575, 350))
            self.screen.blit(pygame.transform.scale(magicien_img, (magicien_img.get_width() * 10, magicien_img.get_height() * 10)), (self.screen_width/2 - 75, 350))
            self.screen.blit(pygame.transform.scale(tank_img, (tank_img.get_width() * 10, tank_img.get_height() * 10)), (self.screen_width/2 + 425, 350))

            for button in [CHEVALIER_BUTTON, MAGICIEN_BUTTON,TANK_BUTTON, RETURN_BUTTON]:
                button.changeColor(CHOIX_MOUSE_POS)
                button.update(self.screen)
            pos = pygame.mouse.get_pos()
            self.screen.blit(self.cursor, pos)      
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CHEVALIER_BUTTON.checkForInput(CHOIX_MOUSE_POS):
                        self.info_perso('chevalier', 1, 6, 1, 'chevalier_sword')
                    if MAGICIEN_BUTTON.checkForInput(CHOIX_MOUSE_POS):
                        self.info_perso('magicien', 1.5, 4, 1.5, 'mage_stick')
                    if TANK_BUTTON.checkForInput(CHOIX_MOUSE_POS):
                        self.info_perso('tank', 0.75, 10, 0.75, 'tank_hammer')
                    if RETURN_BUTTON.checkForInput(CHOIX_MOUSE_POS):
                        self.main_menu()
                    

                pygame.display.update()

    def info_perso(self, name, speed, health, attack, weapon):
        
        while True:
            self.screen.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()
            
            MENU_TEXT = get_font(100).render("The Dungeon", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(self.screen_width/2, 150))
            
            PERSO_IMG_MENU = pygame.image.load(f'graphiques/menu/{name}_menu.png')
            PERSO_HEALTH = get_font(50).render(f"{health}", True, "#ffffff")
            PERSO_HEALTH_IMG = pygame.image.load('graphiques/autres/plein.png')
            PERSO_SPEED = get_font(50).render(f"{speed}", True, "#ffffff")
            PERSO_SPEED_IMG = pygame.image.load('graphiques/autres/shoe.png')
            PERSO_ATTACK = get_font(50).render(f"{attack}", True, "#ffffff")
            PERSO_ATTACK_IMG = pygame.image.load('graphiques/autres/sword.png')
            
        
            PLAY_BUTTON = Button(image=None, pos=(self.screen_width/2, 700),
                          text_input="PLAY", font=get_font(50), base_color="White", hovering_color="Gray")
            
            RETURN_BUTTON = Button(image=None, pos=(100, 150), 
                                    text_input="<-", font=get_font(40), base_color="White", hovering_color="Gray")
            
            self.screen.blit(MENU_TEXT, MENU_RECT)
            self.screen.blit(pygame.transform.scale(PERSO_IMG_MENU, (PERSO_IMG_MENU.get_width() * 10, PERSO_IMG_MENU.get_height() * 10)), (self.screen_width/2 - 75, 400))
            
            
            self.screen.blit(PERSO_HEALTH, (self.screen_width/2 - 450, 415))
            self.screen.blit(pygame.transform.scale(PERSO_HEALTH_IMG, (PERSO_HEALTH_IMG.get_width() * 5, PERSO_HEALTH_IMG.get_height() * 5)), (self.screen_width/2 - 550, 400))
            
            
            self.screen.blit(PERSO_SPEED, (self.screen_width/2 - 450, 525))
            self.screen.blit(pygame.transform.scale(PERSO_SPEED_IMG, (PERSO_SPEED_IMG.get_width() * 5, PERSO_SPEED_IMG.get_height() * 5)), (self.screen_width/2 - 570, 500),)
            
            
            self.screen.blit(PERSO_ATTACK, (self.screen_width/2 - 450, 615))
            self.screen.blit(pygame.transform.scale(PERSO_ATTACK_IMG, (PERSO_HEALTH_IMG.get_width() * 5, PERSO_HEALTH_IMG.get_height() * 5)), (self.screen_width/2 - 550, 600),)
            

            for button in [PLAY_BUTTON, RETURN_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            pos = pygame.mouse.get_pos()
            self.screen.blit(self.cursor, pos)      
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        
                        self.joueur = Joueur(name, speed, health, attack)
                        
                        self.map_manager = MapManager(self.screen, self.joueur)
                    

                        self.weapon = weapon
                        
                        self.go()
                        
                    if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        
                        self.interface_c_persos()
                        
                        
                pygame.display.update()
        
        
    
    def informations(self):
        infos = True
        while True:
            self.screen.blit(BG, (0, 0))

            INFOS_MOUSE_POS = pygame.mouse.get_pos()
            
            INFOS_TEXT = get_font(100).render("The Dungeon", True, "#b68f40")
            INFOS_RECT = INFOS_TEXT.get_rect(center=(self.screen_width/2, 150))
        
            KEYS_BUTTON = Button(image=pygame.image.load("graphiques/menu/Informations Rect.png"), pos=(self.screen_width/2, 350), 
                                text_input="KEYS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
            ATTACK_BUTTON = Button(image=pygame.image.load("graphiques/menu/Informations Rect.png"), pos=(self.screen_width/2, 500), 
                                    text_input="ATTACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            
            RETURN_BUTTON = Button(image=None, pos=(100, 150), 
                                    text_input="<-", font=get_font(40), base_color="White", hovering_color="Gray")
            
            self.screen.blit(INFOS_TEXT, INFOS_RECT)
            pos = pygame.mouse.get_pos()
            self.screen.blit(self.cursor, pos)  
            for button in [KEYS_BUTTON, ATTACK_BUTTON, RETURN_BUTTON]:
                button.changeColor(INFOS_MOUSE_POS)
                button.update(self.screen)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    infos = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if KEYS_BUTTON.checkForInput(INFOS_MOUSE_POS):
                        self.keys_infos()
                    if ATTACK_BUTTON.checkForInput(INFOS_MOUSE_POS):
                        self.attack_infos()
                    if RETURN_BUTTON.checkForInput(INFOS_MOUSE_POS):
                        self.main_menu()
                    
            
                pygame.display.update()
    
    
    def keys_infos(self):

        while True:
            self.screen.blit(BG, (0, 0))

            KEYS_MOUSE_POS = pygame.mouse.get_pos()
            
            KEYS_TEXT = get_font(100).render("The Dungeon", True, "#b68f40")
            KEYS_RECT = KEYS_TEXT.get_rect(center=(self.screen_width/2, 150))
            
        
            Z_BUTTON = Button(image=None, pos=(self.screen_width/2, 500),
                          text_input="Z", font=get_font(80), base_color="White", hovering_color="Gray")
        
            Q_BUTTON = Button(image=None, pos=(self.screen_width/2 - 110, 610), 
                                text_input="Q", font=get_font(80), base_color="White", hovering_color="Gray")
        
            S_BUTTON = Button(image=None, pos=(self.screen_width/2, 610), 
                                text_input="S", font=get_font(80), base_color="White", hovering_color="Gray")
        
            D_BUTTON = Button(image=None, pos=(self.screen_width/2 + 110, 610), 
                                text_input="D", font=get_font(80), base_color="White", hovering_color="Gray")
            
            RETURN_BUTTON = Button(image=None, pos=(100, 150), 
                                    text_input="<-", font=get_font(40), base_color="White", hovering_color="Gray")
            
            self.screen.blit(KEYS_TEXT, KEYS_RECT)
            pos = pygame.mouse.get_pos()
            self.screen.blit(self.cursor, pos)  
            for button in [Z_BUTTON, Q_BUTTON, S_BUTTON, D_BUTTON, RETURN_BUTTON]:
                button.changeColor(KEYS_MOUSE_POS)
                button.update(self.screen)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if Z_BUTTON.checkForInput(KEYS_MOUSE_POS):
                        
                        Z_TEXT = get_font(100).render("FORWARD", True, "White")
                        Z_RECT = Z_TEXT.get_rect(center=(self.screen_width/2, 300))
                        self.screen.blit(Z_TEXT, Z_RECT)
                        
                    if Q_BUTTON.checkForInput(KEYS_MOUSE_POS):
                        
                        Q_TEXT = get_font(100).render("LEFT", True, "White")
                        Q_RECT = Q_TEXT.get_rect(center=(self.screen_width/2, 300))
                        self.screen.blit(Q_TEXT, Q_RECT)
                        
                    if S_BUTTON.checkForInput(KEYS_MOUSE_POS):
                        
                        S_TEXT = get_font(100).render("BACKWARD", True, "White")
                        S_RECT = S_TEXT.get_rect(center=(self.screen_width/2, 300))
                        self.screen.blit(S_TEXT, S_RECT)
                        
                    if D_BUTTON.checkForInput(KEYS_MOUSE_POS):
                        
                        D_TEXT = get_font(100).render("RIGHT", True, "White")
                        D_RECT = D_TEXT.get_rect(center=(self.screen_width/2, 300))
                        self.screen.blit(D_TEXT, D_RECT)
                        
                    if RETURN_BUTTON.checkForInput(KEYS_MOUSE_POS):
                        
                        self.informations()
                    

                pygame.display.update()
    
    def attack_infos(self):
        while True:
            self.screen.blit(BG, (0, 0))

            ATTACK_MOUSE_POS = pygame.mouse.get_pos()
            
            ATTACK_TEXT = get_font(100).render("The Dungeon", True, "#b68f40")
            ATTACK_RECT = ATTACK_TEXT.get_rect(center=(self.screen_width/2, 150))
            
        
            MOUSE_BUTTON = Button(image=pygame.transform.scale(self.img_mouse, (110,210)), pos=(self.screen_width/2, 500),
                          text_input="", font=get_font(100), base_color="White", hovering_color="Gray")
            
            RETURN_BUTTON = Button(image=None, pos=(100, 150), 
                                    text_input="<-", font=get_font(40), base_color="White", hovering_color="Gray")
            
            self.screen.blit(ATTACK_TEXT, ATTACK_RECT)

            for button in [MOUSE_BUTTON, RETURN_BUTTON]:
                button.changeColor(ATTACK_MOUSE_POS)
                button.update(self.screen)
            pos = pygame.mouse.get_pos()
            self.screen.blit(self.cursor, pos)      
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if MOUSE_BUTTON.checkForInput(ATTACK_MOUSE_POS):
                        
                        MOUSE_TEXT = get_font(100).render("LEFT CLICK", True, "White")
                        MOUSE_RECT = MOUSE_TEXT.get_rect(center=(self.screen_width/2, 300))
                        self.screen.blit(MOUSE_TEXT, MOUSE_RECT)
                        
                    if RETURN_BUTTON.checkForInput(ATTACK_MOUSE_POS):
                        
                        self.informations()
                        
                        
                pygame.display.update()
                
    def go(self):

        clock  = pygame.time.Clock()

        jeu = True
        while jeu:
            #cette boucle va répéter toutes les fonctions qui font marcher le jeu jusqu'a ce qu'on appuie sur la croix
            self.joueur.save_location()
            self.update()
            self.map_manager.draw()
            self.update_mobs()
            self.update_items()
            self.update_joueur()
            self.joueur.weapon.update()
            pygame.display.flip()

            #vérification de l'appui sur la croix
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            clock.tick(120)
        pygame.quit()
            
    
    def game_over(self):
        while True:
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.fill("black")

            PLAY_TEXT = get_font(75).render("YOU LOST...", True, "White")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(self.screen_width/2, 260))
            self.screen.blit(PLAY_TEXT, PLAY_RECT)

            PLAY_BACK = Button(image=None, pos=(self.screen_width/2, 660), 
                                text_input="Menu", font=get_font(45), base_color="White", hovering_color="Gray")

            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(self.screen)
            pos = pygame.mouse.get_pos()
            self.screen.blit(self.cursor, pos)  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()
            
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)