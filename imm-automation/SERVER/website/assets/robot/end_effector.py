import RPi.GPIO as GPIO
from time import sleep


class EndEffector:
    def __init__(self):
        # Sets the GPIO pin and PWM signal frequency of SERVO 1
        servo1_pin = 12
        pwm1_freq = 50
        GPIO.setmode(GPIO.BCM)  # Set up the mode
        GPIO.setup(servo1_pin, GPIO.OUT)
        self.pwm1 = GPIO.PWM(servo1_pin, pwm1_freq)
        self.current_angle = 0  # Predefine the current angle

    def set_angle(self, angle):
        """
        Set the angle of the servo motor
        """
        dc_0deg = 2.765  # Define the DutyCycle when SERVO 1 at 0 degeree (min value)
        dc_189deg = 12.6  # Define the DutyCycle when SERVO 1 at 189 degree (max value)
        duty_cycle = dc_0deg + (angle / 189.0) * (dc_189deg - dc_0deg)
        self.pwm1.ChangeDutyCycle(duty_cycle)
        sleep(0.5)

    def pick_part_1(self):
        """
        Pick section 1
        """
        self.pwm1.start(self.current_angle)
        self.set_angle(35)  # SERVO 1 rotate to 15 degree position
        sleep(1)  # Waiting for the trigger of ejector pin

    def pick_part_2(self):
        """
        Pick section 2
        """
        self.set_angle(25)  # SERVO 1 rotate to 0 degree position to clamp the sprue
        self.current_angle = 0
        print("part picked")

    def drop_part(self):
        """
        SERVO 1 rotate to 90 degree position to open the gripper and part dropped
        """
        self.set_angle(90)
        self.current_angle = 90
        print("part dropped")

    def cleanup(self):
        self.pwm1.stop()  # Stop the SERVO 1
        GPIO.cleanup(12)  # clean up the GPIO PIN #12
