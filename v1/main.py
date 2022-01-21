from ast import For
from ctypes import windll, Structure, c_long, byref
import ctypes
from imp import IMP_HOOK
from ntpath import join
import time
import json
from datetime import datetime
import numpy as np
import cv2
from pytesseract import*
import pyautogui
from _thread import *
import matplotlib.pyplot as plt

holdoff_delay = 2

SendInput = ctypes.windll.user32.SendInput
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
M = 0x32
K = 0x25
# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt
    # return { "x": pt.x, "y": pt.y}/


def hold_move(x, y, X, Y):
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
    ctypes.windll.user32.SetCursorPos(X, Y)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002,
                        0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def click(x, y):
    # convert to ctypes pixels
    # x = int(x * 0.666)
    # y = int(y * 0.666)
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up


def moveMouseTo(x, y):
    # convert to ctypes pixels
    # x = int(x * 0.666)
    # y = int(y * 0.666)
    print(x, y)
    ctypes.windll.user32.SetCursorPos(x, y)
    # ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
    # ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


# def IOT_f(data):
#     global data_curr_client
#     ID_temp = data['ID']
#     dev_temp = data['dev']
#     state_temp = data['state']
#     for i in range(len(dev_temp)):
#         data_curr_client['data'][ID_temp]['state'][dev_temp[i]] = state_temp
#         data_curr_client['data'][ID_temp]['user'][dev_temp[i]] = 1
#     w_json(init_client_path, data_curr_client)


# def w_json(file_name, data):

#     with open(file_name, "w") as write_file:
#         json.dump(data, write_file)


def join_class(class_obj):
    print(class_obj)
    click(260, 1050)
    time.sleep(holdoff_delay)
    click(30, 115)
    time.sleep(holdoff_delay)
    click(30, 115)
    time.sleep(holdoff_delay)
    click((160+228*class_obj["number"]), 243+209*class_obj["row"])
    time.sleep(holdoff_delay)

    pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    cv2.imwrite("te.jpg", screen)
    ss = cv2.imread('te.jpg', 0)
    plt.imshow(ss)
    plt.grid()
    plt.show()

    metting_no_image = ss[100:120, 1633:1647]
    plt.imshow(metting_no_image)
    plt.grid()
    plt.show()

    no_mettings = image_to_string(metting_no_image, config='--psm 6')
    print(no_mettings)
    # if  no_mettings.findall('[0-9]+', 'dfgh3'):
    #     pass

    join_area = ss[90:870, 750:850]
    results = image_to_data(
        ss, output_type=Output.DICT, config='--psm 6')
    for i in range(0, len(results["text"])):
        x = results["left"][i]+620
        y = results["top"][i]+90
        w = results["width"][i]
        h = results["height"][i]

        text = results["text"][i]
        conf = results["conf"][i]

        if text=="join":
            print("Confidence: {}".format(conf))
            print("Text: {}".format(text))
            print("x:{} y:{}".format(x, y))
            print("")

            text = "".join(text).strip()
            cv2.rectangle(screen,(x, y),(x + w, y + h),(0, 0, 255), 2)
            cv2.putText(screen,text,(x, y - 10),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 255), 3)
            click(x, y)
            time.sleep(holdoff_delay)
            click(1340, 665)

    # After all, we will show the output image
    cv2.imshow("Image", screen)
    cv2.waitKey(0)

    time.sleep(1000)


def main():
    time_table = ""
    curr_day = datetime.today().strftime('%A')
    with open("tt.json", "r") as read_file:
        time_table_temp = json.load(read_file)
    time_table = time_table_temp[0]["days"][curr_day][0]
    for i in range(0, 7):
        if ((int(time_table["time"][i]["start"]) <= int(time.strftime('%H%M'))) and (int(time_table["time"][i]["end"]) > int(time.strftime('%H%M')))):
            join_class(time_table["time"][i])


main()
# print()
