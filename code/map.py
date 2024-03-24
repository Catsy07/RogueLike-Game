import pygame, pytmx, pyscroll
from player import *
from time import sleep

class Portail:
    def __init__(self, from_world, origin_point, target_world, teleport_point):
        self.from_world = from_world
        self.origin_point = origin_point
        self.target_world = target_world
        self.teleport_point = teleport_point


class Map:
    def __init__(self, nom, murs, groupe, tmx_data, portails, map_layer, mobs):
        # Class map qui a un nom, des collisions et un groupe de calques
        self.nom = nom
        self.murs = murs
        self.groupe = groupe
        self.tmx_data = tmx_data
        self.portails = portails
        self.map_layer = map_layer
        self.mobs = mobs

class MapManager:
    def __init__(self, screen, joueur):
        
        self.maps = dict() #On va stocker toutes les differentes cartes ici
        self.screen = screen
        self.joueur = joueur
        self.current_map = 'Spawn' # Map actuelle 
        
        # On crée les cartes 
        self.nouvelle_carte("Spawn", portails=[
            Portail('Spawn', "sortie_spawn", 'Map 1', 'spawn_map1')
        ]) 
        self.nouvelle_carte("Map 1", portails=[
            Portail('Map 1', "sortie_map1", 'Spawn', 'spawn_spawn')
        ])

        self.teleport("spawn_spawn")

    def collisions(self):
        # teste la collision avec une porte pour se tp
        for portail in self.map_info().portails:
            if portail.from_world == self.current_map:
                point = self.objet(portail.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.joueur.feet.colliderect(rect):
                    copy_portail = portail
                    self.current_map = portail.target_world
                    self.teleport(copy_portail.teleport_point)

        for sprite in self.groupe().sprites():
            if type(sprite) == Joueur:
                if sprite.feet.collidelist(self.murs()) > -1:
                    sprite.collision()
            elif type(sprite) == Monstre:
                if sprite.rect.collidelist(self.murs()) > -1:
                    sprite.collision()

    def teleport(self, nom):
        point = self.objet(nom)
        self.joueur.position[0] = point.x
        self.joueur.position[1] = point.y
        self.joueur.save_location()


    def nouvelle_carte(self,nom, portails=[]):
        # Fonction qui permet de créer une carte et de la stocker dans le dictionnaire "maps"
        tmx_data = pytmx.util_pygame.load_pygame(f"code/Maps2/{nom}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data) # on récupere les données de la carte
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3 # Zoom sur le joueur

        # Liste qui contient tous les murs et donc les collisions
        walls = []
        # On ajoute tous les objets avec le type 'Collision' dans la liste 'walls'
        for obj in tmx_data.objects:
            if obj.type == 'Collisions':
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
         

        mobs = []

        for obj in tmx_data.objects:
            if obj.type == 'spawn_mob':
                mobs.append(Monstre(obj.name, obj.x, obj.y, self.joueur, 14))
        # On crée un groupe qui contient tous les calques de la map pour povoir tous les injecter en meme temps
        groupe = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4) 
        groupe.add(self.joueur)
        for i in mobs:
            groupe.add(i)

        map = Map(nom, walls, groupe, tmx_data, portails, map_layer, mobs) # Finalement on crée la carte a partir des infos qu'on a pu récuperer
        self.maps[nom] = map # On range cette carte dans le dictionnaire

    def map_info(self):
        # Récupération des infos de la map
        return self.maps[self.current_map]
    
    def groupe(self):
        # A partir des infos on récupere le groupe de calques
        return self.map_info().groupe
    
    def map_layer(self):
        # A partir des infos on récupere le groupe de calques
        return self.map_info().map_layer
    
    def murs(self):
        # Et les murs
        return self.map_info().murs
    
    def objet(self,nom):
        return self.map_info().tmx_data.get_object_by_name(nom)
    
    def mobs(self):
        return self.map_info().mobs
    
    

    def draw(self):
        #on dessine la carte
        self.groupe().draw(self.screen)
        self.groupe().center(self.joueur.rect.center)

    def update(self):
        self.groupe().update()
        self.collisions()
        
