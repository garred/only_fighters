'''Manages the game mechanics.'''

import random
import pygame
import pytmx
import pyscroll
import app
from pygame.constants import K_1, K_2
from characters import NinjaPlayer, NinjaEnemy, ArcherPlayer, ArcherEnemy, BanditPlayer, BanditEnemy, keymap1, keymap2
from items import LifePotionSmall, Axe, Bow, Knife, Sword, Portal
from collisions import get_collision_grid, get_positions_in_grid, get_objects_in_range



def update():
    '''Makes the game seems alive and responsive.'''
    global keys_pressed

    keys_pressed = pygame.key.get_pressed() # Needed to handling keyboard and mouse events

    # Processing inputs
    process_inputs()

    # Updating things in the game
    render_group.update() #Updating the relative position of the entities to the camera.
    update_collisions()
    update_objects()

    # If all players died, re-run last map
    if len(players)==0: load_map(last_map_loaded, reset_players=True)



def update_objects():
    for o in animated_objects:
        o.update()



def process_inputs():
    '''Input processing related to the game as a whole.'''
    global keys_pressed

    if keys_pressed[K_1]:
        renderer.zoom *= 1.05
    if keys_pressed[K_2]:
        renderer.zoom /= 1.05



def update_collisions():
    '''Updates collisions between sprites, in a completly unefficient way.'''

    global hitboxes, collisionable_sprites

    # Update collisions between characters

    grid = get_collision_grid(collisionable_sprites, map)
    for a in collisionable_sprites:
        for b in get_objects_in_range(a, grid, map):
            if a is b: continue
            a.bounce(b)
            b.bounce(a)

    # Update hitboxes

    for h in hitboxes:
        for o in get_objects_in_range(h, grid, map):
            if h.colliderect(o.feet_rect):
                o.hitted(h)
    # TODO: Restore this
    hitboxes = list()

    # Update collisions between characters and items

    for b in touchable_objects:
        b.set_animation('stand')
    grid = get_collision_grid(touchable_objects, map)
    for a in collisionable_sprites:
        for b in get_objects_in_range(a, grid, map):
            b.touched_by(a)



def draw():
    '''Draws all the entities and the background.'''

    app.screen.fill((0, 0, 0))

    # center the map/screen on our Heroes
    if len(players)>1:
        center = ((players[0].rect.centerx + players[1].rect.centerx)*0.5,
                  (players[0].rect.centery+players[1].rect.centery)*0.5)
        render_group.center(center)
    elif len(players)==1:
        render_group.center(players[0].rect.center)
    else:
        render_group.center((0,0))


    # draw the map and all sprites
    render_group._spritelist.sort(key=lambda x: x.feet_rect.centery) #Sorting sprites by depth.
    render_group.draw(app.screen)


    # Draw information about players' life, stamina, etc.
    draw_players_info()

    # # TODO: CLEAN THIS CODE WHEN DEBUGGING CHARACTERS IS NO LONGER NEEDED
    # # Raw way of rendering things for debuging
    # camx = -player1.rect.centerx+app.screen_width*0.5
    # camy = -player1.rect.centery+app.screen_height*0.5
    #
    # for h in hitboxes:
    #     rect = (h.rect[0]+camx, h.rect[1]+camy, h.rect[2], h.rect[3])
    #     pygame.draw.rect(app.screen, (255, 0, 0), rect)
    # hitboxes = list()
    #
    # for e in animated_objects:
    #     rect = (e.feet_rect[0]+camx, e.feet_rect[1]+camy, e.feet_rect[2], e.feet_rect[3])
    #     pygame.draw.rect(app.screen, (0, 255, 0), rect)



def draw_players_info():
    render_group.center((0,0))

    # Player 1 info
    if len(players)>0:
        pygame.draw.rect(app.screen, (  0,  0,  0), (20, 20, 200, 20))
        if players[0].life > 0: pygame.draw.rect(app.screen, (255,  0,  0), (23, 23, 194*max(0,players[0].life)/players[0].max_life, 14))
        pygame.draw.rect(app.screen, (  0,  0,  0), (20, 40, 200, 20))
        pygame.draw.rect(app.screen, (255,255,255), (23, 43, 194*max(0,players[0].stamina)/players[0].max_stamina, 14))

    # Player 2 info
    if len(players)>1:
        pygame.draw.rect(app.screen, (  0,  0,  0), (app.screen_width-20-200, 20, 200, 20))
        if players[1].life > 0: pygame.draw.rect(app.screen, (255,  0,  0), (app.screen_width-17-200, 23, 194*players[1].life/players[1].max_life, 14))
        pygame.draw.rect(app.screen, (  0,  0,  0), (app.screen_width-20-200, 40, 200, 20))
        pygame.draw.rect(app.screen, (255,255,255), (app.screen_width-17-200, 43, 194*max(0, players[1].stamina)/players[1].max_stamina, 14))



# Loading main map

def load_map(path, reset_players=False):

    global map, map_rect, renderer
    global render_group, animated_objects, collisionable_sprites, hitboxes, touchable_objects, collisionable_walls, players, grid_collisionable_walls
    global last_map_loaded

    last_map_loaded = path


    # Load the map

    map = pytmx.util_pygame.load_pygame(path)
    map_rect = (0, 0, map.width*map.tilewidth, map.height*map.tileheight)


    # Load music and start playing it
    if hasattr(map, 'music'):
        pygame.mixer.music.load('data/music/' + map.music)
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    # Creating global containers

    renderer = pyscroll.BufferedRenderer(pyscroll.data.TiledMapData(map), app.screen.get_size()) # "Camera" of the game: it renders objects.'''
    renderer.zoom = 1.5

    render_group = pyscroll.group.PyscrollGroup(map_layer=renderer, default_layer=2) # This defines the group of renderizable sprites.

    animated_objects = list() # Holds everything that needs to be updated by PygAnim.
    collisionable_sprites = list() # Sprites that can collide between them
    hitboxes = list() # Hitbox objects
    touchable_objects = list()


    # Creating objects of the map

    # Walls

    collisionable_walls = [pygame.Rect(o.x,o.y, o.width,o.height) for o in map.layernames['walls']] # This contains the walls of the map
    grid_collisionable_walls = get_collision_grid(collisionable_walls, map, size=10) #Used for optimization


    # Characters
    old_players = players if players is not None else []
    players = []
    for map_object in map.layernames['characters']:

        # Selecting keyboard
        key = keymap1 if len(players) == 0 else keymap2

        # Creating the object
        if map_object.class_ninja == 'true':
            if map_object.is_player == 'true':
                new_character = NinjaPlayer(key)
                players.append(new_character)
            else:
                new_character = NinjaEnemy()
        elif map_object.class_archer == 'true':
            if map_object.is_player == 'true':
                new_character = ArcherPlayer(key)
                players.append(new_character)
            else:
                new_character = ArcherEnemy()
        elif map_object.class_bandit == 'true':
            if map_object.is_player == 'true':
                new_character = BanditPlayer(key)
                players.append(new_character)
            else:
                new_character = BanditEnemy()

        # Setting attributes

        # Position
        new_character.position = (map_object.x - 50, map_object.y - 45)

        # Weapons
        weapon_list = []
        if map_object.weapon_unarmed == 'true': weapon_list.append('unarmed')
        if map_object.weapon_knife == 'true': weapon_list.append('knife')
        if map_object.weapon_sword == 'true': weapon_list.append('sword')
        if map_object.weapon_axe == 'true': weapon_list.append('axe')
        if map_object.weapon_bow == 'true': weapon_list.append('bow')

        if len(weapon_list)>0:
            new_character.weapon = random.choice(weapon_list)
        else:
            new_character.weapon = 'unarmed'

        # Things for NPCs:
        if map_object.is_player == 'false':
            # Wandering zones
            new_character.territory_radius = float(map_object.territory_radius) * map.tilewidth

            # Patroling zones (for NPCs):
            if hasattr(map_object, 'points'):
                new_character.path = list()
                for p in map_object.points:
                    new_character.path.append((p[0], p[1]))
                new_character.position = (new_character.path[0][0]-50, new_character.path[0][1]-45)

    if not reset_players:
        for idx, player in enumerate(players):
            if idx < len(old_players):
                player.weapon = old_players[idx].weapon
                player.life = old_players[idx].life



    # Creating items

    for map_object in map.layernames['items']:

        # Creating the object
        item_classes = list()

        if map_object.class_life_small == 'true': item_classes.append(LifePotionSmall)
        if map_object.class_axe == 'true': item_classes.append(Axe)
        if map_object.class_bow == 'true': item_classes.append(Bow)
        if map_object.class_knife == 'true': item_classes.append(Knife)
        if map_object.class_sword == 'true': item_classes.append(Sword)

        if len(item_classes)>0: random.choice(item_classes)((map_object.x - 35, map_object.y - 25))


    # Creating portals

    if 'portals' in map.layernames:
        for map_object in map.layernames['portals']:

            p = Portal((map_object.x - 35, map_object.y - 25))
            p.to_map = map_object.to_map




# Global objects

keys_pressed = {}


# The game mechanics is updating.
active = False
# The game graphics are visible.
visible = True


# Map related objects
map = map_rect = renderer = render_group = animated_objects = collisionable_sprites = hitboxes = touchable_objects = \
    collisionable_walls = grid_collisionable_walls = players = last_map_loaded = None


