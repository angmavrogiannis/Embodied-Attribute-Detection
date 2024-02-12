# Action Module
move_forward()
move_back()
move_left()
move_right()
rotate()

# Perception Module
find()
detect_object()
focus(image_patch)
verify_property(obj, property)

# Example Tasks

# 1. Go to the brown desk
desks = detect_object("desk")
for desk in desks:
	is_brown = verify_property("desk", "brown")
	if is_brown:
		go_to(desk)

# 2. Look at the heaviest object
objects = detect_object(image)
heavy_object = llm.query("Which one of these objects is the heaviest?")
look(heavy_object)

# 3. Tread towards the small door
doors = detect_object("door")
doors.sort(key=lambda door: size)
small_door = doors[0]
go_to(small_door)

# 4. When the light turns on, start heading towards the exit
light_on = verify_property("light", "on")
if light_on:
	objects = detect_object(image)
	exit = llm_query("Which one of these objects could be an exit? {}")
	go_to(exit)

# 5. Head back as long as the light is on
find("light")
while verify_property("light", "on"):
	move_back()

# 6. Proceed to the green landmark slowly, staying between the 2 objects

# 7. Once the door opens, follow whoever comes out

# 8. Visit all the landmarks in front of you

# 9. Go back and forth and stop once you see movement

# 10. Take five steps forward, each time stoping for a second in between