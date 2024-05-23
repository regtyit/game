import pygame, sys, os
import heapq
from random import randint,randrange
path =os.path.dirname(os.path.abspath(__file__))
import math
game_over=False

# def a_star(start, goal, grid):
#     def heuristic(a, b):
#         return abs(a[0] - b[0]) + abs(a[1] - b[1])

#     neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
#     close_set = set()
#     came_from = {}
#     gscore = {start: 0}
#     fscore = {start: heuristic(start, goal)}
#     oheap = []

#     heapq.heappush(oheap, (fscore[start], start))

#     while oheap:
#         current = heapq.heappop(oheap)[1]

#         if current == goal:
#             data = []
#             while current in came_from:
#                 data.append(current)
#                 current = came_from[current]
#             return data[::-1]

#         close_set.add(current)
#         for i, j in neighbors:
#             neighbor = current[0] + i, current[1] + j
#             tentative_g_score = gscore[current] + heuristic(current, neighbor)
#             if 0 <= neighbor[0] < len(grid):
#                 if 0 <= neighbor[1] < len(grid[0]):
#                     if grid[neighbor[0]][neighbor[1]] == 1:
#                         continue
#                 else:
#                     continue
#             else:
#                 continue

#             if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
#                 continue

#             if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
#                 came_from[neighbor] = current
#                 gscore[neighbor] = tentative_g_score
#                 fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
#                 heapq.heappush(oheap, (fscore[neighbor], neighbor))

#     return []


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
		self.image_sprite = [pygame.image.load(path+'/graphics/enemy.png').convert_alpha(),
                pygame.image.load(path+'/graphics/enemy2.png').convert_alpha()]
		self.index=0
		self.image = self.image_sprite[self.index]
		self.base_player_image= self.image
		self.hitbox_rect = self.image.get_rect(center = pos)
		self.rect = self.hitbox_rect.copy()
		self.speed = 13
		self.flag=False
		self.view=False
		self.trigger=True
		self.leader=False
		self.tan=math.tan(tan)
		self.angle = math.degrees(self.tan)
		self.collision_point=(0,0)
		lider_list=[]
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)
		self.rect = self.image.get_rect(center = self.hitbox_rect.center)
		self.anim_cnt=0

	def input(self):
		if self.cooldown>1:
			self.cooldown-=1
		elif player:
			lider_list=[]
			for e in enemy:
				if e.leader==True:
					lider_list.append(e)
			self.count+=0
			if math.dist(self.rect.center,player.rect.center)<self.agr:
			
				if self.trigger==True and self.view==True:
					self.check_los()
					self.trigger=False
					self.agr=700
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

					if self.m_mode:
						self.move(self.chosen)
					else:
						self.follow()
		self.check_hp()
	def move(self,entity):
		self.anim_cnt+=1
		if self.anim_cnt>10:
			self.anim_cnt=0
			self.index=1-self.index
			self.base_player_image= self.image_sprite[self.index]
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90) 
		cord = entity.rect.center
		x_change_mouse_player = (cord[0] - self.rect.centerx)
		y_change_mouse_player = (cord[1] - self.rect.centery)
		self.tan=math.atan2(y_change_mouse_player, x_change_mouse_player)
		self.angle = math.degrees(self.tan)
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)
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
		self.anim_cnt+=1
		if self.anim_cnt>10:
			self.anim_cnt=0
			self.index=1-self.index
			self.base_player_image= self.image_sprite[self.index]
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)

		self.rect = self.image.get_rect(center = self.hitbox_rect.center)

		self.velocity_x=self.speed*math.cos(self.tan)/math.sqrt(2)
		self.velocity_y=self.speed*math.sin(self.tan)/math.sqrt(2)

		self.collision_point=(self.rect.centerx+self.velocity_x,self.rect.centery+self.velocity_y)

		self.collision()

		self.pos += pygame.math.Vector2(self.velocity_x*self.nocol, self.velocity_y*self.nocol)
		self.nocol=1
		self.hitbox_rect.center = self.pos
		self.rect.center = self.hitbox_rect.center
	# def check_los(self):
	# 	self.obj=[]
	# 	self.lst_1=[]
	# 	lst_2=[1,1]
	# 	self.fov=[0]
	# 	for ghost in ghosts:
	# 		self.lst_1.append(ghost)
	# 	for ghost in l_ghosts:
	# 		lst_2.append(ghost)
	# 	if len(lider_list) and len(lst_2)>1 and not(self.leader):
	# 		self.obj.append(lider_list[0])
	# 		self.obj.append(lst_2[-1])
	# 		self.obj.append(lst_2[-2])
	# 		self.fov=[-5,0,5]
	# 	if len(self.lst_1)>1:
	# 			self.obj.append(self.lst_1[len(self.lst_1)//2])
	# 			self.obj.append(self.lst_1[len(self.lst_1)//3])
	# 			self.obj.append(self.lst_1[0])
	# 			self.obj.append(self.lst_1[1])
	# 			self.fov=[-5,0,5]
	# 			self.fov=[-5,0,5,20,-20,45,-45,70,-70,95,-95]
	# 	self.fov.append(160)
	# 	self.fov.append(-160)
	# 	self.obj.insert(0,player)

	# 	self.m_mode=False
	# 	for e in self.fov:
	# 		tan=self.tan+math.radians(e)
	# 		velocity_x=math.cos(tan)*30
	# 		velocity_y=math.sin(tan)*30
	# 		for i in range(0,int(18)):
	# 			self.collision_point=(int((self.rect.centerx+i*velocity_x)),int((self.rect.centery+i*velocity_y)))
	# 			self.collision_rect=(Dot(self.collision_point,camera_group))
	# 			dots.add(self.collision_rect)
	# 			if pygame.sprite.spritecollideany(self.collision_rect, trees):
	# 				break
	# 		for entity in self.obj:
	# 			if pygame.sprite.spritecollideany(entity, dots):
	# 				self.m_mode=True
	# 				self.chosen=entity
	# 				if self.chosen==player: 
	# 					if self.mode==1:
	# 						self.nocol=0.5
	# 						self.view=True
	# 						EBullet((self.rect.centerx,self.rect.centery),self.tan,camera_group)
	# 						sound2.play()
	# 					else:
	# 						self.nocol=1
	# 						self.view=True
					
	# 				break
	# 		if self.m_mode==True:
	# 			break

	def check_los(self):
		self.obj = []
		self.lst_1 = list(ghosts)
		lst_2 = [1, 1] + list(l_ghosts)
		self.fov = [0, -5, 0, 5, 20, -20, 45, -45, 70, -70, 95, -95, 160, -160]

		if lider_list and len(lst_2) > 3 and not self.leader:
			self.obj.extend([lider_list[0], lst_2[-1], lst_2[-2]])

		if len(self.lst_1) > 1:
			self.obj.extend([
				self.lst_1[len(self.lst_1) // 2],
				self.lst_1[len(self.lst_1) // 3],
				self.lst_1[0],
				self.lst_1[1]
			])

		self.obj.insert(0, player)
		self.m_mode = False

		for e in self.fov:
			tan = self.tan + math.radians(e)
			velocity_x = math.cos(tan) * 30
			velocity_y = math.sin(tan) * 30

			for i in range(18):
				self.collision_point = (
					int(self.rect.centerx + i * velocity_x),
					int(self.rect.centery + i * velocity_y)
				)
				self.collision_rect = Dot(self.collision_point, camera_group)
				dots.add(self.collision_rect)

				if pygame.sprite.spritecollideany(self.collision_rect, trees):
					break

			for entity in self.obj:
				if pygame.sprite.spritecollideany(entity, dots):
					self.m_mode = True
					self.chosen = entity
					self.nocol = 0.5 if self.mode == 1 else 1
					self.view = True

					if self.chosen == player and self.mode == 1:
						EBullet((self.rect.centerx, self.rect.centery), self.tan, camera_group)
						sound2.play()

					break

			if self.m_mode:
				break

		# if not self.m_mode:
		# 	start = (self.rect.centerx // 16, self.rect.centery // 16)
		# 	goal = (player.rect.centerx // 16, player.rect.centery // 16)
		# 	grid = [[0 for _ in range(64)] for _ in range(64)]

		# 	for tree in trees:
		# 		grid[tree.rect.y // 16][tree.rect.x // 16] = 1

		# 	path = a_star(start, goal, grid)

		# 	if path:
		# 		next_step = path[1]  # The first step is the current position
		# 		self.rect.centerx = next_step[0] * 16
		# 		self.rect.centery = next_step[1] * 16


	def collision(self):
		if player.rect.collidepoint(self.collision_point):
			player.kill()
			# for e in enemy:
			# 	if e.rect.colliderect(self.newrect) and e.rect!=self.newrect:
			# 		self.nocol=0.1
		for tree in trees:
			if tree.rect.collidepoint(self.collision_point):
				self.nocol=0
				self.call_cnt+=1

	def check_hp(self):
		if self.hp<1:
			self.kill()
		
	def update(self):
		self.input()

class Bullet(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load(path+'/graphics/bullet.png').convert_alpha()
		self.base_player_image= self.image
		self.hitbox_rect = self.image.get_rect(center = pos)
		self.rect = self.hitbox_rect.copy()
		self.vector=self.hitbox_rect.center
		self.tan=player.tan
		self.speed=15
		self.coll_1=0
		self.coll_2=0
		self.mode=player.mode
		self.rand_bullets()
		self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)
	def move(self):

		self.velocity_x=self.speed*math.cos(self.tan)
		self.velocity_y=self.speed*math.sin(self.tan)
		self.coll_1=(self.rect.centerx+self.velocity_x*2,self.rect.centery+self.velocity_y*2)
		self.collision()
		self.vector += pygame.math.Vector2(self.velocity_x, self.velocity_y)
		self.hitbox_rect.center = self.vector
		self.rect.center = self.hitbox_rect.center
		
			
	def collision(self):
		for tree in trees:
			if tree.rect.colliderect(self.rect) or tree.rect.collidepoint(self.coll_1):
				self.kill()
		for e in enemy:
			if e.rect.colliderect(self.rect):
				self.kill()
				e.hp-=4
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
		self.image = pygame.image.load(path+'/graphics/bullet.png').convert_alpha()
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
		self.coll_1=(self.rect.centerx+self.velocity_x*2,self.rect.centery+self.velocity_y*2)
		self.collision()
		self.vector += pygame.math.Vector2(self.velocity_x, self.velocity_y)
		self.hitbox_rect.center = self.vector
		self.rect.center = self.hitbox_rect.center

	def easy_collision(self):
		for tree in trees:
			if tree.rect.colliderect(self.rect) or tree.rect.colliderect(self.hitbox_rect):
				self.kill()
		
			
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
		# self.easy_collision()
		self.move()
		
class Tree(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load(path+'/graphics/tree.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		# self.rect.w=self.rect.w-8
		# self.rect.h=self.rect.h-8
		self.rect = pygame.Rect(self.rect.left, self.rect.top , 30, 30)

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.nocol=1
		self.mode='sg'
		self.pos = pygame.math.Vector2(1740,520)
		self.image_sprite = [pygame.image.load(path+'/graphics/player.png').convert_alpha(),
                pygame.image.load(path+'/graphics/player2.png').convert_alpha()]
		self.punch_sprite = [pygame.image.load(path+'/graphics/punch1.png').convert_alpha(),
                pygame.image.load(path+'/graphics/punch2.png').convert_alpha(),
				pygame.image.load(path+'/graphics/punch3.png').convert_alpha()]
		self.index=0
		self.mask='ton'
		self.image = self.image_sprite[self.index]
		self.base_player_image= self.image_sprite[self.index]
		self.hitbox_rect = self.image.get_rect(center = pos)
		self.rect = self.hitbox_rect.copy()
		self.speed = 7
		self.p_colldown=30
		self.count=0
		self.ghost_cnt=0
		self.forward=False
		self.back=False
		self.right=False
		self.left=False
		self.anim_cnt=0
		self.punch_anim=False

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
		self.rect = self.image.get_rect(center = self.hitbox_rect.center)

		self.velocity_x=self.speed*math.cos(self.tan)/math.sqrt(2)
		self.velocity_y=self.speed*math.sin(self.tan)/math.sqrt(2)

		if self.punch_anim:
			self.anim_cnt+=1
			if self.anim_cnt>5:
				self.anim_cnt=0
				self.index+=1
				if self.index>2:
					self.punch_anim=False
					self.index=0
				else:
					self.base_player_image= self.punch_sprite[self.index]
					self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.forward=True
		else:
			self.forward=False

		if keys[pygame.K_s]:
			self.back=True
		else:
			self.back=False

		if keys[pygame.K_d]:
			self.right=True
		else:
			self.right=False

		if keys[pygame.K_a]:
			self.left=True
		else:
			self.left=False

		if self.left or self.right or self.forward or self.back:
			self.anim_cnt+=1
			if self.anim_cnt>10 and not(self.punch_anim):
				self.anim_cnt=0
				self.index=1-self.index
				self.base_player_image= self.image_sprite[self.index]
			self.image = pygame.transform.rotate(self.base_player_image, -self.angle+90)
			vec=pygame.math.Vector2(self.right-self.left,self.back-self.forward)*self.speed*2**(0.5)
			self.coll_1=(self.rect.centerx+vec.x,self.rect.centery+vec.y)
			self.collision()
			self.pos+=vec*self.nocol
			self.nocol=1
			self.hitbox_rect.center = self.pos
			self.rect.center = self.hitbox_rect.center

		if keys[pygame.K_f] and not(self.mask=='tony'):
			if self.p_colldown>=15:
				self.p_colldown=0
				self.coll_1=(self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*4)
				self.coll_2=(self.rect.centerx+self.velocity_x*6,self.rect.centery+self.velocity_y*6)
				self.punch_collision()
				sound1.play()

		if pygame.mouse.get_pressed()[0] and not(self.mask=='tony'):
			if self.mode=='sg' and self.count>35:
				self.count=0
				sound2.play()
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				sound2.play()
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				sound2.play()
			elif self.mode=='ssg' and self.count>3:
				self.count=0
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				sound2.play()
			elif self.mode!='sg' and self.count>15:
				self.count=0
				Bullet((self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*2.5),camera_group)
				sound2.play()
		elif pygame.mouse.get_pressed()[0] and self.mask=='tony':
				if self.p_colldown>=5:
					self.p_colldown=0
					self.coll_1=(self.rect.centerx+self.velocity_x*4,self.rect.centery+self.velocity_y*4)
					self.coll_2=(self.rect.centerx+self.velocity_x*8,self.rect.centery+self.velocity_y*8)
					self.coll_3=(self.rect.centerx+self.velocity_x*12,self.rect.centery+self.velocity_y*12)
					self.dot_1 = Dot(self.coll_1,camera_group)
					self.dot_2 = Dot(self.coll_2,camera_group)
					self.dot_3 = Dot(self.coll_3,camera_group)
					self.punch_collision()
					sound1.play()
		# if pygame.mouse.get_pressed()[1]:
		# 	self.coll_1=(self.rect.centerx+self.velocity_x*1.5,self.rect.centery+self.velocity_y*1.5)
		# 	self.collision()

		# 	self.pos += pygame.math.Vector2(self.velocity_x*self.nocol, self.velocity_y*self.nocol)
		# 	self.nocol=1
		# 	self.hitbox_rect.center = self.pos
		# 	self.rect.center = self.hitbox_rect.center

	def collision(self):
		for tree in trees:
			if tree.rect.collidepoint(self.coll_1):
				self.nocol=0
	def punch_collision(self):
		self.punch_anim=True
		for e in enemy:
			if self.mask=='tony':
				if e.rect.colliderect(self.dot_1) or e.rect.colliderect(self.dot_2) or e.rect.colliderect(self.dot_3):
					e.hp-=10
					e.cooldown=10
			else:
				if e.rect.collidepoint(self.coll_1) or e.rect.collidepoint(self.coll_2):
					e.hp-=1
					e.cooldown=40

	def update(self):
		self.input()

class GhostPlayer(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.pos = pos
		self.image = pygame.image.load(path+'/graphics/ghost.png').convert_alpha()
		self.rect = player.rect
		self.life_c=0
		self.leader=False
	def update(self):
		self.life_c+=1
		if self.life_c>70:
			self.kill()
class GhostLeader(pygame.sprite.Sprite):
	def __init__(self,pos,rect,group):
		super().__init__(group)
		self.pos = pos
		self.image = pygame.image.load(path+'/graphics/ghost.png').convert_alpha()
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
		self.image = pygame.image.load(path+'/graphics/floor.png').convert_alpha()
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

		self.ground_surf = pygame.image.load(path+'/graphics/ground.png').convert_alpha()
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

	def center_target_camera(self,target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h

	def custom_draw(self,player):
		
		self.center_target_camera(player)

		# ground i
		ground_offset = self.ground_rect.topleft - self.offset
		self.display_surface.blit(self.ground_surf,ground_offset)

		# active elements
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)


pygame.init()

pygame.mixer.music.load(path+'/graphics/mobster.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
sound1 = pygame.mixer.Sound(path+'/graphics/punch.mp3')
sound1.set_volume(0.4)
sound2 = pygame.mixer.Sound(path+'/graphics/gun.mp3')
sound2.set_volume(0.3)

screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()

# setup 
camera_group = CameraGroup()
player = Player((1740,520),camera_group)

trees=pygame.sprite.Group()
enemy=pygame.sprite.Group()
ghosts=pygame.sprite.Group()
l_ghosts=pygame.sprite.Group()
dots=pygame.sprite.Group()
coolmap=open(path+'/graphics/map.txt')
l_index = -16
c_index = -16
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

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
		elif c[0]=='2':
			enemy.add(Enemy(pygame.math.Vector2(c_index,l_index),float(c[2:6]),camera_group))
	lst.pop(-1)
	goodmap.append(lst)

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		if pygame.key.get_pressed()[pygame.K_r] and not player.alive():
			game_over=False
			player = Player((0,0),camera_group)
			coolmap=open(path+'/graphics/map.txt')
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
					elif c[0]=='2':
						enemy.add(Enemy(pygame.math.Vector2(c_index,l_index),float(c[2:6]),camera_group))
			camera_group.ground_surf = pygame.image.load(path+'/graphics/ground.png').convert_alpha()
			camera_group.ground_rect = camera_group.ground_surf.get_rect(topleft = (0,0))

	if not player.alive():
			game_over=True
			for e in camera_group:
				e.kill()
			# remove ground_rect adn ground_image
			camera_group.ground_rect = pygame.Rect(0,0,0,0)
			camera_group.ground_surf = pygame.image.load(path+'/graphics/floor.png').convert_alpha()
			display_surface = pygame.display.get_surface()

			bg = pygame.image.load(path+'/graphics/gameover.png')
			screen.blit(bg,(0,0))
	else:
		screen.fill('#C10087')

	camera_group.update()
	camera_group.custom_draw(player)

	pygame.display.update()
	clock.tick(60)

