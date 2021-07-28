import RPi.GPIO as GPIO
import time

class Breadboard_control:

    def __init__(self, green, red, buttonpin):
         
        self.greenstatus = self.redstatus = False
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        self.green = green
        self.red = red
        self.buttonpin = buttonpin
        
        GPIO.setup(green, GPIO.OUT)
        GPIO.setup(red, GPIO.OUT)
        GPIO.setup(buttonpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def green_toggle(self):
        if(self.greenstatus):
            GPIO.output(self.green, GPIO.LOW)
        else:
            GPIO.output(self.green, GPIO.HIGH)
        self.greenstatus = not self.greenstatus

    def red_toggle(self):
        if(self.redstatus):
            GPIO.output(self.red, GPIO.LOW)
        else:
            GPIO.output(self.red, GPIO.HIGH)
        self.redstatus = not self.redstatus

    def is_button(self):
        return GPIO.input(self.buttonpin) == GPIO.HIGH



