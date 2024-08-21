from SERVER.website.assets.components.limit_switch import LimitSwitch
from SERVER.website.assets.components.linear_actuator import LinearActuator
from SERVER.website.assets.controllers.TB6600 import TB6600
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

home = LimitSwitch(26)
controller = TB6600(17, 27, 22, 200)

linear_actuator = LinearActuator(500, controller, home, 'Y')
controller.forward()

linear_actuator.move(10, 500)

# linear_actuator.home()


GPIO.cleanup()


