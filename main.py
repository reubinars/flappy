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
#sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
#title
init_surface = pygame.image.load('assets/message.png').convert_alpha()
init_rect = init_surface.get_rect(center = (144,256))
#bird
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
# score
score=0
high_score=0
game_font = pygame.font.Font('04B_19.ttf',20)
can_score = True
#flap event every 0.2 sec
BIRDFLAP = pygame.USEREVENT
pygame.time.set_timer(BIRDFLAP, 200)
# pipe event
SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE, 2000)
pipe_list = []

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
    return bottom_pipe,top_pipe #create pipe

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


# score
def score_display():
    if start:
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,30))
        SCREEN.blit(score_surface,score_rect)
    else:
        score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,30))
        SCREEN.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,450))
        SCREEN.blit(high_score_surface,high_score_rect)

def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()#score sound
                can_score = False
            if pipe.centerx < 0:
                can_score = True

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play() #death sound
            can_score = True
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        can_score = True
        return False
    return True

#main loop
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE and not start:
                pipe_list = []
                bird_rect.center = (50, 288)
                score = 0
                start = True
            if event.key == pygame.K_SPACE and start:
                bird_movement = -5
                flap_sound.play() #flap sound
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
        clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                clicked =True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==pygame.BUTTON_LEFT:
                clicked =True
        if clicked and not start:
            pipe_list=[]
            bird_rect.center = (50,288)
            score=0
            start = True
        if clicked and start:
            bird_movement = -5
            flap_sound.play()

    SCREEN.blit(bg_surface, (0,0)) #base

    if start:
        bird_movement += gravity #move down
        bird_rect.centery += bird_movement
        SCREEN.blit(bird_surface, bird_rect)
        #collision
        start = check_collision(pipe_list)
        #high score update
        if not start:
            if high_score < score:
                high_score = score
        #make pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list) #draw pipes
        pipe_score_check() #add
    else:
        # SCREEN.blit(bird_downflap, bird_rect)
        SCREEN.blit(init_surface, init_rect)

# draw floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
# secore
    score_display() 
    pygame.display.update()