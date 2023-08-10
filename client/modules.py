class command:
    def use(self):
        pass

class lfile(command):
    def use(self, bs, args):
        if len(args)==2:
            for i in bs.recvFile(args[1]):
                if i=='Ok!' or i=='Wrong!':
                    break

class sfile(command):
    def use(self, bs, args):
        if len(args)==2:
            for i in bs.sendFile(args[1]):
                if i=='Ok!' or i=='Wrong!':
                    break

commands = {'sfile':sfile(), 'lfile':lfile()}