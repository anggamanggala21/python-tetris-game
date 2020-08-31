import pygame
import random

pygame.font.init()

#GLOBAL VARS
s_width = 600
s_height = 690
play_width = 300
play_height = 550
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - (play_height + 30)

# SHAPE FORMATS
S = [['.....',
	  '.....',
	  '..00.',
	  '.00..',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..00.',
	  '...0.',
	  '.....']]

Z = [['.....',
	  '.....',
	  '.00..',
	  '..00.',
	  '.....'],
	 ['.....',
	  '..0..',
	  '.00..',
	  '.0...',
	  '.....']]

I = [['..0..',
	  '..0..',
	  '..0..',
	  '..0..',
	  '.....'],
	 ['.....',
	  '0000.',
	  '.....',
	  '.....',
	  '.....']]

O = [['.....',
	  '.....',
	  '.00..',
	  '.00..',
	  '.....']]

J = [['.....',
	  '.0...',
	  '.000.',
	  '.....',
	  '.....'],
	 ['.....',
	  '..00.',
	  '..0..',
	  '..0..',
	  '.....'],
	 ['.....',
	  '.....',
	  '.000.',
	  '...0.',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..0..',
	  '.00..',
	  '.....']]

L = [['.....',
	  '...0.',
	  '.000.',
	  '.....',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..0..',
	  '..00.',
	  '.....'],
	 ['.....',
	  '.....',
	  '.000.',
	  '.0...',
	  '.....'],
	 ['.....',
	  '.00..',
	  '..0..',
	  '..0..',
	  '.....']]

T = [['.....',
	  '..0..',
	  '.000.',
	  '.....',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..00.',
	  '..0..',
	  '.....'],
	 ['.....',
	  '.....',
	  '.000.',
	  '..0..',
	  '.....'],
	 ['.....',
	  '..0..',
	  '.00..',
	  '..0..',
	  '.....']]

shapes = [S, Z, I, O, J, L, T]
# index 0-6 present shape

class Piece(object):
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		self.shape = shape
		self.color = [72, 219, 251]
		self.rotation = 0

def create_grid(locked_pos={}):
	grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if (j, i) in locked_pos:
				c = locked_pos[(j,i)]
				grid[i][j] = c
	return grid

def convert_shape_format(shape):
	positions = []
	format = shape.shape[shape.rotation % len(shape.shape)]

	for i, line in enumerate(format):
		row = list(line)
		for j, column in enumerate(row):
			if column == '0':
				positions.append((shape.x + j, shape.y + i))

	for i, pos in enumerate(positions):
		positions[i] = (pos[0] - 2, pos[1] - 4)

	return positions

def valid_space(shape, grid):
	accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
	accepted_pos = [j for sub in accepted_pos for j in sub]

	formatted = convert_shape_format(shape)

	for pos in formatted:
		if pos not in accepted_pos:
			if pos[1] > -1:
				return False
	return True

def check_lost(positions):
	for pos in positions:
		x, y = pos
		if y < 1:
			return True

	return False

def get_shape():	
	return Piece(5, 0, random.choice(shapes))

def draw_grid(surface, grid):		
	sx = top_left_x
	sy = top_left_y

	for i in range(len(grid)):
		pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy + i*block_size))
		for j in range(len(grid[i])):
			pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))

def draw_window(surface, grid):
	surface.fill((0,0,0))

	pygame.font.init()
	font = pygame.font.SysFont('comicsans', 60)
	label = font.render('TETRIS', 1, (255,255,255))
	font = pygame.font.SysFont('comicsans', 20)
	label_created = font.render('Created by Angga Manggala', 1, (255,255,255))

	surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 30))
	surface.blit(label_created, (top_left_x + play_width/2.2 - (label.get_width()/2), 80))

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

	pygame.draw.rect(surface, (55,66,250), (top_left_x, top_left_y, play_width, play_height), 5)	

	draw_grid(surface, grid)
	pygame.display.update()

def main(win):

	locked_positions = {}
	grid = create_grid(locked_positions)

	change_piece = False
	run = True
	current_piece = get_shape()
	next_piece = get_shape()
	clock = pygame.time.Clock()
	fall_time = 0
	fall_speed = 0.27

	while run:
		grid = create_grid(locked_positions)
		fall_time += clock.get_rawtime()
		clock.tick()

		if fall_time/1000 > fall_speed:
			fall_time = 0
			current_piece.y += 1
			if not(valid_space(current_piece, grid)) and current_piece.y > 0:
				current_piece.y -= 1
				change_piece = True

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					current_piece.x -= 1
					if not(valid_space(current_piece, grid)):
						current_piece.x += 1
				if event.key == pygame.K_RIGHT:
					current_piece.x += 1
					if not(valid_space(current_piece, grid)):
						current_piece.x -= 1
				if event.key == pygame.K_DOWN:
					current_piece.y += 1
					if not(valid_space(current_piece, grid)):
						current_piece.y -= 1
				if event.key == pygame.K_UP:
					current_piece.rotation += 1
					if not(valid_space(current_piece, grid)):
						current_piece.rotation -= 1

		shape_pos = convert_shape_format(current_piece)

		for i in range(len(shape_pos)):
			x, y = shape_pos[i]
			if y > -1:
				grid[y][x] = current_piece.color

		if change_piece:
			for pos in shape_pos:
				p = (pos[0], pos[1])
				locked_positions[p] = current_piece.color
			current_piece = next_piece
			next_piece  = get_shape()
			change_piece = False
					
		draw_window(win, grid)

		if check_lost(locked_positions):
			run = False

	pygame.display.quit()

def main_menu(win):
	main(win)
	

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)