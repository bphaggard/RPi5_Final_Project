from gpiozero import LED, MotionSensor
import time
from picamzero import Camera
from signal import pause

# Initialize LED, PIR motion sensor and Camera using GPIO Zero library
led = LED(22)  # LED connected to GPIO pin 22
pir = MotionSensor(17)  # PIR sensor connected to GPIO pin 17
camera = Camera()

def motion_detected():
    global start_time
    start_time = time.time()
    led.on()

def motion_finished():
    led.off()
    motion_duration = time.time() - start_time
    if motion_duration > 5.0:
        print("Taking a photo")
    else:
        print(motion_duration)

pir.when_motion = motion_detected
pir.when_no_motion = motion_finished
pause()