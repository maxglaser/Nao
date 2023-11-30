import qi
import sys
import pygame

robot_ip = '10.42.0.98'

def init_pygame():
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        raise Exception("No joystick detected")
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick

def main(robot_ip, robot_port=9559):
    # Connect to NAO robot
    session = qi.Session()
    try:
        session.connect("tcp://" + robot_ip + ":" + str(robot_port))
    except RuntimeError as e:
        print("Can't connect to Naoqi at ip %s on port %s. Error: %s" % (robot_ip, robot_port, e))
        sys.exit(1)

    # Initialize services
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Initialize Pygame and joystick
    joystick = init_pygame()

    x_button_pressed_last = False  # For toggling the posture
    is_moving = False  # To track if the robot is currently moving

    try:
        print("Use the joystick to control the robot's movement. Press the X (Blue) button to toggle the robot's posture. Press CTRL+C to quit.")
        while True:
            pygame.event.pump()

            # Read joystick axes for direction
            x_axis = joystick.get_axis(0)  # Left joystick horizontal
            y_axis = -joystick.get_axis(1)  # Left joystick vertical, inverted

            # Threshold to avoid unintentional movement
            if abs(x_axis) < 0.1: x_axis = 0
            if abs(y_axis) < 0.1: y_axis = 0

            # Start or stop moving based on joystick position
            if x_axis != 0 or y_axis != 0:
                if not is_moving:
                    if not motion_service.robotIsWakeUp():
                        motion_service.wakeUp()
                    if posture_service.getPosture() != "StandInit":
                        posture_service.goToPosture("StandInit", 0.5)

                    motion_service.moveTo(y_axis, x_axis, 0, _async=True)
                    is_moving = True
            else:
                if is_moving:
                    motion_service.stopMove()
                    is_moving = False

            # Check for X button press to toggle posture
            x_button = joystick.get_button(0)  # Update this index based on your mapping
            if x_button and not x_button_pressed_last:
                current_posture = posture_service.getPosture()
                if current_posture in ["Sitting", "Crouch"]:
                    posture_service.goToPosture("StandInit", 1.0)
                elif current_posture in ["Stand", "StandInit"]:
                    posture_service.goToPosture("Crouch", 1.0)
            x_button_pressed_last = x_button

    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")
        pygame.quit()
        motion_service.rest()
        session.close()

if __name__ == "__main__":
    main(robot_ip)

