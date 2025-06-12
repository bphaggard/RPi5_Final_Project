from gpiozero import LED, MotionSensor
import time
import os
import yagmail
from picamzero import Camera
from signal import pause
from datetime import datetime
from dotenv import load_dotenv

# Initialize LED, PIR motion sensor and Camera using GPIO Zero library
led = LED(22)  # LED connected to GPIO pin 22
pir = MotionSensor(17)  # PIR sensor connected to GPIO pin 17
camera = Camera()

last_time_photo_taken = 0

load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def motion_detected():
    print("Start motion timer")
    global start_time
    start_time = time.time()
    led.on()

def motion_finished():
    global last_time_photo_taken
    led.off()
    motion_duration = time.time() - start_time
    if motion_duration > 5.0:
        if time.time() - last_time_photo_taken > 30.0:
            last_time_photo_taken = time.time()
            take_photo()
            send_photo_by_email()
    else:
        print(f"Motion duration: {motion_duration}")

def take_photo():
    global filepath
    photo_folder = "/home/haggard/Desktop/Final_Project/photos"
    datetime_value = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filename = f"img_{datetime_value}.jpg"
    filepath = f"{photo_folder}/{filename}"
    log_file = "/home/haggard/Desktop/Final_Project/photo_logs.txt"

    # Take a photo
    camera.take_photo(filepath)
    print("Photo was taken")

    # Save photo path and name to log file if file does not exist
    isFile = os.path.isfile(log_file)
    if isFile:
        os.remove(log_file)
        print("Previous log file was removed")
    with open(log_file, mode="a") as file:
        file.write(f"{filepath}\n")

def send_photo_by_email():
    yag_mail = yagmail.SMTP(email, password)
    yag_mail.send(to=email, 
              subject="Motion Alert!", 
              contents="Motion was detected. Check image captured by camera in attachment",
              attachments=filepath)
    print("Email alert has been sent")

pir.when_motion = motion_detected
pir.when_no_motion = motion_finished
pause()