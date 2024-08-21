from time import sleep


class LinearActuator:
    def __init__(self, length, controller, home_switch, axis):
        self.length = length  # units: mm
        self.pitch = 2  # units: mm
        self.controller = controller
        self.hs = home_switch
        self.homed = False
        self.axis = axis
        self.position = None

    def move(self, distance, velocity, home = False):
        """
        Moves the actuator a set distance at a specified velocity.

        :param distance: Distance to travel in mm
        :param velocity: Velocity to travel at
        """
        # TODO: max velocity

        if distance < 0 and self.controller.DIR_BOOL:
            self.controller.reverse()
        elif distance > 0 and not self.controller.DIR_BOOL:
            self.controller.forward()

        delay = self._velocity_to_delay(velocity)
        steps = self._distance_to_steps(distance)
        self.controller.enable()

        if home:
            for i in range(abs(steps)):
                self.controller.pulse(delay)
        else:
            for i in range(abs(steps)):
                if self.hs.get_state():
                    self.controller.pulse(delay)


        self.controller.disable()

    def _distance_to_steps(self, distance):
        """
        Coverts the length of travel in mm to number of steps needed.

        :param distance: Travel in mm
        :return: Number of steps (pulses) for the stepper motor
        """
        return int(distance*self.controller.PPR/self.pitch)

    def _velocity_to_delay(self, velocity):
        """

        :param velocity: Velocity in mm/s
        :return: Step (pulse) delay to get target velocity
        """
        return 0.001 #  self.pitch/(2*velocity*200)

    def home(self):
        """
        Homes the axis and sets the position to zero
        """
        print(f"homing {0} axis...", self.axis)
        # self.controller.reverse()

        while self.hs.get_state():
            self.controller.pulse(0.001)
            sleep(0.001)

        sleep(1)

        self.controller.reverse()

        self.move(-1, 100, True)
        self.position = 0
