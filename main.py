import pygame, sys
from random import randint,randrange
import math
lol=True
global_path='/data/data/com.hmandroid.hmandroid/files/app/'


class Enemy(pygame.sprite.Sprite):
	def __init__(self,pos,tan,group):
		super().__init__(group)
		global lider_list
		self.nocol=1
		self.agr=512
		self.hp=6
		self.mode=randint(0,1)
		self.m_mode=False
		self.pos = pos
		self.count=0
		self.chosen=0
		self.call_cnt=0
		self.um_count=30
		self.l_count=0
		self.cooldown=0
		self.image = pygame.image.load(global_path+'graphics/man.png').convert_alpha()
		self.base_player_image= self.image
		self.hitbox_rect = self.image.get_rect(center = pos)
		self.rect = self.hitbox_rect.copy()
		self.newrect = pygame.Rect(self.rect.left, self.rect.top , 48, 48)
		self.speed = 13
		self.flag=False
		self.view=False
		self.trigger=True
		self.leader=False
		self.tan=math.tan(tan)
		self.angle = math.degrees(self.tan)
		self.collision_point=(0,0)
		lider_list=[]
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle-90)
		self.rect = self.image.get_rect(center = self.hitbox_rect.center)

	def input(self):
		if self.cooldown>1:
			self.cooldown-=1
		elif player:
			lider_list=[]
			for e in enemy:
				if e.leader==True:
					lider_list.append(e)
			self.count+=0
			if math.dist(self.rect.center,player.rect.center)<512:
			
				if self.trigger==True and self.view==True:
					self.check_los()
					self.trigger=False
				else:
					self.um_count+=1
					if self.um_count>10:
						self.um_count=0
						self.check_los()

						if self.leader:
							self.count+=1
							self.l_count+=1

							if self.count>4:
								self.count=0
								l_ghosts.add(GhostLeader(self.pos,self.rect,camera_group))

							if self.l_count>180:
								self.l_count=0
								self.leader=False

					if self.m_mode==True:
						self.move(self.chosen)
					else:
						self.follow()
		self.check_hp()

	def move(self,entity):
		cord = entity.rect.center
		x_change_mouse_player = (cord[0] - self.rect.centerx)
		y_change_mouse_player = (cord[1] - self.rect.centery)
		self.tan=math.atan2(y_change_mouse_player, x_change_mouse_player)
		self.angle = math.degrees(self.tan)
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle-90)
		self.rect = self.image.get_rect(center = self.hitbox_rect.center)

		self.velocity_x=self.speed*math.cos(self.tan)/math.sqrt(2)
		self.velocity_y=self.speed*math.sin(self.tan)/math.sqrt(2)

		self.collision_point=(self.rect.centerx+self.velocity_x,self.rect.centery+self.velocity_y)

		self.collision()
		self.pos += pygame.math.Vector2(self.velocity_x*self.nocol, self.velocity_y*self.nocol)
		if self.mode!=1:
			self.nocol=1
		self.hitbox_rect.center = self.pos
		self.rect.center = self.hitbox_rect.center

	def follow(self):
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle-90)
		self.rect = self.image.get_rect(center = self.hitbox_rect.center)

		self.velocity_x=self.speed*math.cos(self.tan)/math.sqrt(2)
		self.velocity_y=self.speed*math.sin(self.tan)/math.sqrt(2)

		self.collision_point=(self.rect.centerx+self.velocity_x,self.rect.centery+self.velocity_y)

		self.collision()

		self.pos += pygame.math.Vector2(self.velocity_x*self.nocol, self.velocity_y*self.nocol)
		if self.mode!=1:
			self.nocol=1
		self.hitbox_rect.center = self.pos
		self.rect.center = self.hitbox_rect.center

	def check_los(self):
		self.obj=[]
		self.lst_1=[]
		lst_2=[1,1]
		self.fov=[0]
		for ghost in ghosts:
			self.lst_1.append(ghost)
		for ghost in l_ghosts:
			lst_2.append(ghost)
		if len(lider_list) and len(lst_2)>1 and not(self.leader):
			self.obj.append(lider_list[0])
			self.obj.append(lst_2[-1])
			self.obj.append(lst_2[-2])
			self.fov=[-5,0,5]
		if len(self.lst_1)>1:
				self.obj.append(self.lst_1[len(self.lst_1)//2])
				self.obj.append(self.lst_1[len(self.lst_1)//3])
				self.obj.append(self.lst_1[0])
				self.obj.append(self.lst_1[1])
				self.fov=[-5,0,5]
				self.fov=[-5,0,5,20,-20,45,-45,70,-70,95,-95]
		self.fov.append(160)
		self.fov.append(-160)
		self.obj.insert(0,player)

		# for i in np.arange(-50,50,15):
		# 	self.fov.append(i)
		self.m_mode=False
		for e in self.fov:
			tan=self.tan+math.radians(e)
			velocity_x=math.cos(tan)*30
			velocity_y=math.sin(tan)*30
			for i in range(0,int(18)):
				self.collision_point=(int((self.rect.centerx+i*velocity_x)),int((self.rect.centery+i*velocity_y)))
				self.collision_rect=(Dot(self.collision_point,camera_group))
				dots.add(self.collision_rect)
				if pygame.sprite.spritecollideany(self.collision_rect, trees):
					break
			for entity in self.obj:
				if pygame.sprite.spritecollideany(entity, dots):
					self.m_mode=True
					self.chosen=entity
					if self.chosen==player: 
						if self.mode==1:
							self.view=True
							self.nocol=0
							EBullet((self.rect.centerx+velocity_x*1.5,self.rect.centery+velocity_y*1.5),self.tan,camera_group)
						else:
							self.nocol=1
							self.view=True
					
					break
			if self.m_mode==True:
				break
	def collision(self):
		if player.rect.collidepoint(self.collision_point):
			player.kill()
		# for e in enemy:
		# 	if e.rect.colliderect(self.newrect) and e.rect!=self.newrect:
		# 		self.nocol=0.1
		for tree in trees:
			if tree.newrect.collidepoint(self.collision_point):
				self.nocol=0
				self.call_cnt+=1
				if self.call_cnt>100:
					self.call_cnt=0
					self.tan=-self.tan
					self.follow()
					self.check_los()
	
	def check_hp(self):
		if self.hp<1:
			self.kill()
	
	def update(self):
		self.input()

class Bullet(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load(global_path+'graphics/bullet.png').convert_alpha()
		self.base_player_image= self.image
		self.hitbox_rect = self.image.get_rect(center = pos)
		self.rect = self.hitbox_rect.copy()
		self.vector=self.hitbox_rect.center
		self.tan=TabletShoot.global_tan_shoot
		self.speed=15
		self.coll_1=0
		self.coll_2=0
		self.mode=player.mode
		self.rand_bullets()
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)
	def move(self):

		self.velocity_x=self.speed*math.cos(self.tan)
		self.velocity_y=self.speed*math.sin(self.tan)
		self.coll_1=(self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*4)
		self.coll_2=(self.rect.centerx+self.velocity_x*2,self.rect.centery+self.velocity_y*2)
		self.collision()
		self.vector += pygame.math.Vector2(self.velocity_x, self.velocity_y)
		self.hitbox_rect.center = self.vector
		self.rect.center = self.hitbox_rect.center
		
			
	def collision(self):
		for tree in trees:
			if tree.rect.colliderect(self.rect) or tree.rect.collidepoint(self.coll_1):
				self.kill()
		for e in enemy:
			if e.rect.colliderect(self.rect) or tree.rect.collidepoint(self.coll_2):
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

class EBullet(pygame.sprite.Sprite):
	def __init__(self,pos,tan,group):
		super().__init__(group)
		self.image = pygame.image.load(global_path+'graphics/bullet.png').convert_alpha()
		self.base_player_image= self.image
		self.hitbox_rect = self.image.get_rect(center = pos)
		self.rect = self.hitbox_rect.copy()
		self.vector=self.hitbox_rect.center
		self.tan=tan
		self.speed=15
		self.coll_1=0
		self.coll_2=0
		self.mode=player.mode
		self.rand_bullets()
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)
	def move(self):

		self.velocity_x=self.speed*math.cos(self.tan)
		self.velocity_y=self.speed*math.sin(self.tan)
		self.coll_1=(self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*4)
		self.coll_2=(self.rect.centerx+self.velocity_x*2,self.rect.centery+self.velocity_y*2)
		self.collision()
		self.vector += pygame.math.Vector2(self.velocity_x, self.velocity_y)
		self.hitbox_rect.center = self.vector
		self.rect.center = self.hitbox_rect.center
		
			
	def collision(self):
		for tree in trees:
			if tree.rect.colliderect(self.rect) or tree.rect.collidepoint(self.coll_1):
				self.kill()
		if player.rect.colliderect(self.rect):
			player.kill()
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
		self.image = pygame.image.load(global_path+'graphics/tree.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.newrect = pygame.Rect(self.rect.left, self.rect.top , 30, 30)

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.nocol=1
		self.mode='ssg'
		self.pos = pygame.math.Vector2(-100,700)
		self.image = pygame.image.load(global_path+'graphics/player.png').convert_alpha()
		self.base_player_image= self.image
		self.hitbox_rect = self.image.get_rect(center = pos)
		self.rect = self.hitbox_rect.copy()
		self.speed = 15
		self.p_colldown=30
		self.count=0
		self.ghost_cnt=0
		self.tan=0
		self.velocity_x=0
		self.velocity_y=0

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
		if TabletMove.global_move:
			self.tan=TabletMove.global_tan_walk
			self.angle = math.degrees(self.tan)
			self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)
			self.rect = self.image.get_rect(center = self.hitbox_rect.center)


		self.velocity_x=self.speed*math.cos(self.tan)/math.sqrt(2)
		self.velocity_y=self.speed*math.sin(self.tan)/math.sqrt(2)

	def collision(self):
		for tree in trees:
			if tree.newrect.collidepoint(self.coll_1):
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
		self.image = pygame.image.load(global_path+'graphics/ghost.png').convert_alpha()
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
		self.image = pygame.image.load(global_path+'graphics/ghost.png').convert_alpha()
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
		self.image = pygame.image.load(global_path+'graphics/floor.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.life_c=0
	def update(self):
		self.life_c+=1
		if self.life_c>5:
			self.kill()

class TabletMove(pygame.sprite.Sprite):
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.image=pygame.image.load(global_path+'graphics/tablet.png').convert_alpha()
		self.pos=(200,650)
		self.rect = self.image.get_rect(topleft = self.pos)
		TabletMove.global_move=False
		TabletMove.global_tan_walk=0
	def input(self):
		self.mouse_coords = pygame.mouse.get_pos()
		if self.rect.collidepoint(self.mouse_coords):
			TabletMove.global_move=True
			self.x_change_mouse_player = (self.mouse_coords[0] - self.rect.centerx)
			self.y_change_mouse_player = (self.mouse_coords[1] - self.rect.centery)
			TabletMove.global_tan_walk=math.atan2(self.y_change_mouse_player, self.x_change_mouse_player)
			player.coll_1=(player.rect.centerx+player.velocity_x*1.5,player.rect.centery+player.velocity_y*1.5)
			player.collision()

			player.pos += pygame.math.Vector2(player.velocity_x*player.nocol, player.velocity_y*player.nocol)
			player.nocol=1
			player.hitbox_rect.center = player.pos
			player.rect.center = player.hitbox_rect.center
	def update(self):
		self.input()

class TabletShoot(pygame.sprite.Sprite):
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.image=pygame.image.load(global_path+'graphics/tablet.png').convert_alpha()
		self.pos=(700,650)
		self.rect = self.image.get_rect(topleft = self.pos)
		TabletShoot.global_shoot=False
		TabletShoot.global_tan_shoot=0
	def input(self):
		self.mouse_coords = pygame.mouse.get_pos()
		if self.rect.collidepoint(self.mouse_coords):
			TabletShoot.global_shoot=True
			self.x_change_mouse_player = (self.mouse_coords[0] - self.rect.centerx)
			self.y_change_mouse_player = (self.mouse_coords[1] - self.rect.centery)
			TabletShoot.global_tan_shoot=math.atan2(self.y_change_mouse_player, self.x_change_mouse_player)
			if TabletShoot.global_shoot:
				velocity_x=player.speed*math.cos(TabletShoot.global_tan_shoot)/math.sqrt(2)
				velocity_y=player.speed*math.sin(TabletShoot.global_tan_shoot)/math.sqrt(2)
				if player.mode=='sg' and player.count>70:
					player.count=0
					Bullet((player.rect.centerx+velocity_x*4,player.rect.centery+velocity_y*2.5),camera_group)
					Bullet((player.rect.centerx+velocity_x*4,player.rect.centery+velocity_y*2.5),camera_group)
					Bullet((player.rect.centerx+velocity_x*4,player.rect.centery+velocity_y*2.5),camera_group)
					Bullet((player.rect.centerx+velocity_x*4,player.rect.centery+velocity_y*2.5),camera_group)
					Bullet((player.rect.centerx+velocity_x*4,player.rect.centery+velocity_y*2.5),camera_group)
				elif player.mode=='ssg' and player.count>3:
					player.count=0
					Bullet((player.rect.centerx+velocity_x*4,player.rect.centery+velocity_y*2.5),camera_group)
				elif player.mode!='sg' and player.count>15:
					player.count=0
					Bullet((player.rect.centerx+velocity_x*4,player.rect.centery+velocity_y*2.5),camera_group)
	def update(self):
		self.input()

class TabletPunch(pygame.sprite.Sprite):
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.image=pygame.image.load(global_path+'graphics/punch.png').convert_alpha()
		self.pos=(800,500)
		self.rect = self.image.get_rect(topleft = self.pos)
	def input(self):
			if player.p_colldown>=15:
				player.p_colldown=0
				player.coll_1=(player.rect.centerx+player.velocity_x*4,player.rect.centery+player.velocity_y*4)
				player.coll_2=(player.rect.centerx+player.velocity_x*6,player.rect.centery+player.velocity_y*6)
				player.punch_collision()
	def update(self):
		self.input()

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		self.ground_surf = pygame.image.load(global_path+'graphics/ground.png').convert_alpha()
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
		self.display_surface.blit(t_move.image,t_move.pos)
		self.display_surface.blit(t_shoot.image,t_shoot.pos)
		self.display_surface.blit(punch.image,punch.pos)


pygame.init()

pygame.mixer.music.load(global_path+'graphics/mobster.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((1280,960))
clock = pygame.time.Clock()

# setup 
camera_group = CameraGroup()
player = Player((-100,700),camera_group)

trees=pygame.sprite.Group()
enemy=pygame.sprite.Group()
ghosts=pygame.sprite.Group()
dots=pygame.sprite.Group()
l_ghosts=pygame.sprite.Group()
coolmap=open(global_path+'graphics/map.txt')
l_index = -16
c_index = -16
goodmap=[]
for line in coolmap:
	l_index += 16
	line=line.split(global_path+',')
	c_index = -16
	lst=[]
	for c in line:
		c_index += 16
		lst.append(c)
		if c=='1':
			trees.add(Tree((c_index,l_index),camera_group))
		elif c[0]=='2':
			enemy.add(Enemy(pygame.math.Vector2(c_index,l_index),float(c[2:6]),camera_group))
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
			coolmap=open(global_path+'graphics/map.txt')
			l_index = -16
			c_index = -16
			for line in coolmap:
				l_index += 16
				line=line.split(global_path+',')
				c_index = -16
				for c in line:
					c_index += 16
					if c=='1':
						trees.add(Tree((c_index,l_index),camera_group))
					elif c[0]=='2':
						enemy.add(Enemy(pygame.math.Vector2(c_index,l_index),float(c[2:6]),camera_group))
	screen.fill(global_path+'#C10087')
	t_move=TabletMove()
	t_move.update()
	
	t_shoot=TabletShoot()
	t_shoot.update()

	punch=TabletPunch()
	punch.update()

	camera_group.update()
	camera_group.custom_draw(player)

	pygame.display.update()
	clock.tick(70)