export(NodePath) var character_path
var character

var movementVel = Vector2(0,0)
var slash_button = false
var shoot_button = false
var jump_button = false
var slash_button_released = true
var shoot_button_released = true
var jump_button_released = true

onready var fps_label = get_node('fps_label')


func _ready():
	if character_path!=null: 
		character = get_node(character_path)
		character.add_to_group('allies')
		character.faction = 'allies'
	
	# We only show the touchpad if we are in smartphones.
	if not (OS.get_name() in ['Android', 'iOS']):
		get_node('left_pad').hide()
		get_node('right_pad').hide()

	set_process(true)


func analog_force_change(inForce):
	movementVel = Vector2(inForce.x, -inForce.y);


func _process(delta):
	
	# Depending of the platform used, we allow one set of controls or other
	if not (OS.get_name() in ['Android', 'iOS']):
		# Considering the keyboard inputs
		if Input.is_action_pressed('jump'): jump_button = true
		if Input.is_action_pressed('shoot'): shoot_button = true
		if Input.is_action_pressed('slash'): slash_button = true	
		var vel_factor = 1 - (not Input.is_action_pressed('ui_select'))*0.5
		var destination = Vector2(0,0)
		destination.y = (Input.is_action_pressed('ui_down') - Input.is_action_pressed('ui_up'))*vel_factor
		destination.x = (Input.is_action_pressed('ui_right') - Input.is_action_pressed('ui_left'))*vel_factor
		if Input.is_action_pressed('shoot'):
			movementVel = movementVel*0.99 + destination*0.01
		else:
			movementVel = movementVel*0.9 + destination*0.1
		if movementVel.length_squared() > 1: movementVel = movementVel.normalized()
			
		#movementVel *= 0.9

	# Applying movement
	if character: character.input(movementVel, slash_button, shoot_button, jump_button)
	slash_button = false
	jump_button = false
	
	# Letting shoot button to be pressed for a while
	if Input.is_action_pressed('shoot'): shoot_button = false
	
	# Writing fps
	fps_label.set_text(str(OS.get_frames_per_second()))
	
	
func _on_slash_pressed(): slash_button = true

func _on_shoot_pressed(): shoot_button = true
func _on_shoot_released(): shoot_button = false

func _on_jump_pressed(): jump_button = true
