var height = OS.get_screen_size()[1]+50
var vel = Vector2(5+5*randf(), 50)

func _ready():
	set_process(true)

func _process(delta):
	set_pos(get_pos() + vel*delta)
	vel.x = vel.x * (1 - 0.1*delta)