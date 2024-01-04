import pygame
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
tmx_data = load_pygame("C:/Users/manaz/Desktop/Work/Game-Tinker/Tiled/Desert Game/test-level.tmx")
sprite_group = pygame.sprite.Group()
SCALE = 2.5     # scale to apply before rendering anything 
TILESIZE = 16   # tiles are 16 x 16 pixels

print("------ LAYERS -------")
for layer in tmx_data.visible_layers:
    print(layer.name)

print("------ OBJECTS -------")
object_layer = tmx_data.get_layer_by_name('Objects')
for obj in object_layer:
    print(obj, obj.x, obj.y, obj.image)



class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale_by(surf, SCALE)
        self.rect = self.image.get_rect(topleft=pos)

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("black")

    for layer in tmx_data.visible_layers:
        # Grab only non object layers
        if hasattr(layer, 'data'):     
            for x, y, surf in layer.tiles():
                pos = (x*TILESIZE*SCALE, y*TILESIZE*SCALE)
                Tile(pos=pos, surf=surf, groups=sprite_group)
    
    for obj in tmx_data.objects:
        pos = (obj.x*SCALE, obj.y*SCALE)
        Tile(pos=pos, surf=obj.image, groups=sprite_group)
    
    sprite_group.draw(screen)

    pygame.display.update()
    