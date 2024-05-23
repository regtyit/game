import heapq

def a_star(start, goal, grid):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < len(grid):
                if 0 <= neighbor[1] < len(grid[0]):
                    if grid[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return []

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

    if not self.m_mode:
        start = (self.rect.centerx // 16, self.rect.centery // 16)
        goal = (player.rect.centerx // 16, player.rect.centery // 16)
        grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

        for tree in trees:
            grid[tree.rect.y // 16][tree.rect.x // 16] = 1

        path = a_star(start, goal, grid)

        if path:
            next_step = path[1]  # The first step is the current position
            self.rect.centerx = next_step[0] * 16
            self.rect.centery = next_step[1] * 16

class Enemy(pygame.sprite.Sprite):
    def __init__(self, ...):
        # Initialization code
        pass

    def update(self):
        self.check_los()
        if pygame.sprite.spritecollideany(self, trees):
            self.follow_path_to_player()

    def follow_path_to_player(self):
        start = (self.rect.centerx // 16, self.rect.centery // 16)
        goal = (player.rect.centerx // 16, player.rect.centery // 16)
        grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

        for tree in trees:
            grid[tree.rect.y // 16][tree.rect.x // 16] = 1

        path = a_star(start, goal, grid)

        if path:
            next_step = path[1]  # The first step is the current position
            self.rect.centerx = next_step[0] * 16
            self.rect.centery = next_step[1] * 16
























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