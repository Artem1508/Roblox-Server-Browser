import pyautogui
from time import sleep
def open_browser():
    pyautogui.press("win")
    sleep(1)
    pyautogui.typewrite("chrome.exe")
    sleep(1)
    pyautogui.press("enter")

def navigate_to_url(url):
    pyautogui.hotkey('ctrl', 't')
    pyautogui.typewrite(url)
    sleep(2)