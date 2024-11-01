# encoding: utf-8
r"""
  __         .__                                      
_/  |_  ____ |  |   ____   ________________    _____  
\   __\/ __ \|  | _/ __ \ / ___\_  __ \__  \  /     \ 
 |  | \  ___/|  |_\  ___// /_/  >  | \// __ \|  Y Y  \
 |__|  \___  >____/\___  >___  /|__|  (____  /__|_|  /
           \/          \/_____/            \/      \/ 
                   .______.                           
  _____   ____   __| _/\_ |__  __ __  ______          
 /     \ /  _ \ / __ |  | __ \|  |  \/  ___/          
|  Y Y  (  <_> ) /_/ |  | \_\ \  |  /\___ \           
|__|_|  /\____/\____ |  |___  /____//____  >          
      \/            \/      \/           \/ 

this module provides a simple encapsulation for modbus on lora
"""
"""
author: vectorwang@hotmail.com
change_history:
    20230106    remastered by vectorwang
    20230206    write func,
                exception catch in init,
                lock support by vectorwang
    20230415    implemented comments
                by vectorwang
"""

import modbus_tk.defines as df
from modbus_tk import modbus_rtu
from threading import Lock
from functools import wraps
from serial import Serial
from serial import serialutil
from typing import Tuple, List, Dict


# Master modbus obj
MASTER = None
SERIAL = None

telegram_lock = Lock()
# set this var to enable lock
_enable_lock = False
# set this var to enable debug info
_enable_debug_info = False


def lock_addon(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _enable_lock:
            telegram_lock.acquire()
        result = func(*args, **kwargs)
        if _enable_lock:
            telegram_lock.release()
        return result
    return wrapper


def debug_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if _enable_debug_info:
            print(result)
        return result
    return wrapper


@debug_info
@lock_addon
def telegram_modbus_init(
    port:str ="COM1",
    baud:int =115200,
    timeout:float =1.0,
) -> bool:
    """
    init modbus for communication with the USV, thru the lora telegram
    params:
        port, str, com port for the telegram, can be found in 'device manager'
        baud, int, baud rate for the port
        timeout, float, timeout for modbus
    returns:
        bool, if the init process is successful
    """
    global MASTER
    global SERIAL

    try:
        SERIAL = Serial(
            port=port,
            baudrate=baud,
        )
        MASTER = modbus_rtu.RtuMaster(SERIAL)
        MASTER.set_timeout(timeout)
    except serialutil.SerialException:
        return False

    return True


@debug_info
@lock_addon
def telegram_modbus_unit() -> bool:
    """
    uninit the modbus obj
    returns:
        bool, if the unit process is successful
    """
    global MASTER
    global SERIAL

    if MASTER:
        try:
            MASTER.close()
            SERIAL.close()
        except:
            return False

    return True     # if master not inited or closed


@debug_info
@lock_addon
def telegram_modbus_query(
    slave_id: int,
    start_address: int,
    data_length: int,
) -> Tuple:
    """
    send a query command to the USV
    params:
        slave_id, int
        start_address, int
        data_length: int
    returns:
        q_result, bool, if the query was successful
        response, list of ints, status of the USV if query was successful
    """
    global MASTER
    q_result = True     # query result
    response = None

    try:
        response = MASTER.execute(
                slave_id,       # slave id
                df.READ_HOLDING_REGISTERS,  # action
                start_address,       # start reg address
                data_length,       # data length
        )
    except:
        q_result = False

    return q_result, response


@debug_info
@lock_addon
def telegram_modbus_write(
    slave_id: int,
    start_address: int,
    data: List[int],
) -> Tuple:
    """
    send a write command to the USV
    params:
        slave_id, int
        start_address, int
        data, a list of ints
    returns:
        w_result, bool, if the write process was successful
        response, list of ints, status of the USV if query was successful
            None otherwise
    """
    global MASTER
    w_result = True     # query result
    response = None

    try:
        response = MASTER.execute(
                slave_id,       # slave id
                df.WRITE_MULTIPLE_REGISTERS,  # action
                start_address,       # start reg address
                output_value=data,       # data
        )
    except:
        w_result = False

    return w_result, response
