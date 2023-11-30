import pygame

def main():
    pygame.init()
    pygame.joystick.init()

    # Check for joysticks
    if pygame.joystick.get_count() == 0:
        print("No joystick detected")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        print("Press buttons or move the joystick to see their mapping. Press CTRL+C to quit.")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Button {} pressed".format(event.button))
                elif event.type == pygame.JOYBUTTONUP:
                    print("Button {} released".format(event.button))
                elif event.type == pygame.JOYAXISMOTION:
                    print("Joystick Axis {} moved to {}".format(event.axis, event.value))
                elif event.type == pygame.JOYHATMOTION:
                    print("Hat {} moved to {}".format(event.hat, event.value))

    except KeyboardInterrupt:
        print("Exiting program.")
        pygame.quit()

if __name__ == "__main__":
    main()

