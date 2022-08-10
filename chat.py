import socket
import rsa
import pickle
from threading import Thread

'''
Autores: Gustavo Soares
'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 7777
size = 512

def genMyKeys():
  return rsa.newkeys(int(size))

def sendMyPubKey(pub, conn):
  conn.send(pickle.dumps(pub))

def getTheOtherPubKey(conn):
  pubkey_aux = conn.recv(1024)

  return pickle.loads(pubkey_aux)

def writeMessage(conn, other_pub):
  message = input(str('\n<<< (You): \n'))
  if message == 'bye':
    conn.close()
  message = rsa.encrypt(message.encode('utf-8'), other_pub)
  conn.send(message)

def receiveMessage(conn, pri):
  while 1:
    message_recv = conn.recv(1024)
    message_recv = rsa.decrypt(message_recv, pri)
    if not message_recv: break
    print('\n>>>', message_recv)
    print('\n<<< (You):')
  conn.close()

choice = input('([1] for make connection or [2] for wait connection): ')
(pub, pri) = genMyKeys()

print("Pra sair do chat digite: CTRL + C ou digite bye.\n")

if choice == '1':
  s.connect((host, port))

  # Transferencias de public key
  sendMyPubKey(pub, s)
  other_pub = getTheOtherPubKey(s)

  while 1:
    '''No envio de mensagem do client, eu passo como
    parametro o s (socket.socket)'''
    writeMessage(s, other_pub)
    Thread(target=receiveMessage, args=(s,pri,)).start()

if choice == '2':
  s.bind((host, port))
  s.listen(1)
  conn, addr = s.accept()

  # Transferencias de public key
  other_pub = getTheOtherPubKey(conn)
  sendMyPubKey(pub, conn)

  while 1:
    '''NO envio de mensagem do server, eu posso como
    parametro o conn'''
    Thread(target=receiveMessage, args=(conn,pri,)).start()
    writeMessage(conn, other_pub)
