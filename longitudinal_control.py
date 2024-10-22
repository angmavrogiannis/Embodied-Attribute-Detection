from klt.getFeatures import getFeatures
from klt.estimateAllTranslation import estimateAllTranslation
from klt.applyGeometricTransformation import applyGeometricTransformation
import sys
import signal
import time
import robomaster
from robomaster import robot
import numpy as np
import cv2

def normalize_coords(pixel_coord, dimension):
    return 2 * pixel_coord / dimension - 1

class Distance:
    def __init__(self):
        self.distance = None

    def sub_data_handler(self, sub_info):
        distance = sub_info
        self.distance = distance[0]

class PID:
    def __init__(self, kp, ki, kd, dt):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.error_prev = 0
        self.error_sum = 0

    def update(self, error, dt):
        self.dt = dt
        p_term = self.kp * error
        i_term = self.ki * self.error_sum * self.dt
        d_term = self.kd * (error - self.error_prev) / self.dt
        control = p_term + i_term + d_term
        self.error_sum += error
        self.error_prev = error
        return control

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    ep_chassis = ep_robot.chassis

    # Initializing and subscribing to distance sensor
    ep_sensor = ep_robot.sensor
    ir_distance = Distance()
    ep_sensor.sub_distance(freq=5, callback=ir_distance.sub_data_handler)
    time.sleep(0.25)

    finished = False
    curr_time = 0
    prev_time = 0
    longitudinal_controller = PID(0.3, 0.05, 0.3, 0.1)
    longitudinal_threshold = 20

    max_distance = 6000

    # target longitudinal position: 200mm from the object
    target_z_pos = 180

    print("Entering loop")
    try:
        while finished == False:
            curr_time = time.time()
            dt = curr_time - prev_time

            # Get the reading for the current distance to the object from the IR sensor
            cZ = ir_distance.distance

            print("Current distance from object: ", cZ)

            longitudinal_error = cZ - target_z_pos
            norm_longitudinal_error = normalize_coords(cZ, max_distance) - normalize_coords(target_z_pos, max_distance)

            print(f"Longitudinal error in pixels: {longitudinal_error}")
            if longitudinal_error < longitudinal_threshold:
                finished = True
                print("Done, ready to pick up the object!")
            else:
                pid_output_z = longitudinal_controller.update(norm_longitudinal_error, dt)
                print(f"PID Z Output: {pid_output_z}")
                ep_chassis.drive_speed(x=pid_output_z, y=0, z=0, timeout=1)

            prev_time = curr_time
            time.sleep(1)

    except KeyboardInterrupt:
        ep_chassis.drive_speed(x=0, y=0, z=0, timeout=5)

    ep_robot.close()
