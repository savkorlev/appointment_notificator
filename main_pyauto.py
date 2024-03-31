import subprocess
import pyautogui
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cv2
import numpy
import json

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

# Setting up the MIME
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = 'Appointment found!'
body = 'Appointment found!'
message.attach(MIMEText(body, 'plain'))

chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

subprocess.Popen([chrome_path, target_url])
pyautogui.sleep(5)

pyautogui.click(dropdown_coordinates[0], dropdown_coordinates[1])
pyautogui.press('down')
pyautogui.press('enter')
pyautogui.sleep(30)

pyautogui.click(verification_coordinates[0], verification_coordinates[1])

for i in range(1,6):  # 5 months
    pyautogui.sleep(1)

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
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp-mail.outlook.com', 587)
        session.starttls() # enable security
        session.login(sender_email, sender_password)
        session.sendmail(sender_email, receiver_email, message.as_string())
        print('Mail Sent')
        session.quit()
    else:
        print('No free appointments')
        pyautogui.click(next_coordinates[0], next_coordinates[1])

pyautogui.click(close_coordinates[0], close_coordinates[1])
