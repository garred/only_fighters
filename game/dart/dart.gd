var parent
var height = 1.5
var vertical_vel = 4
onready var fire_particles_scene = preload('res://particles/fire.tscn')
var fire_particles
var with_fire
var hit_damage
var faction = 'none'
var alpha = 10.0

var dir = Vector2(0,0) setget set_dir
func set_dir(new_dir):
	dir = new_dir 
	set_rot(dir.angle())

func _init():
	set_fixed_process(true)

func _ready():	
	if with_fire:
		var fire_particles_pos = get_node('fire_position')
		fire_particles = fire_particles_scene.instance()
		fire_particles_pos.add_child(fire_particles)
		fire_particles_pos.set_rot(-dir.angle())
		hit_damage = 8 * dir.length()
	else:
		hit_damage = 4 * dir.length()
	

func _fixed_process(delta):
	set_pos(get_pos() + dir*1000*delta - Vector2(0,vertical_vel*delta*10))
	var col_list = get_overlapping_areas()
	if col_list.size()>0:
		if dir.length_squared()>0: 
			for o in col_list:
				if o.get_name()=='body' and o.get_parent()!=parent:
					if o.get_parent().hitted_by(self):
						dir=Vector2(0,0)
	
	if height>0:
		vertical_vel -= 9.8*delta
		height += vertical_vel*delta
	else:
		vertical_vel = 0
		dir=Vector2(0,0)
		if with_fire:
			fire_particles.set_emitting(false)
			for node in fire_particles.get_children():
				node.set_emitting(false)
	
	alpha -= delta	
	set_opacity(max(0, min(1, alpha)))
				

func _on_Timer_timeout():
	queue_free()
	
