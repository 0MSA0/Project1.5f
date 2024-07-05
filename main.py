import time

from machine import Pin, ADC

from lib.LCD import LCD_1inch28
from lib.PinDefines import Vbat_Pin
from lib.QMI8658 import QMI8658


def draw_base_screen(lcd: LCD_1inch28):
    # Draw background for all screens
    lcd.fill(lcd.blue)
    lcd.draw_filled_circle(120, 120, 110, lcd.white)


def draw_pay_screen(lcd: LCD_1inch28, center_x: int, center_y: int):
    pixel_size = 2
    pay_pixels = [
        "                                      XXXXXXXXXXXXXXXXXXX                                      ",
        "                              XXXXXXXX                   XXXXXXXX                              ",
        "                         XXXXX                                   XXXXX                         ",
        "                     XXXX                                             XXXX                     ",
        "                  XXX                                                     XXX                  ",
        "               XXX                       XX                                  XXX               ",
        "             XX                          XXX                                    XX             ",
        "           XX                      XX     XXX                          XX XX      XX           ",
        "         XX                        XXX     XX                          XX XX        XX         ",
        "        X                           XXX    XXX                       XXXXXXXXX        X        ",
        "      XX                      XX     XX     XX                      XXXXXXXXXXX        XX      ",
        "     X                        XXX    XXX    XXX                    XXX XX XX XXX         X     ",
        "    X                  XX      XX     XX     XX                   XXX  XX XX  XXX         X    ",
        "   X                   XXX     XXX    XXX    XXX                 XXX   XX XX   XXX         X   ",
        "  X              XX     XX      XX     XX     XX                 XX    XX XX    XX          X  ",
        "  X              XXX    XXX     XX     XX     XX                 XX    XX XX    XX          X  ",
        " X                XX     XX     XX     XX     XX                 XX    XX XX                 X ",
        " X                XXX    XXX    XXX    XXX    XXX                XXX   XX XX                 X ",
        "X                  XX     XX     XX     XX     XX                 XXX  XX XX                  X",
        "X                  XX     XX     XX     XX     XX                  XXX XX XX                  X",
        "X                  XX     XX     XX     XX     XX                   XXXXXXXXXX                X",
        "X                  XX     XX     XX     XX     XX                    XXXXXXXXXX               X",
        "X                  XX     XX     XX     XX     XX                      XX XX XXX              X",
        " X                XXX    XXX    XXX    XXX    XXX                      XX XX  XXX            X ",
        " X                XX     XX     XX     XX     XX                       XX XX   XXX           X ",
        "  X              XXX    XXX     XX     XX     XX                 XX    XX XX    XX          X  ",
        "  X              XX     XX      XX     XX     XX                 XX    XX XX    XX          X  ",
        "   X                   XXX     XXX    XXX    XXX                 XXX   XX XX   XXX         X   ",
        "    X                  XX      XX     XX     XX                   XXX  XX XX  XXX         X    ",
        "     X                        XXX    XXX    XXX                    XXX XX XX XXX         X     ",
        "      XX                      XX     XX     XX                      XXXXXXXXXXX        XX      ",
        "        X                           XXX    XXX                       XXXXXXXXX        X        ",
        "         XX                        XXX     XX                          XX XX        XX         ",
        "           XX                      XX     XXX                          XX XX      XX           ",
        "             XX                          XXX                                    XX             ",
        "               XXX                       XX                                  XXX               ",
        "                  XXX                                                     XXX                  ",
        "                     XXXX                                             XXXX                     ",
        "                         XXXXX                                   XXXXX                         ",
        "                              XXXXXXXX                   XXXXXXXX                              ",
        "                                      XXXXXXXXXXXXXXXXXXX                                      "
    ]

    pay_height = len(pay_pixels)
    pay_width = len(pay_pixels[0])

    for row in range(pay_height):
        for col in range(pay_width):
            if pay_pixels[row][col] == 'X':
                x = center_x - (pay_width * pixel_size) // 2 + col * pixel_size
                y = center_y - (pay_height * pixel_size) // 2 + row * pixel_size
                lcd.rect(x, y, pixel_size, pixel_size, 0)


if __name__ == '__main__':
    # Display init
    LCD = LCD_1inch28()
    LCD.set_bl_pwm(65535)

    while True:
        # Screen 1
        draw_base_screen(LCD)
        draw_pay_screen(LCD, 120, 120)
        LCD.show()
        time.sleep(5)
        # Screen 2
        draw_base_screen(LCD)
        LCD.text("Screen 2", 120, 120, 0x0)
        LCD.show()
        time.sleep(5)
        # Screen 3
        draw_base_screen(LCD)
        LCD.text("Screen 3", 120, 120, 0x0)
        LCD.show()
        time.sleep(5)
