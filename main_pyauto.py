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
import sys

# Load the input data
with open('resources/input_data.json', 'r') as file:
    input_data = json.load(file)
sender_email = input_data['sender_email']
sender_password = input_data['sender_password']
receiver_email = input_data['receiver_email']
target_url = input_data['target_url']
dropdown_coordinates = input_data['dropdown_coordinates']
verification_coordinates = input_data['verification_coordinates']
table_coordinates = input_data['table_coordinates']
mainpage_coordinates = input_data['mainpage_coordinates']
next_coordinates = input_data['next_coordinates']
close_coordinates = input_data['close_coordinates']

def take_screenshot(region_coordinates, screenshot_path):
    screenshot_region = (region_coordinates[0], region_coordinates[1], region_coordinates[2], region_coordinates[3])
    screenshot = pyautogui.screenshot(region=screenshot_region)
    screenshot.save(screenshot_path)

def compare_images(screenshot_path, reference_path):
    # Load the images
    screenshot_image = cv2.imread(screenshot_path)
    reference_image = cv2.imread(reference_path)
    # Convert them to grayscale
    screenshot_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)
    reference_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    # Find the difference
    difference = cv2.absdiff(screenshot_gray, reference_gray)
    if numpy.any(difference):
        return True
    else:
       return False

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
time.sleep(10)

mainpage_region = (mainpage_coordinates[0], mainpage_coordinates[1], mainpage_coordinates[2], mainpage_coordinates[3])
screenshot_path = 'output/mainpage.png'
take_screenshot(mainpage_region, screenshot_path)
reference_path = 'resources/mainpage.png'
difference = compare_images(screenshot_path, reference_path)
if difference:
    print('Error while loading the page, exiting the script.')
    pyautogui.click(close_coordinates[0], close_coordinates[1])
    sys.exit()

pyautogui.click(dropdown_coordinates[0], dropdown_coordinates[1])
time.sleep(1)
pyautogui.press('down')
pyautogui.press('enter')
time.sleep(1)  # TODO: improve

pyautogui.click(verification_coordinates[0], verification_coordinates[1])
pyautogui.moveTo(1, 1)
time.sleep(5)

for i in range(1,3):  # 2 months
    time.sleep(1)

    table_region = (table_coordinates[0], table_coordinates[1], table_coordinates[2], table_coordinates[3])
    screenshot_path = f'output/table_{i}.png'
    take_screenshot(table_region, screenshot_path)
    reference_path = f'resources/table_{i}.png'
    difference = compare_images(screenshot_path, reference_path)
    if difference:
        print('Appointment found!')
        send_email()
        play_music('resources/Anthem of Europe.mp3', 60)
        break
    else:
        print('No free appointments')

    pyautogui.click(next_coordinates[0], next_coordinates[1])

pyautogui.click(close_coordinates[0], close_coordinates[1])
