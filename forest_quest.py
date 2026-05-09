#Natalia Sander
#Forest Quest
#4 May 2026


import pygame
import sys
import random
import math

# -----------------------------
# BASIC SETUP
# -----------------------------

# This starts pyagme so the program can use fonts, draw graphics etc.
pygame.init()

# this is the window size for the game screen.
WIDTH = 900
HEIGHT = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Quest")

# this controls how fast the game updates.
clock = pygame.time.Clock()

# Colors - all the colors used during the game.
DARK_GREEN = (22, 48, 32)
FOREST_GREEN = (34, 85, 50)
LIGHT_GREEN = (150, 200, 150)
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
BROWN = (120, 80, 40)
GRAY = (180, 180, 180)
DARK_GRAY = (80, 80, 80)
GOLD = (230, 190, 90)
RED = (180, 60, 60)
MOON_YELLOW = (240, 230, 180)
PURPLE_BLACK = (18, 14, 30)
MIST = (90, 110, 100)
GLOW_BLUE = (90, 180, 200)

# Fonts
TITLE_FONT = pygame.font.SysFont("arial", 56, bold=True)
HEADING_FONT = pygame.font.SysFont("arial", 34, bold=True)
TEXT_FONT = pygame.font.SysFont("arial", 24)
BUTTON_FONT = pygame.font.SysFont("arial", 24, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 18)


# -----------------------------
# THIS IS THE HELPER FUNCTION FOR TEXT
# -----------------------------
def wrap_text(text, font, max_width):
# this breaks long string of text into shorter lines so everything fits   
   
 # a list of shorter text lines that fit on the screen  
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)
    return lines

#this draws wrapped text on the screen one line at a time.
def draw_wrapped_text(text, font, color, x, y, max_width, line_height):
    
    lines = wrap_text(text, font, max_width)
    for i, line in enumerate(lines):
        rendered_line = font.render(line, True, color)
        screen.blit(rendered_line, (x, y + i * line_height))


# -----------------------------
# CLASSES
# -----------------------------

# this one is for one clickable decision the player can make.
# Each Choice stores the text shown on the button, the ID of the scene it
    # leads to and optional changes to the player's bravery and wisdom stats.
class Choice:
   
    def __init__(self, text, next_scene_id, bravery_change=0, wisdom_change=0):
        self.text = text
        self.next_scene_id = next_scene_id
        self.bravery_change = bravery_change
        self.wisdom_change = wisdom_change

# this one represents one section of the story. It has story text, a list of choise object and info about whether the scene is ending.
class Scene:
    
    def __init__(self, scene_id, text, choices=None, is_ending=False, ending_title=""):
        self.scene_id = scene_id
        self.text = text
        self.choices = choices if choices is not None else []
        self.is_ending = is_ending
        self.ending_title = ending_title

# this one stores all the info about the player. The player has bravery and wisdom points that change depending on the choices they make.
class Player:

 # creates a new player with starting stats set to zero  
    def __init__(self):
        self.bravery = 0
        self.wisdom = 0

# this resets the player stats when the game restarts
    def reset(self):
        self.bravery = 0
        self.wisdom = 0

# this one represents a clickable button on the screen. 
# the Button class draws a rectangular button, changes its color when the mouse hovers over it and checks whether it has been clicked.
class Button:
   
    def __init__(self, x, y, width, height, text, color=BROWN, hover_color=GOLD):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color

# draws the button and changes its color
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        pygame.draw.rect(screen, current_color, self.rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=12)

        text_surface = BUTTON_FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

# checks if the button was clicked
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

# this one controls the entire game
# this class creates the player, stores all the scenes, handles screen changes, draws the background and scene graphics, processes mouse clicks and runs the main game loop.
class Game:

 # sets up the starting game state, buttons, screen and graphics    
    def __init__(self):
        self.player = Player()
        self.scenes = self.create_scenes()
        self.current_scene_id = "start"
        self.screen_state = "start_screen"

        self.start_button = Button(WIDTH // 2 - 130, 380, 260, 60, "Start Quest")
        self.restart_button = Button(WIDTH // 2 - 130, 500, 260, 60, "Restart Game")


       
        # Fog slowly moving.
        self.fog_clouds = []
        for i in range(9):
            self.fog_clouds.append({
                "x": random.randint(-100, WIDTH),
                "y": random.randint(120, 520),
                "speed": random.uniform(0.2, 0.7),
                "size": random.randint(70, 160)
            })

        # Fireflies float around the forest.
        self.fireflies = []
        for i in range(25):
            self.fireflies.append({
                "x": random.randint(0, WIDTH),
                "y": random.randint(80, 520),
                "speed": random.uniform(0.4, 1.2),
                "phase": random.uniform(0, 6.28)
            })

# this one creates and returns all story scenes in the game.
    def create_scenes(self):
        scenes = {}

        scenes["start"] = Scene(
            "start",
            "You wake up in a dark forest with no memory of how you got there. The trees are too tall, the air is too quiet, and somewhere far away, a bell rings once. A narrow path leads deeper into the woods. A strange glowing mushroom lights another path to your left.",
            [
                Choice("Follow the narrow path", "old_bridge", bravery_change=1),
                Choice("Touch the glowing mushroom", "mushroom_circle", wisdom_change=1),
                Choice("Call out for help", "footsteps", bravery_change=1),
            ]
        )

        scenes["old_bridge"] = Scene(
            "old_bridge",
            "The narrow path leads you to an old wooden bridge over a black river. The bridge looks weak, but across it you see a lantern hanging from a tree. Under the bridge, something moves in the water.",
            [
                Choice("Carefully cross the bridge", "lantern_tree", bravery_change=1),
                Choice("Look under the bridge", "river_creature", wisdom_change=1),
                Choice("Turn back into the forest", "footsteps"),
            ]
        )

        scenes["mushroom_circle"] = Scene(
            "mushroom_circle",
            "The mushroom glows brighter when you touch it. Suddenly, more mushrooms light up in a circle around you. In the center of the circle, a small fox with silver eyes appears. It tilts its head like it has been waiting for you.",
            [
                Choice("Follow the fox", "fox_path", wisdom_change=1),
                Choice("Run away from the circle", "footsteps", bravery_change=1),
                Choice("Ask the fox for help", "fox_riddle", wisdom_change=1),
            ]
        )

        scenes["footsteps"] = Scene(
            "footsteps",
            "You hear footsteps getting closer. They stop whenever you stop. When you turn around, you see a tall shadow standing between the trees. It does not move, but it raises one long arm and points toward a ruined cabin.",
            [
                Choice("Go to the ruined cabin", "cabin", bravery_change=1),
                Choice("Hide behind a tree", "hidden_tree", wisdom_change=1),
                Choice("Run away", "stranger_man", bravery_change=-1),
            ]
        )

        scenes["stranger_man"] = Scene(
            "stranger_man",
            "You run deeper into the forest until you see a man standing beside an old tree. He smiles like he has been expecting you. 'You look lost,' he says. 'I know the way out. Follow me, and I can help you.'",
            [
                Choice("Accept his offer and follow him", "bad_ending_trust_man"),
                Choice("Run away from him", "old_bridge", bravery_change=1),
            ]
        )

        scenes["lantern_tree"] = Scene(
            "lantern_tree",
            "You cross the bridge safely. The lantern on the tree flickers with golden light. Inside the lantern, you see a tiny map of the forest. The map shows three symbols: a crown, a cave, and a door.",
            [
                Choice("Follow the crown symbol", "forest_king", bravery_change=1),
                Choice("Follow the cave symbol", "crystal_cave", wisdom_change=1),
                Choice("Follow the door symbol", "hidden_door", wisdom_change=1),
            ]
        )

        scenes["river_creature"] = Scene(
            "river_creature",
            "You lean over the bridge and see a creature made of water staring back at you. It whispers, 'The forest only frees those who listen.' It offers you a silver stone.",
            [
                Choice("Take the silver stone", "crystal_cave", wisdom_change=2),
                Choice("Refuse and cross the bridge", "lantern_tree", bravery_change=1),
                Choice("Ask what the stone does", "river_answer", wisdom_change=1),
            ]
        )

        scenes["river_answer"] = Scene(
            "river_answer",
            "The creature says the silver stone can open one locked path, but only if you are brave enough to carry it. The stone feels cold in your hand, but somehow comforting.",
            [
                Choice("Carry the stone to the cave", "crystal_cave", bravery_change=1, wisdom_change=1),
                Choice("Leave the stone and go to the lantern", "lantern_tree"),
            ]
        )

        scenes["fox_path"] = Scene(
            "fox_path",
            "The fox leads you through a tunnel of branches. You arrive at a clearing where moonlight falls on an ancient door standing alone in the dirt. There are no walls around it, but the door is locked.",
            [
                Choice("Open the door", "hidden_door", bravery_change=1),
                Choice("Look for another path", "crystal_cave", wisdom_change=1),
                Choice("Follow the fox again", "fox_riddle", wisdom_change=1),
            ]
        )

        scenes["fox_riddle"] = Scene(
            "fox_riddle",
            "The fox speaks: 'I grow when you share me, but disappear when you hide me. What am I?' The forest becomes silent, waiting for your answer.",
            [
                Choice("A secret", "bad_ending_secret"),
                Choice("A story", "forest_king", wisdom_change=2),
                Choice("A shadow", "lost"),
            ]
        )

        scenes["cabin"] = Scene(
            "cabin",
            "Inside the ruined cabin, you find an old journal. The last page says: 'The forest is not trying to trap you. It is testing whether you run from fear or walk through it.' A trapdoor creaks open under the rug.",
            [
                Choice("Go down the trapdoor", "crystal_cave", bravery_change=1),
                Choice("Read more pages", "journal_truth", wisdom_change=1),
                Choice("Leave the cabin", "hidden_tree"),
            ]
        )

        scenes["hidden_tree"] = Scene(
            "hidden_tree",
            "You hide behind a tree and hold your breath. The shadow walks past you and drops something on the ground: a wooden key shaped like a leaf.",
            [
                Choice("Take the leaf key", "hidden_door", wisdom_change=1),
                Choice("Follow the shadow", "forest_king", bravery_change=1),
                Choice("Stay hidden", "lost"),
            ]
        )

        scenes["journal_truth"] = Scene(
            "journal_truth",
            "The journal explains that the forest was created to protect a sleeping spirit. Anyone who enters must choose: escape alone, or help the forest heal.",
            [
                Choice("Help the forest", "forest_king", bravery_change=1, wisdom_change=1),
                Choice("Escape alone", "hidden_door"),
            ]
        )

        scenes["crystal_cave"] = Scene(
            "crystal_cave",
            "The cave walls sparkle with blue crystals. In the center of the cave is a cracked crystal heart. The whole forest seems to be breathing through it. You realize the forest is alive, but injured.",
            [
                Choice("Touch the crystal heart", "heal_forest", wisdom_change=1),
                Choice("Take a crystal and leave", "bad_ending_greed"),
                Choice("Search for the forest ruler", "forest_king", bravery_change=1),
            ]
        )

        scenes["hidden_door"] = Scene(
            "hidden_door",
            "The strange door hums softly in front of you. The handle feels warm, like it knows you are there. Behind it, you hear birds, wind, and something that almost sounds like sunlight.",
            [
                Choice("Step through the door", "escape_ending", bravery_change=1),
                Choice("Stay and search for answers", "forest_king", wisdom_change=1),
            ]
        )

        scenes["forest_king"] = Scene(
            "forest_king",
            "You reach a throne made of roots. Sitting on it is the Forest King, a creature with antlers, glowing eyes, and a voice like wind. He says, 'You may leave, but the forest will remain broken unless someone chooses to help.'",
            [
                Choice("Promise to help the forest", "final_choice", bravery_change=1, wisdom_change=1),
                Choice("Ask to leave safely", "escape_ending"),
                Choice("Challenge the Forest King", "bad_ending_pride", bravery_change=1),
            ]
        )

        scenes["heal_forest"] = Scene(
            "heal_forest",
            "The crystal heart glows under your hand. Memories rush into your mind: lost travelers, broken trees, and the lonely spirit guarding everything. You understand that the forest needs courage and kindness to heal.",
            [
                Choice("Give part of your courage to the forest", "good_ending", bravery_change=2),
                Choice("Give part of your wisdom to the forest", "wise_ending", wisdom_change=2),
                Choice("Pull your hand away", "escape_ending"),
            ]
        )

        scenes["final_choice"] = Scene(
            "final_choice",
            "The Forest King places a glowing seed in your hand. 'Plant this in the crystal cave, and the forest will heal. But once you do, you may never be the same.'",
            [
                Choice("Plant the glowing seed", "good_ending", bravery_change=1, wisdom_change=1),
                Choice("Keep the seed and leave", "bad_ending_greed"),
                Choice("Return the seed and ask for another way", "wise_ending", wisdom_change=2),
            ]
        )

        # ENDINGS
        scenes["escape_ending"] = Scene(
            "escape_ending",
            "You step through the door and wake up at the edge of the forest as sunrise spills across the grass. You survived, but when the wind moves through the trees, you wonder what would have happened if you had stayed.",
            is_ending=True,
            ending_title="You Survived"
        )

        scenes["good_ending"] = Scene(
            "good_ending",
            "You plant the glowing seed. Roots burst with golden light, flowers open in seconds, and the broken crystal heart becomes whole again. The Forest King bows to you. When you wake up outside the woods, a tiny glowing leaf rests in your hand.",
            is_ending=True,
            ending_title="Best Ending: Forest Guardian"
        )

        scenes["wise_ending"] = Scene(
            "wise_ending",
            "Instead of forcing an answer, you listen. The forest answers back. The trees open a safe path home, and the fox walks beside you until sunrise. You leave with the knowledge that not every quest is won by fighting.",
            is_ending=True,
            ending_title="Wise Ending: The Listener"
        )

        scenes["bad_ending_secret"] = Scene(
            "bad_ending_secret",
            "The fox shakes its head. 'A secret grows heavier when hidden, not stronger when shared.' The mushroom lights go out one by one. In the darkness, the path disappears beneath your feet.",
            is_ending=True,
            ending_title="Game Over"
        )

        scenes["bad_ending_greed"] = Scene(
            "bad_ending_greed",
            "The moment you take what does not belong to you, the forest turns cold. The trees close around you like prison bars. Some treasures are not meant to be stolen.",
            is_ending=True,
            ending_title="Game Over: Greed"
        )

        scenes["bad_ending_pride"] = Scene(
            "bad_ending_pride",
            "You challenge the Forest King, but the forest itself rises to protect him. Roots wrap around your feet, and the throne room fades into darkness.",
            is_ending=True,
            ending_title="Game Over: Pride"
        )

        scenes["bad_ending_trust_man"] = Scene(
            "bad_ending_trust_man",
            "You follow the strange man deeper into the forest. The trees get darker. The path disappears. He turns around and smiles. Why would you trust a man?",
            is_ending=True,
            ending_title="Game Over: Bad Decision"
        )

        scenes["lost"] = Scene(
            "lost",
            "You run without looking back. The trees blur around you. Soon, every path looks the same. You hear the bell ring again, but this time it sounds much closer.",
            is_ending=True,
            ending_title="Game Over: Lost in the Forest"
        )

        return scenes

# this one restarts the game by resetting the player and returning to the first scene.
    def reset_game(self):
        self.player.reset()
        self.current_scene_id = "start"
        self.screen_state = "story_screen"

    def draw_forest_background(self):
        # this one draws the animated forest background, including fog, trees and fireflies.
        # Dark night sky
        screen.fill(PURPLE_BLACK)

        current_time = pygame.time.get_ticks() / 1000

        # Moon
        pygame.draw.circle(screen, MOON_YELLOW, (730, 95), 45)
        pygame.draw.circle(screen, PURPLE_BLACK, (710, 85), 38)

        # Creepy far-away trees
        for x in range(-20, WIDTH, 80):
            pygame.draw.polygon(screen, (12, 35, 25), [(x, 560), (x + 45, 210), (x + 90, 560)])
            pygame.draw.rect(screen, (45, 30, 20), (x + 38, 390, 18, 170))

        # Moving fog
        for fog in self.fog_clouds:
            fog["x"] += fog["speed"]
            if fog["x"] > WIDTH + 180:
                fog["x"] = -180
                fog["y"] = random.randint(120, 520)

            fog_surface = pygame.Surface((fog["size"] * 2, 70), pygame.SRCALPHA)
            pygame.draw.ellipse(fog_surface, (MIST[0], MIST[1], MIST[2], 45), (0, 10, fog["size"] * 2, 45))
            screen.blit(fog_surface, (fog["x"], fog["y"]))

        # Front trees with spooky branches
        for x in range(20, WIDTH, 130):
            pygame.draw.rect(screen, BROWN, (x + 35, 350, 30, 210))
            pygame.draw.line(screen, BROWN, (x + 50, 390), (x - 10, 320), 8)
            pygame.draw.line(screen, BROWN, (x + 55, 420), (x + 115, 340), 7)
            pygame.draw.circle(screen, (18, 65, 38), (x + 50, 305), 75)
            pygame.draw.circle(screen, (10, 45, 30), (x + 20, 330), 50)
            pygame.draw.circle(screen, (10, 45, 30), (x + 85, 335), 55)

        # Glowing magical mushrooms
        glow_size = 10 + int(4 * math.sin(current_time * 3))
        for x in range(90, WIDTH, 180):
            pygame.draw.rect(screen, WHITE, (x + 8, 515, 8, 25))
            pygame.draw.circle(screen, GLOW_BLUE, (x + 12, 512), glow_size)
            pygame.draw.circle(screen, WHITE, (x + 12, 512), 5)

        # Moving fireflies
        for fly in self.fireflies:
            fly["x"] += fly["speed"]
            fly["y"] += math.sin(current_time * 2 + fly["phase"]) * 0.3

            if fly["x"] > WIDTH:
                fly["x"] = 0
                fly["y"] = random.randint(80, 520)

            brightness = 120 + int(100 * abs(math.sin(current_time * 3 + fly["phase"])))
            pygame.draw.circle(screen, (brightness, brightness, 120), (int(fly["x"]), int(fly["y"])), 3)

        # Ground
        pygame.draw.rect(screen, (12, 50, 30), (0, 550, WIDTH, 100))

        # Creepy eyes in the forest
        if self.screen_state != "start_screen":
            pygame.draw.circle(screen, RED, (95, 260), 5)
            pygame.draw.circle(screen, RED, (115, 260), 5)
            pygame.draw.circle(screen, RED, (790, 310), 5)
            pygame.draw.circle(screen, RED, (810, 310), 5)


    # this one draws the title screen and the button that starts the game.
    def draw_start_screen(self):
        self.draw_forest_background()

        title = TITLE_FONT.render("Forest Quest", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 160))
        screen.blit(title, title_rect)

        subtitle = TEXT_FONT.render("A choice-based adventure game", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 235))
        screen.blit(subtitle, subtitle_rect)

        instructions = SMALL_FONT.render("Click Start Quest to begin your journey.", True, WHITE)
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, 300))
        screen.blit(instructions, instructions_rect)

        self.start_button.draw()

    # this one draws a small custom graphic for the currect scene.
    def draw_scene_graphic(self, scene_id):
        
        graphic_box = pygame.Rect(250, 330, 400, 140)
        pygame.draw.rect(screen, (5, 15, 18), graphic_box, border_radius=16)
        pygame.draw.rect(screen, (95, 170, 175), graphic_box, 2, border_radius=16)

        # This keeps all mini-graphic drawings inside the box.
        old_clip = screen.get_clip()
        screen.set_clip(graphic_box)

        cx = graphic_box.centerx
        cy = graphic_box.centery
        t = pygame.time.get_ticks() / 1000
        glow = 7 + int(3 * math.sin(t * 3))

        # Mini forest background inside every graphic
        for x in range(265, 650, 42):
            height = 65 + (x % 3) * 10
            pygame.draw.polygon(
                screen,
                (12, 45, 38),
                [(x, 450), (x + 22, 450 - height), (x + 44, 450)]
            )
            pygame.draw.rect(screen, (8, 30, 25), (x + 19, 430, 6, 25))

        # Small moon / magical light
        pygame.draw.circle(screen, (170, 220, 220), (610, 355), 17)
        pygame.draw.circle(screen, (5, 15, 18), (602, 350), 14)

        # Soft fog lines
        for y in [390, 420, 445]:
            offset = int((t * 12) % 40)
            pygame.draw.line(screen, (45, 95, 100), (260 + offset, y), (380 + offset, y), 1)
            pygame.draw.line(screen, (45, 95, 100), (450 - offset, y + 5), (620 - offset, y + 5), 1)

        # Scene-specific symbol in front of the forest
        if scene_id in ["start", "footsteps", "stranger_man", "hidden_tree", "lost"]:
            # Stranger / shadow in trees
            pygame.draw.circle(screen, (30, 70, 65), (cx, cy - 25), 16)
            pygame.draw.ellipse(screen, (20, 55, 50), (cx - 22, cy - 10, 44, 65))
            pygame.draw.circle(screen, (170, 220, 220), (cx - 6, cy - 23), 2)
            pygame.draw.circle(screen, (170, 220, 220), (cx + 6, cy - 23), 2)
            pygame.draw.line(screen, (30, 70, 65), (cx - 16, cy + 5), (cx - 50, cy + 25), 3)
            pygame.draw.line(screen, (30, 70, 65), (cx + 16, cy + 5), (cx + 50, cy + 25), 3)

        elif scene_id in ["old_bridge", "river_creature", "river_answer"]:
            # Bridge over glowing water
            pygame.draw.line(screen, (120, 200, 200), (cx - 110, cy + 15), (cx + 110, cy + 15), 3)
            pygame.draw.line(screen, (80, 145, 145), (cx - 100, cy - 5), (cx + 100, cy - 5), 2)
            for plank_x in range(cx - 95, cx + 100, 24):
                pygame.draw.line(screen, (95, 170, 175), (plank_x, cy - 5), (plank_x + 8, cy + 15), 1)
            pygame.draw.arc(screen, (80, 145, 145), (cx - 70, cy + 10, 140, 45), 0, 3.14, 2)
            pygame.draw.circle(screen, (150, 220, 220), (cx, cy + 35), glow)

        elif scene_id in ["mushroom_circle", "fox_path", "fox_riddle"]:
            # Fox silhouette with glowing mushroom circle
            pygame.draw.ellipse(screen, (25, 75, 60), (cx - 35, cy - 5, 70, 42))
            pygame.draw.circle(screen, (25, 75, 60), (cx + 30, cy - 15), 18)
            pygame.draw.polygon(screen, (25, 75, 60), [(cx + 20, cy - 25), (cx + 10, cy - 55), (cx + 35, cy - 35)])
            pygame.draw.polygon(screen, (25, 75, 60), [(cx + 40, cy - 25), (cx + 55, cy - 55), (cx + 50, cy - 30)])
            pygame.draw.circle(screen, (170, 220, 220), (cx + 35, cy - 17), 3)
            for angle in range(0, 360, 45):
                mx = cx + int(105 * math.cos(math.radians(angle)))
                my = cy + int(38 * math.sin(math.radians(angle))) + 25
                pygame.draw.rect(screen, (180, 230, 230), (mx - 2, my, 4, 10))
                pygame.draw.circle(screen, (120, 200, 200), (mx, my), 5)

        elif scene_id in ["cabin", "journal_truth"]:
            # Ruined cabin
            pygame.draw.rect(screen, (22, 65, 52), (cx - 65, cy - 5, 130, 60))
            pygame.draw.polygon(screen, (10, 35, 30), [(cx - 80, cy - 5), (cx, cy - 60), (cx + 80, cy - 5)])
            pygame.draw.rect(screen, (5, 15, 18), (cx - 15, cy + 20, 30, 35))
            pygame.draw.line(screen, (120, 200, 200), (cx - 55, cy + 10), (cx + 50, cy + 45), 1)
            pygame.draw.line(screen, (120, 200, 200), (cx + 45, cy + 5), (cx - 50, cy + 45), 1)

        elif scene_id == "lantern_tree":
            # Tree branch and lantern
            pygame.draw.rect(screen, (12, 45, 38), (cx - 85, cy - 55, 22, 110))
            pygame.draw.line(screen, (12, 45, 38), (cx - 75, cy - 35), (cx + 25, cy - 55), 7)
            pygame.draw.line(screen, (120, 200, 200), (cx + 20, cy - 55), (cx + 20, cy - 10), 1)
            pygame.draw.rect(screen, (50, 110, 105), (cx + 5, cy - 12, 30, 45), border_radius=7)
            pygame.draw.circle(screen, (170, 220, 220), (cx + 20, cy + 10), glow)

        elif scene_id in ["crystal_cave", "heal_forest", "final_choice"]:
            # Crystal heart / cave
            pygame.draw.polygon(screen, (12, 35, 38), [(cx - 130, cy + 55), (cx - 60, cy - 45), (cx, cy + 55)])
            pygame.draw.polygon(screen, (12, 35, 38), [(cx + 130, cy + 55), (cx + 60, cy - 45), (cx, cy + 55)])
            pygame.draw.polygon(screen, (120, 200, 200), [(cx, cy - 45), (cx - 35, cy), (cx, cy + 48), (cx + 35, cy)])
            pygame.draw.polygon(screen, (190, 240, 240), [(cx, cy - 25), (cx - 17, cy), (cx, cy + 25), (cx + 17, cy)])
            pygame.draw.circle(screen, (170, 220, 220), (cx, cy), glow)

        elif scene_id in ["hidden_door", "escape_ending"]:
            # Magical door between trees
            pygame.draw.rect(screen, (15, 55, 45), (cx - 35, cy - 55, 70, 105), border_radius=8)
            pygame.draw.rect(screen, (120, 200, 200), (cx - 28, cy - 45, 56, 90), 2, border_radius=6)
            pygame.draw.circle(screen, (170, 220, 220), (cx + 18, cy), 3)
            pygame.draw.arc(screen, (95, 170, 175), (cx - 60, cy - 70, 120, 130), 0, 6.28, 2)

        elif scene_id in ["forest_king", "good_ending", "wise_ending"]:
            # Forest King / antlers
            pygame.draw.circle(screen, (18, 70, 55), (cx, cy + 10), 30)
            pygame.draw.circle(screen, (170, 220, 220), (cx - 10, cy + 5), 3)
            pygame.draw.circle(screen, (170, 220, 220), (cx + 10, cy + 5), 3)
            pygame.draw.line(screen, (120, 200, 200), (cx - 20, cy - 10), (cx - 65, cy - 55), 3)
            pygame.draw.line(screen, (120, 200, 200), (cx + 20, cy - 10), (cx + 65, cy - 55), 3)
            pygame.draw.line(screen, (120, 200, 200), (cx - 50, cy - 42), (cx - 75, cy - 35), 2)
            pygame.draw.line(screen, (120, 200, 200), (cx + 50, cy - 42), (cx + 75, cy - 35), 2)
            pygame.draw.circle(screen, (170, 220, 220), (cx, cy + 40), glow)

        else:
            # Elegant bad ending mark
            pygame.draw.circle(screen, (30, 75, 75), (cx, cy), 36, 2)
            pygame.draw.line(screen, (150, 220, 220), (cx - 22, cy - 22), (cx + 22, cy + 22), 2)
            pygame.draw.line(screen, (150, 220, 220), (cx + 22, cy - 22), (cx - 22, cy + 22), 2)

        # Stop clipping after the scene graphic is done.
        screen.set_clip(old_clip)


    # This one draws the current story scene, including text, stats, graphics and choice buttons.
    def draw_story_screen(self):
        self.draw_forest_background()
        current_scene = self.scenes[self.current_scene_id]

        # Story box
        story_box = pygame.Rect(70, 60, 760, 245)
        pygame.draw.rect(screen, BLACK, story_box, border_radius=15)
        pygame.draw.rect(screen, WHITE, story_box, 3, border_radius=15)

        draw_wrapped_text(current_scene.text, TEXT_FONT, WHITE, 100, 90, 700, 31)

        # Player stats
        stats_text = SMALL_FONT.render(
            f"Bravery: {self.player.bravery}   Wisdom: {self.player.wisdom}",
            True,
            GOLD
        )
        screen.blit(stats_text, (70, 30))

        # Draw a custom picture under each story/question.
        self.draw_scene_graphic(current_scene.scene_id)

        # Choice buttons
        self.choice_buttons = []
        start_y = 485

        for index, choice in enumerate(current_scene.choices):
            button = Button(120, start_y + index * 55, 660, 45, choice.text)
            self.choice_buttons.append((button, choice))
            button.draw()

    # this one draws the ending screen, final message, final stats and restrt button.
    def draw_ending_screen(self):
        self.draw_forest_background()
        current_scene = self.scenes[self.current_scene_id]

        ending_title = HEADING_FONT.render(current_scene.ending_title, True, GOLD)
        ending_rect = ending_title.get_rect(center=(WIDTH // 2, 85))
        screen.blit(ending_title, ending_rect)

        ending_box = pygame.Rect(90, 130, 720, 175)
        pygame.draw.rect(screen, BLACK, ending_box, border_radius=15)
        pygame.draw.rect(screen, WHITE, ending_box, 3, border_radius=15)

        draw_wrapped_text(current_scene.text, TEXT_FONT, WHITE, 120, 160, 660, 31)

        self.draw_scene_graphic(current_scene.scene_id)

        final_stats = SMALL_FONT.render(
            f"Final Stats - Bravery: {self.player.bravery}   Wisdom: {self.player.wisdom}",
            True,
            GOLD
        )
        final_stats_rect = final_stats.get_rect(center=(WIDTH // 2, 480))
        screen.blit(final_stats, final_stats_rect)

        self.restart_button.draw()

    # handles all player input.
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.screen_state == "start_screen":
                if self.start_button.is_clicked(event):
                    self.reset_game()

            elif self.screen_state == "story_screen":
                for button, choice in self.choice_buttons:
                    if button.is_clicked(event):
                        self.player.bravery += choice.bravery_change
                        self.player.wisdom += choice.wisdom_change
                        self.current_scene_id = choice.next_scene_id

                        if self.scenes[self.current_scene_id].is_ending:
                            self.screen_state = "ending_screen"

            elif self.screen_state == "ending_screen":
                if self.restart_button.is_clicked(event):
                    self.reset_game()

    # runs the main game loop.
    # the loop repeatedly handles events, draws the correct screen, updates the display and limits the game speed to 60 frames per second.
    def run(self):
        while True:
            self.handle_events()

            if self.screen_state == "start_screen":
                self.draw_start_screen()
            elif self.screen_state == "story_screen":
                self.draw_story_screen()
            elif self.screen_state == "ending_screen":
                self.draw_ending_screen()

            pygame.display.flip()
            clock.tick(60)


# -----------------------------
# START THE GAME
# -----------------------------
if __name__ == "__main__":
    game = Game()
    game.run()
