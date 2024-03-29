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
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Soul Knight")

        # On crée un instance de la classe Joueur
        self.joueur = Joueur()
        self.map_manager = MapManager(self.screen, self.joueur)

        #liste des mobs
        self.mobs = []
        
        self.img_mouse = pygame.image.load("graphiques/menu/mouse.png")

        potion = Item('potion', 1, 'heal', 2, self.joueur)
        self.joueur.inventory.append(potion)
    def attaque(self):
        self.joueur_pos = self.map_manager.map_layer().translate_point(self.joueur.position)
        self.joueur_vect = pygame.Vector2(self.joueur_pos[0],self.joueur_pos[1])
        self.joueur.weapon = Weapon(self.joueur_vect, 'grande_epee', self.screen, self.map_manager.groupe()._spritelist, self.joueur)
        self.joueur.use_item()
        print(self.joueur.inventory)
    

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

    def check_stop(self):
        if self.joueur.health <= 0:
            self.game_over()
            
    

    def update(self):
        #cette fonction vérifie les parametres du jeu pour gerer les collisions, les interactions, etc...
        self.joueur.presse()
        self.map_manager.update()
        self.attaque()
        
    def main_menu(self):
        menu = True
        while True:
            self.screen.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("The Dungeon", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(self.screen_width/2, 150))

            PLAY_BUTTON = Button(image=pygame.image.load("graphiques/menu/Play Rect.png"), pos=(self.screen_width/2, 350), 
                                text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            INFORMATIONS_BUTTON = Button(image=pygame.image.load("graphiques/menu/Informations Rect.png"), pos=(self.screen_width/2, 500), 
                                text_input="INFOS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("graphiques/menu/Quit Rect.png"), pos=(self.screen_width/2, 650), 
                                text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, INFORMATIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.go()
                    if INFORMATIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.informations()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        jeu = False
                        pygame.quit()
                

            pygame.display.update()
    
    def go(self):

        clock  = pygame.time.Clock()

        jeu = True
        while jeu:
            #cette boucle va répéter toutes les fonctions qui font marcher le jeu jusqu'a ce qu'on appuie sur la croix
            self.check_stop()
            self.joueur.save_location()
            self.update()
            self.map_manager.draw()
            self.joueur.weapon.update()
            self.update_mobs()
            self.joueur.show_life(self.screen)
            pygame.display.flip()

            #vérification de l'appui sur la croix
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            clock.tick(120)
        pygame.quit()

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
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
            
        
            MOUSE_BUTTON = Button(image=pygame.transform.scale(self.img_mouse, (100,100)), pos=(self.screen_width/2, 500),
                          text_input="", font=get_font(100), base_color="White", hovering_color="Gray")
            
            RETURN_BUTTON = Button(image=None, pos=(100, 150), 
                                    text_input="<-", font=get_font(40), base_color="White", hovering_color="Gray")
            
            self.screen.blit(ATTACK_TEXT, ATTACK_RECT)

            for button in [MOUSE_BUTTON, RETURN_BUTTON]:
                button.changeColor(ATTACK_MOUSE_POS)
                button.update(self.screen)
                
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