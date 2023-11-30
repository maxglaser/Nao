import qi
import sys
import time

robot_ip = '10.42.0.98'

def main(robot_ip, robot_port=9559):
    # Connect to the robot
    try:
        session = qi.Session()
        session.connect("tcp://" + robot_ip + ":" + str(robot_port))
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + robot_ip + "\" on port " + str(robot_port) +".\n"
              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    # Access the ALTextToSpeech service and make the robot speak
    tts = session.service("ALTextToSpeech")
    tts.say("Hello, I am NAO")

if __name__ == "__main__":
        main(robot_ip)

