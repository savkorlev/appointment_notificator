from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
import logging
import random
import pygame.mixer

logging.basicConfig(level=logging.INFO)

pygame.mixer.init()
sound = pygame.mixer.Sound('resources/Anthem of Europe.mp3')

with open('resources/url.txt', 'r') as file:
    url = file.read()

service = Service(executable_path='chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get(url)

user_input = input('Enter "p" to proceed: ')

if user_input.lower() == 'p':
    while True:
        time.sleep(random.uniform(60, 120))
        if len(driver.find_elements(By.XPATH, '//span[text()="0/30"]')) == 15:
            logging.info('No Available Appointment :(')
            driver.refresh()
        else:
            logging.info('Available Appointment Found :)')
            while True:
                sound.play()
                time.sleep(sound.get_length())
