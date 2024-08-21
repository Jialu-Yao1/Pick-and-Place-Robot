from django.shortcuts import render
from datetime import datetime
from .assets.robot.end_effector import EndEffector
from .assets.controllers.TB6600 import TB6600
from .assets.components.limit_switch import LimitSwitch
from .assets.components.linear_actuator import LinearActuator
from .assets.robot.linear_robot import LinearRobot
from collections import deque
# from .assets.components.camera import USBCamera
from SERVER.celery import app  # This is not an error
from .tasks import automate
import json
from django.http import JsonResponse

import asyncio
from asyncua import Client, ua
import time
# from .assets.imm.imm import IMM

import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup(12)

# url = "opc.tcp://192.168.9.2:49320"
# namespace = ""
# IMMobj = IMM(url)

# Instantiating robot class
y_limit_switch = LimitSwitch(5)  # Set pin please
z_limit_switch = LimitSwitch(6)  # Set pin please
y_controller = TB6600(24, 23, 22, 200)  # Set pin please
z_controller = TB6600(27, 26, 25, 200)  # Set pin please
y_actuator = LinearActuator(1000, y_controller, y_limit_switch, 'y')
z_actuator = LinearActuator(500, z_controller, z_limit_switch, 'z')
robot = LinearRobot(y_actuator, z_actuator)

# Instantiate camera, update port number
# camera = USBCamera(0)

# Instantiating end effector class
ee = EndEffector()

# Main loop variables
stopnext = False
running = False
robotison = False
task_id = None
# imm_status = False
# firstcycle = True


def read_batch_history():
    # This function reads the batch history from a text file located in the 'assets' directory to update the website
    # on startup. It returns a list containing the lines from the file.
    #
    # Returns:
    # A list of strings, with each string representing a line from the 'batch_history.txt' file.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'assets', 'batch_history.txt')
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            return [line.strip() for line in lines]
    except FileNotFoundError:
        return []


def add_batch(batch):
    # This function appends a new batch to the 'batch_history.txt' file located in the 'assets' directory so that
    # batch numbers are preserved across server restarts
    #
    # param batch (String): The batch to be added to the batch history file.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'assets', 'batch_history.txt')
    with open(file_path, 'a') as f:
        f.write(f'{batch}\n')


batch_history = deque(read_batch_history())  # Variable to store the list of batches currently in storage


def homepage(request):
    # This function handles the homepage view of the website. It processes the incoming HTTP requests; processes
    # the commands and controls the respective robot parts; updates the state of the robot, its parts, and the
    # connections; and renders the 'website.html' template.
    #
    # param request (HttpRequest): The incoming HTTP request from the client.
    #
    # Returns: 1. A JsonResponse containing updated information about the the state of the robot, its parts,
    # and the connections or a rendered HTML template. 2. The website HTML file
    global running
    global stopnext
    global robotison
    global task_id
    # global imm_status
    # global firstcycle

    jog_step = 10  # Adjust jog step value as required

    if request.method == 'POST':
        # If the request method is POST, load the JSON data from the request
        data = json.loads(request.body)
        command = data.get('command')

        # Start/Stop buttons to start the cycle or indicate that the cycle should stop at the end of the run
        if command == 'start':
            print("Start")
            if not running and robotison:
                print("Started")
                # main cycle_loop
                stopnext = False
                # creates new batch in storage for every cycle start
                now = datetime.now()  # get current date and time
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                add_batch(current_time)
                batch_history.append(current_time)

                # TODO: move to celery worker task
                # while not stopnext:
                #
                #     if firstcycle:
                #
                #         await IMMobj.IMMfirstcycle()
                #         imm_status = True
                #         firstcycle = False
                #     else:
                #         await IMMobj.IMMconsequentcycle()
                #
                #     # robo stufff
                #     print("Robot stuff happening")
                #     robot.home()
                #
                #     ee.drop_part()
                #
                #     ee.pick_part_1()
                #     time.sleep(5)
                #
                #     await IMMobj.IMMejectPart()
                #     running = True
                #
                #     ee.pick_part_2()
                #
                #     if stopnext:
                #         running = False
                # if command == 'stop':
                #     if running:
                #         stopnext = True

                # while not stopnext:
                #     sleep(1)
                #     running = True
                #     print("looping")
                #     if stopnext:
                #         running = False

                # task_id = automate.delay()
                # print(task_id)

                robot.go_to(y=-50, velocity=100)
                robot.go_to(z=-25, velocity=100)
                time.sleep(5)
                ee.pick_part_1()
                time.sleep(5)
                ee.pick_part_2()
                time.sleep(5)
                robot.home()
                ee.drop_part()
        if command == 'stop':
            if running:
                stopnext = True
                app.control.revoke(task_id)

        # Turn on drivers and initialise robot
        if command == 'on':
            if not robotison and not running:
                robotison = True
                robot.Y_axis.controller.enable()
                robot.Z_axis.controller.enable()
        # Turn off drivers
        if command == 'off':
            if robotison and not running:
                robotison = False
                robot.Y_axis.controller.disable()
                robot.Z_axis.controller.disable()

        # Clear list of batches currently in storage (button to be pressed after storage is manually cleared
        if command == 'clear_storage':
            batch_history.clear()
            print('storage cleared')

        if not running and robotison:
            # Buttons to open/close the end effector
            if command == 'ee_close':
                ee.pick_part_1()
                time.sleep(5)
                ee.pick_part_2()
            if command == 'ee_open':
                ee.drop_part()

            # Jog axes buttons
            # Jog axes buttons
            if command == 'xp':
                robot.go_to(y=jog_step, jog=True)
            if command == 'xn':
                robot.go_to(y=-1 * jog_step, jog=True)
            if command == 'yp':
                robot.go_to(z=jog_step, jog=True)
            if command == 'yn':
                robot.go_to(z=-1 * jog_step, jog=True)

            # Home robot
            if command == 'home':
                robot.home()

        response_data = {
            # replace "True" with the name of the variables to be passed
            'batch_history': '\n'.join(batch_history),
            'robot_status': robot.status,
            'imm_status': True,
            'an_status': True,
            'odoo_status': True,
            'robot_location': True,
            'robotison': robotison,
            'running': running,
        }
        return JsonResponse(response_data)
    return render(request, 'website.html')
