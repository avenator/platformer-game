from os import walk
import pygame
import math
from settings import tile_size, world_map
import heapq
def import_sprite(path):
	surface_list = []
	for _, __, img_file in walk(path):
		for image in img_file:
			full_path = f"{path}/{image}"
			img_surface = pygame.image.load(full_path).convert_alpha()
			surface_list.append(img_surface)
	return surface_list
def find_node(player_x, player_y):
	return player_x // tile_size, (player_y - 25) // tile_size
def heuristic(src_x, src_y, target_x, target_y):
   # Manhattan distance on a square grid
   return abs(src_x - target_x) + abs(src_y - target_y)
def find_path(player_x, player_y, dest_x, dest_y, world_data):
	frontier = []
	y, x = find_node(player_x, player_y)
	dy, dx = find_node(dest_x, dest_y)
	#print(dy, dx)
	x += 1
	dx += 1
	heapq.heappush(frontier, (0, (x, y)))
	came_from = dict()
	cost_so_far = dict()
	came_from[(x, y)] = None
	cost_so_far[(x, y)] = 0

	while len(frontier):
		current = heapq.heappop(frontier)[1]

		if current == (dx, dy):
			break

		for next in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
			corr = (current[0] + next[0], current[1] + next[1])
			if corr[0] > -1 and corr[0] < 10 and corr[1] > -1 and corr[1] < len(world_data[0]) + 1  and world_data[corr[0]][corr[1]] == '.' and not corr in cost_so_far or corr == (dy, dx):
				new_cost = cost_so_far[current] + 1
				if next not in cost_so_far or new_cost < cost_so_far[next]:
					cost_so_far[corr] = new_cost
					priority = new_cost + heuristic(dx, dy, corr[0], corr[1])
					heapq.heappush(frontier, (priority, corr))
					came_from[corr] = current
					#print(corr)
	path = []
	current = (dx, dy - 1)
	commands = []
	if current in came_from:
		while current != None:
			path.append(current)
			current = came_from[current]
		path.reverse()

		for i in range(len(path) - 1):
			ny, nx = path[i + 1][0], path[i + 1][1]
			p_x, p_y = y, x
			if nx == p_x and p_y > ny:
				commands.append('space')
				break
			if nx == p_x and y < ny:
				commands.append('down')
				break
			if p_x < nx and p_y == ny:
				commands.append('right')
				#print(p_y, p_x, ny, nx)
				break
			if p_x > nx and p_y == ny:
				commands.append('left')
				break
	else:
		commands = []
	return commands
