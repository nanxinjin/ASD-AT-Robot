import anki_vector
import random 
from anki_vector import lights
import time

from anki_vector.events import Events
from anki_vector.util import degrees

import threading
from anki_vector.user_intent import UserIntent
from anki_vector.util import distance_mm, speed_mmps

import speech_recognition as sr
import subprocess

# def drive_and_lift(robot):


def respond_to_answers():
	r = sr.Recognizer()
	mic = sr.Microphone()
	with mic as source:
		r.adjust_for_ambient_noise(source)
		print('you can say something now')
		audio = r.listen(source)
		transcript = r.recognize_google(audio)

		return transcript		

def red_cube_game(robot):
	print('connecting to the cube')
	while not robot.world.connected_light_cube:
		print('No cube Yet...')
		robot.world.connect_cube()
	print('Connected')

	cube = robot.world.connected_light_cube
	colors = [lights.red_light,
			lights.yellow_light,
			lights.green_light,
			lights.cyan_light,
			lights.blue_light,
			lights.magenta_light]

	while(True):
		show_color(cube, lights.red_light)
		# ask a question
		say_words(robot, "What is the color of this cube?")
		respond = respond_to_answers()
		if 'red' in respond:
			say_words(robot, "good job!")
			break
		else:
			say_words(robot, "Maybe not. Try again!")

	print('going to pick up cube')
	robot.behavior.drive_off_charger()
	robot.world.connect_cube()   
	if robot.world.connected_light_cube:        
		print("Found cube")    
	robot.behavior.pickup_object(robot.world.connected_light_cube)
	show_color(cube, lights.off_light)

def show_color(cube, color):
	cube.set_light_corners(color, color, color, color)
	# time.sleep(0.5)
	# cube.set_light_corners(color, color, color, color)
	# time.sleep(0.5)
	# cube.set_light_corners(color, color, color, color)
	# time.sleep(0.5)
	# cube.set_light_corners(color, color, color, color)
	# time.sleep(0.5)



def set_with_different_lights(cube, colors): # colors is a 1 * 4 list
	#cube.set_light_corners(colors[0], colors[1], colors[2], colors[3])
	cube.set_light_corners(lights.red_light, lights.off_light, lights.off_light, lights.off_light)
	time.sleep(0.5)
	cube.set_light_corners(lights.off_light, lights.yellow_light, lights.off_light, lights.off_light)
	time.sleep(0.5)
	cube.set_light_corners(lights.off_light, lights.off_light, lights.blue_light, lights.off_light)
	time.sleep(0.5)
	cube.set_light_corners(lights.off_light, lights.off_light, lights.off_light, lights.green_light)
	time.sleep(0.5)

def set_with_all_lights(cube, color):
	cube.set_lights(color)
	time.sleep(0.1)
	cube.set_lights(lights.off_light) # make it shrink
	time.sleep(0.1)

def say_words(robot, text):
	robot.behavior.say_text(text)

def connect_cube(robot):
	print('Connecting to a cube')
	while not robot.world.connected_light_cube:
		print('No Cube Yet...')
		robot.world.connect_cube()
	print('Connected')

	cube = robot.world.connected_light_cube
	colors = [ lights.red_light,
				lights.yellow_light,
				lights.green_light,
				lights.cyan_light,
				lights.blue_light,
				lights.magenta_light]

	#for i in range(0, 10):
	#	set_with_different_lights(cube, colors)
	
	say_words(robot, 'What is color of this Cube.')
	for i in range(0, 5):
		set_with_all_lights(cube, lights.red_light)
		cube.set_lights(lights.red_light)
		#say_words(robot, 'this is a red cube.')
	say_words(robot, 'this is a red cube.')

	cube.set_lights_off()
	time.sleep(0.5)

def go_left(robot):
	robot.motors.set_wheel_motors(25,50)

def go_right(robot):
	robot.motors.set_wheel_motors(50,25)

def go_stright(robot):
	robot.motors.set_wheel_motors(25,25)
	unobstructed = robot.proximity.last_sensor_reading.unobstructed
	if not unobstructed:
		robot.behavior.turn_in_place(degrees(90))

def go_back(robot):
	robot.motors.set_wheel_motors(-25,-25)

def stop(robot):
	robot.motors.set_wheel_motors(0,0)

def motor_move(robot):
	robot.behavior.drive_off_charger()

	# set wheel motor 
	# trun left
	# wait for user input
	key = input()
	while(1):
		if key == 'a':
			go_left(robot)
		elif key == 'd':
			go_right(robot)
		elif key == 'w':
			go_stright(robot)
		elif key == 's':
			go_back(robot)
		elif key == 'c':
			stop(robot)
			break

		key = input()


	robot.motors.set_wheel_motors(0,0)
	robot.motors.set_lift_motor(0)
	robot.motors.set_head_motor(0)

def pickupcube(robot):
	robot.world.connect_cube()
	robot.behavior.drive_off_charger()

	if robot.world.connected_light_cube:
		robot.behavior.go_to_object(robot.world.connected_light_cube, distance_mm(100.0))
		robot.behavior.pickup_object(robot.world.connected_light_cube)


		
def main():
	args = anki_vector.util.parse_command_args()
	#print(Events.user_intent)
	#exit(0)
	# with anki_vector.Robot(default_logging=False, show_viewer=True, show_3d_viewer=True, enable_nav_map_feed=True) as robot:
	with anki_vector.Robot(args.serial) as robot:
		# define red cube game
		red_cube_game(robot)

		# move robot
		#motor_move(robot)

		# pick up a cube
		# pickupcube(robot)

if __name__ == "__main__":
	main()
