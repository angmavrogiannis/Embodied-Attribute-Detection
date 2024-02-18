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
    ep_camera = ep_robot.camera
    ep_sensor = ep_robot.sensor

    # Get the latest 1 frame image display each time, and stay for 1 second
    ep_camera.start_video_stream(display=False)
    curr_frame = ep_camera.read_cv2_image(strategy="newest")
    cv2.imwrite("curr_frame.jpg", curr_frame)
    curr_frame
    with open("bbox.txt", "w") as f:
        detected_bbox_coords = f.read()

    # [xmin, ymin, xmax, ymax]
    detected_bbox_coords = [int(val) for val in curr_bbox.strip('][').split(', ')]
    xmin = detected_bbox_coords[0]
    ymin = detected_bbox_coords[1]
    xmax = detected_bbox_coords[2]
    ymax = detected_bbox_coords[3]
    boxw = xmax - xmin
    boxh = ymax - ymin

    curr_bbox = np.array([[[xmin, ymin],[xmax, ymin],[xmin, ymax],[xmax, ymax]]]).astype(float)
    # curr_bbox = np.array([[[291,187],[405,187],[291,267],[405,267]]]).astype(float)
    # Get features from the initial frame for KLT Tracking
    startXs,startYs = getFeatures(cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY), curr_bbox, use_shi=False)

    finished = False
    curr_time = 0
    prev_time = 0
    lateral_controller = PID(2, 0, 0.1, 0.1)
    longitudinal_controller = PID(0.4, 0, 0.1, 0.1)
    lateral_threshold = 10
    longitudinal_threshold = 10

    height, width, channels = curr_frame.shape
    max_distance = 200

    # target lateral position: centering object patch in image frame
    target_x_pos = int(width / 2)

    # target longitudinal position: 200mm from the object
    target_z_pos = 200

    play_realtime = True
    save_to_file = False

    try:
        while finished == False:
            curr_time = time.time()
            dt = curr_time - prev_time

            prev_frame = curr_frame
            prev_bbox = curr_bbox
            curr_frame = ep_camera.read_cv2_image(strategy="newest")

            # Track object with KLT
            newXs, newYs = estimateAllTranslation(startXs, startYs, prev_frame, curr_frame)
            Xs, Ys, curr_bbox = applyGeometricTransformation(startXs, startYs, newXs, newYs, prev_bbox)
            
            # update coordinates
            startXs = Xs
            startYs = Ys

            # update feature points as required
            n_features_left = np.sum(Xs != -1)
            print('# of Features: %d' % n_features_left)
            if n_features_left < 15:
                print('Generate New Features')
                startXs,startYs = getFeatures(cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY), curr_bbox)

            # Compute the lateral coordinate of the center of the patch
            cX = int(xmin + boxw / 2)

            # Get the reading for the current distance to the object from the IR sensor
            cZ = ep_sensor.ir_distance_sensor_ctrl.get_distance_info(1) # param: port_id

            print("Center of patch x position in image frame: ", cX)
            print("Current distance from object: ", cZ)
            # print("Image center x position: {}".format(target_y_pos))

            lateral_error = cX - target_x_pos
            norm_lateral_error = normalize_coords(cX, width) - normalize_coords(target_x_pos, width)

            longitudinal_error = cZ - target_z_pos
            norm_longitudinal_error = normalize_coords(cZ, max_distance) - normalize_coords(target_z_pos, max_distance)

            print(f"Lateral error in pixels: {lateral_error}")
            print(f"Longitudinal error in pixels: {longitudinal_error}")
            if abs(lateral_error) < lateral_threshold and abs(longitudinal_error) < longitudinal_threshold:
                finished = True
                print("Done, ready to pick up the object!")
            else:
                if abs(lateral_error) >= lateral_threshold:
                    pid_output_x = lateral_controller.update(norm_lateral_error, dt)
                    print(f"PID X Output: {pid_output_x}")
                    ep_chassis.drive_speed(x=0, y=pid_output_x, z=0, timeout=5)
                elif abs(longitudinal_error) >= longitudinal_threshold:
                    pid_output_z = longitudinal_controller.update(norm_longitudinal_error, dt)
                    print(f"PID Z Output: {pid_output_z}")
                    ep_chassis.drive_speed(x=pid_output_z, y=0, z=0, timeout=5)

            prev_time = curr_time

            # draw bounding box and visualize feature point for each object
            frame_draw = curr_frame.copy()
            (xmin, ymin, boxw, boxh) = cv2.boundingRect(curr_bbox[:, :].astype(int))
            frame_draw = cv2.rectangle(frame_draw, (xmin, ymin), (xmin + boxw, ymin + boxh), (255,0,0), 2)
            for k in range(startXs.shape[0]):
                frame_draw = cv2.circle(frames_draw, (int(startXs[k]), int(startYs[k])), 3, (0, 0, 255), thickness=2)
            
            # imshow if to play the result in real time
            if play_realtime:
                cv2.imshow("Robot", frame_draw)
            if save_to_file:
                out.write(frame_draw)

            cv2.waitKey(1)
            time.sleep(1)

    except KeyboardInterrupt:
        ep_chassis.drive_speed(x=0, y=0, z=0, timeout=5)

    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()

    ep_robot.close()