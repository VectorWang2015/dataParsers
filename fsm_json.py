# encoding: utf-8
r"""
     ____.                                       
    |    | __________   ____                     
    |    |/  ___/  _ \ /    \                    
/\__|    |\___ (  <_> )   |  \                   
\________/____  >____/|___|  /                   
              \/           \/                    
___________.__       .__  __                     
\_   _____/|__| ____ |__|/  |_  ____             
 |    __)  |  |/    \|  \   __\/ __ \            
 |     \   |  |   |  \  ||  | \  ___/            
 \___  /   |__|___|  /__||__|  \___  >           
     \/            \/              \/            
  _________ __          __                       
 /   _____//  |______ _/  |_  ____               
 \_____  \\   __\__  \\   __\/ __ \              
 /        \|  |  / __ \|  | \  ___/              
/_______  /|__| (____  /__|  \___  >             
        \/           \/          \/              
   _____                .__    .__               
  /     \ _____    ____ |  |__ |__| ____   ____  
 /  \ /  \\__  \ _/ ___\|  |  \|  |/    \_/ __ \ 
/    Y    \/ __ \\  \___|   Y  \  |   |  \  ___/ 
\____|__  (____  /\___  >___|  /__|___|  /\___  >
        \/     \/     \/     \/        \/     \/ 

this module provides a json finite state machine
"""
"""
author: vectorwang@hotmail.com
change_history:
    20230408    created by vectorwang
    20230415    added comments by vectorwang
"""

import json


class JSON():
    """
    finite state machine for json
    usage:
        feed str into parse_chs(),
        will return a list of parsed msg, if any
    """
    # states setup
    waitingStart = 0
    waitingEnd = 1

    def __init__(self):
        """
        init states, transitions etc.
        """
        self.message = ""
        self.brace_count = 0
        self.state = self.waitingStart

    def _clear_message(self):
        """
        clear cache
        """
        self.message = ""
        self.brace_count = 0

    def parse_ch(self, ch):
        """
        feed a char into finite state machine
        will return a parsed dict of data
        if this char is the last char of a complete message
        params:
            ch, char, string with length 1
        returns:
            none or list[dict] with length 1, parsed data
        """
        if ch == "{":
            if self.state == self.waitingStart:
                self._clear_message()
                self.state = self.waitingEnd
                self.message += ch
                self.brace_count += 1
                return None
            else:
                self.message += ch
                self.brace_count += 1
                return None
        elif ch == "}":
            if self.state == self.waitingStart:
                return None
            else:
                self.message += ch
                self.brace_count -= 1
                if self.brace_count == 0:
                    self.state = self.waitingStart
                    return [json.loads(self.message)]
                return None
        else:
            if self.state == self.waitingStart:
                return None
            else:
                self.message += ch
                return None

    def parse_chs(self, chs):
        """
        feed a string into finite state machine
        will return a list of parsed dicts
        if this string contains one or more complete message
        params:
            chs, chars, string
        returns:
            none or dict, parsed data
        """
        results = []
        for ch in chs:
            msg = self.parse_ch(ch)
            if msg:
                results.append(msg[0])

        return results
