import ev3dev.ev3 as ev3
import time
import utilities as util
import math

def followLines():

    color_sensor = ev3.ColorSensor(ev3.INPUT_4);
    color_sensor.connected
    color_sensor.mode = 'COL-REFLECT'

    R_motor = ev3.LargeMotor('outC')
    R_motor.connected

    L_motor = ev3.LargeMotor('outB')
    L_motor.connected

    duty_cycle = 65
    duration = 13

    # The value which color sensor gives if its above the edge of the line
    # going towards 80 means getting to white area and towards 0 to black
    perfect_value = 40

    temp_color_value = color_sensor.value()
    difference = abs(perfect_value - temp_color_value)

#Code for clockwise traversal ; turn right if going towards black, turn left if going towards white
#Currently just turning
#TODO: Make magnitude of turn proportional to magnitude of difference
    while True:

        if difference < 30:
            L_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            R_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            time.sleep(.012)
        #    print('straight')

        elif temp_color_value < 20:
            L_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            time.sleep(.012)
        #    print('turning right')

        elif temp_color_value > 60:
            R_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
            time.sleep(.012)
        #    print('turning left')

        temp_color_value = color_sensor.value()
        difference = abs(perfect_value - temp_color_value)



#    while difference < 20:
#        print(str(difference) + '\n')
#        L_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
#        R_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
#        time.sleep(.3)
#
#        temp_color_value = color_sensor.value()
#        difference = abs(perfect_value - temp_color_value)
