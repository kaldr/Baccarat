import pyautogui

pyautogui.size()
# (1366, 768)
width, height = pyautogui.size()
print(width, height)

for i in range(10):
    print('移动到300，300')
    pyautogui.moveTo(300, 300, duration=0.25)
    print('移动到400，300')
    pyautogui.moveTo(400, 300, duration=0.25)
    print('移动到400，400')
    pyautogui.moveTo(400, 400, duration=0.25)
    print('移动到300，400')
    pyautogui.moveTo(300, 400, duration=0.25)