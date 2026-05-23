from pygame import *
from random import randint
import math
import json
import os

init()

SAVE_FILE = "save_data.json"

default_save = {
    "skill_points": 0,
    "quick_in_n_out": False,
    "extended_mag": False,
    "lightning_reload": False,
    "infinity_between": False
}

def load_save():

    if os.path.exists(SAVE_FILE):

        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        if "quick_in_n_out" not in data:
            data["quick_in_n_out"] = False

        if "extended_mag" not in data:
            data["extended_mag"] = False

        if "lightning_reload" not in data:
            data["lightning_reload"] = False
        
        if "infinity_between" not in data:
            data["infinity_between"] = False
        
        return data

    with open(SAVE_FILE, "w") as f:
        json.dump(default_save, f)

    return default_save.copy()

def save_game(data):

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

save_data = load_save()

def skill_tree_screen():

    scroll_x = 0
    dragging = False
    last_mouse_x = 0

    screen = display.set_mode((700, 500))
    display.set_caption("Skill Tree")

    title_font = font.Font(None, 60)
    text_font = font.Font(None, 36)
    small_font = font.Font(None, 28)

    skill_width = 900

    while True:

        screen.fill((15, 15, 30))

        title = title_font.render("SKILL TREE", True, (255, 220, 0))

        points_text = text_font.render(
            f"Skill Points: {save_data['skill_points']}",
            True,
            (255, 255, 255)
        )

        skill1 = small_font.render(
            "1 - Quick In N Out (Cost: 1) [Learn the skill to change your magazine faster, making reload speed from 3 seconds to 2.5 seconds]",
            True,
            (255, 180, 255)
        )

        skill2 = small_font.render(
            "2 - Extended Mag (Cost: 2) [Carry more bullets, totalling 8 instead of 5]",
            True,
            (120, 255, 120)
        )

        skill3 = small_font.render(
            "3 - Lightning Reload (Cost: 5) [Reload in the speed of lightning, making reload speed only 1 second]",
            True,
            (255, 255, 120)
        )

        skill4 = small_font.render(
            "4 - Infinity Between (Cost: 20) [Take advantage of the amount of numbers between any two points, believed by many to be limitless]",
            True,
            (180, 180, 255)
        )
        
        info = small_font.render(
            "Drag left/right to scroll | ESC to return",
            True,
            (120, 200, 255)
        )

        for e in event.get():

            if e.type == QUIT:
                quit()

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    return

                if e.key == K_1:
                    if save_data["skill_points"] >= 1 and not save_data["quick_in_n_out"]:
                        save_data["skill_points"] -= 1
                        save_data["quick_in_n_out"] = True
                        save_game(save_data)

                if e.key == K_2:
                    if (
                        save_data["skill_points"] >= 2
                        and save_data["quick_in_n_out"]
                        and not save_data["extended_mag"]
                    ):
                        save_data["skill_points"] -= 2
                        save_data["extended_mag"] = True
                        save_game(save_data)

                if e.key == K_3:
                    if (
                        save_data["skill_points"] >= 5
                        and save_data["extended_mag"]
                        and not save_data["lightning_reload"]
                    ):
                        save_data["skill_points"] -= 5
                        save_data["lightning_reload"] = True
                        save_game(save_data)

                if e.key == K_4:
                    if (
                        save_data["skill_points"] >= 20
                        and not save_data["infinity_between"]
                    ):
                        save_data["skill_points"] -= 20
                        save_data["infinity_between"] = True
                        save_game(save_data)
            
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    dragging = True
                    last_mouse_x = e.pos[0]

            if e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    dragging = False

            if e.type == MOUSEMOTION and dragging:
                dx = e.pos[0] - last_mouse_x
                scroll_x += dx
                last_mouse_x = e.pos[0]

        scroll_x = max(-800, min(0, scroll_x))

        screen.blit(title, (190 + scroll_x, 40))
        screen.blit(points_text, (220 + scroll_x, 160))
        screen.blit(skill1, (80 + scroll_x, 300))
        screen.blit(skill2, (80 + scroll_x, 340))
        screen.blit(skill3, (80 + scroll_x, 380))
        screen.blit(skill4, (80 + scroll_x, 420))
        screen.blit(info, (80 + scroll_x, 470))

        display.update()

def tutorial_screen():

    screen = display.set_mode((900, 650))
    display.set_caption("Tutorial")

    title_font = font.Font(None, 60)
    text_font = font.Font(None, 34)
    small_font = font.Font(None, 28)

    screen = display.set_mode((900, 650))
    display.set_caption("Tutorial")

    title_font = font.Font(None, 60)
    text_font = font.Font(None, 34)
    small_font = font.Font(None, 28)

    tutorial = [
    "WELCOME TO SHOOTER!",
    "",
    "GOAL:",
    "- Destroy UFO enemies before they escape.",
    "- Reach win score to win.",
    "- Too many missed = GAME OVER.",
    "",
    "CONTROLS:",
    "- LEFT / RIGHT = Move",
    "- SPACE = Shoot",
    "- Q = CHRONO BREAK",
    "- E = FREEZING VOID",
    "- 4 = SKILL TREE",
    "",
    "SKILL SYSTEM:",
    "- Win games to earn Skill Points",
    "- Easy = 1 point",
    "- Medium = 2 points",
    "- Hardcore = 4 points",
    "- Progress is saved permanently",
    "",
    "SKILL TREE:",
    "- Press 4 in menu or game",
    "- Spend skill points on upgrades ",
    "",
    "AMMO SYSTEM:",
    "- 5 bullets max",
    "- 3 second reload when empty",
    "",
    "TIPS:",
    "- Don’t spam shots",
    "- Save abilities for large waves",
    "- Focus UFOs first",
    "",
    "Press ENTER to start EASY mode."
]

    scroll_y = 0
    scroll_speed = 35

    content_height = len(tutorial) * 35 + 200

    while True:

        screen.fill((15, 15, 25))

        title = title_font.render("GAME TUTORIAL", True, (255, 220, 0))
        screen.blit(title, (240, 20))

        y = 100 - scroll_y

        for line in tutorial:

            if line == "":
                y += 15
                continue

            if ":" in line or "WELCOME" in line:
                txt = text_font.render(line, True, (0, 255, 255))
            else:
                txt = small_font.render(line, True, (255, 255, 255))

            if -40 < y < 700:
                screen.blit(txt, (40, y))

            y += 35

        for e in event.get():

            if e.type == QUIT:
                quit()
                return

            if e.type == MOUSEWHEEL:
                scroll_y -= e.y * scroll_speed

            if e.type == KEYDOWN:

                if e.key == K_DOWN:
                    scroll_y += scroll_speed

                if e.key == K_UP:
                    scroll_y -= scroll_speed

                if e.key == K_RETURN:
                    return "easy"

        max_scroll = max(0, content_height - 650)

        if scroll_y < 0:
            scroll_y = 0

        if scroll_y > max_scroll:
            scroll_y = max_scroll

        display.update()

def select_difficulty():

    screen = display.set_mode((500, 430))
    display.set_caption("Select Difficulty")

    f = font.Font(None, 40)
    small = font.Font(None, 26)

    while True:

        screen.fill((20, 20, 20))

        title = f.render("SELECT DIFFICULTY", True, (255, 220, 0))

        tutorial = f.render("0 - TUTORIAL", True, (100, 220, 255))
        easy = f.render("1 - EASY", True, (0, 255, 0))
        medium = f.render("2 - MEDIUM", True, (255, 255, 0))
        hard = f.render("3 - HARDCORE", True, (255, 0, 0))
        skill = f.render("4 - SKILL TREE", True, (200, 120, 255))

        hint = small.render(
            "Easy=1 Medium=2 Hardcore=4 Skill Points",
            True,
            (180, 180, 180)
        )

        screen.blit(title, (85, 40))
        screen.blit(tutorial, (120, 100))
        screen.blit(easy, (120, 150))
        screen.blit(medium, (120, 200))
        screen.blit(hard, (120, 250))
        screen.blit(skill, (120, 300))
        screen.blit(hint, (55, 380))

        for e in event.get():

            if e.type == QUIT:
                quit()
                return

            if e.type == KEYDOWN:

                if e.key == K_0:
                    return "tutorial"

                if e.key == K_1:
                    return "easy"

                if e.key == K_2:
                    return "medium"

                if e.key == K_3:
                    return "hardcore"

                if e.key == K_4:
                    skill_tree_screen()

        display.update()

difficulty = select_difficulty()

if difficulty == "tutorial":
    difficulty = tutorial_screen()

window = display.set_mode((700, 500))
display.set_caption("Shooter")

FPS = 60
clock = time.Clock()
game = True

background = transform.scale(image.load("galaxy.jpg"), (700, 500))

class GameSprite(sprite.Sprite):

    def __init__(self, speed, img, x, y, width, height):

        super().__init__()

        self.image = transform.scale(image.load(img), (width, height))
        self.speed = speed

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def action(self):

        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < 700 - self.rect.width:
            self.rect.x += self.speed

class Enemy(GameSprite):

    def action(self):

        self.rect.y += self.speed

        if self.rect.y > 500:

            self.rect.y = randint(-150, -50)
            self.rect.x = randint(0, 600)

            return True

        return False

class Bullet(GameSprite):

    def shoot(self):

        self.rect.y -= self.speed

        return self.rect.y < 0

if difficulty == "easy":
    win_score = 10
    max_missed = 3

elif difficulty == "medium":
    win_score = 15
    max_missed = 2

else:
    win_score = 25
    max_missed = 1

player = Player(6, "rocket.png", 350, 390, 100, 100)

monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

for i in range(5):

    speed = randint(2, 3) if difficulty == "hardcore" else randint(1, 3)

    monsters.add(
        Enemy(
            speed,
            "ufo.png",
            randint(0, 600),
            randint(-150, -50),
            100,
            80
        )
    )

for i in range(3):

    asteroids.add(
        Enemy(
            2,
            "asteroid.png",
            randint(0, 620),
            randint(-300, -50),
            80,
            80
        )
    )

mixer.init()

mixer.music.load("space.ogg")
mixer.music.play(-1)

fire_sound = mixer.Sound("fire.ogg")

font1 = font.Font(None, 36)
big_font = font.Font(None, 80)
q_font = font.Font(None, 28)
chrono_font = font.Font(None, 33)

hit = 0
missed = 0

shot_cooldown = 0

if save_data.get("extended_mag"):
    max_ammo = 8
else:
    max_ammo = 5
ammo = max_ammo

reloading = False
if save_data.get("lightning_reload"):
    reload_time = 60
elif save_data.get("extended_mag"):
    reload_time = 150
elif save_data.get("quick_in_n_out"):
    reload_time = 150
else:
    reload_time = 180
reload_timer = 0

chrono_active = False
chrono_timer = 0
chrono_duration = 120
chrono_cooldown = 0
chrono_cooldown_max = 900
chrono_angle = 0

freeze_active = False
freeze_timer = 0
freeze_duration = 300
freeze_cooldown = 0
freeze_cooldown_max = 1800

ability_lock = False

reward_given = False

while game:

    window.blit(background, (0, 0))

    for e in event.get():

        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:

            if (
                e.key == K_SPACE
                and shot_cooldown == 0
                and not chrono_active
                and not reloading
                and ammo > 0
            ):

                bullets.add(
                    Bullet(
                        10,
                        "bullet.png",
                        player.rect.x + player.rect.width // 2 - 15,
                        player.rect.y,
                        30,
                        20
                    )
                )

                fire_sound.play()

                if not save_data.get("infinity_between"):
                    ammo -= 1
                shot_cooldown = 30

            if e.key == K_q and not ability_lock and chrono_cooldown == 0 and not chrono_active:
                chrono_active = True
                chrono_timer = chrono_duration
                chrono_cooldown = chrono_cooldown_max
                ability_lock = True

            if e.key == K_e and not ability_lock and freeze_cooldown == 0 and not freeze_active:
                freeze_active = True
                freeze_timer = freeze_duration
                freeze_cooldown = freeze_cooldown_max
                ability_lock = True

    if not chrono_active and not freeze_active:
        ability_lock = False

    if not chrono_active:
        player.action()

    player.reset()

    if not chrono_active:

        for b in list(bullets):

            if not freeze_active:

                if b.shoot():
                    bullets.remove(b)
                    continue

                hits = sprite.spritecollide(b, monsters, False)
                asteroid_hits = sprite.spritecollide(b, asteroids, False)

                if hits or asteroid_hits:

                    hit += len(hits) + len(asteroid_hits)
                    bullets.remove(b)

                    for m in hits:
                        m.rect.y = randint(-150, -50)
                        m.rect.x = randint(0, 600)

                    for a in asteroid_hits:
                        a.rect.y = randint(-300, -50)
                        a.rect.x = randint(0, 620)

                    continue

            b.reset()

    else:

        for b in bullets:
            b.reset()

    for m in monsters:

        if not chrono_active and not freeze_active:
            if m.action():
                missed += 1

        m.reset()

    for a in asteroids:

        if not chrono_active and not freeze_active:
            if a.action():
                missed += 1

        a.reset()

    if chrono_active:

        chrono_timer -= 1
        chrono_angle += 8

        if chrono_timer <= 0:

            chrono_active = False

            for m in monsters:
                m.rect.y -= 100

            for a in asteroids:
                a.rect.y -= 100

    if freeze_active:

        freeze_timer -= 1

        if freeze_timer <= 0:
            freeze_active = False

        for i in range(140):

            sx = (randint(0, 700) - i * 6) % 700
            sy = randint(0, 500)

            draw.rect(window, (255, 255, 255), (sx, sy, 4, 4))

    if chrono_cooldown > 0:
        chrono_cooldown -= 1

    if freeze_cooldown > 0:
        freeze_cooldown -= 1

    if shot_cooldown > 0:
        shot_cooldown -= 1

    if not save_data.get("infinity_between"):

        if ammo <= 0 and not reloading:
            reloading = True
            reload_timer = reload_time

        if reloading:
            reload_timer -= 1

            if reload_timer <= 0:
                ammo = max_ammo
                reloading = False

    else:
        reloading = False
        reload_timer = 0
        ammo = max_ammo

    window.blit(font1.render(f"Hit: {hit}", True, (255, 255, 255)), (10, 10))
    window.blit(font1.render(f"Missed: {missed}", True, (255, 255, 255)), (10, 50))
    if save_data.get("infinity_between"):
        window.blit(font1.render("Ammo: Limitless", True, (255, 255, 255)), (10, 90))
    else:
        window.blit(font1.render(f"Ammo: {ammo}/{max_ammo}", True, (255, 255, 255)), (10, 90))
        window.blit(font1.render(f"Skill Points: {save_data['skill_points']}", True, (255, 255, 255)), (10, 130))

    if reloading:
        window.blit(font1.render("RELOADING...", True, (255, 100, 100)), (10, 170))

    if chrono_active:

        cx, cy = 350, 250
        r = 150
        y = (255, 220, 0)

        draw.circle(window, y, (cx, cy), r, 4)

        ex = cx + r * math.cos(math.radians(chrono_angle))
        ey = cy - r * math.sin(math.radians(chrono_angle))

        draw.line(window, y, (cx, cy), (ex, ey), 5)

    cool_x, cool_y = 60, 440
    cool_radius = 50

    yellow = (255, 220, 0)

    draw.circle(window, (60, 60, 60), (cool_x, cool_y), cool_radius)

    if chrono_cooldown > 0:

        progress = chrono_cooldown / chrono_cooldown_max
        end_angle = int(360 * progress)

        for angle in range(end_angle):

            x = cool_x + cool_radius * math.cos(math.radians(angle))
            y = cool_y - cool_radius * math.sin(math.radians(angle))

            draw.line(window, yellow, (cool_x, cool_y), (x, y), 2)

    else:
        draw.circle(window, yellow, (cool_x, cool_y), cool_radius, 2)

    q_text = q_font.render("Q", True, yellow)

    window.blit(q_text, (cool_x - cool_radius + 7, cool_y - q_text.get_height() // 2 - 55))

    chrono_text = chrono_font.render("CHRONO BREAK", True, (255, 255, 255))
    window.blit(chrono_text, (cool_x - chrono_text.get_width() // 2 + 35, cool_y + cool_radius - 15))

    fx2, fy2 = 550, 440
    fr = 50

    blue = (80, 170, 255)

    draw.circle(window, (60, 60, 60), (fx2, fy2), fr)

    if freeze_cooldown > 0:

        progress = freeze_cooldown / freeze_cooldown_max
        end_angle = int(360 * progress)

        for angle in range(end_angle):

            x = fx2 + fr * math.cos(math.radians(angle))
            y = fy2 - fr * math.sin(math.radians(angle))

            draw.line(window, blue, (fx2, fy2), (x, y), 2)

    else:
        draw.circle(window, blue, (fx2, fy2), fr, 2)

    e_text = q_font.render("E", True, blue)

    window.blit(e_text, (fx2 - fr + 7, fy2 - e_text.get_height() // 2 - 55))

    freeze_text = chrono_font.render("FREEZING VOID", True, (255, 255, 255))
    window.blit(freeze_text, (fx2 - freeze_text.get_width() // 2 + 20, fy2 + fr - 15))

    if missed >= max_missed:

        window.blit(big_font.render("YOU LOSE!", True, (255, 0, 0)), (200, 200))
        display.update()
        time.delay(3000)
        game = False

    if hit >= win_score:

        if not reward_given:

            if difficulty == "easy":
                save_data["skill_points"] += 1
            elif difficulty == "medium":
                save_data["skill_points"] += 2
            elif difficulty == "hardcore":
                save_data["skill_points"] += 4

            save_game(save_data)
            reward_given = True

        window.blit(big_font.render("YOU WIN!", True, (0, 255, 0)), (200, 200))
        display.update()
        time.delay(3000)
        game = False

    clock.tick(FPS)
    display.update()