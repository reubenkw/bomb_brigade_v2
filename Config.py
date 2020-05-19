class Cfg:
	output_images = False

	tiles_x = 80
	tiles_y = 48

	tile_width = 16
	tile_height = 16

	info_height = 160

	map_width = tiles_x * tile_width
	map_height = tiles_y * tile_height

	win_width = map_width
	win_height = map_height + info_height

	# Resources

	health_max = 5
	health_start = 2
	health_num_deposit = 12

	bombs_max = 5
	bombs_start = 2
	bombs_num_deposit = 25
	bomb_delay = 15
	bomb_spawn_rate = 120

	# Deposit size should be between 0 and 1
	walls_max = 15
	walls_start = 5
	walls_num_deposit = 3
	walls_deposit_size = 0.7

	burning_delay = 50

	border_shrink_delay = 2000
	border_shrink_rate = 50

	fps = 10
