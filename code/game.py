import pygame
import pytmx
import pyscroll
from map import MapManager
import math

from player import *

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
        self.joueur_pos = self.map_manager.map_layer().translate_point(self.joueur.position)
        self.joueur_vect = pygame.Vector2(self.joueur_pos[0],self.joueur_pos[1])
        self.vect_center = self.joueur_vect//2
        self.xbool = False

    def souris(self):
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            self.joueur_pos = self.map_manager.map_layer().translate_point(self.joueur.position)
            self.joueur_vect = pygame.Vector2(self.joueur_pos[0],self.joueur_pos[1])
            self.joueur.attaque(self.joueur_vect, 'hache', self.screen)


    def presse(self):
        #Cette fonction va servir a récupérer les touches pressées par le joueur sur le clavier ou la souris
        presse = pygame.key.get_pressed()
        
        # Mouvements du joueur avec ZSQD ou les fleches
        if presse[pygame.K_UP] or presse[pygame.K_z]:
            self.joueur.move_high(-1)
            self.joueur.change_animation('run',self.xbool)
        elif presse[pygame.K_DOWN] or presse[pygame.K_s]:
            self.joueur.move_high(1)
            self.joueur.change_animation('run',self.xbool)
        elif presse[pygame.K_LEFT] or presse[pygame.K_q]:
            self.joueur.move_side(-1)
            self.xbool = True
            self.joueur.change_animation('run',self.xbool)
        elif presse[pygame.K_RIGHT] or presse[pygame.K_d]:
            self.joueur.move_side(1)
            self.xbool = False
            self.joueur.change_animation('run',self.xbool)
        else:
            
            self.joueur.change_animation('idle',self.xbool)

    def update(self):
        #cette fonction vérifie les parametres du jeu pour gerer les collisions, les interactions, etc...
        self.map_manager.update()
        

    def go(self):

        clock  = pygame.time.Clock()

        jeu = True
        while jeu:
            #cette boucle va répéter toutes les fonctions qui font marcher le jeu jusqu'a ce qu'on appuie sur la croix
            self.joueur.save_location()
            self.presse()
            self.update()
            self.map_manager.draw()
            self.souris()
            pygame.display.flip()

            #vérification de l'appui sur la croix
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            clock.tick(120)
        pygame.quit()