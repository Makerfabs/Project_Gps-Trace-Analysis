from machine import UART,Pin,I2C
import machine
import ssd1306
import utime

uart = UART(2, baudrate=115200, rx=21, tx=22,timeout=10)

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)      #Init i2c
lcd=ssd1306.SSD1306_I2C(128,64,i2c)           
lcd.text('Hello, Makerfabs',0,0)
lcd.text('waiting...',0,8)
lcd.show()

A9G_RESET_PIN = Pin(33, Pin.OUT) 
A9G_RESET_PIN.value(0)             

utime.sleep_ms(2000)
A9G_PWR_KEY = Pin(27, Pin.OUT) 
A9G_PWR_KEY.value(0)
utime.sleep_ms(2000)
A9G_PWR_KEY.value(1)
utime.sleep_ms(20000)

p=0 
def text(string,c=0,r=0): 
    global p 
    if p>80: 
        p=0
        lcd.fill(0) 
    colum=int(len(string)/15)+2 
    i=0
    for a in range(0,colum):
        lcd.text(string[i:i+15],c,a*8)
        i=i+15 
    lcd.show() 


if True:
    
    uart.write('AT+GPS=0\r\n')#1: turn on GPS  0:Turn off GPS
    utime.sleep_ms(1000)
    uart.write('AT+CCID\r\n')
    utime.sleep_ms(1000)
    uart.write('AT+CREG?\r\n')
    utime.sleep_ms(1000)
    uart.write('AT+CGATT=1\r\n')
    utime.sleep_ms(1000)
    uart.write('AT+CGACT=1,1\r\n')
    utime.sleep_ms(1000)
    uart.write('AT+CGDCONT=1,\"IP\",\"CMNET\"\r\n')
    utime.sleep_ms(1000)
    uart.write('AT+CSQ\r\n')
    utime.sleep_ms(1000)
    uart.write('AT+CPMS="SM","SM","SM"\r\n')
    utime.sleep_ms(1000)
    uart.write('AT+CMGF=1\r\n')
    utime.sleep_ms(1000)
    #uart.write('AT+CMGL="ALL"\r\n')
    #utime.sleep_ms(1000)
    while True:      
      if uart.any():
        lcd.fill(0)
        uart.write('AT+CMGR=1\r\n')
        utime.sleep_ms(1000)
        bin_data = uart.readline()
        print(bin_data)
        text(bin_data,0,0)
        lcd.show() 
      utime.sleep_ms(2000)
      
