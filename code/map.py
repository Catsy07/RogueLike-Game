import pygame, pytmx, pyscroll
from player import *
from time import sleep
import xml.etree.ElementTree as ET
import random

last_attack_time = 0
attack_cooldown = 500
class Portail:
    def __init__(self, from_world, origin_point, target_world, teleport_point):
        self.from_world = from_world
        self.origin_point = origin_point
        self.target_world = target_world
        self.teleport_point = teleport_point


class Map:
    def __init__(self, nom, murs, groupe, tmx_data, portails, map_layer, mobs, items, pics, tresor):
        # Class map qui a un nom, des collisions et un groupe de calques
        self.nom = nom
        self.murs = murs
        self.groupe = groupe
        self.tmx_data = tmx_data
        self.portails = portails
        self.map_layer = map_layer
        self.mobs = mobs
        self.items = items
        self.pics = pics
        self.tresor = tresor

class MapManager:
    def __init__(self, screen, joueur):
        
        self.maps = dict() #On va stocker toutes les differentes cartes ici
        self.screen = screen
        self.joueur = joueur
        self.EO = ['EO_1.tmx', 'EO_2.tmx']
        self.NE = ['NE_1.tmx', 'NE_2.tmx']
        self.NO = ['NO_1.tmx', 'NO_2.tmx']
        self.NS = ['NS_1.tmx', 'NS_2.tmx']
        self.NSE = ['NSE_1.tmx', 'NSE_2.tmx']
        self.O = ['O_1.tmx', 'O_2.tmx','O_3.tmx']
        self.SE = ['SE_1.tmx', 'SE_2.tmx']
        self.SEO = ['SEO_1.tmx', 'SEO_2.tmx']
        self.SO = ['SO_1.tmx', 'SO_2.tmx']
        self.SIDE = 'SIDE.tmx'
        self.current_map = 'Spawn' # Map actuelle 
        self.current_level = 'lvl1'
        self.maps1 = [self.SIDE, self.SIDE, self.SIDE, self.SIDE, self.SIDE, self.SIDE, random.choice(self.NE), random.choice(self.EO), random.choice(self.NO), self.SIDE, self.SIDE, random.choice(self.NS), 'sortie_lvl2.tmx', 'spawn_lvl2.tmx', self.SIDE, self.SIDE, random.choice(self.SE), random.choice(self.SEO), random.choice(self.O), self.SIDE, self.SIDE, self.SIDE, self.SIDE, self.SIDE, self.SIDE]
        #self.maps1 = [random.choice(self.O),random.choice(self.O),random.choice(self.O),random.choice(self.O), 'sortie_lvl2.tmx',random.choice(self.O),random.choice(self.O),random.choice(self.O),random.choice(self.O)]
        self.niveau1 = self.assemblage_map(self.maps1, 'niveau1')
        # On crée les cartes 
        self.nouvelle_carte("Spawn", portails=[
            Portail('Spawn', "sortie_spawn", 'niveau1', 'spawn_lvl2')
        ]) 
        self.nouvelle_carte("niveau1", portails=[
            Portail('niveau1', "sortie_lvl2", 'Spawn', 'spawn_spawn')
        ])

        self.teleport("spawn_spawn")


    def collisions(self):
        global last_attack_time, attack_cooldown
        
        current_time = pygame.time.get_ticks()
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
            if type(sprite) == Joueur:
                if sprite.feet.collidelist(self.pics()) > -1 and current_time - last_attack_time > attack_cooldown:
                    sprite.health -= 1
                    last_attack_time = current_time
            elif type(sprite) == Monstre:
                if sprite.rect.collidelist(self.murs()) > -1:
                    sprite.collision()

    def teleport(self, nom):
        point = self.objet(nom)
        self.joueur.position[0] = point.x
        self.joueur.position[1] = point.y
        self.joueur.save_location()

    def assemblage_map(self, maps, nom):

        sol = [[]]
        murs = [[]]
        obj1 = [[]]
        obj2 = [[]]
        objects = []
        a = 2
        for i in range(5):
            nb = 1
            layer_data3 = []
            b = 0
            for map in maps[i*5:i*5+5]:
                # Charger le contenu du fichier TMX (remplacez 'your_map_file.tmx' par le chemin réel du fichier)
                tree = ET.parse(f'code/Maps2/{map}')
                root = tree.getroot()

                # Accéder à la première couche <layer> et extraire les données <data> à l'intérieur
                for layer in root.findall('layer'):
                    layer_data = ''
                    layer_data2 = []
                    layer_data += layer.find('data').text.strip()
                    layer_data = layer_data.split(',')
                    # Ici, 'data' contient le contenu textuel de la balise <data>, c'est-à-dire les indices des tuiles
                        
                    for i in range(0, 1600, 40):
                        #crée une liste avec des listes de 20 caracteres (représentant chaque ligne de la layer)
                        layer_data2.append(layer_data[i:(i+40)])
                    
                    nbsol = 1
                    nbmurs = 1
                    nbobj1 = 1
                    for j in layer_data2:
                    #insere la liste au bon endroit dans la 'liste finale'
                        if layer.get('name') == 'Sol':
                            sol[0].insert(nb*nbsol-1 , j)
                            nbsol += 1
                        elif layer.get('name') == 'Murs':
                            murs[0].insert(nb*nbmurs-1 , j)
                            nbmurs += 1
                        elif layer.get('name') == 'Objets 1':
                            obj1[0].insert(nb*nbobj1-1 , j)
                            nbobj1 += 1
                for objectgroup in root.findall('objectgroup'):
                    # Itérer sur chaque <object> à l'intérieur du groupe d'objets
                    for obj in objectgroup.findall('object'):
                        obj.set('x', str(float(obj.get('x'))+640*b))
                        obj.set('y', str(float(obj.get('y'))+ 1280 + 640*(a)))
                        objects.append(obj)
                nb+=1
                b += 1
            a-=1
        def list_to_str(list):
            string = ''
            for section in list:
                for row in section:
                    row2 = ','.join(row)
                    string += row2
                    string += ','
            return string[:len(string)-1]

        string_sol = list_to_str(sol)
        string_murs = list_to_str(murs)
        string_obj1 = list_to_str(obj1)
        pygame.display.set_caption("Dungeon Example")
        # Créer l'élément racine <map> avec ses attributs
        map_elem = ET.Element("map", version="1.10", tiledversion="1.10.2",
                            orientation="orthogonal", renderorder="right-down", width="200", height="200", tilewidth="16",
                            tileheight="16", infinite="0", nextlayerid="2", nextobjectid="1")

        # Créer un tileset
        tileset = ET.SubElement(map_elem, "tileset", firstgid="1", source="Nv 1.tsx")

        # Sauvegarder l'arbre XML dans un fichier
        tree = ET.ElementTree(map_elem)
        tree.write(f"code/Maps2/{nom}.tmx", xml_declaration=True, encoding='UTF-8')

        # Créer un élément <layer>
        layer_sol = ET.SubElement(map_elem, "layer", id="1", name="Sol", width='200', height="200")
        layer_mur = ET.SubElement(map_elem, "layer", id="2", name="Murs", width='200', height="200")
        layer_obj1 = ET.SubElement(map_elem, "layer", id="3", name="Objets 1", width='200', height="200")

        # Créer un élément <data> avec un encodage CSV
        data_sol = ET.SubElement(layer_sol, "data", encoding="csv")
        data_mur = ET.SubElement(layer_mur, "data", encoding="csv")
        data_obj1 = ET.SubElement(layer_obj1, "data", encoding="csv")

        # Insérer les données de tuiles (vous devriez remplacer cela par vos propres données)
        data_sol.text = string_sol
        data_mur.text = string_murs
        data_obj1.text = string_obj1

        layer_objects = ET.SubElement(map_elem,'objectgroup', id='5', name="objets")
        id = 6
        for obj in objects:
            if type(obj.get('width')) == str:
                new_obj = ET.SubElement(layer_objects, "object", name=obj.get('name'), type=obj.get('type'), x=obj.get('x'), y=obj.get('y'), width=obj.get('width'), height=obj.get('height'))
            else:
                new_obj = ET.SubElement(layer_objects, "object", name=obj.get('name'), type=obj.get('type'), x=obj.get('x'), y=obj.get('y'))
                # Pour un point, ajouter un élément <point/> à l'objet
                point = ET.SubElement(new_obj, "point")
        # Sauvegarder les modifications dans le fichier
        tree.write(f"code/Maps2/{nom}.tmx", xml_declaration=True, encoding='UTF-8')

        tmx_data = pytmx.util_pygame.load_pygame(f'code/Maps2/{nom}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, (1200, 1200))
        groupe = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        return groupe
    
    def nouvelle_carte(self,nom, portails=[]):
        # Fonction qui permet de créer une carte et de la stocker dans le dictionnaire "maps"
        tmx_data = pytmx.util_pygame.load_pygame(f"code/Maps2/{nom}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data) # on récupere les données de la carte
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2.5 # Zoom sur le joueur

        # Liste qui contient tous les murs et donc les collisions
        walls = []
        # On ajoute tous les objets avec le type 'Collision' dans la liste 'walls'
        for obj in tmx_data.objects:
            if obj.type == 'Collisions':
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
         

        mobs = []

        
        for obj in tmx_data.objects:
            if obj.type == 'spawn_mob':
                if 'bebe' in obj.name:
                    mobs.append(Monstre(obj.name, obj.x, obj.y, self.joueur, 1, 1, 2.6))
                else:
                    mobs.append(Monstre(obj.name, obj.x, obj.y, self.joueur, 3, 1, 2))

        items = []

        for obj in tmx_data.objects:
                if obj.type == 'item':
                    name, level, type = obj.name.split()
                    items.append(Item(name, type, int(level), self.joueur, obj.x, obj.y, 20, 22, (obj.x, obj.y), 0))
                
        pics = []
        # On ajoute tous les objets avec le type 'Collision' dans la liste 'walls'
        for obj in tmx_data.objects:
            if obj.type == 'Pics':
                pics.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            
        tresor = []
        # On ajoute tous les objets avec le type 'Collision' dans la liste 'walls'
        for obj in tmx_data.objects:
            if obj.type == 'Tresor':
                tresor.append(Tresor(obj.x, obj.y, self.joueur))

        # On crée un groupe qui contient tous les calques de la map pour povoir tous les injecter en meme temps
        groupe = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4) 
        groupe.add(self.joueur)
        for i in mobs:
            groupe.add(i)
        map = Map(nom, walls, groupe, tmx_data, portails, map_layer, mobs, items, pics, tresor) # Finalement on crée la carte a partir des infos qu'on a pu récuperer
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
    
    def items(self):
        return self.map_info().items
    
    def pics(self):
        return self.map_info().pics
    
    def tresors(self):
        return self.map_info().tresor

    def draw(self):
        #on dessine la carte
        self.groupe().draw(self.screen)
        self.groupe().center(self.joueur.rect.center)

    def update(self):
        self.groupe().update()
        self.collisions()
        
