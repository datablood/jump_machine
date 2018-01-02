#-*- coding:utf-8 -*-
import numpy as np
import subprocess
from PIL import Image
import time
import copy

PRESSTIME = [300, 500, 600, 700, 800, 900, 1000, 1100]


class GameState:
    def __init__(self):
        self.xbegin, self.ybegin = get_beginbutton()

    def frame_step(self, input_actions):
        reward = 0.1
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        action_index = np.argmax(input_actions)
        presstime = PRESSTIME[action_index]


        im_begin= get_im()
        isCrash_begin = checkCrash(im_begin)
        if isCrash_begin:
            jump(20,self.xbegin,self.ybegin)
            print 'play again'
            im_begin=get_im()
            return self.frame_step(input_actions)
        else:
            jump(presstime,5,5)
        im_end= get_im()
        isCrash_end = checkCrash(im_end)
        if isCrash_end :
            terminal = True
            reward = -1
        else :
            reward = 1

        image_data = im_begin
        return image_data, reward, terminal

def jump(presstime,xbegin,ybegin):
    cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=xbegin,
        y1=ybegin,
        x2=xbegin,
        y2=ybegin,
        duration=presstime)
    subprocess.call(cmd,shell=True)
    time.sleep(6)
    get_screenshot()

def get_im():
    im = Image.open('./data/jump_temp.png')
    return copy.deepcopy(np.array(im))

def get_screenshot():
    retcode = 0
    retcode += subprocess.call(
        'adb shell screencap -p /sdcard/jump_temp.png', shell=True)
    retcode += subprocess.call(
        'adb pull /sdcard/jump_temp.png ./data/', shell=True)
    if retcode != 0:
        subprocess.call('adb kill-server', shell=True)
        subprocess.call('adb devices', shell=True)
        get_screenshot()


# 获取按键位置
def get_beginbutton():
    print 'get begin button'

    get_screenshot()
    im = Image.open('./data/jump_temp.png')
    w, h = im.size
    x = w / 2
    y = 1003 * (h / 1280.0) + 10
    return x, y



def checkCrash(arrim):
    # arrim = np.array(im)
    print arrim.mean()
    if arrim.mean() < 138:
        return True
    return False
