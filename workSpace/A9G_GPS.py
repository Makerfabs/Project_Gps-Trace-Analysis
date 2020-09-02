# for Makepython A9G GPS Tracker V1.1
from machine import UART, Pin, I2C
import machine
import ssd1306
import utime

uart = UART(2, baudrate=115200, rx=21, tx=22, timeout=10)
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)  # Init i2c
lcd = ssd1306.SSD1306_I2C(128, 64, i2c)
lcd.text('Hello, Makerfabs', 0, 0)
lcd.text('waiting...', 0, 8)
lcd.show()

A9G_RESET_PIN = Pin(33, Pin.OUT)
A9G_RESET_PIN.value(0)  # set pin to low

utime.sleep_ms(2000)
A9G_PWR_KEY = Pin(27, Pin.OUT)
A9G_PWR_KEY.value(0)
utime.sleep_ms(2000)
A9G_PWR_KEY.value(1)
utime.sleep_ms(20000)

# Display line wrap
p = 0


def text(string, c=0, r=0):
    global p
    if p > 80:
        p = 0
        lcd.fill(0)
    colum = int(len(string)/15)+2
    i = 0
    for a in range(0, colum):
        lcd.text(string[i:i+15], c, a*8)
        i = i+15
    lcd.show()


if True:
    lcd.fill(0)
    uart.write('AT+GPS=1\r\n')  # 1: turn on GPS  0:Turn off GPS
    utime.sleep_ms(1000)
    uart.write('AT+GPSRD=10\r\n')
    utime.sleep_ms(1000)
    uart.write('AT+LOCATION=2\r\n')
    utime.sleep_ms(1000)
    while True:
        if uart.any():
            uart.write('AT+LOCATION=2\r\n')  # Get GPS address
            bin_data = uart.readline()
            msg = len(bin_data)
            print(bin_data)
            mystr = str(bin_data[0:msg-2], 'utf-8')
            lcd.fill(0)
            text(mystr, 0, 0)
            lcd.show()
        utime.sleep_ms(2000)
