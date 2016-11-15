#    while True:
#

#
"""   turns to right in order to check line steering direction,"""

#        R_motor.run_timed(duty_cycle_sp=25, time_sp=30)
#        temp_color_value = color_sensor.value()
#        difference = perfect_value - temp_color_value;
#
#        if difference < 0:
#            line_steering = "left"
#        else:
#            line_steering = "right"
#
#    #    print(line_steering)
#        difference_ratio = abs(float(difference) / 80)
#        adjust = int(40 * difference_ratio)
#    #    duty_cycle_adjusted = int(duty_cycle * difference_ratio)
#    #    print(difference_ratio)
#        duty_cycle_adjusted = duty_cycle - adjust
    #    print (duty_cycle_adjusted)
#
#        if line_steering == "right":
#            L_motor.run_timed(duty_cycle_sp=duty_cycle_adjusted, time_sp=duration)
#            R_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
#            time.sleep(2)

#        if line_steering == "left":
#            duty_cycle_adjusted = int(duty_cycle * difference_ratio)
#            L_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=duration)
#            R_motor.run_timed(duty_cycle_sp=duty_cycle_adjusted, time_sp=duration)
#            time.sleep(2)

#        L_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=time)
#        R_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=time)
#        time.sleep(2)



#    rB = R_motor.position
#    lB = L_motor.position
#
#    L_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=time)
#    R_motor.run_timed(duty_cycle_sp=duty_cycle, time_sp=time)
#    time.sleep(2)
#
#    rA = R_motor.position
#    lA = L_motor.position

#    print(str(d)+ ' ' + str(t) + ' ' + str(rB) + ' ' + str(lB) + ' ' + str(rA) + ' ' + str(lA))
#    color_sensor = ev3.ColorSensor(ev3.INPUT_4);
#    color_sensor.connected
#    color_sensor.mode = 'COL-REFLECT'
#
#    while True:
#        print(str(color_sensor.value()) + '\n')
#
