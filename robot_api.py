from robomaster import robot
import cv2
import time

class SimpleRobot(robot.Robot):
	def __init__(self, def_speed_xy=0.7, def_speed_z=45):
		super().__init__(self)
		self.def_speed = def_speed
		self.chassis = self.chassis
		self.def_speed_xy = def_speed_xy
		self.def_speed_z = def_speed_z
		self.def_power = 50

	def move_forward(self, x_val, speed=self.def_speed)
		self.chassis.move(x=x_val, y=0, z=0, xy_speed=speed).wait_for_completed()

	def move_backwards(self, x_val, speed=self.def_speed)
		self.chassis.move(x=-x_val, y=0, z=0, xy_speed=speed).wait_for_completed()

	def move_right(self, y_val, speed=self.def_speed)
		self.chassis.move(x=0, y=y_val, z=0, xy_speed=speed).wait_for_completed()

	def move_left(self, y_val, speed=self.def_speed)
		self.chassis.move(x=0, y=-y_val, z=0, xy_speed=speed).wait_for_completed()

	def rotate_counterclockwise(self, z_val, speed=self.def_speed_z)
		self.ep_chassis.move(x=0, y=0, z=z_val, z_speed=self.def_speed_z).wait_for_completed()

	def rotate_clockwise(self, z_val, speed=self.def_speed_z)
		self.ep_chassis.move(x=0, y=0, z=-z_val, z_speed=self.def_speed_z).wait_for_completed()

	def move_arm_forward(self, dx):
		self.arm.move(x=dx, y=0).wait_for_completed()

	def move_arm_backwards(self, dx):
		self.arm.move(x=-dx, y=0).wait_for_completed()

	def move_arm_up(self, dy):
		self.arm.move(x=0, y=dy).wait_for_completed()

	def move_arm_down(self, dy):
		self.arm.move(x=0, y=-dy).wait_for_completed()

	def open_gripper(self, def_power, sec=1):
		self.gripper.open(power=def_power)
		time.sleep(sec)
		self.gripper.pause()

	def close_gripper(self, def_power, sec=1):
		self.gripper.close(power=def_power)
		time.sleep(sec)
		self.gripper.pause()

	def stream_video(self, num_sec=5):
		self.camera.start_video_stream(display=False)
		for i in range(0, num_sec * 30): # 30fps
	        img = self.camera.read_cv2_image()
	        cv2.imshow("Robot", img)
	        cv2.waitKey(1)
	    cv2.destroyAllWindows()
	    ep_camera.stop_video_stream()