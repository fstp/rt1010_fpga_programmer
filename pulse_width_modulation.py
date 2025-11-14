from time import sleep

from machine import PWM, Pin


def pulse_width_test():
    pin = Pin("D4", Pin.OUT)
    pwm2 = PWM(pin, freq=10000, duty_u16=0)

    max_width = 65535
    min_width = 0
    wstep = 10
    cur_width = min_width

    while True:
        pwm2.duty_u16(cur_width)
        sleep(0.00125)
        if cur_width == 0:
            sleep(5)
        cur_width += wstep
        if cur_width > max_width:
            cur_width = max_width
            wstep *= -1
        elif cur_width < min_width:
            cur_width = min_width
            wstep *= -1
