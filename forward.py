#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import time
import threading
import traceback
import errno
import sys
 
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
            if not data:
                print 'remoteSock:' + str(remoteSock)+' recv 0 will Close.'
                break
            conn.send(data)
        except Exception as e:
            print str(e)
            print errno.errorcode[e.errno]
            print 'format_exc():\r\n',traceback.format_exc()
            break
    remoteSock.close()
    print  'remoteSock.close()'
    remoteSock = None
    conn.close()
    print  'conn.close()'
    conn = None
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
        print 'connect'+str(forward_EP)
        remoteSock.connect(forward_EP)
        print 'remoteSock:' + str(remoteSock.getpeername())
    except Exception as e:
        print str(e)
        print errno.errorcode[e.errno]
        print 'format_exc():\r\n',traceback.format_exc()
        remoteSock.close()
        conn.close()
        return
    conn.send(bytes(response_str))
    remote_thr = threading.Thread(target=Thread_RemoteRecv_Fun,args=(conn,remoteSock,))
    remote_thr.daemon = True
    remote_thr.start()
    while True:
        try:
            data = conn.recv(8192)
            if not data:
                print 'conn:' + str(conn)+' recv 0 will Close.'
                break
            remoteSock.send(data)
        except Exception as e:
            print str(e)
            print errno.errorcode[e.errno]
            print 'format_exc():\r\n',traceback.format_exc()
            break

    remoteSock.shutdown(socket.SHUT_RDWR)
    remoteSock.close()
    print  'remoteSock.close()'
    remoteSock = None
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    print  'conn.close()'
    conn = None
    return
 
def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverPort = 36000
    try:
        sock.bind(('127.0.0.1', serverPort))
        sock.listen(5)
        print 'listen '+str(sock.getsockname())
    except Exception as e:
        print str(e)
        print errno.errorcode[e.errno]
        print 'format_exc():\r\n',traceback.format_exc()
        return
        
    while True:
        try:
            conn, address = sock.accept()
        except KeyboardInterrupt:
            print  'Input KeyboardInterrupt'
            break;
        except:
            print 'format_exc():\r\n',traceback.format_exc()
            continue
        mainThr = threading.Thread(target=Main_Thread_Fun,args=(conn,))
        mainThr.start()
        print 'accept'+ str(address)
        
    print 'close && exit\r\n'
    sock.close()
    sys.exit()
if __name__ == '__main__':
    run()
    