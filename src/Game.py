import pygame, random
from GameObjects import *

class Game:
    def __init__(self, centerPoint):
        self.centerPoint = centerPoint
        self.sprites = pygame.sprite.LayeredUpdates()
        self.viruses = pygame.sprite.Group()
        self.tagged_viruses = pygame.sprite.Group()
        self.antibodies = pygame.sprite.Group()
        self.proteasomes = pygame.sprite.Group()
        self.selected_proteasome = None
        self.cellGroup = pygame.sprite.GroupSingle(Cell(self.centerPoint))
        self.nucleusGroup = pygame.sprite.GroupSingle(Nucleus(self.centerPoint))
        self.sprites.add(self.cellGroup.sprite)
        self.sprites.add(self.nucleusGroup.sprite)
        self.seconds = 0

    def spawn_virus(self):
        width = self.centerPoint.x * 2
        radius = (width + 200) / 2
        # TIME TO DO SOME MATH YO
        # Problem: We want to randomly generate a position for the virus to spawn at but we want it to be on the edge of the screen instead of anywhere on the screen
        # Solution: Pretend there's an imaginary circle with a diameter close to the size of the screen and pick a random point on its circumference
        angle = random.random() * math.pi * 2
        rand_x = int(math.cos(angle) * radius)
        rand_y = int(math.sin(angle) * radius)
        # There's probably a reasonable explanation as to why this works but I'm too tired to attempt to comprehend it
        # But wait! There's more!
        # http://i.imgur.com/ZOOgrOA.png
        # New problem: (0, 0) in pygame is the top left corner, so the imaginary circle is apparently centered on that
        # New solution: offset the generated coordinates so they appear centered on the...well, center
        x = rand_x + self.centerPoint.x
        y = rand_y + self.centerPoint.y
        # Result: http://i.imgur.com/IHVvm6g.png
        # Happy times.
        position = Coordinates(x, y)
        virus = Virus(position, self.centerPoint)
        self.viruses.add(virus)
        self.sprites.add(virus)

    def spawn_proteasome(self):
        radius = 100
        angle = random.random() * math.pi * 2
        rand_x = int(math.cos(angle) * radius)
        rand_y = int(math.sin(angle) * radius)
        x = rand_x + self.centerPoint.x
        y = rand_y + self.centerPoint.y
        position = Coordinates(x, y)
        proteasome = Proteasome(position)
        self.proteasomes.add(proteasome)
        self.sprites.add(proteasome)


    def spawn_antibody(self, pos):
        antibody = Antibody(pos)
        self.antibodies.add(antibody)
        self.sprites.add(antibody)

    # See https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollide for docs on spritecollide
    def update(self):
        '''
        Algorithm:
        1. Update all the sprites, causing a change in position for the ones who need it.
        2. If viruses touch the nucleus, kill them.
        3. If viruses touch a proteasome, kill them.
        4. If viruses touch an antibody, tag them and remove the antibody.
        5. If untagged viruses touch tagged viruses, tag them too.
        * Rendering is handled in render_scene method of GameScene
        '''
        self.sprites.update()
        for virus in pygame.sprite.groupcollide(self.viruses, self.nucleusGroup, False, False):
            # End the game
            end_game_event = pygame.event.Event(pygame.USEREVENT + 2, seconds = self.seconds)
            pygame.event.post(end_game_event)
        # dokill1 is set to true so any viruses that touch will be killed
        pygame.sprite.groupcollide(self.viruses, self.proteasomes, True, False)
        for virus in pygame.sprite.groupcollide(self.viruses, self.antibodies, False, True):
            # dokill2 is set to True - any sprites in self.antibodies will be killed upon contact
            virus.tag()
            self.tagged_viruses.add(virus)
        for untagged_virus in pygame.sprite.groupcollide(self.viruses, self.tagged_viruses, False, False, pygame.sprite.collide_circle):
            untagged_virus.tag()
            self.tagged_viruses.add(untagged_virus)

    def every_second(self):
        self.seconds += 1
        if self.seconds == 1:
            self.spawn_proteasome()
            self.spawn_proteasome()
            self.spawn_proteasome()
        if self.seconds % 2 == 0:
            self.spawn_virus()
            self.spawn_virus()
            self.spawn_virus()

    def handle_click(self, pos):
        coords = Coordinates(pos[0], pos[1])
        click_sprite = MouseClickSprite(coords)
        '''
        Algorithm:
        1. If a proteasome has been previously selected, ensure that the click is within the cell but not on the nucleus. If true, command the proteasome to move there and unselect it. Else, alert the user somehow.
        2. If a click was placed on a proteasome, select that proteasome.
        3. If the click was not placed on a virus or the cell, spawn an antibody at that location.
        '''
        # 1
        if self.selected_proteasome != None:
            if pygame.sprite.spritecollide(click_sprite, self.cellGroup, False, pygame.sprite.collide_circle) and not pygame.sprite.spritecollide(click_sprite, self.nucleusGroup, False, pygame.sprite.collide_circle):
                self.selected_proteasome.move_to(coords)
            else:
                # Click was not within the cell or in the nucleus
                pass
            self.selected_proteasome.unselect()
            self.selected_proteasome = None
            return
        # 2
        potential_selection = pygame.sprite.spritecollide(click_sprite, self.proteasomes, False)
        if len(potential_selection) != 0:
            self.selected_proteasome = potential_selection[0]
            self.selected_proteasome.select()
            return
        # 3
        # We don't need to check for collisions with nucleusGroup because cellGroup's rect contains it
        if pygame.sprite.spritecollide(click_sprite, self.viruses, False) or pygame.sprite.spritecollide(click_sprite, self.cellGroup, False, pygame.sprite.collide_circle):
            return
        self.spawn_antibody(coords)
