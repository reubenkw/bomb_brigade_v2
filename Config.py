class Cfg:
	tiles_x = 80
	tiles_y = 48

	tile_width = 16
	tile_height = 16

	map_width = tiles_x * tile_width
	map_height = tiles_y * tile_height

	# Resources
	# Deposit size should be between 0 and 1

	health_max = 5
	health_start = 2
	health_num_deposit = 12

	bombs_max = 5
	bombs_start = 2
	bombs_num_deposit = 25
	bomb_delay = 15

	walls_max = 15
	walls_start = 5
	walls_num_deposit = 3
	walls_deposit_size = 0.7

	fps = 10