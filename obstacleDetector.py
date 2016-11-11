import ev3dev.ev3 as ev3
import time
import utilities as util

#Starting position of sonar needs to be ~60 degrees anti-clockwise
#This function rotates the sonar between 3 positions: 60 degrees anti-clockwise, straight, and
#60 degrees clockwise. And it records the sonar reading at each position.
#TODO: Could adjust the numbers in motor control to turn motor between a greater range of positions
def searchForObstacles():
    motor = ev3.MediumMotor('outA')
    motor.connected

    sonar = ev3.UltrasonicSensor(ev3.INPUT_1)
    sonar.connected
    sonar.mode = 'US-DIST-CM' # will return value in mm

    readings = ""
    readings_file = open('results.txt', 'w')

    btn = ev3.Button()

    directions = (1, 1, -1, -1)
    count = 0

    while count<12:
        readings = readings + str(sonar.value()) + '\n'
        direction = directions[count%4]
        motor.run_timed(duty_cycle_sp=25*direction, time_sp=350)

        time.sleep(2)
        count+=1

    readings_file.write(readings)
    readings_file.close() # Will write to a text file in a column
