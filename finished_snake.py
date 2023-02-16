import random
import pygame
import time
import sys

pygame.init()
pygame.display.set_caption("SNAKE!") 

# ------ variables ------
# display width and height have to be a multiple of box
box = 40
display_width = 800
display_height = 600

rows = display_height/box
cols = display_width/box

w = (display_width/2) 
h = (display_height/2)

death_text_pos = ((w - 140),(h - 200))
start_text_pos = ((w - 150),(h - 50))

display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock() 

radius = 19
player_score = 0

#starting pos:
x = 380 
y = 340

food_x = 0
food_y = 0

#fonts
scorefont = pygame.font.SysFont("comicsansms", 25)
endfont = pygame.font.SysFont("arial", 75)

# colors
black = (0,0,0)
white = (255,255,255)
food_color = (128, 0, 0)
snake_color = (183, 111, 70)
snake_secondary_color = (183, 111, 70) # s(102, 48, 26)

# sprite [ERROR] pygame.error: Failed loading libwebp-7.dll: The specified module could not be found.
# apple = pygame.image.load("Game Project/other/apple_sprite_og.png").convert() 

# ------ functions ------
def score_display(score): 
    dis_score = scorefont.render("Score: " + str(score), 1, (255,255,255))
    display.blit(dis_score, (0, 0))
        

def snake(snake_list,secondary_list):
    for i in range(len(snake_body)-1):
        xx1 = (snake_body[i][0] + snake_body[i+1][0])/2
        yy1 = (snake_body[i][1] + snake_body[i+1][1])/2
        pygame.draw.circle(display,snake_secondary_color, (xx1,yy1) , radius)  
    for l in snake_body:
        pygame.draw.circle(display,snake_secondary_color, l , radius) 

def snake_eye(location):
    xi = snake_location[0]
    yi = snake_location[1]
    if direction == "up" or direction == "down":
        pygame.draw.circle(display, snake_secondary_color, (xi-13, yi), 8)
        pygame.draw.circle(display, white, (xi-13, yi), 7)
        pygame.draw.circle(display, black, (xi-13, yi), 5)

    
        pygame.draw.circle(display, snake_secondary_color, (xi+13, yi), 8)
        pygame.draw.circle(display, white, (xi+13, yi), 7)
        pygame.draw.circle(display, black, (xi+13, yi), 5)

    if direction == "right" or direction == "left":
        pygame.draw.circle(display, snake_secondary_color, (xi, yi-13), 8)
        pygame.draw.circle(display, white, (xi, yi-13), 7)
        pygame.draw.circle(display, black, (xi, yi-13), 5)

    
        pygame.draw.circle(display, snake_secondary_color, (xi, yi+13), 8)
        pygame.draw.circle(display, white, (xi, yi+13), 7)
        pygame.draw.circle(display, black, (xi, yi+13), 5)


# def death_text():
#     text = endfont.render("You Died!",1, white)
#     display.blit(text, death_text_pos)
#     time.sleep(3)

# background                        original code: https://blog.furas.pl/pygame-draw-background-chekerboard-gb.html 
bg_green_light = (170, 215, 81)
bg_green_dark = (88, 140, 52)

display_background = pygame.surface.Surface(display.get_size())
def background():
    color = bg_green_light
    for x in range(0, display_width, box):
        for y in range(0, display_height, box):
            pygame.draw.rect(display_background, color, [x, y, box, box])
            if color == bg_green_light:
                color = bg_green_dark
            else:
                color = bg_green_light
# background()
# display.blit(display_background, (0,0))
# pygame.display.flip()

# ------ food ------
food_size = radius - 4
food_x = ((random.randrange(1, cols))*box)-20
food_y = ((random.randrange(1, rows))*box)-20

food_location = (food_x,food_y)

pygame.draw.circle(display, food_color, food_location, food_size)

# ------ PYGAME LOOPS ------

# ---- Start Screen ----
starts = False
bg = pygame.image.load("Game Project/snake_start.png")
while not starts:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            starts = True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            direction = "up"
            starts = True
        
        display.blit(bg,(0,0))
        pygame.display.update()

# -- background --       
background()
display.blit(display_background, (0,0))
pygame.display.flip()

# ---- Game Loop ----
#displacement from last position
x1 = 0
y1 = 0

direction = ""

dead = False
player_death = False
snake_body = []
snake_secondary = []

while not dead and starts == True:

    score_display(player_score)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            dead = True

        # snake direction change
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if direction != "down":
                    y1 = -box
                    x1 = 0
                    direction = "up"
                    # print(direction)
                
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if direction != "up":
                    y1 = box
                    x1 = 0
                    direction = "down"
                    # print(direction)
                    
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if direction != "left":
                    x1 = box
                    y1 = 0
                    direction = "right"
                    # print(direction)

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if direction != "right":
                    x1 = -box
                    y1 = 0
                    direction = "left"
                    # print(direction)

    background()
    display.blit(display_background, (0,0))

    x += x1
    y += y1

    snake_location = (x,y) #location of the head
    snake_body.append(snake_location)

    # snake score = the number of circle coordinates in the list
    if len(snake_body) > (player_score + 1):
        del snake_body[0]

    
    snake(snake_body,snake_secondary)
    
    
    pygame.draw.circle(display, food_color, food_location, food_size)
        
    pygame.draw.circle(display, snake_color, (x,y) , radius) 
    score_display(player_score)
    snake_eye(snake_location)
    pygame.display.update()

    # --- deaths ---
    if y < 0 or x < 0 or x > display_width or y > display_height:  
        print("out of bounds death")
        text = endfont.render("You Died!",1, white)
        display.blit(text, death_text_pos)
        pygame.display.update()
        time.sleep(3)
        player_death = True
        dead = True
    
    if snake_body.count(snake_location) > 1:
        print("overlap death")
        text = endfont.render("You Died!",1, white)
        display.blit(text, death_text_pos)
        pygame.display.update()
        time.sleep(3)
        player_death == True
        dead = True

    if food_location == snake_location:
        player_score += 1
        while food_location in snake_body:
            food_x = ((random.randrange(1, cols))*box)-20
            food_y = ((random.randrange(1, rows))*box)-20
            food_location = (food_x,food_y)
    
    fps = 5
    if player_score > 10 and player_score >= 20:
        fps = 7
    elif player_score >= 30:
        fps = 10
    elif player_score >= 50:
        fps = 15
    elif player_score >= 75:
        fps = 20
    clock.tick(fps) #fps + speed

# ------ x ------
pygame.quit()
quit()