import smbus
from time import sleep, strftime
from datetime import datetime
from LCD1602 import CharLCD1602
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_pressed = False
def button_callback(channel):
    global button_pressed
    print("Button pressed!")
    button_pressed = True

lcd1602 = CharLCD1602()
def get_cpu_temp():     # get CPU temperature from file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C '

def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')

def loop():
    lcd1602.init_lcd()
    count = 0
    while(True):
        if button_pressed:
            print("Closing")
            lcd1602.closelight()
            sleep(1)
            print("Opening")
            lcd1602.openlight()
            
        lcd1602.clear()
        lcd1602.write(0, 0, 'CPU: ' + get_cpu_temp() )# display CPU temperature
        lcd1602.write(0, 1, get_time_now() )   # display the time
        sleep(1)

def destroy():
    lcd1602.clear()


if __name__ == '__main__':
    print ('Program is starting ... ')

    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(19, GPIO.FALLING, callback=button_callback, bouncetime=200)
    print("Added Event")


    try:
        loop()
    except KeyboardInterrupt:
        destroy()