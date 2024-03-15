import pygame, sys
from random import randint,randrange
import math
lol=True
import pygame, sys

class Enemy(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		global lider_list
		self.nocol=1
		self.agr=512
		self.hp=6
		self.m_mode=False
		self.pos = pos
		self.count=0
		self.um_count=30
		self.l_count=0
		self.call_cnt=69
		self.cooldown=0
		self.image = pygame.image.load('graphics/man.png').convert_alpha()
		self.base_player_image= self.image
		self.hitbox_rect = self.image.get_rect(center = pos)
		self.rect = self.hitbox_rect.copy()
		self.speed = 15
		self.flag=False
		self.trigger=True
		self.leader=False
		self.tan=math.atan2(0,0)
		self.collision_point=(0,0)
		lider_list=[]

	def input(self):
		if self.cooldown>1:
			self.cooldown-=1
		else:
			lider_list=[]
			for e in enemy:
				if e.leader==True:
					lider_list.append(e)
			self.count+=0
			self.coords = player.rect.center
			self.x_change_mouse_player = (self.coords[0] - self.rect.centerx)
			self.y_change_mouse_player = (self.coords[1] - self.rect.centery)
			if math.sqrt(self.x_change_mouse_player**2+self.y_change_mouse_player**2)<self.agr:
				if self.trigger==True:
					self.check_los()
				else:
					self.um_count+=1
					if self.leader:
						self.count+=1
						self.l_count+=1

						if self.count>4:
							self.count=0
							l_ghosts.add(GhostLeader(self.pos,self.rect,camera_group))

						if self.l_count>180:
							self.l_count=0
							self.leader=False

					if self.um_count>70:
						self.um_count=0
						self.check_los()

				if self.m_mode==True:
					self.move()
				elif self.m_mode==2:
					self.move_leader()
				else:
					self.follow()
				self.trigger=False
			else:
				self.trigger=True
		self.check_hp()

	def follow(self):

		self.angle = math.degrees(self.tan)
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle-90)
		self.rect = self.image.get_rect(center = self.hitbox_rect.center)

		self.velocity_x=self.speed*math.cos(self.tan)/math.sqrt(2)
		self.velocity_y=self.speed*math.sin(self.tan)/math.sqrt(2)

		self.collision_point=(self.rect.centerx+self.velocity_x*1.5,self.rect.centery+self.velocity_y*1.5)

		self.collision()

		self.pos += pygame.math.Vector2(self.velocity_x*self.nocol, self.velocity_y*self.nocol)
		self.nocol=1
		self.hitbox_rect.center = self.pos
		self.rect.center = self.hitbox_rect.center

	def move(self):
		cord = player.rect.center
		x_change_mouse_player = (cord[0] - self.rect.centerx)
		y_change_mouse_player = (cord[1] - self.rect.centery)
		self.tan=math.atan2(y_change_mouse_player, x_change_mouse_player)
		self.angle = math.degrees(self.tan)
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle-90)
		self.rect = self.image.get_rect(center = self.hitbox_rect.center)

		self.velocity_x=self.speed*math.cos(self.tan)/math.sqrt(2)
		self.velocity_y=self.speed*math.sin(self.tan)/math.sqrt(2)

		self.collision_point=(self.rect.centerx+self.velocity_x*1.5,self.rect.centery+self.velocity_y*1.5)

		self.collision()

		self.pos += pygame.math.Vector2(self.velocity_x*self.nocol, self.velocity_y*self.nocol)
		self.nocol=1
		self.hitbox_rect.center = self.pos
		self.rect.center = self.hitbox_rect.center
	def move_leader(self):
		cord = lider_list[-1].rect.center
		x_change_mouse_player = (cord[0] - self.rect.centerx)
		y_change_mouse_player = (cord[1] - self.rect.centery)
		self.tan=math.atan2(y_change_mouse_player, x_change_mouse_player)
		self.angle = math.degrees(self.tan)
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle-90)
		self.rect = self.image.get_rect(center = self.hitbox_rect.center)

		self.velocity_x=self.speed*math.cos(self.tan)/math.sqrt(2)
		self.velocity_y=self.speed*math.sin(self.tan)/math.sqrt(2)

		self.collision_point=(self.rect.centerx+self.velocity_x*1.5,self.rect.centery+self.velocity_y*1.5)

		self.collision()

		self.pos += pygame.math.Vector2(self.velocity_x*self.nocol, self.velocity_y*self.nocol)
		self.nocol=1
		self.hitbox_rect.center = self.pos
		self.rect.center = self.hitbox_rect.center

	def check_los(self):
		self.coords=[]
		lst_1=[]
		lst_2=[]
		for ghost in ghosts:
			lst_1.append(ghost)
		for ghost in l_ghosts:
			lst_2.append(ghost)
		if len(lst_1)>1 and len(lst_2)>1:
			if not(self.leader) and len(lider_list)>0:
				for i in lider_list:
					self.coords.insert(0,i)
				self.coords.append(lst_2[-1])
				self.coords.append(lst_2[-2])
			else:
				self.coords.append(lst_1[-1])
				self.coords.append(lst_1[-2])
				self.coords.append(lst_1[len(lst_1)//2])
				self.coords.append(lst_1[0])
		self.coords.insert(0,player)
		for e in self.coords:
			self.flag=False
			cord = e.rect.center
			x_change_mouse_player = (cord[0] - self.rect.centerx)
			y_change_mouse_player = (cord[1] - self.rect.centery)
			self.tan=math.atan2(y_change_mouse_player, x_change_mouse_player)
			velocity_x=math.cos(self.tan)*20
			velocity_y=math.sin(self.tan)*20
			for i in range(int(x_change_mouse_player//velocity_x)):
				self.collision_point=(int((self.rect.centerx+i*velocity_x)),int((self.rect.centery+i*velocity_y)))
				# self.collision_rect=Dot(self.collision_point,camera_group)
				for tree in trees:
					if tree.rect.collidepoint(self.collision_point):
						self.flag=True
						break
			if self.flag==False and e==player:
				self.m_mode=True
				break
			if self.flag==False and e.leader==True:
				self.m_mode=2
				break
			elif self.flag==False:
				self.m_mode=False
				break
	
	def collision(self):
		if player.rect.collidepoint(self.collision_point):
			player.kill()
		for ghost in ghosts:
			if ghost.rect.collidepoint(self.collision_point):
				self.call_cnt+=1
				self.leader=True
				if self not in lider_list:
					lider_list.append(self)
				if self.call_cnt%4==0:
					self.check_los()
				if self.call_cnt>30:
					self.call_cnt=0
					for e in enemy:
						cord = e.rect.center
						x_change_mouse_player = (cord[0] - self.rect.centerx)
						y_change_mouse_player = (cord[1] - self.rect.centery)
						if math.sqrt(x_change_mouse_player**2+y_change_mouse_player**2)<self.agr:
							e.um_count=0
							e.move_leader()
				ghost.kill()
				break
		# for e in enemy:
		# 	if e.rect.collidepoint(self.collision_point) and e.collision_point!=self.collision_point:
		# 		self.nocol=0
		for tree in trees:
			if tree.rect.collidepoint(self.collision_point):
				self.nocol=0
				self.call_cnt+=1
				if self.call_cnt>100:
					self.call_cnt=0
					self.check_los()
	def check_hp(self):
		if self.hp<1:
			self.kill()
	
	def update(self):
		self.input()

class Bullet(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/bullet.png').convert_alpha()
		self.base_player_image= self.image
		self.hitbox_rect = self.image.get_rect(center = pos)
		self.rect = self.hitbox_rect.copy()
		self.vector=self.hitbox_rect.center
		self.tan=player.tan
		self.speed=15
		self.mode=player.mode
		self.rand_bullets()
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)
	def move(self):

		self.velocity_x=self.speed*math.cos(self.tan)
		self.velocity_y=self.speed*math.sin(self.tan)

		self.vector += pygame.math.Vector2(self.velocity_x, self.velocity_y)
		self.hitbox_rect.center = self.vector
		self.rect.center = self.hitbox_rect.center
		
		self.collision_point=(self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*4)
		for tree in trees:
			if tree.rect.colliderect(self.rect):
				self.kill()
		for e in enemy:
			if e.rect.colliderect(self.rect):
				self.kill()
				e.hp-=2
		if abs(self.rect.center[0])>5000 or abs(self.rect.center[1])>5000:
			self.kill()
		
	def rand_bullets(self):
		if self.mode=='sg':
			rand=randrange(-110,110)
			self.tan= self.tan+0.001*abs(rand) if self.tan>0 else self.tan-0.001*abs(rand)
			self.vector=(self.vector[0]+0.1*rand,self.vector[1]+0.1*rand)
		else:
			rand=randrange(-100,100)
			self.tan=self.tan+0.0005*rand
		self.angle = math.degrees(self.tan)
	def update(self):
		self.move()

class Tree(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/tree.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.nocol=1
		self.mode='ssg'
		self.pos = pygame.math.Vector2(640,320)
		self.image = pygame.image.load('graphics/player.png').convert_alpha()
		self.base_player_image= self.image
		self.hitbox_rect = self.image.get_rect(center = pos)
		self.rect = self.hitbox_rect.copy()
		self.speed = 15
		self.p_colldown=30
		self.count=0
		self.ghost_cnt=0

	def input(self):
		if self.p_colldown<=16:
			self.p_colldown+=1
		if self.count<71:
			self.count+=1
		if self.ghost_cnt<2:
			self.ghost_cnt+=1
		else:
			self.ghost_cnt=0
			ghosts.add(GhostPlayer(self.pos,camera_group))
		self.mouse_coords = pygame.mouse.get_pos()
		display_surface = pygame.display.get_surface()
		self.half_w = display_surface.get_size()[0] // 2
		self.half_h = display_surface.get_size()[1] // 2
		self.x_change_mouse_player = (self.mouse_coords[0] - self.half_w)
		self.y_change_mouse_player = (self.mouse_coords[1] - self.half_h)
		self.tan=math.atan2(self.y_change_mouse_player, self.x_change_mouse_player)
		self.angle = math.degrees(self.tan)
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)
		self.rect = self.image.get_rect(center = self.hitbox_rect.center)


		self.velocity_x=self.speed*math.cos(self.tan)/math.sqrt(2)
		self.velocity_y=self.speed*math.sin(self.tan)/math.sqrt(2)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.coll_1=(self.rect.centerx+self.velocity_x*1.5,self.rect.centery+self.velocity_y*1.5)
			self.collision()

			self.pos += pygame.math.Vector2(self.velocity_x*self.nocol, self.velocity_y*self.nocol)
			self.nocol=1
			self.hitbox_rect.center = self.pos
			self.rect.center = self.hitbox_rect.center
		if keys[pygame.K_f]:
			if self.p_colldown>=15:
				self.p_colldown=0
				self.coll_1=(self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*4)
				self.coll_2=(self.rect.centerx+self.velocity_x*6,self.rect.centery+self.velocity_y*6)
				Dot(self.coll_1,camera_group)
				Dot(self.coll_2,camera_group)
				self.punch_collision()
		if pygame.mouse.get_pressed()[0]:
			if self.mode=='sg' and self.count>70:
				self.count=0
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
			elif self.mode=='ssg' and self.count>3:
				self.count=0
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
			elif self.mode!='sg' and self.count>15:
				self.count=0
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)

	def collision(self):
		for tree in trees:
			if tree.rect.collidepoint(self.coll_1):
				self.nocol=0
	def punch_collision(self):
		for e in enemy:
			if e.rect.collidepoint(self.coll_1) or e.rect.collidepoint(self.coll_2):
				e.hp-=1
				e.cooldown=40

	def update(self):
		self.input()

class GhostPlayer(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.pos = pos
		self.image = pygame.image.load('graphics/ghost.png').convert_alpha()
		self.rect = player.rect
		self.life_c=0
		self.leader=False
	def update(self):
		self.life_c+=1
		if self.life_c>75:
			self.kill()
class GhostLeader(pygame.sprite.Sprite):
	def __init__(self,pos,rect,group):
		super().__init__(group)
		self.pos = pos
		self.image = pygame.image.load('graphics/ghost.png').convert_alpha()
		self.rect = rect.copy()
		self.life_c=0
		self.leader=False
	def update(self):
		self.life_c+=1
		if self.life_c>45:
			self.kill()

class Dot(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.pos = pos
		self.image = pygame.image.load('graphics/floor.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.life_c=0
	def update(self):
		self.life_c+=1
		if self.life_c>30:
			self.kill()

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		self.ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

	def center_target_camera(self,target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h

	def custom_draw(self,player):
		
		self.center_target_camera(player)

		# ground 
		ground_offset = self.ground_rect.topleft - self.offset
		self.display_surface.blit(self.ground_surf,ground_offset)

		# active elements
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)


pygame.init()

pygame.mixer.music.load('graphics/mobster.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()

# setup 
camera_group = CameraGroup()
player = Player((640,320),camera_group)

trees=pygame.sprite.Group()
enemy=pygame.sprite.Group()
ghosts=pygame.sprite.Group()
l_ghosts=pygame.sprite.Group()
coolmap=open('graphics/map.txt')
l_index = -16
c_index = -16
goodmap=[]
for line in coolmap:
	l_index += 16
	line=line.split(',')
	c_index = -16
	lst=[]
	for c in line:
		c_index += 16
		lst.append(c)
		if c=='1':
			trees.add(Tree((c_index,l_index),camera_group))
		elif c=='2':
			enemy.add(Enemy(pygame.math.Vector2(c_index,l_index),camera_group))
	lst.pop(-1)
	goodmap.append(lst)

while lol:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		if pygame.key.get_pressed()[pygame.K_r] and not player.alive():
			for e in camera_group:
				e.kill()
			player = Player((0,0),camera_group)
			coolmap=open('graphics/map.txt')
			l_index = -16
			c_index = -16
			for line in coolmap:
				l_index += 16
				line=line.split(',')
				c_index = -16
				for c in line:
					c_index += 16
					if c=='1':
						trees.add(Tree((c_index,l_index),camera_group))
					elif c=='2':
						enemy.add(Enemy(pygame.math.Vector2(c_index,l_index),camera_group))
	screen.fill('#C10087')

	camera_group.update()
	camera_group.custom_draw(player)

	pygame.display.update()
	clock.tick(70)