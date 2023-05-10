import os
import time
import smtplib
import picamera
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

camera = picamera.PiCamera()
camera.resolution = (1024, 768)


pir_pin = 14

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = '1032201793@mitwpu.edu.in'
smtp_password = '2bTIk601#45ZeHd'
from_email = smtp_username
to_email = '1062190962@mitwpu.edu.in'

print("PIR sensor warming up...")
time.sleep(10)
print("PIR sensor ready.")

while True:
   
    while True:
        if GPIO.input(pir_pin):
            break
        time.sleep(0.1)

    
    print("Motion detected!")
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"image_{timestamp}.jpg"
    camera.capture(filename)

    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"Motion detected at {timestamp}"
    msg.attach(MIMEText('Motion detected!'))
    with open(filename, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name=os.path.basename(filename))
    msg.attach(image)

    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
    print("Email sent.")

    time.sleep(5)