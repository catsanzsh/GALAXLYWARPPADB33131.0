# B3313 Engine v1.0 – Comet Observatory Demo (Engine Room Upgrade)
# By Cat-san & CatGPT
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()
window.title = "B3313 Engine – Comet Observatory Demo"
window.borderless = False
window.fullscreen = False

# ---- Colors (adjust for max N64/SMG vibes) ----
OBS_COLOR = color.rgba(210, 230, 255, 255)
DOME_COLOR = color.rgba(120, 180, 240, 255)
FLOOR_COLOR = color.rgba(160, 180, 210, 255)
STAR_COLOR = color.yellow
ENGINE_COLOR = color.rgba(90, 90, 160, 240)
GLASS_COLOR = color.rgba(160, 220, 255, 120)

# ---- Game State ----
current_room = "observatory"

# ---- Observatory + Domes ----
main_floor = Entity(model='plane', color=FLOOR_COLOR, scale=(32,1,32), y=0)
observatory = Entity(model='sphere', color=OBS_COLOR, scale=7, y=3)
# Domes: x+ = red, x- = green, z+ = cyan
dome_red = Entity(model='sphere', color=color.red, scale=2, position=(11,2,0))
dome_green = Entity(model='sphere', color=color.green, scale=2, position=(-11,2,0))
dome_cyan = Entity(model='sphere', color=color.cyan, scale=2, position=(0,2,11))
# Warps (cubes inside domes)
warp_red = Entity(model='cube', color=color.red.tint(-0.2), scale=(1,2,1), position=(11,1,0), collider='box', visible=True)
warp_green = Entity(model='cube', color=color.green.tint(-0.2), scale=(1,2,1), position=(-11,1,0), collider='box', visible=True)
warp_cyan = Entity(model='cube', color=color.cyan.tint(-0.2), scale=(1,2,1), position=(0,1,11), collider='box', visible=True)

# ---- Central NPC Star ----
star_npc = Entity(model='sphere', color=STAR_COLOR, scale=0.9, position=(0,4,0), collider='sphere')

# ---- Skybox ----
sky = Sky()

# ---- Player ----
player = FirstPersonController()
player.gravity = 0.2
player.speed = 7
player.cursor.visible = False
player.position = (0,2,0)
camera.fov = 92

# ---- ENGINE ROOM (Inspired by your image) ----
# Large round engine base
en_base = Entity(model='cylinder', color=ENGINE_COLOR, scale=(7,0.8,7), y=1.2, z=-8)
# Engine's glowing glass ring
en_glass = Entity(model='torus', color=GLASS_COLOR, scale=(4,4,0.7), position=(0,2.3,-8), rotation=(90,0,0))
# Tall central engine core
en_core = Entity(model='cylinder', color=ENGINE_COLOR.tint(0.2), scale=(2,4.5,2), position=(0,4,-8))
# Multiple connecting 'spokes'
for angle in range(0, 360, 45):
    Entity(model='cube', color=ENGINE_COLOR.tint(-0.1), scale=(0.4,0.4,7), position=(0,2,-8), rotation=(0,angle,0))
# Energy nodes (spheres on glass ring)
for i in range(8):
    theta = i * (2 * math.pi / 8)
    x = 4 * math.cos(theta)
    z = -8 + 4 * math.sin(theta)
    Entity(model='sphere', color=color.azure, scale=0.4, position=(x,2.5,z))

# ---- Room Logic ----
def load_room(room):
    global current_room
    current_room = room

    if room == "observatory":
        player.position = (0,2,0)
        camera.position = (0, 5, -18)
        sky.color = color.rgb(40,45,85)
        print("You feel a cosmic breeze. Welcome to the Observatory.")
    elif room == "red_dome":
        player.position = (11,3,0)
        camera.position = (11,5,0)
        sky.color = color.rgb(110,40,40)
        print("Red Dome: Gravity feels heavy. The walls pulse faintly.")
    elif room == "green_dome":
        player.position = (-11,3,0)
        camera.position = (-11,5,0)
        sky.color = color.rgb(38,120,40)
        print("Green Dome: Music echoes in reverse. You sense being watched.")
    elif room == "cyan_dome":
        player.position = (0,3,11)
        camera.position = (0,5,11)
        sky.color = color.rgb(60,210,240)
        print("Cyan Dome: Time feels weird. Space loops around you.")
    elif room == "secret_zone":
        player.position = (0,10,0)
        camera.position = (0,18,0)
        sky.color = color.pink
        print("??? Secret Zone: Everything glitches and loops.")
    # Random secret: ~5% chance to warp to Secret Zone from any dome
    if room != "secret_zone" and random.random() < 0.05:
        print("A strange force pulls you away...")
        invoke(load_room, "secret_zone", delay=1.2)

# ---- Input / Warp Logic ----
def input(key):
    # Warps: stand near warp and click LMB
    if key == 'left mouse down':
        if distance(player.position, warp_red.position) < 2:
            load_room("red_dome")
        elif distance(player.position, warp_green.position) < 2:
            load_room("green_dome")
        elif distance(player.position, warp_cyan.position) < 2:
            load_room("cyan_dome")
        elif distance(player.position, star_npc.position) < 2:
            dialogues = [
                "⭐ Star: Welcome, visitor. The galaxy remembers you.",
                "⭐ Star: Time flows strangely here. Beware the domes.",
                "⭐ Star: Have you found the secret yet?",
                "⭐ Star: Sometimes the rooms don't lead where you expect...",
            ]
            print(random.choice(dialogues))
        elif abs(player.position[1]) > 15:
            # Fall/glitch: Reset to observatory
            print("Reality snapped back to the Observatory.")
            load_room("observatory")
    # Quick return to observatory with 'R'
    if key == 'r':
        load_room("observatory")

# ---- Lighting/FX (Simple) ----
DirectionalLight(y=3, z=-5, shadows=True)
AmbientLight(color=color.rgba(170,170,255,90))

# ---- Main Setup ----
load_room("observatory")
print("Controls: WASD/arrows to move, Mouse to look, LMB near warp/star, 'R' to return to Observatory.")

app.run()
