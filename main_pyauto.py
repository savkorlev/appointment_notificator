import subprocess
import pyautogui
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cv2
import numpy
import json
import time
import pygame

# Load the input data
with open('resources/input_data.json', 'r') as file:
    input_data = json.load(file)
sender_email = input_data['sender_email']
sender_password = input_data['sender_password']
receiver_email = input_data['receiver_email']
target_url = input_data['target_url']
dropdown_coordinates = input_data['dropdown_coordinates']
verification_coordinates = input_data['verification_coordinates']
screenshot_coordinates = input_data['screenshot_coordinates']
next_coordinates = input_data['next_coordinates']
close_coordinates = input_data['close_coordinates']

def send_email():
    # Setting up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Appointment found!'
    body = 'Appointment found!'
    message.attach(MIMEText(body, 'plain'))
    # Create SMTP session for sending the email
    session = smtplib.SMTP('smtp-mail.outlook.com', 587)
    session.starttls() # enable security
    session.login(sender_email, sender_password)
    session.sendmail(sender_email, receiver_email, message.as_string())
    print('Mail Sent')
    session.quit()

def play_music(file_path, duration_in_seconds):
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the music file
    pygame.mixer.music.load(file_path)
    # Start playing the music
    pygame.mixer.music.play()
    # Play music for the specified duration
    time.sleep(duration_in_seconds)
    # Stop the music
    pygame.mixer.music.stop()

chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

subprocess.Popen([chrome_path, target_url])
time.sleep(5)

pyautogui.click(dropdown_coordinates[0], dropdown_coordinates[1])
time.sleep(1)
pyautogui.press('down')
pyautogui.press('enter')
time.sleep(30)

pyautogui.click(verification_coordinates[0], verification_coordinates[1])
time.sleep(5)

for i in range(1,4):  # 3 months
    time.sleep(1)

    # Step 1: Take a screenshot of a specific area and save it
    screenshot_region = (screenshot_coordinates[0], screenshot_coordinates[1], 595, 128)
    screenshot = pyautogui.screenshot(region=screenshot_region)
    screenshot_path = f'output/table_{i}.png'
    screenshot.save(screenshot_path)

    # Step 2: Load the reference image and the screenshot for comparison
    reference_path = f'resources/table_{i}.png'
    reference_image = cv2.imread(reference_path)
    screenshot_image = cv2.imread(screenshot_path)
    # Step 3: Compare the images (simple absolute difference here, can be more complex)
    # Convert images to grayscale for simpler comparison
    reference_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)
    difference = cv2.absdiff(reference_gray, screenshot_gray)

    if numpy.any(difference):
        print('Appointment found!')
        send_email()
        play_music('resources/Anthem of Europe.mp3', 60)
    else:
        print('No free appointments')

    pyautogui.click(next_coordinates[0], next_coordinates[1])

pyautogui.click(close_coordinates[0], close_coordinates[1])
