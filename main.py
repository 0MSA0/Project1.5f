import time

from machine import Pin, ADC

from lib.LCD import LCD_1inch28
from lib.PinDefines import Vbat_Pin
from lib.QMI8658 import QMI8658

if __name__ == '__main__':

    LCD = LCD_1inch28()
    LCD.set_bl_pwm(65535)

    while True:
        LCD.fill(LCD.blue)
        LCD.draw_filled_circle(120, 120, 110, LCD.white)

        LCD.show()
        time.sleep(0.1)
