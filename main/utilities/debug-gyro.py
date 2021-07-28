from sense_hat import SenseHat
import time

sense = SenseHat()
while True:
    orientation = sense.get_orientation_degrees()
    print("roll=" + str(orientation["roll"]))
    time.sleep(0.5)
