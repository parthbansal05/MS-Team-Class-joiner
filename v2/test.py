import pyautogui as keys
from datetime import datetime
import time
import json

keys.PAUSE = 1


def keyPress_hold(hotkey, key):
    keys.keyDown(str(hotkey))
    keys.press(str(key))
    keys.keyUp(str(hotkey))


def dist_calc(img):
    cord_x = []
    cord_y = []
    cord = []
    base_x = 0
    dist_x = 0
    base_y = 0
    dist_y = 0
    for box in keys.locateAllOnScreen(img):
        cord_x.append(keys.center(box)[0])
        cord_y.append(keys.center(box)[1])
    base_x = cord_x[0]
    dist_x = int(0.835*base_x)
    base_y = cord_y[0]+30
    dist_y = int(1.31*base_y)
    temp_x = []
    temp_y = []
    for i in range(10):
        temp_x.append(base_x+i*dist_x)
        temp_y.append(base_y+i*dist_y)
    cord.append(temp_x)
    cord.append(temp_y)
    return(cord)


def multi_loc(img):
    cord_x = []
    cord_y = []
    cord = []
    for box in keys.locateAllOnScreen(img):
        cord_x.append(keys.center(box)[0])
        cord_y.append(keys.center(box)[1])
    cord.append(cord_x)
    cord.append(cord_y)
    return(cord)


def join_class(json_obj):
    short_menue = "short_menue.png"
    short_menue_l = "short_menue_l.png"
    teams_key = "teams_key.png"
    teams_key_l = "teams_key_l.png"
    init_join_key = "init_join_key.png"
    init_join_key_stacked = "init_join_key_stacked.png"
    sec_join_key = "sec_join_key.png"
    team_mic_on = "team_mic_on.png"
    keyPress_hold("win", 2)
    loc = keys.locateCenterOnScreen(teams_key)
    keys.click(loc)
    keys.click(loc)
    keys.click(loc)
    cords = dist_calc(short_menue)
    keys.click(cords[0][json_obj["number"]], cords[1][json_obj["row"]])
    time.sleep(5)
    cords = multi_loc(init_join_key)
    cords_stacked = multi_loc(init_join_key_stacked)
    if (len(cords[0]) == 1):
    # if(True):
        keys.click(cords[0][0], cords[1][0])
        time.sleep(10)
        cords = multi_loc(sec_join_key)
        keys.click(cords[0][0], cords[1][0])
        time.sleep(10)
        cords = multi_loc(team_mic_on)
        keys.click(cords[0][0], cords[1][0])

    elif(len(cords[0]) != 0):
        if (len(cords_stacked[0]) > 0):
            pass
    else:
        time.sleep(60)
        join_class(json_obj)


def leave_class():
    team_leave_key = "team_leave_key.png"
    teams_key = "teams_key.png"
    loc = keys.locateCenterOnScreen(team_leave_key)
    keys.click(loc)
    keyPress_hold("win", 2)
    loc = keys.locateCenterOnScreen(teams_key)
    keys.click(loc)
    keys.click(loc)


def stay(json_obj):
    team_leave_key = "team_leave_key.png"
    loc = keys.locateCenterOnScreen(team_leave_key)
    if loc != None:
        print("staying")
        pass
    else:
        print("rejoining")
        join_class(json_obj)


def main():
    time_table = ""
    curr_day = datetime.today().strftime('%A')
    with open("tt.json", "r") as read_file:
        time_table_temp = json.load(read_file)
    time_table = time_table_temp[0]["days"][curr_day][0]
    for i in range(0, 7):
        table_ref = time_table["time"][i]
        time_ref = int(time.strftime('%H%M'))
        if (int(table_ref["class"]) and (int(table_ref["start"]) <= time_ref) and (int(table_ref["end"]) > time_ref)):
            join_class(time_table["time"][i])
        while (int(table_ref["end"]) > time_ref):
            time.sleep(5*60)
            # time.sleep(5)
            stay(time_table["time"][i])
            time_ref = int(time.strftime('%H%M'))
        leave_class()


main()
time.sleep(20)
