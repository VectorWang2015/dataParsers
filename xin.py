# encoding: utf-8
r"""
____  ___.__         
\   \/  /|__| ____   
 \     / |  |/    \  
 /     \ |  |   |  \ 
/___/\  \|__|___|  / 
      \_/        \/ 

this module provides supports for xbox controller
"""
"""
author: vectorwang@hotmail.com
change_history:
    20230225    re-organized by vectorang

reference:
https://zhuanlan.zhihu.com/p/444431769
https://docs.microsoft.com/en-us/windows/win32/xinput/getting-started-with-xinput
"""

import time
import ctypes
from ctypes import wintypes
from typing import Dict

# buttons
BTN_MASKS = {
    "DPAD_UP" : 0x0001,
    "DPAD_DOWN" : 0x0002,
    "DPAD_LEFT" : 0x0004,
    "DPAD_RIGHT" : 0x0008,
    "START" : 0x0010,
    "BACK" : 0x0020,
    "LEFT_THUMB" : 0x0040,
    "RIGHT_THUMB" : 0x0080,
    "LEFT_SHOULDER" : 0x0100,
    "RIGHT_SHOULDER" : 0x0200,
    "A" : 0x1000,
    "B" : 0x2000,
    "X" : 0x4000,
    "Y" : 0x8000,
}


class XINPUT_GAMEPAD(ctypes.Structure):
    """to map to dll"""
    _fields_ = [
        ('wButtons', wintypes.WORD),
        ('bLeftTrigger', ctypes.c_ubyte),  # wintypes.BYTE is signed
        ('bRightTrigger', ctypes.c_ubyte),  # wintypes.BYTE is signed
        ('sThumbLX', wintypes.SHORT),
        ('sThumbLY', wintypes.SHORT),
        ('sThumbRX', wintypes.SHORT),
        ('sThumbRY', wintypes.SHORT)
    ]


class XINPUT_STATE(ctypes.Structure):
    """to map to dll"""
    _fields_ = [
        ('dwPacketNumber', wintypes.DWORD),
        ('Gamepad', XINPUT_GAMEPAD)
    ]


def _get_state(user_index):
    """query api and returns xbox input result"""
    xinput = ctypes.windll.XInput1_4
    c_state = XINPUT_STATE()
    ret = xinput.XInputGetState(user_index, ctypes.byref(c_state))
    # ret shows whether query was successful
    # c_state is current xin state
    return ret, c_state


def get_state(user_index=0) -> Dict:
    """call this func to get xinput"""
    ret, c_state = _get_state(user_index)
    packet_num = c_state.dwPacketNumber
    gamepad = c_state.Gamepad

    gamepad_buttons = gamepad.wButtons
    gamepad_state_dict = {
        "l_trigger" : gamepad.bLeftTrigger,
        "r_trigger" : gamepad.bRightTrigger,
        "l_x" : gamepad.sThumbLX,
        "l_y" : gamepad.sThumbLY,
        "r_x" : gamepad.sThumbRX,
        "r_y" : gamepad.sThumbRY,
    }

    for btn_name in BTN_MASKS.keys():
        gamepad_state_dict[btn_name] = \
            True if gamepad_buttons & BTN_MASKS[btn_name] \
            else False

    return gamepad_state_dict
