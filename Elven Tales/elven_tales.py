import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
     def __init__(self):
         super().__init__()
         fantasy_warrior_run1 = pygame.image.load('Elven Tales/graphics/frame1.png').convert_alpha()
         fantasy_warrior_run2 = pygame.image.load('Elven Tales/graphics/frame2.png').convert_alpha()
         fantasy_warrior_run3 = pygame.image.load('Elven Tales/graphics/frame3.png').convert_alpha()
         fantasy_warrior_run4 = pygame.image.load('Elven Tales/graphics/frame4.png').convert_alpha()
         fantasy_warrior_run5 = pygame.image.load('Elven Tales/graphics/frame5.png').convert_alpha()
         fantasy_warrior_run6 = pygame.image.load('Elven Tales/graphics/frame6.png').convert_alpha()
         fantasy_warrior_run7 = pygame.image.load('Elven Tales/graphics/frame7.png').convert_alpha()
         fantasy_warrior_run8 = pygame.image.load('Elven Tales/graphics/frame8.png').convert_alpha()
         
         self.fantasy_warrior_run = [fantasy_warrior_run1,fantasy_warrior_run2,fantasy_warrior_run3,fantasy_warrior_run4,fantasy_warrior_run5,fantasy_warrior_run6,fantasy_warrior_run7,fantasy_warrior_run8]
         self.fantasy_warrior_index = 0
         self.fantasy_warrior_jump = pygame.image.load('Elven Tales/graphics/jump1.png').convert_alpha()
          

         self.image = self.fantasy_warrior_run[self.fantasy_warrior_index]
         self.rect = self.image.get_rect(midbottom = (200,395))
         self.gravity = 0

         self.jump_sound = pygame.mixer.Sound('Elven Tales/audio/jump.wav')
         self.jump_sound.set_volume(1)

     def player_input(self):
         keys = pygame.key.get_pressed()
         if keys[pygame.K_SPACE] and self.rect.bottom >= 395:
            self.gravity = -20
            self.jump_sound.play()
      
     def apply_gravity(self):
         self.gravity += 1
         self.rect.y += self.gravity
         if self.rect.bottom >= 395:
            self.rect.bottom = 395
      
     def animation_state(self):
         if self.rect.bottom <395:
            self.image = self.fantasy_warrior_jump
         else:
            self.fantasy_warrior_index += 0.1
            if self.fantasy_warrior_index >= len(self.fantasy_warrior_run):self.fantasy_warrior_index = 0
            self.image = self.fantasy_warrior_run[int(self.fantasy_warrior_index)]

     def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
     def __init__(self,type):
         super().__init__()
         
         if type == 'fly':
             flying_eye_surf =pygame.image.load('Elven Tales/graphics/fly/flying_eye.png').convert_alpha()
             flying_eye_frame1 =pygame.transform.flip(flying_eye_surf, True, False)
             flying_eye_surf_two = pygame.image.load('Elven Tales/graphics/fly/flying_eye2.png').convert_alpha()
             flying_eye_frame2 =   pygame.transform.flip(flying_eye_surf_two, True, False)
             self.frames = [flying_eye_frame1,flying_eye_frame2]
             y_pos = 305
         else:
             goblin_surface = pygame.image.load('Elven Tales/graphics/goblin/gob1.png').convert_alpha()
             goblin_frame1 = pygame.transform.flip(goblin_surface, True, False)
             goblin_surface_two = pygame.image.load('Elven Tales/graphics/goblin/gob2.png').convert_alpha()
             goblin_frame2 = pygame.transform.flip(goblin_surface_two, True, False)
             self.frames= [goblin_frame1,goblin_frame2]
             y_pos =395

         self.animation_index = 0
         
         self.image = self.frames[self.animation_index]
        
         self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
     
     def animation_state(self):
         self.animation_index += 0.1
         if self.animation_index >= len(self.frames): self.animation_index =0
         self.image = self.frames[int(self.animation_index)]

     def update(self):
         self.animation_state()
         self.rect.x -= 6
         self.destroy()
    
     def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
   current_time = int(pygame.time.get_ticks() / 1000)- start_time
   score_surf = test_font.render(f'Score:{current_time}',False,'Black')
   score_rect = score_surf.get_rect(center = (400,50))
   screen.blit(score_surf, score_rect)
   return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
       obstacle_group.empty()
       return False
    else: return True

pygame.init() 
#parameters for display window
screen = pygame.display.set_mode((800,420)) 
#captioning the file
pygame.display.set_caption('Elven Tales')        
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('Elven Tales/audio/Graceful_Resistance.ogg')
bg_music.play(loops = -1)
#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

test_font = pygame .font.Font('Elven Tales/font/hexenkoetel.ttf', 50)
font_test = pygame.font.Font('Elven Tales/font/hexenkoetel.ttf', 70)
forest_surface = pygame.image.load('Elven Tales/graphics/forest.png')

#Intro screen
fantasy_warrior_stand = pygame.image.load('Elven Tales/graphics/endscreen.png').convert_alpha()
fantasy_warrior_stand = pygame.transform.scale2x(fantasy_warrior_stand)
fantasy_warrior_stand_rect = fantasy_warrior_stand.get_rect(center =(400,210))

game_name = font_test.render('Elven Tales', False, (245,245,220))
game_name_rect = game_name.get_rect(center = (380, 60))

game_message = test_font.render('Press space to play', False, (94,129,162))
game_message_rect = game_message.get_rect(center =(380, 320))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True: 
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
         
            if game_active:      
                   if event.type == obstacle_timer:
                           obstacle_group.add(Obstacle(choice(['fly','goblin','goblin','goblin'])))
            else:
               if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                  game_active = True
         
                  start_time = int(pygame.time.get_ticks() / 1000)
    if game_active:

     screen.blit(forest_surface,(0,0)) 
     #screen.blit(score_surface, score_rect)
     score = display_score()
     
     player.draw(screen)
     player.update()
     
     obstacle_group.draw(screen)
     obstacle_group.update()

     #collision
     game_active = collision_sprite()
    
    else:
       screen.fill((16, 38, 32))
       screen.blit(fantasy_warrior_stand, fantasy_warrior_stand_rect)
       
       score_message = test_font.render(f'Your score: {score}',False, (94,129,162))
       score_message_rect = score_message.get_rect(center = (380,320))
       screen.blit(game_name, game_name_rect)  
       
       if score == 0:screen.blit(game_message, game_message_rect)
       else:screen.blit(score_message,score_message_rect)
      
    pygame.display.update()
    #specification  to run at 60 fps 
    clock.tick(60)           