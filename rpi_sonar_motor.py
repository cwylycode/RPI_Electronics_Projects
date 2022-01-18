"""
This project allows you to control the spin of a dc motor using the distance of your hand!

Depending on the distance of you hand from the sensor (up to half a meter), the speed of the motor will change. Also an RGB LED will light up with different colors depending on distance.

Required parts:
- RPI 40-pin GPIO
- Breadboard
- DC motor w/ motor microcontroller (such as L293D)
- Ultrasonic range sensor
- RGB LED
- Battery pack
- Wires and resistors
"""

from gpiozero import DistanceSensor,Motor,RGBLED
from gpiozero.tools import scaled,inverted
from time import sleep

# In meters
sensor_range = 0.5
thresh = sensor_range - 0.01 if sensor_range > 0.01 else 0

sensor = DistanceSensor(echo=24,trigger=23,max_distance=sensor_range,threshold_distance=thresh)
motor = Motor(forward=19,backward=26,enable=13)
led = RGBLED(red=21,green=20,blue=16,active_high=False)

def app():
    motor.source = scaled(inverted(sensor),0,1)
    while True:
        sleep(0.1)
        if sensor.distance < sensor_range * 1/5: led.color = (1,0,0)
        elif sensor.distance < sensor_range * 2/5: led.color = (1,0.5,0)
        elif sensor.distance < sensor_range * 3/5: led.color = (1,1,0)
        elif sensor.distance < sensor_range * 4/5: led.color = (0,1,0)
        elif sensor.distance < sensor_range * 5/5: led.color = (0,0,1)
        else: led.color = (0.1,0.1,0.1)

# Execute
if __name__ == "__main__":
    try: app()
    #Auto-cleanup of gpio
    except Exception as e: print(e)