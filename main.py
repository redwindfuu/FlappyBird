import random

import pygame,sys


pygame.mixer.pre_init(frequency=44100,size= -16,channels= 2 ,buffer=512)
pygame.init()

screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF",40)
#check game
score = 0
high_score = 0
with open('scoreHigh.txt') as f:
    high_score = int(f.read())
game_active = True
#tạo màn hình kết thức
game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/message.png")).convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (216,384))
# nền
bg = pygame.transform.scale2x(pygame.image.load("assets/background-night.png")).convert()
# sàn
floor = pygame.transform.scale2x(pygame.image.load("assets/floor.png"))
floor_x_pos = 0
#chim
bird_mid = pygame.transform.scale2x(pygame.image.load("assets/yellowbird-midflap.png")).convert_alpha()
bird_up = pygame.transform.scale2x(pygame.image.load("assets/yellowbird-upflap.png")).convert_alpha()
bird_down = pygame.transform.scale2x(pygame.image.load("assets/yellowbird-downflap.png")).convert_alpha()
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 1
bird =  bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,384))
gravity = 0.25
bird_movement = 0
#chim đập cánh
birdflap = pygame.USEREVENT +1
pygame.time.set_timer(birdflap,200)
#chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
# ống
pipes_surface =  pygame.transform.scale2x(pygame.image.load("assets/pipe-green.png")).convert()
pipes_list = []
pipes_height = [200,300,400]
spwanpipes = pygame.USEREVENT
pygame.time.set_timer(spwanpipes,1200)
def update_score(score,high_score):
    if score > high_score:
        high_score  = score
    return high_score
def score_display(gamestare):
    if gamestare == 'main game' :
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216 ,100))
        screen.blit(score_surface,score_rect)
    if gamestare == 'game_over':
        score_surface = game_font.render(f'Score :{int(score)} ', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score :{int(high_score)} ', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center = (190, 630))
        screen.blit(high_score_surface, high_score_rect)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432 , 650))
def create_pipes():
    random_pipe_pos = random.choice(pipes_height)
    bottom_pipe = pipes_surface.get_rect(midtop = (500,random_pipe_pos ))
    top_pipe = pipes_surface.get_rect(midtop=(500, random_pipe_pos-650))
    return bottom_pipe,top_pipe
def pipe_move(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def pipe_draw(pipes):
    for pipe in pipes:
        if pipe.bottom >=  600 :
            screen.blit(pipes_surface,pipe)
        else:
            screen.blit(pygame.transform.flip(pipes_surface,False,True),pipe)
def rotate_bird(bird1):
    new_bird  = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird =bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('scoreHigh.txt',"w") as f:
                f.write(str(int(high_score)) )
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipes_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spwanpipes :
            pipes_list.extend(create_pipes())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird,bird_rect = bird_animation()

    screen.blit(bg,(0,0))

    if game_active:
        #chim
        bird_movement += gravity
        rotated_bird =  rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipes_list)
        # ống
        pipes_list = pipe_move(pipes_list)
        pipe_draw(pipes_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <=0 :
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score )
        score_display('game_over')
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)