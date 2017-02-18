# This is the character controled by the AI
onready var character = get_parent()
# This are the clocks
onready var short_timer = get_node('short_timer')
onready var long_timer = get_node('long_timer')

# This is the state of the AI
var state = EmptyState.new(self) setget set_state
func set_state(new_state):
	if new_state.name == state.name: return
	state.exit()
	state = new_state
	state.start()

# Parameters of the AI based on the character
var attack_range		#Minimum distance to hit
var spot_range			#Max distance I can see the enemy
var flee_range			#Distance to enemy that makes me feel unsecure
var stop_flee_range		#Distance to enemy that makes me feel secure
var target = null		#Enemy considered
var territory_pos		#Position in the map to watch
var territory_radius
var forget_time			#Time to forget an attack
var last_patrol_point = -1	#Last point visited

# Artificial intelligence "game pad": Inputs to the character 
var move = Vector2(0,0)
var slash = false
var jump = false
var shoot = false


func _ready():
	set_process(true)
	add_to_group('enemies')
	character.faction = 'enemies'
	
	# Adjusting parameters based on character class and weapons
	spot_range = 500
	forget_time = 5
	if character.weapon == 'bow':
		attack_range = 400
		flee_range = 100
		stop_flee_range = 200
	else:
		attack_range = 30
		flee_range = -1
	
	# Setting the main territory
	territory_pos = character.get_pos()
	territory_radius = 300
	
	# Setting the state 
	self.state = WaitState.new(self)
	update_target()
	

func _process(delta):
	# Update states each frame (if needed)
	state.update(delta)
	
	# Send the input to the character
	character.input(move, slash, shoot, jump)


func _on_short_timer_timeout():
	state.on_short_timer_timeout()

func _on_long_timer_timeout():
	update_target()
	state.on_long_timer_timeout()


# Functions to check if transitions are needed
func must_flee(): return target and character.get_pos().distance_to(target.get_pos()) < flee_range
func can_attack(): return target and character.get_pos().distance_to(target.get_pos()) < attack_range
func target_spoted(): return target and character.get_pos().distance_to(target.get_pos()) < spot_range
func can_patrol(): return character.patrol_path
func far_enough(): return target and character.get_pos().distance_to(target.get_pos()) > stop_flee_range
func wants_revenge(): return character.last_attack_received < forget_time
func target_close_to_home(): return target and character.get_pos().distance_to(target.get_pos()) < territory_radius
func far_from_home(): return character.get_pos().distance_to(territory_pos) > territory_radius

# Functions to change states
func wait(): self.state = WaitState.new(self)
func flee(): self.state = FleeState.new(self)
func chase(): self.state = ChaseState.new(self)
func think(): self.state = ThinkState.new(self)
func patrol(): self.state = PatrolState.new(self)
func wander(): self.state = WanderState.new(self)
func combat(): self.state = CombatState.new(self)


# Find the closest tarjet
func update_target():
	var target_dis
	target = null
	for t in get_tree().get_nodes_in_group('allies'):
		if t.life <= 0: continue
		var t_dis = character.get_pos().distance_to(t.get_pos())
		if not target or t_dis < target_dis:
			target = t
			target_dis = t_dis



# FSM CLASSES

# Empty state of the finite state machine, needed only as a template
class EmptyState:
	var ai
	var name = 'empty'
	
	func _init(_ai):
		ai = _ai		
	func start():
		pass
	func update(delta):
		pass
	func exit():
		pass
	func on_short_timer_timeout():
		pass
	func on_long_timer_timeout():
		pass


# FSM CLASSES

# Empty state of the finite state machine, needed only as a template
class WaitState:
	var ai
	var name = 'wait'
	
	func _init(_ai):
		ai = _ai
	
	func start():
		ai.short_timer.set_wait_time(2.0); ai.short_timer.start()
		ai.long_timer.set_wait_time(randf()*8 + 4); ai.long_timer.start()
		ai.slash=false; ai.shoot=false; ai.jump=false

	func update(delta):
		pass
		
	func exit():
		pass
	
	func on_short_timer_timeout():
		# Look randomly
		ai.move = Vector2(randf()-0.5,randf()-0.5).normalized()*0.001

		# If detects the target, go for him	
		if ai.target_spoted():
			if ai.must_flee():
				ai.flee()
			else:
				ai.chase()
	
	func on_long_timer_timeout():
		ai.think()

# Empty state of the finite state machine, needed only as a template
class ThinkState:
	var ai
	var name = 'think'
	
	func _init(_ai):
		ai = _ai
		
	func start():
		ai.short_timer.set_wait_time(1.0); ai.short_timer.start()
		ai.long_timer.set_wait_time(randf()*4 + 1); ai.long_timer.start()

		ai.move = Vector2(0,0)
		ai.slash=false; ai.shoot=false; ai.jump=false
		
	func update(delta):
		pass
		
	func exit():
		pass
		
	func on_short_timer_timeout():
		if ai.must_flee():
			ai.flee()
		elif ai.wants_revenge() or ai.target_close_to_home():
			ai.chase()
		elif ai.can_patrol():
			ai.patrol()
		else:
			ai.wander()
	
	func on_long_timer_timeout():
		pass


# Empty state of the finite state machine, needed only as a template
class FleeState:
	var ai
	var name = 'flee'
	
	func _init(_ai):
		ai = _ai
		
	func start():
		ai.short_timer.set_wait_time(2.0); ai.short_timer.start()
		ai.long_timer.set_wait_time(4); ai.long_timer.start()
		ai.slash=false; ai.shoot=false; ai.jump=false
		fleeing()
		
	func update(delta):
		pass
		
	func exit():
		pass
		
	func on_short_timer_timeout():
		if ai.far_enough():
			ai.think()
		else:
			fleeing()

	func on_long_timer_timeout():
		pass
	
	func fleeing():
		if not ai.target: return
		
		ai.move = (ai.character.get_pos() - ai.target.get_pos()).normalized()
		if ai.move.length() > (ai.stop_flee_range+ai.flee_range)*0.5:
			ai.move *= 0.5


# Empty state of the finite state machine, needed only as a template
class PatrolState:
	var ai
	var name = 'patrol'
	
	func _init(_ai):
		ai = _ai
		
	func start():
		ai.short_timer.set_wait_time(1); ai.short_timer.start()
		ai.long_timer.set_wait_time(5); ai.long_timer.start()
		ai.slash=false; ai.shoot=false; ai.jump=false
		patroling()
		
	func update(delta):
		pass
		
	func exit():
		pass
	
	func patroling():
		# If we don't have a last patrol point, get the closest one
		if ai.last_patrol_point == -1:
			var closest_idx = -1
			var closest_dis = 100000000.0
			for i in range(ai.character.patrol_path.get_curve().get_point_count()):
				var point = ai.character.patrol_path.get_curve().get_point_pos(i)
				var dis = ai.character.get_pos().distance_to(point)
				if closest_idx < 0 or dis < closest_dis:
					closest_idx = i
					closest_dis = dis
			ai.last_patrol_point = closest_idx
		
		# Now start moving to the point. If we reached it, pick up the next one.
		var next_point = ai.character.patrol_path.get_curve().get_point_pos(ai.last_patrol_point)
		var dis = ai.character.get_pos().distance_to(next_point)
		if dis < 50:
			ai.last_patrol_point = (ai.last_patrol_point+1) % ai.character.patrol_path.get_curve().get_point_count()
			next_point = ai.character.patrol_path.get_curve().get_point_pos(ai.last_patrol_point)
		ai.move = (next_point-ai.character.get_pos()).normalized() * 0.4
		
		ai.territory_pos = next_point
		
		
	func on_short_timer_timeout():
		if ai.target_close_to_home() or ai.wants_revenge():
			ai.chase()
		else:
			patroling()
		
	func on_long_timer_timeout():
		ai.wait()


# Empty state of the finite state machine, needed only as a template
class ChaseState:
	var ai
	var name = 'chase'
	
	func _init(_ai):
		ai = _ai
		
	func start():
		print('!!!')
		ai.short_timer.set_wait_time(0.1); ai.short_timer.start()
		ai.long_timer.set_wait_time(3); ai.long_timer.start()
		ai.slash=false; ai.shoot=false; ai.jump=false
		chasing()
		
	func update(delta):
		pass
		
	func exit():
		pass
		
	func on_short_timer_timeout():		
		if ai.can_attack():
			ai.combat()
		else:
			chasing()
		
	func on_long_timer_timeout():
		if not ai.target_close_to_home() and \
		not ai.wants_revenge(): 
			ai.think()
	
	func chasing():
		if not ai.target: return
		
		var dis_to_home = (ai.target.get_pos() - ai.territory_pos).length()
		var target_dir = ai.target.get_pos() - ai.character.get_pos()
		var dis = target_dir.length()
		target_dir = target_dir.normalized()
		
		# Different velocity depending on the distance to territory or revenge desire
		if ai.wants_revenge() or dis_to_home < ai.territory_radius:
			target_dir = target_dir*1.0
		elif dis_to_home < ai.territory_radius*1.5:
			target_dir = target_dir*0.5
		else:
			target_dir = target_dir*0.001
		
		# Move the character
		ai.move = target_dir


# Empty state of the finite state machine, needed only as a template
class WanderState:
	var ai
	var name = 'wander'
	
	func _init(_ai):
		ai = _ai
	
	func start():
		ai.short_timer.set_wait_time(2.0); ai.short_timer.start()
		ai.long_timer.set_wait_time(4.0); ai.long_timer.start()
		ai.slash=false; ai.shoot=false; ai.jump=false
		wandering()

	func update(delta):
		pass
		
	func exit():
		pass	
	
	func on_short_timer_timeout():
		if ai.target_spoted():
			ai.chase()
		else:
			wandering()
	
	func wandering():
		# Look randomly (except if it's far from home)
		if ai.far_from_home():
			ai.move = (ai.territory_pos - ai.character.get_pos()).normalized()
		else:
			ai.move = Vector2(randf()-0.5,randf()-0.5).normalized() * 0.3
	
	func on_long_timer_timeout():
		ai.think()
		
		
# Empty state of the finite state machine, needed only as a template
class CombatState:
	var ai
	var name = 'combat'
	var dodge_difficulty
	
	func _init(_ai):
		ai = _ai
		
	func start():
		if ai.character.weapon == 'bow':
			ai.short_timer.set_wait_time(0.25)
			ai.long_timer.set_wait_time(randf()*2+0.5)
		else:
			ai.short_timer.set_wait_time(0.01)
			ai.long_timer.set_wait_time(randf())
		ai.short_timer.start()
		ai.long_timer.start()
		
		dodge_difficulty = randi() % 10

		combat()
		
	func update(delta):
		pass
		
	func exit():
		pass
	
	func combat():
		# Hit the player		
		ai.move = (ai.target.get_pos() - ai.character.get_pos()).normalized() * 0.001
		if ai.character.weapon == 'bow':
			ai.slash=false; ai.shoot=true; ai.jump=false
		else:
			ai.slash=true; ai.shoot=false; ai.jump=false
		dodge()
	
	func dodge():
		if ai.character.weapon != 'bow' and \
		ai.target and \
		ai.target.state.name == 'slash' and \
		dodge_difficulty < ai.character.dodge_skill:
			ai.move = Vector2(randf()-0.5, randf()-0.5).normalized()
			ai.jump=true
		else:
			ai.jump=false

		
	func on_short_timer_timeout():
		ai.slash=false#; ai.shoot=false
		if not ai.target: return
		ai.move = (ai.target.get_pos() - ai.character.get_pos()).normalized() * 0.001
		dodge()
		

	func on_long_timer_timeout():
		if false:#ai.target and ai.character.weapon=='bow':
			ai.character.ray.set_cast_to(ai.target.get_pos() - ai.character.get_pos())
			ai.character.ray.clear_exceptions()
			ai.character.ray.add_exception(ai.character.get_node('body'))
			ai.character.ray.add_exception(ai.character.get_node('feet'))
			if not ai.character.ray.is_colliding():
				ai.shoot = false
				ai.think()
			else:
				var collider = ai.character.ray.get_collider().get_parent()
				if 'faction' in collider.get_property_list() and collider.faction != ai.character.faction:
					ai.shoot = false
					ai.think()
			
		else:
			ai.think()
