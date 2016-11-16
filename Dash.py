import ev3dev.ev3 as ev3
import time
import utilities as util
import math

duty_cycle = 30
duration = 13
perfect_value = 40
next_turn_right = False

#TODO
#Stop after 4 lines

def followLines():

    #Setup sensors and motors
    color_sensor = ev3.ColorSensor(ev3.INPUT_4);
    color_sensor.connected
    color_sensor.mode = 'COL-REFLECT'
    R_motor = ev3.LargeMotor('outC')
    R_motor.connected
    L_motor = ev3.LargeMotor('outB')
    L_motor.connected

    line_count = 0
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

    next_turn_right = calibration_value > temp_color_value

    temp_color_value = color_sensor.value()
    difference = abs(perfect_value - temp_color_value)

    if next_turn_right:
        print('White on my right')
        traverse(difference, color_sensor, temp_color_value, L_motor, R_motor, line_count)
    else:
        print('White on my left')
        traverse(difference, color_sensor, temp_color_value, R_motor, L_motor, line_count)


#Code for adjusting robot movements based on value of color sensor
#Motor1: Turn towards white. motor2: turn towards black.
def traverse(difference, color_sensor, temp_color_value, motor1, motor2, line_count):
    white_cycle_count = 0

    while True:
        #IF difference is low, keep going straight
        if difference < 20:
            motor1.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            motor2.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            time.sleep(.013)

        #If there's too much black, turn towards white
        elif temp_color_value < 20:
            motor1.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            time.sleep(.013)

        #If there's too much white, turn towards black
        elif temp_color_value > 60:
            motor2.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            time.sleep(.013)

        #If we're in a completely white region, keep track of how long we stay there
        if temp_color_value > 70:
            white_cycle_count = white_cycle_count+1

        else:
            white_cycle_count = 0

        #If you've been in a completely white region for 50 cycles, we assume that the robot has reached
        #the end of the black line
        if white_cycle_count > 15:
            line_count = line_count +1
            if line_count == 2:
                ev3.Sound.speak('All done!').wait()
                break
            ev3.Sound.speak('End of line').wait()
            turn(motor1, motor2, color_sensor, line_count)


        temp_color_value = color_sensor.value()
        difference = abs(perfect_value - temp_color_value)



def turn(motor1, motor2, color_sensor, line_count):

    while color_sensor.value() > 50:
        motor1.run_timed(duty_cycle_sp=30, time_sp=duration)
        #motor2.run_timed(duty_cycle_sp=15, time_sp=duration)
        time.sleep(.013)

    difference = abs(color_sensor.value() - perfect_value)

    ev3.Sound.speak('New line').wait()
    traverse(difference, color_sensor, color_sensor.value(), motor2, motor1, line_count)
