# GLOBAL VARIABLES

# Movement and last direction moved
var look_dir = Vector2(0,1) setget set_look
func set_look(new_look):
	if new_look.length_squared() > 0: look_dir = new_look.normalized()
	
var move_dir = Vector2(0,0) setget set_movement
func set_movement(new_move):
	move_dir = new_move
	self.look_dir = move_dir

# Configurable variables
export(float, 0,300,25) var velocity = 150.0
export(String, 'unarmed', 'knife', 'sword', 'axe', 'bow') var weapon = 'unarmed'
export(String, 'ninja', 'archer', 'bandit') var type = 'ninja'
export(NodePath) var patrol_path_path
var patrol_path
export(float, 0,10, 1) var life = 10.0
export(NodePath) var respawn_point = null
var faction = 'none'

# Which state is active right now
var state = IdleWalkRunState.new(self) setget set_state
func set_state(new_state):
	if new_state.name != state.name:
		state.exit()
		state = new_state
		state.start()

# Instanciable objects
var dart_scene = preload('res://dart/dart.tscn')
var animation_types = {\
	'ninja': preload('res://character/ninja/animation.tscn'), \
	'archer': preload('res://character/archer/animation.tscn'),
	'bandit': preload('res://character/bandit/animation.tscn') }
onready var animation = animation_types[type].instance()

# Local objects
#onready var animation = get_node('animation')
onready var dust_particles = get_node('dust_particles')
onready var blood_particles = get_node('blood_particles')
onready var blood_leak_particles = get_node('blood_leak_particles')
onready var hitbox = {\
	'unarmed': get_node('hitbox/unarmed'), \
	'knife': get_node('hitbox/knife'), \
	'sword': get_node('hitbox/sword'), \
	'axe': get_node('hitbox/axe')}
onready var trail = get_node('trail')
onready var ray = get_node('ray')
onready var sound = get_node('sound')
var sounds = {\
	'aargh': ['aargh0', 'aargh1', 'aargh2', 'aargh3', 'aargh4', 'aargh5', 'aargh6', 'aargh7'], \
	'axe': ['axe0', 'axe1', 'axe2'], \
	'fail': ['fail0', 'fail1', 'fail2', 'fail3'], \
	'hit': ['hit0', 'hit1'], \
	'swing': ['swing0', 'swing1', 'swing2'], \
	'shoot': ['bow_release0']}


# Other state variables
var last_attack_received = 10000000.0
var weapon_damages = {\
	'unarmed': 1, \
	'knife': 3, \
	'sword': 5, \
	'axe': 8, \
	'bow': 0}
onready var hit_damage = weapon_damages[weapon]
var impulse = Vector2(0,0) #Impulse applied to characters when they avoid succesfully an attack
var dodge_skills = {\
	'ninja': 8,
	'archer': 3,
	'bandit': 1}
onready var dodge_skill = dodge_skills[type]

# CLASS FUNCTIONS

# Initial configuration
func _ready():
	# Basic process settings
	set_fixed_process(true)
	set_process(true)

	# Adding animation object
	add_child(animation)
	move_child(animation, 3)
	
	# Adding patrol path (assuming that the path is a child of the character, this loop corrects the frame)
	if patrol_path_path:
		patrol_path = get_node(patrol_path_path)
		for i in range(patrol_path.get_curve().get_point_count()):
			var point = patrol_path.get_curve().get_point_pos(i)
			point += get_pos()
			patrol_path.get_curve().set_point_pos(i, point)
	else:
		patrol_path = false
	
	# Setting particles
	dust_particles.set_emitting(false)
	blood_leak_particles.set_amount(0)
	blood_leak_particles.set_emitting(false)

	# Choosing and setting the initial animation
	var animation_name = get_direction_name() + '_' + weapon
	animation_name = 'idle_' + animation_name
	dust_particles.set_emitting(false)
	animation.play(animation_name)
	animation.set_flip_h(is_looking_left())


# FSM updating
func _process(delta):
	# Updates the state of the FSM
	state.update(delta)
	
	# Reduce the agression mode if not attacked
	last_attack_received = max(0, last_attack_received + delta)
	
	# Updates the life indicator
	if life > 9.5:
		blood_leak_particles.set_emitting(false)
		blood_leak_particles.set_amount(0)
	elif life > 0:
		blood_leak_particles.set_emitting(true)
		blood_leak_particles.set_amount((10-life)/2)	
		life = min(10, life + delta*0.2)
	else:
		self.state = DeathState.new(self)


# Physical updating
func _fixed_process(delta):
	# Perform the physical movement
	var motion = move((move_dir*velocity + impulse)*delta)
	if is_colliding():
		var n = get_collision_normal()
		motion = n.slide(motion)
		move_dir = n.slide(move_dir)
		move(motion)
	
	impulse *= 0.9


# Inputs updating
func input(analog_pad, slash_button, shoot_button, jump_button):
	state.input(analog_pad, slash_button, shoot_button, jump_button)


# Hitboxes
func hitted_by(object):
	
	var hitted = state.hitted_by(object)
	
	if object.faction!=faction and hitted:
		# Character gets irritated
		last_attack_received = -100.0
		# Life reduces
		life = max(0, life - object.hit_damage)
		# Blood splash
		blood_particles.set_param(Particles2D.PARAM_DIRECTION, 140.0+randf()*80.0)
		blood_particles.set_amount(object.hit_damage*20)
		blood_particles.set_emitting(true)
		# Blood sounds
		play_sound('hit')
	else:
		play_sound('swing')
	
	return hitted


# HELPER FUNCTIONS

func is_looking_right():
    return look_dir.x - abs(look_dir.y) >= 0
func is_looking_down():
    return look_dir.y - abs(look_dir.x) >= 0
func is_looking_left():
    return abs(look_dir.y) + look_dir.x <= 0
func is_looking_up():
    return abs(look_dir.x) + look_dir.y <= 0

func get_direction_name():
    if is_looking_down():
        return 'front'
    elif is_looking_up():
        return 'back'
    elif is_looking_right():
        return 'right'
    elif is_looking_left():
        return 'right'
    else:
        return 'front'

func play_sound(type):
	var s = sounds[type][randi() % sounds[type].size()]
	#if not sound.is_voice_active(0): sound.play(s, 0)
	sound.play(s, 0)


# FSM CLASSES

# Empty state of the finite state machine, needed only as a template
class EmptyState:
	var character
	var name
	func _init(_character):
		character = _character
	func start():
		pass
	func update(delta):
		pass
	func exit():
		pass
	func input(analog_pad, slash_button, shoot_button, jump_button):
		pass
	func hitted_by(character):
		pass


# In this state the characters idles, walks and run freely.
class IdleWalkRunState:
	var character
	var name = 'idle_walk_run'
	
	func _init(_character):
		character = _character
	
	func start():
		pass
		
	func exit():
		pass
		
	func update(delta):
		pass
	
	# Moves the character based on some input (player controller or AI).
	func input(analog_pad, slash_button, shoot_button, jump_button):
		var c = self.character
	
		# Updates the movement and where are the character looking
		c.move_dir = analog_pad
		
		# Choosing the animation name
		var animation_name = c.get_direction_name() + '_' + c.weapon
		var vel = c.move_dir.length_squared()
		if vel < 0.001:
			animation_name = 'idle_' + animation_name
			c.dust_particles.set_emitting(false)
		elif vel < 0.4:
			animation_name = 'walking_' + animation_name
			c.dust_particles.set_emitting(true)
		else:
			animation_name = 'running_' + animation_name
			c.dust_particles.set_emitting(true)
		
		# Setting the animation
		c.animation.play(animation_name)
		c.animation.set_flip_h(c.is_looking_left())
		
		# Transitions
		if slash_button:
			c.state = c.SlashState.new(c)
		elif shoot_button: 
			c.state = c.ShootState.new(c)
		elif jump_button: 
			c.state = c.JumpState.new(c)
	
	func hitted_by(char):
		return true


# Shooting state. The only thing that character can do is jumping, or release the button.
class ShootState:
	var character
	var total_time
	var remaining_time
	var name = 'shoot'
	
	func _init(_character):
		character = _character
	
	func start():
		var c = character
		
		# Setting the graphics
		# Choosing the animation name
		var animation_name = 'shoot_' + c.get_direction_name()
		c.animation.play(animation_name)
		c.animation.set_flip_h(c.is_looking_left())
		# Deactivating particles
		c.dust_particles.set_emitting(false)
		
		# Stopping the character
		c.move_dir = Vector2(0,0)
		
		# Variable to charge the shoot
		var anim_name = c.animation.get_animation()
		var frames = c.animation.get_sprite_frames()
		total_time = 0.1 * frames.get_frame_count(anim_name)
		remaining_time = total_time
		
		c.trail.show()
		
	func update(delta):
		remaining_time = max(0, remaining_time - delta)
		character.trail.set_rot((-character.look_dir).angle())
		character.trail.set_scale(Vector2(1,(1-(remaining_time/total_time))*2))
		
	func exit():
		var strength = (1-(remaining_time/total_time))
		if strength > 0.4:
			var dart = character.dart_scene.instance()
			dart.with_fire = character.type == 'archer'
			dart.parent = character
			dart.set_pos(character.get_pos() + character.look_dir*30)
			dart.dir = character.look_dir * strength
			character.get_parent().add_child(dart)
			character.play_sound('shoot')
		character.trail.hide()
		
		
	func input(analog_pad, slash_button, shoot_button, jump_button):
		if jump_button:
			character.move_dir = analog_pad
			character.state = character.JumpState.new(character)
		
		else:			
			if not shoot_button:
				character.state = character.IdleWalkRunState.new(character)
			else:
				var c = character
				c.look_dir = analog_pad
				var frame = c.animation.get_frame()
				c.animation.play('shoot_' + c.get_direction_name())
				c.animation.set_flip_h(c.is_looking_left())
				c.animation.set_frame(frame)

		
	func hitted_by(char):
		return true


# Slashing state. The only thing that character can do is jumping, or wait until animation finish.
class SlashState:
	var character
	var remaining_time
	var attack_time; var attacked
	var name = 'slash'
	
	func _init(_character):
		character = _character
	
	func start():
		var c = character
		
		# Setting the graphics
		# Choosing the animation name
		var animation_name = 'slash_' + c.get_direction_name() + '_' + c.weapon
		c.animation.play(animation_name)
		c.animation.set_flip_h(c.is_looking_left())
		# Deactivating particles
		c.dust_particles.set_emitting(false)

		# Calculates how much time the character will be slashing
		var anim_name = c.animation.get_animation()
		var frames = c.animation.get_sprite_frames()
		remaining_time = 0.1 * frames.get_frame_count(anim_name)
		attack_time = remaining_time * 0.3
		attacked = false
		
		# Stopping the character and setting the position of the hitbox
		c.move_dir = Vector2(0,0)
		var hit_pos = c.look_dir.normalized() * c.hitbox[c.weapon].get_pos().length()
		c.hitbox[c.weapon].set_pos(hit_pos)
				
	func update(delta):
		var c = character
		# Calculates if the hit is done. If it's done, change the state.
		remaining_time -= delta		
		if remaining_time < 0:
			c.state = c.IdleWalkRunState.new(c)
		attack_time -= delta
		
		if not attacked and attack_time < 0:
			var collision_list = c.hitbox[c.weapon].get_overlapping_bodies()
			for o in collision_list:
				if o==c or o extends StaticBody2D: continue
				o.hitted_by(c)
			attacked = true
			
			# Playing sounds
			if c.weapon == 'axe':
				character.play_sound('axe')
			else:
				character.play_sound('swing')

		
	func exit():
		pass
		
	func input(analog_pad, slash_button, shoot_button, jump_button):
		if jump_button:
			character.move_dir = analog_pad
			character.state = character.JumpState.new(character)
	
	func hitted_by(object):
		if object extends KinematicBody2D:
			if object.look_dir.dot(character.look_dir) < 0:
				var dir = (object.get_pos()-character.get_pos()).normalized()
				character.impulse = -dir * object.hit_damage * 40
				object.impulse = dir * character.hit_damage * 40
				character.play_sound('fail')
				object.play_sound('fail')
				return false
		return true


# Jumping state. Character can't do anything else util the jump is ended, but he 
# doesn't take damage meanwhile.
class JumpState:
	var character
	var remaining_time
	var name = 'jump'
	
	func _init(_character):
		character = _character
	
	func start():
		var c = character
		# Setting the graphics
		# Choosing the animation name
		var animation_name = 'jumping_' + c.get_direction_name() + '_' + c.weapon
		c.animation.play(animation_name)
		c.animation.set_flip_h(c.is_looking_left())
		# Activating particles
		c.dust_particles.set_emitting(true)

		# Calculates how much time the character will be jumping
		var anim_name = c.animation.get_animation()
		var frames = c.animation.get_sprite_frames()
		remaining_time = 0.1 * frames.get_frame_count(anim_name)
		
		self.character.move_dir = self.character.look_dir.normalized()
		
	func update(delta):
		# Calculates if the jumping is done. If it's done, change the state, else keep moving.
		remaining_time -= delta		
		if remaining_time < 0:			
			self.character.state = self.character.IdleWalkRunState.new(self.character)
		else:
			self.character.move_dir = self.character.look_dir
		
	func exit():
		pass
	func input(analog_pad, slash_button, shoot_button, jump_button):
		pass
	
	func hitted_by(char):
		return false


# Character dies
class DeathState:
	var character
	var name = 'death'
	var remaining_time
	var total_time
	
	func _init(_character):
		character = _character
	
	func start():
		var c = character

		c.animation.play('death')
		c.dust_particles.set_emitting(false)
		c.blood_leak_particles.set_emitting(false)

		self.character.move_dir = Vector2(0,0)
		
		c.play_sound('aargh')
		total_time = 0.1 * c.animation.get_sprite_frames().get_frame_count('death')
		remaining_time = total_time
		
		if not c.respawn_point:
			c.get_node('feet').queue_free()

		
	func update(delta):
		remaining_time -= delta
		if remaining_time <= 0:
			if not character.respawn_point:
				for c in character.get_children():
					c.queue_free()
			else:
				self.character.state = self.character.IdleWalkRunState.new(self.character)
				character.set_pos(character.get_node(character.respawn_point).get_pos())
				character.life = 10

		
	func exit():
		pass
	func input(analog_pad, slash_button, shoot_button, jump_button):
		pass
	
	func hitted_by(char):
		return false