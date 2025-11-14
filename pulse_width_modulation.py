from time import sleep

from machine import PWM, Pin


def pulse_width_test():
    pin = Pin("D4", Pin.OUT)
    pwm2 = PWM(pin, freq=10000, duty_u16=0)

    max_width = 65535
    min_width = 5000
    wstep = 50
    cur_width = min_width

    while True:
        pwm2.duty_u16(cur_width)
        sleep(0.0025)
        cur_width += wstep
        if cur_width > max_width:
            sleep(1)
            cur_width = max_width
            wstep *= -1
        elif cur_width < min_width:
            sleep(1)
            cur_width = min_width
            wstep *= -1
