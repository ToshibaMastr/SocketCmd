from bestSocket import BestSocket
from bCCmd import BCCmd
from modules import execute

#/lfile c:\Users\ggost\Downloads\2267231.jpg 22.jpg
#Toshiba - лучшая компания, ToshibaMastru - хороший человек)
print('\033[0m  ______\033[90m____  _____ __  __________  ___ \033[0m   _ _\n /_  __/\033[90m __ \/ ___// / / /  _/ __ )/   |\033[0m  / V \\\n  / /\033[90m / / / /\__ \/ /_/ // // __  / /| |\033[0m  | \033[90mM\033[0m |\n / /\033[90m / /_/ /___/ / __  // // /_/ / ___ |\033[0m  \\   /\n/_/\033[90m  \____//____/_/ /_/___/_____/_/  |_|\033[0m   \\_/\n')

URL = '127.0.0.1'
PORT = 9090

bs = BestSocket(URL, PORT, 'server')
bc = BCCmd()

execute('findconn', bc, bs)
execute('setconn 0', bc, bs)

bc.newLine()

while True:
    try:
        tp, text = bs.recvMsg()
        match tp:
            case '|O':  # Текстовая информация
                bc.write(text)
            case '|E':  # Текстовая информация (ошибки)
                bc.error(text)
            case '_ ':  # Ждёт ответа сервера
                com = bc.read()
                if com and com[0] == '/':
                    execute(com[1:], bc, bs)
                    bc.newLine()
                else:
                    bs.send(com+'\n')
    except (ConnectionResetError):
        bc.error('Соединение потеряно!\n')

        bc.newLine()

        bs.delConnection()

        execute('findconn', bc, bs)
        execute('setconn 0', bc, bs)

        bc.newLine()
