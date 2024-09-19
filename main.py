import pygame,sys,random
pygame.init()

# var
SCREEN = pygame.display.set_mode((288,512))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
FPS = 120
start = False
bird_movement = 0
gravity = 0.1

#asset load
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bg_surface = pygame.image.load('assets/background-day.png').convert()
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_downflap.get_rect(center = (50,256))
# floor
floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0
# pipe
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_height = [200,300,400]

#flap event every 0.2 sec
BIRDFLAP = pygame.USEREVENT
pygame.time.set_timer(BIRDFLAP, 200)

# bird anim func
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

# floor func
def draw_floor():
    SCREEN.blit(floor_surface,(floor_x_pos,450))
    SCREEN.blit(floor_surface,(floor_x_pos + 288,450))

#pipe 
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (300,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (300,random_pipe_pos - 150))
    return bottom_pipe,top_pipe
pipe_list = create_pipe() #create pipe 

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            SCREEN.blit(pipe_surface,pipe)
        else: 
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            SCREEN.blit(flip_pipe,pipe)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    visible_pipes = [pipe for pipe in pipes if pipe.right > -25]
    return visible_pipes

#main loop
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE and not start:
                start = True
            if event.key == pygame.K_SPACE and start:
                bird_movement = -5
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    SCREEN.blit(bg_surface, (0,0))

    if start:
        bird_movement += gravity #move down
        bird_rect.centery += bird_movement
        SCREEN.blit(bird_surface, bird_rect)
        #make pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list) #draw pipes
    else:
        SCREEN.blit(bird_downflap, bird_rect)
                
# draw floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
    pygame.display.update()