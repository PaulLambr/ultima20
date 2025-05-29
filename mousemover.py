import pyautogui
import time
import random

def jiggle_mouse(interval=5):
    print("Mouse jiggler started. Press Ctrl+C to stop.")
    while True:
        x_move = random.randint(-50, 50)
        y_move = random.randint(-50, 50)

        pyautogui.moveRel(x_move, y_move)
        pyautogui.moveRel(-x_move, -y_move)

        time.sleep(interval)

if __name__ == "__main__":
    jiggle_mouse()
