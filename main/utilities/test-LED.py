import RPi.GPIO as GPIO
import time

LEDPIN = 37

GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
GPIO.setup(LEDPIN, GPIO.OUT)
print("LED ON")
GPIO.output(LEDPIN, GPIO.HIGH)
time.sleep(1)
print("LED OFF")
GPIO.output(LEDPIN, GPIO.LOW)


