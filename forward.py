#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import base64
import hashlib
import time
import traceback
import thread
 
def get_headers(data):

    header_dict = {}
    data = str(data)
 
    header, body = data.split('\r\n\r\n', 1)
    header_list = header.split('\r\n')
    for i in range(0, len(header_list)):
        if i == 0:
            if len(header_list[i].split(' ')) == 3:
                header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[i].split(' ')
        else:
            k, v = header_list[i].split(':', 1)
            header_dict[k] = v.strip()
    return header_dict

def Thread_RemoteRecv_Fun(conn,remoteSock): 
    while True:
        try:
            data = remoteSock.recv(8192)
            conn.send(data)
        except:
            print 'format_exc():\r\n',traceback.format_exc()
            remoteSock.close()
            conn.close()
            return
    return
    
def Main_Thread_Fun(conn):
    try:
        data = conn.recv(1024)
    except:
        print 'format_exc():\r\n',traceback.format_exc()
        conn.close()
        return
    headers = get_headers(data)
    response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection:Upgrade\r\n" \
                   "Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=\r\n" \
                   "WebSocket-Location:ws://%s%s\r\n\r\n"
 
    response_str = response_tpl % (headers['Host'], headers['url'])
    
    forwardHost = headers['ForwardHost']
    forwardPort = headers['ForwardPort']
    forward_EP = (forwardHost,int(forwardPort))
    
    remoteSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remoteSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        remoteSock.connect(forward_EP)
    except:
        print 'format_exc():\r\n',traceback.format_exc()
        remoteSock.close()
        conn.close()
        return
    conn.send(bytes(response_str))
    
    thread.start_new_thread(Main_Thread_Fun,(conn,remoteSock))
    
    while True:
        try:
            data = conn.recv(8192)
            remoteSock.send(data)
        except:
            print 'format_exc():\r\n',traceback.format_exc()
            remoteSock.close()
            conn.close()
            return
    return
 
def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print 'bind'
    serverPort = 36000
    try:
        sock.bind(('127.0.0.1', serverPort))
        sock.listen(5)
    except:
        print 'format_exc():\r\n',traceback.format_exc()
        return
        
    while True:
        try:
            conn, address = sock.accept()
        except:
            print 'format_exc():\r\n',traceback.format_exc()
            continue
        thread.start_new_thread(Main_Thread_Fun,(conn))
        print 'accept'+ str(address)
        
    print 'close'
    sock.close()
 
if __name__ == '__main__':
    run()
    