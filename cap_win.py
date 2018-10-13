import os
import pyautogui

os.chdir("screenshot")

def save_screenshot():
    pic = pyautogui.screenshot()
    pic.save('Screenshot.png') 

def get_screenshot():
    pic = pyautogui.screenshot()
    return pic