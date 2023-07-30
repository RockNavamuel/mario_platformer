
import pygame as pg 
import random
import sys
import time

pg.font.init()
FONT = pg.font.SysFont("comicsans", 30)

WIDTH, HEIGHT = 800,400
FLOOR = 307
FLOOR_RECT = pg.Rect(0,345, WIDTH, 53)

#Game Window
WIN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Mario Platformer!")

PWIDTH = 30
PHEIGHT = 40

# Dimensions
FIREBALL_WIDTH = 20
FIREBALL_HEIGHT = 28
FIREBALL_VEL = 2

STAR_WIDTH = 30
STAR_HEIGHT = 40

ENEMY_WIDTH = 35
ENEMY_HEIGHT = 35

# Misc
MAX_PLATFORMS = 9
JUMP = 8
GRAVITY = 0.75
FPS = 60

## Images
BG = pg.transform.scale(pg.image.load("images/mario.jpg"), (WIDTH, HEIGHT))
LEFT_MARIO = pg.transform.scale(pg.image.load("images/mario_character_left.png"), (PWIDTH, PHEIGHT))
RIGHT_MARIO = pg.transform.scale(pg.image.load("images/mario_character_right.png"), (PWIDTH, PHEIGHT))
JUMP_MARIO_RIGHT = pg.transform.scale(pg.image.load("images/mario_character_up_right.png"), (PWIDTH, PHEIGHT))
JUMP_MARIO_LEFT = pg.transform.scale(pg.image.load("images/mario_character_up_left.png"), (PWIDTH, PHEIGHT))
FIREBALL = pg.transform.scale(pg.image.load("images/fireball.png"), (FIREBALL_WIDTH, FIREBALL_HEIGHT+2))
PLATFORM = pg.transform.scale(pg.image.load("images/platform.png"), (90, 18))
STAR = pg.transform.scale(pg.image.load("images/star.png"), (STAR_WIDTH, STAR_HEIGHT))
ENEMY = pg.transform.scale(pg.image.load("images/goomba.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))


class Hero(pg.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = PWIDTH
        self.height = PHEIGHT
        self.player_vel = 6
        self.vel_y = 0
        self.jump_count = JUMP
        self.life_count = 3
        self.star_count = 0
        self.right_face = True
        self.left_face = False
        self.jump = False
        self.falling = True
        self.hit = False
        self.power_up = False
        self.rect = pg.Rect(x, y, self.width, self.height)
    
    def apply_gravity(self):
        self.y += JUMP
        self.rect.y = self.y
        self.falling = True
        
        ## Floor
        if FLOOR_RECT.colliderect(self.rect):
            self.y = FLOOR_RECT.top - self.height
            self.rect.bottom = FLOOR_RECT.top
            self.falling = False
            self.jump = False
        
    
    ## Character movement
    def move_hero(self, keyInput):
        ## Lateral
        if keyInput[pg.K_a] and self.x - self.player_vel >= 0:
            self.x -= self.player_vel
            self.rect.x = self.x
            self.left_face = True
            self.right_face = False
        elif keyInput[pg.K_d] and self.x + self.player_vel  <= WIDTH - 30:
            self.x += self.player_vel
            self.rect.x = self.x
            self.left_face = False
            self.right_face = True
        else: 
            self.right_face = True 
            self.left_face = False
        
        ## Jump 
        if self.jump is False and (keyInput[pg.K_SPACE] or keyInput[pg.K_w]):
            self.jump = True
            self.falling = False
        
        if self.jump: 
            if self.jump_count >= -JUMP:
                self.y -= (self.jump_count * abs(self.jump_count)) * 0.5
                self.rect.y = self.y
                self.jump_count -= 1
            else:
                self.jump_count = JUMP
                self.jump = False
                self.falling = True
        else: 
            self.apply_gravity()

        ## Platform collision
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if self.rect.bottom < platform.rect.centery:
                    if self.y > 0:
                        self.jump = False                                                    
                        self.rect.bottom = platform.rect.top
                        self.y = self.rect.top
                        self.jump_count = JUMP
                        

        
        pg.time.delay(15)
        pg.display.update()


    ## Life reduction
    def lives(self):
        if self.hit == True:
            self.life_count -= 1
            if self.life_count  == 0: 
                lost_text = FONT.render("You Lost!", 1, "white")
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT-350 - lost_text.get_height()/2))
                pg.display.update()
                pg.time.delay(4000)
                pg.quit()
                sys.exit()
              
            else:
                life_text = FONT.render("Be Careful! You lost 1 life", 1, 'white')
                WIN.blit(life_text, (WIDTH/2 - life_text.get_width()/2, HEIGHT-350 - life_text.get_height()/2)) 
                pg.display.update()
                pg.time.delay(2500)
                self.hit = False

    def powerUp(self):
        if self.power_up == True:
            self.star_count += 1
            if self.star_count == 10:
                win_text = FONT.render("You Won!", 1, 'white')
                WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT-350 - win_text.get_height()/2))
                pg.display.update()
                pg.time.delay(4000)
                pg.quit()
                sys.exit()
            else:
                self.power_up = False
                


    ## Direction Hero faces
    def draw_hero(self, WIN):
        #pg.draw.rect(WIN, (255,255,255), self.rect, 2)
        if self.left_face:
            WIN.blit(LEFT_MARIO, (self.x, self.y))
        if self.right_face:
            WIN.blit(RIGHT_MARIO, (self.x, self.y))

        if self.jump and self.right_face:
            self.right_face = False
            WIN.blit(JUMP_MARIO_RIGHT, (self.x, self.y))
        if self.jump and self.left_face:
            self.left_face = False
            WIN.blit(JUMP_MARIO_LEFT, (self.x, self.y))




class Object(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, width, height)
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.width = width
        self.height = height


## Create Platforms
class Platform(Object):
    def __init__(self,x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.blit(PLATFORM, (x,y)) 
        self.mask = pg.mask.from_surface(self.image)

p_width = 90
p_height = 20
platforms = [
            Platform(200, 150, p_width, p_height), Platform(350, 150, p_width, p_height), Platform(500, 150, p_width, p_height),
            Platform(200, 250, p_width, p_height), Platform(350, 250, p_width, p_height), Platform(500, 250, p_width, p_height)
            ]


def draw(player, fireballs, platforms, stars, enemies): 
    
    ## Game Window
    WIN.blit(BG, (0,0))
    
    ## Player 
    player.draw_hero(WIN)

    ## Platform
    for platform in platforms: 
        WIN.blit(PLATFORM, (platform.x, platform.y))
    
    ## Fireballs
    for fireball in fireballs: 
        WIN.blit(FIREBALL, (fireball.x, fireball.y))

    ## Stars
    for star in stars:
        WIN.blit(STAR, (star.x, star.y))

    ## Enemies
    for enemy in enemies:
        WIN.blit(ENEMY, (enemy.x, enemy.y))
        
    ## Life Counter
    life_text = FONT.render(f"Lives: {player.life_count}", 1, "white")
    WIN.blit(life_text, (10,10))

    ## Star Counter
    star_text = FONT.render(f"Stars: {player.star_count}", 1, "white")
    WIN.blit(star_text, (675,10))

    pg.display.update()


def createProjectiles(count, increment, height, width, lst, number):
    if count > increment: 
        for _ in range(number):
            xpos = random.randint(75,700)
            obj = pg.Rect(xpos, -height, width, height)
            lst.append(obj)
            
        increment = max(200, increment - 50)
        count = 0
        
    return lst, increment, count

def createEnemies(count, increment, height, width, lst, number):
    if count > increment: 
        for _ in range(number):
            xpos = int(-5)
            obj = pg.Rect(xpos, (FLOOR_RECT.top - height), width, height)
            lst.append(obj)
            
        increment = max(200, increment - 50)
        count = 0
        
    return lst, increment, count


def fireballCollision(array, player):
    for fireball in array[:]:
        fireball.y += FIREBALL_VEL
        if fireball.y > HEIGHT:
            array.remove(fireball)
        if fireball.colliderect(player.rect):
            array.remove(fireball)
            player.hit = True 
            break
    return array, player.hit

def starCollision(array, player):
    for star in array[:]:
        star.y += FIREBALL_VEL
        if star.y > HEIGHT:
            array.remove(star)
        if star.colliderect(player.rect):
            array.remove(star)
            player.power_up = True 
            break
    return array, player.power_up 

def enemyCollision(array, player):
    for enemy in array[:]:
            enemy.x += 2
            if enemy.x > WIDTH: 
                array.remove(enemy) ## removes enemies off-screen
            if enemy.colliderect(player.rect):
                array.remove(enemy)  
                player.hit = True 
                break
    return array, player.hit


    
def main():
    run = True
    
    
    ## Create character/set starting position
    player = Hero(25, 25)
    clock = pg.time.Clock()
    
    # Projectile variables
    fireball_add_increment = 3000
    fireball_count = 0 
    fireballs = []


    star_add_increment = 3000
    star_count = 0
    stars = []

    enemy_add_increment = 3000
    enemy_count = 0
    enemies = []
    

    
    while run == True:
        pg.init()
        
        ## Quit game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
        
        ## Input
        keysInput = pg.key.get_pressed()

        ## Draw game
        draw(player, fireballs, platforms, stars, enemies)

        ## Movement
        player.move_hero(keysInput)
        
        ## Runtime(fps) of projectiles
        fireball_count += clock.tick(FPS)
        star_count += clock.tick(FPS*2)
        enemy_count += clock.tick(FPS*2)

        ## Fireballs
        fireballs, fireball_add_increment, fireball_count = createProjectiles(fireball_count, fireball_add_increment, FIREBALL_HEIGHT, FIREBALL_WIDTH, fireballs, 6)
        fireballs, player.hit = fireballCollision(fireballs, player) 
        
        ## Stars
        stars, star_add_increment, star_count = createProjectiles(star_count, star_add_increment, STAR_HEIGHT, STAR_WIDTH, stars, 1)
        stars, player.power_up = starCollision(stars, player)

        ## Enemies
        enemies, enemy_add_increment, enemy_count = createEnemies(enemy_count, enemy_add_increment, ENEMY_HEIGHT, ENEMY_WIDTH, enemies, 1)
        enemies, player.hit = enemyCollision(enemies, player)
        
        ## Life Counter
        player.lives()

        ## Star Counter
        player.powerUp()

    pg.quit()
    sys.exit()    
    


if __name__ == "__main__":
    main()
 