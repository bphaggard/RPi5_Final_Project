from flask import Flask
import os

log_file = "/home/haggard/Desktop/Final_Project/photo_logs.txt"
camera_folder_path = "/home/haggard/Desktop/Final_Project/photos"
previous_line_count = 0

app = Flask(__name__, static_url_path=camera_folder_path, static_folder=camera_folder_path)

@app.route("/")
def index():
    return "Hello from Flask"

@app.route("/check-photos")
def check_photos():
    global previous_line_count
    line_count = 0
    if os.path.exists(log_file):
        with open(log_file) as file:
            for line in file:
                line_count += 1
                last_photo_file_name = line.rstrip()
            
        difference = line_count - previous_line_count
        previous_line_count = line_count
        message = str(difference) + " new photos since you last checked <br/>"
        message += "Last photo: " + last_photo_file_name + "<br/>"
        message += "<img src=\"" + last_photo_file_name + "\">"
        return message
    else:
        return "No photos available"

app.run(host="0.0.0.0")