import curses
import time
from servor import servo_Class

class CarController:
    def __init__(self):
        self.servo = servo_Class(Channel=0, ZeroOffset=0)
        self.speed = 20
        self.steering_angle = 0
        self.is_moving = False

    def move_forward(self):
        # Set motor speed for forward movement
        self.servo.SetPos(int(self.speed))
        self.is_moving = True

    def stop(self):
        # Stop the car
        self.servo.SetPos(375)  # Assuming 0.5 corresponds to the neutral position
        self.is_moving = False

    def turn_off_motor(self):
        # Turn off the motor completely
        self.servo.MotorCleanup()
        self.is_moving = False

    def move_left(self):
        # Turn the car left
        self.steering_angle = max(-30, self.steering_angle - 5)
        self.servo.SetPos(375 + self.steering_angle)

    def move_right(self):
        # Turn the car right
        self.steering_angle = max(-30, self.steering_angle + 10)
        self.servo.SetPos(375 + self.steering_angle)

def main(stdscr):
    # Initialize car controller
    car = CarController()

    # Set up the screen
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(100)  # 100ms timeout
    stdscr.addstr(0, 0, "Use 'W' to move forward, 'S' to stop, 'A' to move left, 'D' to move right, 'X' to turn off the motor. Press 'Q' to quit.")

    while True:
        # Get user input
        key = stdscr.getch()
        if key == ord('w'):
            car.move_forward()
        elif key == ord('s'):
            car.stop()
        elif key == ord('a'):
            car.move_left()
        elif key == ord('d'):
            car.move_right()
        elif key == ord('x'):
            car.turn_off_motor()
        elif key == ord('q'):
            break

        # Clear screen and display car status
        stdscr.clear()
        stdscr.addstr(0, 0, f"Moving: {'Yes' if car.is_moving else 'No'}")
        stdscr.addstr(1, 0, f"Speed: {car.speed}")
        stdscr.addstr(2, 0, f"Steering Angle: {car.steering_angle}")
        stdscr.refresh()

        # Pause for a short while to control the refresh rate
        time.sleep(0.1)

# Run the curses application
curses.wrapper(main)
