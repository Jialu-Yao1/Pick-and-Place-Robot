import RPi.GPIO as GPIO


class LimitSwitch:
    def __init__(self, PIN):
        self.PIN = PIN
        GPIO.setup(self.PIN, GPIO.IN)

    def get_state(self):
        """
        Gets the state of the limit switch
        :return: 1/TRUE if high or 0/FALSE if low
        """
        return GPIO.input(self.PIN)
