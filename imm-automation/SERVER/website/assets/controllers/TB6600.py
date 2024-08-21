import RPi.GPIO as GPIO
from time import sleep


class TB6600:
    def __init__(self, PUL, DIR, ENA, PPR):
        self.PUL = PUL
        self.DIR = DIR
        self.ENA = ENA
        self.DIR_BOOL = True
        self.ENA_BOOL = True

        # Pulse per revolution
        self.PPR = PPR

        GPIO.setup(self.PUL, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)

        self._initialize()

    def _initialize(self):
        """
        Sets the initial direction state to forward and disables motor drive outputs
        """
        GPIO.output(self.DIR, GPIO.HIGH)
        GPIO.output(self.ENA, GPIO.LOW)

    def pulse(self, delay):
        """
        Triggers the pulse input on the stepper driver, one call of this function is one step
        """
        GPIO.output(self.PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(self.PUL, GPIO.LOW)
        sleep(delay)

    def forward(self):
        """
        Sets the DIR pin on the stepper driver to HIGH, forward direction
        """
        GPIO.output(self.DIR, GPIO.HIGH)
        self.DIR_BOOL = True

    def reverse(self):
        """
        Sets the DIR pin on the stepper driver to LOW, reverse direction
        """
        GPIO.output(self.DIR, GPIO.LOW)
        self.DIR_BOOL = False

    def enable(self):
        """
        Sets the ENA pin on the stepper driver HIGH, motor drive outputs on
        """
        print("Trying to enable")
        GPIO.output(self.ENA, GPIO.HIGH)
        self.ENA_BOOL = True

    def disable(self):
        """
        Sets the ENA pin on the stepper driver LOW, motor drive outputs off
        """
        GPIO.output(self.ENA, GPIO.LOW)
        self.ENA_BOOL = False