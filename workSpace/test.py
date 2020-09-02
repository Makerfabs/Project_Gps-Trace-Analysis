# for Makepython A9G GPS Tracker V1.1
from machine import UART, Pin, I2C, SPI
import ssd1306
import time
import os
import sdcard
import random


def main():
    # UART init
    uart = UART(2, baudrate=115200, rx=21, tx=22, timeout=10)
    print("UART OK")

    # LCD init
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)  # Init i2c
    lcd = ssd1306.SSD1306_I2C(128, 64, i2c)
    print("LCD OK")
    lcd.fill(0)
    lcd.text('LCD OK', 0, 0)

    # SD init
    spi = SPI(1, baudrate=400000, polarity=1, phase=0,
              sck=Pin(14), mosi=Pin(13), miso=Pin(12))
    spi.init()  # Ensure right baudrate
    lcd.text('SPI OK', 0, 8)
    sd = sdcard.SDCard(spi, Pin(32))  # Compatible with PCB
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/SD")
    random.seed(len(os.listdir("/SD")))
    print("SD OK")
    lcd.text('SPI OK', 0, 16)

    # LCD show
    lcd.fill(0)
    lcd.text('Hello, Makerfabs', 0, 0)
    lcd.text('GPS..', 0, 8)
    lcd.show()

    # A9G open
    A9G_RESET_PIN = Pin(33, Pin.OUT)
    A9G_RESET_PIN.value(0)  # set pin to low

    time.sleep(1)
    A9G_PWR_KEY = Pin(27, Pin.OUT)
    A9G_PWR_KEY.value(0)
    time.sleep(1)
    A9G_PWR_KEY.value(1)
    time.sleep(1)
    lcd.fill(0)
    lcd.text('A9G open', 0, 0)

    # A9G GPS open
    uart.write('AT+GPS=1\r\n')  # 1: turn on GPS  0:Turn off GPS
    time.sleep(1)
    uart.write('AT+GPSRD=0\r\n')
    time.sleep(1)
    lcd.fill(0)
    lcd.text('A9G GPS open', 0, 0)
    while uart.any():
        clean_buffer = uart.readline()
        print(clean_buffer)

    # Time and index init
    index = 0
    filename = '/SD/trace' + str(random.randint(0, 10000)) + '.txt'
    print(filename)
    lcd.fill(0)
    lcd.text('Preare pen ' + filename, 0, 0)
    f = open(filename, "w")
    lcd.fill(0)
    lcd.text('Already pen ' + filename, 0, 0)
    print('Open ' + filename)
    f.write(filename + '\t create by Vincent\n')
    f.write("-----------------------\n")
    f.flush()

    while True:
        uart.write('AT+LOCATION=2\r\n')  # Get GPS address
        time.sleep(1)
        while uart.any():
            bin_data = uart.readline()
            uart_str = bin_data.decode().replace('\n', '').replace('\r', '')

            #uart_str = '22.611830,113.835153'

            if uart_str == "":
                continue
            print(uart_str)

            if uart_str.find('+LOCATION') == 0:
                index = index + 1

                data ={}
                data['time'] = time.time()
                data['index'] = index
                data['latitude'] = "NULL"
                data['longitude'] = "NULL"
                f.write(str(data) + '\n')
                f.flush()

                lcd.fill(0)
                lcd.text(str(index), 0, 0)
                lcd.text("NULL", 0, 8)
                lcd.show()
                print(data)
            elif uart_str.find(',') != -1:
                index = index + 1
                gps_str_list = uart_str.split(',')
                #纬度
                latitude = float(gps_str_list[0])
                #经度
                longitude = float(gps_str_list[1])

                data ={}
                data['time'] = time.time()
                data['index'] = index
                data['latitude'] = latitude
                data['longitude'] = longitude
                f.write(str(data) + '\n')
                f.flush()

                lcd.fill(0)
                lcd.text(str(index), 0, 0)
                lcd.text(str(latitude), 0, 8)
                lcd.text(str(longitude), 0, 16)
                lcd.show()
                print(data)

        time.sleep(5)


if __name__ == "__main__":
    main()
    pass
