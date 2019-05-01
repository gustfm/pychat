import socket
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 7777

def writeMessage(conn):
  message = input(str('\n<<< (You): \n'))
  if message == 'shutdown -c':
    message = message.encode()
    conn.send(message)
    conn.close()
  message = message.encode()
  conn.send(message)

def receiveMessage(conn):
  while 1:
    message_recv = conn.recv(1024)
    if not message_recv or message_recv.decode() == 'shutdown -c': break
    message_recv = message_recv.decode()
    print('\n>>>', message_recv)
    print('\n<<< (You):')
  conn.close()

choice = input('([1] for make connection or [2] for wait connection): ')

if choice == '1':
  s.connect((host, port))

  while 1:
    '''No envio de mensagem do client, eu passo como
    parametro o s (socket.socket)'''
    writeMessage(s)
    Thread(target=receiveMessage, args=(s,)).start()

if choice == '2':
  s.bind((host, port))
  s.listen(1)
  conn, addr = s.accept()

  while 1:
    '''NO envio de mensagem do server, eu posso como
    parametro o conn'''
    Thread(target=receiveMessage, args=(conn,)).start()
    writeMessage(conn)