import ev3dev.ev3 as ev3
import time
import utilities as util
import math

#TODO:
#Proportional Turning
#Try and reduce num of white cycles needed before stopping
#Make robot speak instead of printing

duty_cycle = 40
duration = 13
perfect_value = 40

def followLines():

    #Setup sensors and motors
    color_sensor = ev3.ColorSensor(ev3.INPUT_4);
    color_sensor.connected
    color_sensor.mode = 'COL-REFLECT'
    R_motor = ev3.LargeMotor('outC')
    R_motor.connected
    L_motor = ev3.LargeMotor('outB')
    L_motor.connected

    # The value which color sensor gives if its above the edge of the line
    # going towards 80 means getting to white area and towards 0 to black
    temp_color_value = color_sensor.value()

    #Calibration: Turn slightly to the right. If the sensor value increases, then the white space is to the
    #right of the robot. If the value decreases, then the white space is to the left of the robot.
    L_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=100)
    time.sleep(.5)
    calibration_value = color_sensor.value()
    L_motor.run_timed(duty_cycle_sp=-duty_cycle, time_sp=100)
    time.sleep(.5)

    white_on_right = calibration_value > temp_color_value

    temp_color_value = color_sensor.value()
    difference = abs(perfect_value - temp_color_value)

    #Call helper function
    #IMPORTANT: Notice that we switch the motor parameters based on white_on_right.
    #This way, all the logic stays the same; all that changes is the direction in which the robot must turn
    if white_on_right:
        print('White on my right')
        traverse(difference, color_sensor, temp_color_value, L_motor, R_motor)
    else:
        print('White on my left')
        traverse(difference, color_sensor, temp_color_value, R_motor, L_motor)



#Code for adjusting robot movements based on value of color sensor
def traverse(difference, color_sensor, temp_color_value, L_motor, R_motor):
    white_cycle_count = 0

    while True:
        #IF difference is low, keep going straight
        if difference < 30:
            L_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            R_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            time.sleep(.012)

        #If there's too much black, turn towards white
        elif temp_color_value < 20:
            L_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            time.sleep(.012)

        #If there's too much white, turn towards black
        elif temp_color_value > 60:
            R_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            time.sleep(.012)

        #If we're in a completely white region, keep track of how long we stay there
        if temp_color_value > 80:
            white_cycle_count = white_cycle_count+1

        else:
            white_cycle_count = 0

        #If you've been in a completely white region for 50 cycles, we assume that the robot has reached
        #the end of the black line
        if white_cycle_count > 50:
            print('Im Done Here')
            break;

        temp_color_value = color_sensor.value()
        difference = abs(perfect_value - temp_color_value)
