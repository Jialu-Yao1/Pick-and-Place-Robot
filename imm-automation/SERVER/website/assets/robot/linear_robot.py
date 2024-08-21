from time import sleep

class LinearRobot:
    def __init__(self, Y, Z):
        self.Y_axis = Y
        self.Z_axis = Z
        self.velocity = 100
        self.status = False

    # def __del__(self):
    #     """
    #     Destructor method that will home the robot before the LinearRobot class is destroyed. Will trigger when program
    #     (server) is stopped.
    #     """
    #     self.home()

    def initialize(self):
        """
        Initializes the robot by first homing it and then setting the initial positions for the y and z axes to zero for
        position tracking.
        """
        self.home()

    def home(self):
        """
        Sends the robot to its home position.
        """
        self.Z_axis.home()
        sleep(1)
        self.Y_axis.home()

        self.status = True

    def go_to(self, y=None, z=None, velocity=None, jog=False):
        """
        Moves the linear actuators to a target position. Default velocity for jogging to prevent fast uncontrolled
        movements.
        :param y: Target y position
        :param z: Target z position
        :param velocity: Velocity of stages
        :param jog: Boolean value, sets jog mode
        """
        if jog:
            if y is not None:
                self.Y_axis.move(y, self.velocity)
                self.Y_axis.position = y + self.Y_axis.position
            if z is not None:
                self.Z_axis.move(z, self.velocity)
                self.Z_axis.position = z + self.Z_axis.position
        else:
            if y is not None:
                # Always home Z axis before moving Y axis to prevent collision with IMM
                if self.Z_axis.position is not 0:
                    self.Z_axis.home()
                self.Y_axis.move(y - self.Y_axis.position, velocity)
                self.Y_axis.position = y

            if z is not None:
                self.Z_axis.move(z - self.Z_axis.position, velocity)
                self.Z_axis.position = z

    def get_status(self):
        return self.status

