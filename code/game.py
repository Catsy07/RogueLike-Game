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

        # On crée un instance de la classe Joueur
        self.joueur = Joueur()
        self.map_manager = MapManager(self.screen, self.joueur)

        #liste des mobs
        self.mobs = []
        
        #self.joueur.weapon = Weapon(self.joueur_vect, 'grande_epee', self.screen, self.map_manager.groupe()._spritelist, self.joueur)

    def attaque(self):
        self.joueur_pos = self.map_manager.map_layer().translate_point(self.joueur.position)
        self.joueur_vect = pygame.Vector2(self.joueur_pos[0],self.joueur_pos[1])
        self.joueur.weapon = Weapon(self.joueur_vect, 'grande_epee', self.screen, self.map_manager.groupe()._spritelist, self.joueur)
    

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
            OPTIONS_BUTTON = Button(image=pygame.image.load("graphiques/menu/Options Rect.png"), pos=(self.screen_width/2, 500), 
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("graphiques/menu/Quit Rect.png"), pos=(self.screen_width/2, 650), 
                                text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.go()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pass
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