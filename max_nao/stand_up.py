import qi
import sys
import time

robot_ip = '10.42.0.98'

def main(robot_ip, robot_port=9559):
    # Connect to the robot
    try:
        session = qi.Session()
        session.connect("tcp://" + robot_ip + ":" + str(robot_port))
    except RuntimeError as e:
        print("Can't connect to Naoqi at ip \"" + robot_ip + "\" on port " + str(robot_port) +".\n"
              "Please check your script arguments. Error was: ", e)
        sys.exit(1)

    # Access the ALRobotPosture and ALMotion services
    posture_service = session.service("ALRobotPosture")
    motion_service = session.service("ALMotion")

    # Wake up robot
    motion_service.wakeUp()

    # Go to the initial posture
    posture_service.goToPosture("StandInit", 0.5)

    # Walk forward: parameters are (x, y, theta)
    motion_service.moveTo(0.5, 0, 0)

    # Rest after the action is done
    motion_service.rest()

if __name__ == "__main__":
    main(robot_ip)


