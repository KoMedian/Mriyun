import pyautogui
import time


time.sleep(5)

for i in range(0,50):
    pyautogui.typewrite(f"Happy Birthday Kuhi!")
    pyautogui.press("enter")
