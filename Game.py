import pygame
from sys import exit
from random import randint, choice


GLOBAL_FONTCOLOR = (110, 255, 255)
GLOBAL_WINDOW_WIDTH = 1280
GLOBAL_WINDOW_HEIGHT = 720
GLOBAL_LAND_Y = 335
GLOBAL_SPEED = 6
GLOBAL_THEME = "Day"

INVENTORY_MAC10 = False
INVENTORY_GOLDMAC10 = False

AWARD_REACH_NIGHT = False
AWARD_REACH_HELL = False

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('Assets/Entity/Spinka/RunRight1.png').convert_alpha()
		player_walk_2 = pygame.image.load('Assets/Entity/Spinka/RunRight2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('Assets/Entity/Spinka/JumpRight.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,GLOBAL_LAND_Y))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('Audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= GLOBAL_LAND_Y:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= GLOBAL_LAND_Y:
			self.rect.bottom = GLOBAL_LAND_Y

	def animation_state(self):
		if self.rect.bottom < GLOBAL_LAND_Y: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('Assets/Entity/ShrimpFly/ShrimpFly1.png').convert_alpha()
			fly_2 = pygame.image.load('Assets/Entity/ShrimpFly/ShrimpFly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 245
		else:
			snail_1 = pygame.image.load('Assets/Entity/Shrimp/Shrimp1.png').convert_alpha()
			snail_2 = pygame.image.load('Assets/Entity/Shrimp/Shrimp2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = GLOBAL_LAND_Y

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= GLOBAL_SPEED
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(GLOBAL_WINDOW_WIDTH * 0.07,GLOBAL_WINDOW_HEIGHT * 0.07,64))
	score_rect = score_surf.get_rect(center = (GLOBAL_WINDOW_WIDTH/2,GLOBAL_WINDOW_HEIGHT * 0.07))
	screen.blit(score_surf,score_rect)
	return current_time

def display_bscore():
	bscore_surf = test_font.render(f'Best: {bestscore}',False,(GLOBAL_WINDOW_WIDTH * 0.07,GLOBAL_WINDOW_HEIGHT * 0.07,64))
	bscore_rect = bscore_surf.get_rect(center = (GLOBAL_WINDOW_WIDTH * 0.07,GLOBAL_WINDOW_HEIGHT * 0.07))
	screen.blit(bscore_surf,bscore_rect)
	return bestscore

def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			obstacle_rect.x -= GLOBAL_SPEED-1

			if obstacle_rect.bottom == GLOBAL_LAND_Y: screen.blit(snail_surf,obstacle_rect)
			else: screen.blit(fly_surf,obstacle_rect)

		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

		return obstacle_list
	else: return []

def collisions(player,obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if player.colliderect(obstacle_rect): return False
	return True

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True

def player_animation():
	global player_surf, player_index

	if player_rect.bottom < GLOBAL_LAND_Y:
		player_surf = player_jump
	else:
		player_index += 0.1
		if player_index >= len(player_walk):player_index = 0
		player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((GLOBAL_WINDOW_WIDTH,GLOBAL_WINDOW_HEIGHT))
pygame.display.set_caption('SpinkaJumper 0.1a by c4thead for skazka')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Fonts/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bestscore = 0
bg_music = pygame.mixer.Sound('Audio/meow at the loop.wav')
bg_music.set_volume(0.4)
bg_music.play(loops = -1)
ClickMenu = pygame.mixer.Sound('Audio/ClickMenu_001.mp3')
ClickMenu.set_volume(1.0)

MAC10Blank = pygame.image.load('Assets/Icons/MAC-10_Blank.png').convert_alpha()
MAC10 = pygame.image.load('Assets/Icons/MAC-10.png').convert_alpha()
MAC10Gold = pygame.image.load('Assets/Icons/MAC-10_Gold.png').convert_alpha()

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('Assets/BackgroundDay.png').convert()
ground_surface = pygame.image.load('Assets/LandDay.png').convert_alpha()

sky_surface_Night = pygame.image.load('Assets/BackgroundNight.png').convert()
ground_surface_Night = pygame.image.load('Assets/LandNight.png').convert_alpha()

sky_surface_Hell = pygame.image.load('Assets/BackgroundHell.png').convert()
ground_surface_Hell = pygame.image.load('Assets/LandHell.png').convert_alpha()

# score_surf = test_font.render('My game', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400,50))

# Snail 
snail_frame_1 = pygame.image.load('Assets/Entity/Shrimp/Shrimp1.png').convert_alpha()
snail_frame_2 = pygame.image.load('Assets/Entity/Shrimp/Shrimp2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame1 = pygame.image.load('Assets/Entity/ShrimpFly/ShrimpFly1.png').convert_alpha()
fly_frame2 = pygame.image.load('Assets/Entity/ShrimpFly/ShrimpFly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []


player_walk_1 = pygame.image.load('Assets/Entity/Spinka/RunRight1.png').convert_alpha()
player_walk_2 = pygame.image.load('Assets/Entity/Spinka/RunRight2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('Assets/Entity/Spinka/JumpRight.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,GLOBAL_LAND_Y))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('Assets/Entity/Spinka/Idle.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (GLOBAL_WINDOW_WIDTH / 2,GLOBAL_WINDOW_HEIGHT / 2))

game_name = test_font.render('SpinkaRunner 0.1a',False,GLOBAL_FONTCOLOR)
game_name_rect = game_name.get_rect(center = (GLOBAL_WINDOW_WIDTH / 2,GLOBAL_WINDOW_HEIGHT * 0.07))

game_message = test_font.render('Press <X> or <R> to start',False,GLOBAL_FONTCOLOR)
game_message_rect = game_message.get_rect(center = (GLOBAL_WINDOW_WIDTH / 2,GLOBAL_WINDOW_HEIGHT * 0.93))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

bgX = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		if game_active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if player_rect.collidepoint(event.pos) and player_rect.bottom >= GLOBAL_LAND_Y: 
					player_gravity = -20
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and player_rect.bottom >= GLOBAL_LAND_Y:
					player_gravity = -20
		else:
			if event.type == pygame.KEYDOWN and (event.key == pygame.K_z or event.key == pygame.K_x or event.key == pygame.K_c or event.key == pygame.K_v or event.key == pygame.K_b or event.key == pygame.K_n or event.key == pygame.K_m or event.key == pygame.K_r) :
				game_active = True
				ClickMenu.play()
				start_time = int(pygame.time.get_ticks() / 1000)

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
				# if randint(0,2):
				# 	obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
				# else:
				# 	obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))

			if event.type == snail_animation_timer:
				if snail_frame_index == 0: snail_frame_index = 1
				else: snail_frame_index = 0
				snail_surf = snail_frames[snail_frame_index] 

			if event.type == fly_animation_timer:
				if fly_frame_index == 0: fly_frame_index = 1
				else: fly_frame_index = 0
				fly_surf = fly_frames[fly_frame_index] 


	if game_active:
		if GLOBAL_THEME == "Day":
			screen.blit(sky_surface,(0,0))
			screen.blit(ground_surface,(bgX,0))
			screen.blit(ground_surface,(bgX+1280,0))
		elif GLOBAL_THEME == "Night":
			screen.blit(sky_surface_Night,(0,0))
			screen.blit(ground_surface_Night,(bgX,0))
			screen.blit(ground_surface_Night,(bgX+1280,0))
		elif GLOBAL_THEME == "Hell":
			screen.blit(sky_surface_Hell,(0,0))
			screen.blit(ground_surface_Hell,(bgX,0))
			screen.blit(ground_surface_Hell,(bgX+1280,0))
		
		bgX -= GLOBAL_SPEED
		if bgX <= -1280: bgX = 0
		
		if score >= 15 and score < 30 :
			GLOBAL_SPEED = 8
			GLOBAL_THEME = "Day"
		elif score >= 30 and score < 50:
			GLOBAL_SPEED = 10
			GLOBAL_THEME = "Day"
		elif score >= 50 and score < 75:
			GLOBAL_SPEED = 12
			GLOBAL_THEME = "Day"
		elif score >= 75 and score < 100:
			GLOBAL_SPEED = 15
			GLOBAL_THEME = "Day"
		elif score >= 100 and score < 120:
			GLOBAL_SPEED = 16
			GLOBAL_THEME = "Night"
		elif score >= 120 and score < 150:
			GLOBAL_SPEED = 18
			GLOBAL_THEME = "Night"
		elif score >= 150 and score < 200:
			GLOBAL_SPEED = 20
			GLOBAL_THEME = "Night"
		elif score >= 200 and score < 300:
			GLOBAL_SPEED = 21
			GLOBAL_THEME = "Day"
			INVENTORY_MAC10 = True # MAC-10
		elif score >= 300 and score < 400:
			GLOBAL_SPEED = 22
			GLOBAL_THEME = "Night"
		elif score >= 400 and score < 500:
			GLOBAL_SPEED = 23
			GLOBAL_THEME = "Day"
		elif score >= 500 and score < 600:
			GLOBAL_SPEED = 23
			GLOBAL_THEME = "Night"
			INVENTORY_GOLDMAC10 = True # MAC-10 Gold
		elif score >= 600 and score < 700:
			GLOBAL_SPEED = 24
			GLOBAL_THEME = "Day"
		elif score >= 700 and score < 800:
			GLOBAL_SPEED = 25
			GLOBAL_THEME = "Night"
		elif score >= 1000:
			GLOBAL_SPEED = 30
			GLOBAL_THEME = "Hell"
		else:
			GLOBAL_SPEED = 6
			GLOBAL_THEME = "Day"
		
		if GLOBAL_THEME == "Night":
			AWARD_REACH_NIGHT = True
		if GLOBAL_THEME == "Hell":
			AWARD_REACH_HELL = True

		# pygame.draw.rect(screen,'#c0e8ec',score_rect)
		# pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
		# screen.blit(score_surf,score_rect)
		score = display_score()
		bestscore = display_bscore()
		
		# snail_rect.x -= 4
		# if snail_rect.right <= 0: snail_rect.left = 800
		# screen.blit(snail_surf,snail_rect)

		# Player 
		# player_gravity += 1
		# player_rect.y += player_gravity
		# if player_rect.bottom >= 300: player_rect.bottom = 300
		# player_animation()
		# screen.blit(player_surf,player_rect)
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		# Obstacle movement 
		# obstacle_rect_list = obstacle_movement(obstacle_rect_list)

		# collision 
		game_active = collision_sprite()
		# game_active = collisions(player_rect,obstacle_rect_list)
		
	

	else:
		if AWARD_REACH_NIGHT:
			screen.fill((22,22,68))
			if AWARD_REACH_HELL:
				screen.fill((155,5,10))
		else:
			screen.fill((46,160,151))

		screen.blit(player_stand,player_stand_rect)
		obstacle_rect_list.clear()
		player_rect.midbottom = (80,GLOBAL_LAND_Y)
		player_gravity = 0

		if score > bestscore: bestscore = score

		score_message = test_font.render(f'Your Score: {score}',False,GLOBAL_FONTCOLOR)
		score_message_rect = score_message.get_rect(center = (GLOBAL_WINDOW_WIDTH /  2, GLOBAL_WINDOW_HEIGHT * 0.85))
		screen.blit(game_name,game_name_rect)
		bscore_message = test_font.render(f'Your Best: {bestscore}',False,GLOBAL_FONTCOLOR)
		bscore_message_rect = bscore_message.get_rect(center = (GLOBAL_WINDOW_WIDTH /  2, GLOBAL_WINDOW_HEIGHT * 0.93))
		screen.blit(game_name,game_name_rect)

		if INVENTORY_MAC10:
			screen.blit(MAC10, (82, 170))
		else:
			screen.blit(MAC10Blank, (82, 170))
		
		if INVENTORY_GOLDMAC10:
			screen.blit(MAC10Gold, (920, 170))
		else:
			screen.blit(MAC10Blank, (920, 170))

		if score == 0: screen.blit(game_message,game_message_rect)
		else:
			screen.blit(score_message,score_message_rect)
			screen.blit(bscore_message,bscore_message_rect)

	pygame.display.update()
	clock.tick(60)
