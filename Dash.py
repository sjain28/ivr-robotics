import ev3dev.ev3 as ev3
import time
import utilities as util
import math

duty_cycle = 30
next_turn_right = False
kp = 0.5
ki = 0.05
kd = 1.4

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
    gyro_sensor = ev3.GyroSensor(ev3.INPUT_2)
    gyro_sensor.connected
    gyro_sensor.mode = 'GYRO-ANG'

    line_count = 0
    # The value which color sensor gives if its above the edge of the line
    # going towards 80 means getting to white area and towards 0 to black
    temp_color_value = color_sensor.value()
    last_error = 0


    #Calibration: Turn slightly to the right. If the sensor value increases, then the white space is to the
    #right of the robot. If the value decreases, then the white space is to the left of the robot.
    L_motor.run_timed(duty_cycle_sp=50, time_sp=100)
    time.sleep(.5)
    calibration_value = color_sensor.value()
    print(str(calibration_value))
    L_motor.run_timed(duty_cycle_sp=-50, time_sp=100)
    time.sleep(.5)

    L_motor.run_timed(duty_cycle_sp=-50, time_sp=100)
    time.sleep(.5)
    opposite_value = color_sensor.value()
    print(str(opposite_value))
    L_motor.run_timed(duty_cycle_sp=50, time_sp=100)
    time.sleep(.5)

    white_on_right = calibration_value > temp_color_value

    #Call helper function
    #IMPORTANT: Notice that we switch the motor parameters based on white_on_right.
    #This way, all the logic stays the same; all that changes is the direction in which the robot must turn
    if white_on_right:
        print('White on my right')
        white = calibration_value
        black = opposite_value
        midpoint = ( white - black ) / 2 + black
        print("midpoint: " + str(midpoint))
        traverse(midpoint, last_error,color_sensor, temp_color_value, L_motor, R_motor, gyro_sensor, white)
    else:
        print('White on my left')
        white = opposite_value
        black = calibration_value
        midpoint = ( white - black ) / 2 + black
        print("midpoint: " + str(midpoint))
        traverse(midpoint, last_error, color_sensor, temp_color_value, R_motor, L_motor, gyro_sensor, white, line_count)


#Code for adjusting robot movements based on value of color sensor
#Motor1: Turn towards white. motor2: turn towards black.
def traverse(midpoint, last_error, color_sensor, temp_color_value, L_motor, R_motor, gyro_sensor, white, line_count):
    white_cycle_count = 0
    helper = 0
    row = 0
    integral = 0
    temp_angle = 0


    while True:
        row = row + 1
        temp_color_value = color_sensor.value()

        if temp_color_value > white - 10:
            if(white_cycle_count == 0):
                temp_angle = gyro_sensor.value()
                print("angle starting: " + str(temp_angle))
                helper = row
                white_cycle_count = 1
            elif(helper + 1 == row):
                helper = row
                white_cycle_count = white_cycle_count + 1
                print("white_cycle_count: " + str(white_cycle_count))
            else:
                white_cycle_count = 0

        print("reading val: " + str(temp_color_value))
        error = midpoint - temp_color_value
        integral = integral + error
        derivative = error - last_error

        correction = kp * error + ki * integral + kd * derivative
        if(correction > 70):
            correction = 69
        elif(correction < -70):
            corection = -69
        powerL = duty_cycle + correction
        powerR = duty_cycle - correction

        L_motor.run_direct(duty_cycle_sp=powerL)
        R_motor.run_direct(duty_cycle_sp=powerR)

        if white_cycle_count > 10:
            L_motor.stop()
            R_motor.stop()
            cur_angle = gyro_sensor.value()
            print("current angle: " + str(cur_angle))
            print("start angle: " + str(temp_angle))

            #if(gyro_sensor.value() < temp_angle):
            #    print("if")
            #    L_motor.run_direct(duty_cycle_sp=abs(gyro_sensor.value() - temp_angle))
            while abs(temp_angle - cur_angle) > 2:
                if(temp_angle < cur_angle):
                    print("current angle: " + str(cur_angle))
                    print("start angle: " + str(temp_angle))
                    L_motor.run_direct(duty_cycle_sp = 13)
                elif(temp_angle > cur_angle):
                    print("current angle: " + str(cur_angle))
                    print("start angle: " + str(temp_angle))
                    R_motor.run_direct(duty_cycle_sp = 13)
                cur_angle = gyro_sensor.value()
            #else:
            #    print("else")
            #    R_motor.run_direct(duty_cycle_sp=abs(gyro_sensor.value() - temp_angle))
            ev3.Sound.speak('End of line').wait()
            turn(midpoint, last_error, temp_color_value, L_motor, R_motor, gyro_sensor, white, color_sensor, line_count)
            break;
        last_error = error



def turn(midpoint, last_error, temp_color_value, motor1, motor2, gyro_sensor, white, color_sensor, line_count):

    while color_sensor.value() > midpoint:
        motor1.run_direct(duty_cycle_sp=duty_cycle)
        motor2.run_direct(duty_cycle_sp=duty_cycle/2)

    ev3.Sound.speak('New line').wait()
    traverse(midpoint, last_error, color_sensor, temp_color_value, motor2, motor1, gyro_sensor, white, line_count)
