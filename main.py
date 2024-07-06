import time

from machine import Pin, ADC

from lib.LCD import LCD_1inch28
from lib.PinDefines import Vbat_Pin
from lib.QMI8658 import QMI8658


def draw_base_screen(lcd: LCD_1inch28, r: int, c: int = 0xf800):
    # Draw background for all screens
    lcd.fill(c)
    lcd.draw_filled_circle(120, 120, r, lcd.white)


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
    guthabentext = "Guthaben: 4,20"
    bezahltext = "Bezahlen"
    lcd.text(guthabentext, (120 - len(guthabentext) * 4), 60)
    lcd.text(bezahltext, 120 - len(bezahltext) * 4, 180)


def draw_qr_code(lcd: LCD_1inch28, start_x: int, start_y: int, size: int):
    pattern = [
        "1110110000110111",
        "1010101101010101",
        "1110101111010111",
        "0000101010010000",
        "1111111101011111",
        "0110100100000101",
        "0101011111011111",
        "0000110000101010",
        "1111110000010100",
        "1000001111011011",
        "1111101111101011",
        "0000110010100101",
        "1110101001010101",
        "1010110001011001",
        "1110101011101101",
    ]
    cell_size = size // len(pattern)
    for i, row in enumerate(pattern):
        for j, cell in enumerate(row):
            if cell == "1":
                c = 0  # Black color
            else:
                c = lcd.white  # White color
            lcd.fill_rect(start_x + j * cell_size, start_y + i * cell_size, cell_size, cell_size, c)


def draw_figure(lcd: LCD_1inch28, x_pos: int, y_pos: int):
    lcd.draw_filled_circle((x_pos + 12), y_pos, 8, 1)
    lcd.fill_rect((x_pos + 6), (y_pos + 10), 12, 50, 1)
    lcd.fill_rect(x_pos, (y_pos + 20), 25, 20, 1)


def draw_queue(lcd: LCD_1inch28):
    x_start = 60
    y_start = 160
    lcd.text("Stand:", x_start, y_start)
    lcd.text("Wartezeit:", x_start, (y_start + 20))
    lcd.text("XYZ", (x_start + 85), y_start)
    lcd.text("7 min", (x_start + 85), (y_start + 20))
    draw_figure(lcd, 50, 78)
    draw_figure(lcd, 80, 68)
    draw_figure(lcd, 110, 58)
    draw_figure(lcd, 140, 48)


if __name__ == '__main__':
    # Display init
    LCD = LCD_1inch28()
    LCD.set_bl_pwm(65535)
    circle_radius = 110
    qr_code_size = int(circle_radius * 2 * 0.70)  # 70% of the circle's diameter to ensure it fits well
    qr_code_start_x = 120 - qr_code_size // 2
    qr_code_start_y = 120 - qr_code_size // 2

    while True:
        # Screen 1
        draw_base_screen(LCD, circle_radius, LCD.red)
        draw_pay_screen(LCD, 120, 120)
        LCD.show()
        time.sleep(5)
        # Screen 2
        draw_base_screen(LCD, circle_radius)
        draw_qr_code(LCD, qr_code_start_x, qr_code_start_y, qr_code_size)
        LCD.show()
        time.sleep(5)
        # Screen 3
        draw_base_screen(LCD, circle_radius, LCD.green)
        draw_queue(LCD)
        LCD.show()
        time.sleep(5)
