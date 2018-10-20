#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import time
import threading
import traceback
import errno
import sys
 
def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverPort = 8080
    try:
        sock.bind(('127.0.0.1', serverPort))
        sock.listen(5)
    except Exception as e:
        return
        
    while True:
        try:
            conn, address = sock.accept()
        except KeyboardInterrupt:
            break;
        except:
            continue
        #mainThr = threading.Thread(target=Main_Thread_Fun,args=(conn,))
        #mainThr.start()
    sock.close()
    sys.exit()
if __name__ == '__main__':
    run()
    
