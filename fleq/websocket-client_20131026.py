#!/usr/bin/env python
# encoding: utf-8

# import websocket, httplib, sys, asyncore
#  
# 
# def connect():
#     
#     print "connecting..."
#     conn  = httplib.HTTPConnection("localhost:8004")
#     conn.request('GET','/socket.io/1/')
#     print "connected"
#     resp  = conn.getresponse() 
#     print "RESP"
# 
#     hskey = resp.read()
#     hskey2 = ''.join(hskey).split(':')[0]
#     print "HSKEY"
#     print hskey
#     print hskey2
#     print "--------------------------"
#     ws = websocket.create_connection('ws://localhost:8004/socket.io/1/websocket/'+hskey2)
#     
#     return ws
#  
# 
#     
# ws = connect()
# ws.send("FLEQBOT2")
# ws.close()

import httplib
import websocket
import threading
import time


global ws


def on_message(ws, message):
    print "MESSAGE: " + message
    #msg = '3:1::Recibido'
    #print msg
    
    time.sleep(3)
    
    if message == "2::":
        ws.send(message)
        return
    
    if message == '3:::{"code":"1"}':
        msg = '3:::{"code": "2", "room": "2", "user": "FLEQBOT", "message": "hola"}'
        ws.send(msg)
        return
    else:
        msg = '3:::{"code": "1", "room": "2", "user": "FLEQBOT"}'
        ws.send(msg)

    

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    #msg = '1::/'
    #print msg
    #ws.send(msg)
    None


class send_ping(threading.Thread):
    def run(self):

        while True:
            time.sleep(15)
            ws.send("2::")
            print "PING SENT"


if __name__ == "__main__":

    conn  = httplib.HTTPConnection("localhost:8004")
    conn.request('GET','/socket.io/1/')
    resp  = conn.getresponse() 
 
    hskey = resp.read()
    hskey2 = ''.join(hskey).split(':')[0]    
    

    #websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("ws://localhost:8004/socket.io/1/websocket/" + hskey2,
#                                 on_message = on_message,
#                                 on_error = on_error,
#                                 on_close = on_close)
    #ws.on_open = on_open

    #ws.run_forever()
    
    
    
    ws = websocket.create_connection('ws://localhost:8004/socket.io/1/websocket/'+hskey2)
    
    print "WEBSOCKET CREATED"
    
    ping = send_ping()
    ping.start()
    
    print "THREAD STARTED"
    
    data = ws.recv()
    
    print data
    
    ws.send('3:::{"code": "1", "room": "2", "user": "FLEQBOT"}')

    data = ws.recv()

    print data

    if data== '3:::{"code":"1"}':
        ws.send('3:::{"code": "2", "room": "2", "user": "FLEQBOT", "message": "La partida comenzará en 2 min 30 seg"}')    

    #time.sleep(60)
    
    ws.send('3:::{"code": "2", "room": "2", "user": "FLEQBOT", "message": "Quedan 2 min"}')
