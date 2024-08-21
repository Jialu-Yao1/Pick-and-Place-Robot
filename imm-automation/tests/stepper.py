from time import sleep
import RPi.GPIO as GPIO

PUL = 17  # Pulse
DIR = 27  # Direction
# ENA = 22  # Enable

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
# GPIO.setup(ENA, GPIO.OUT)

print('PUL = GPIO 17 - RPi 3B-Pin #11')
print('DIR = GPIO 27 - RPi 3B-Pin #13')
# print('ENA = GPIO 22 - RPi 3B-Pin #15')

durationFwd = 5000
durationBwd = 5000
print('Duration Fwd set to ' + str(durationFwd))
print('Duration Bwd set to ' + str(durationBwd))
delay = 0.0000001  # motor rotation speed (delay between pulse)
print('Speed set to ' + str(delay))
cycles = 10
cycle_count = 0
print('number of Cycles to Run set to ' + str(cycles))


def forward():
    # GPIO.output(ENA, GPIO.HIGH)
    # print('ENA set to HIGH - Controller Enabled')
    sleep(.5)
    GPIO.output(DIR, GPIO.LOW)
    print('DIR set to LOW - Moving Forward at ' + str(delay))
    print('Controller PUL being driven.')
    for x in range(durationFwd):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    # GPIO.output(ENA, GPIO.LOW)
    # print('ENA set to LOW - Controller Disabled')
    sleep(.5)  # pause for possible change direction
    return


def reverse():
    # GPIO.output(ENA, GPIO.HIGH)
    # print('ENA set to HIGH - Controller Enabled')
    #
    sleep(.5)
    GPIO.output(DIR, GPIO.HIGH)
    print('DIR set to HIGH - Moving Backward at ' + str(delay))
    print('Controller PUL being driven.')
    #
    for y in range(durationBwd):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    # GPIO.output(ENA, GPIO.LOW)
    # print('ENA set to LOW - Controller Disabled')
    sleep(.5)  # pause for possible change direction
    return


while cycle_count < cycles:
    forward()
    reverse()
    cycle_count = (cycle_count + 1)
    print('Number of cycles completed: ' + str(cycle_count))
    print('Number of cycles remaining: ' + str(cycles - cycle_count))

GPIO.cleanup()
print('Cycling Completed')
