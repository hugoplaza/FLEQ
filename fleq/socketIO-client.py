from socketIO_client import SocketIO

with SocketIO('localhost', 8010) as socketIO:
    socketIO.emit('aaa')
    socketIO.wait(seconds=1)