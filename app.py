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
        #mainThr = threading.Thread(target=Main_Thread_Fun,args=(conn,))
        #mainThr.start()
        print 'accept'+ str(address)
        
    print 'close && exit\r\n'
    sock.close()
    sys.exit()
if __name__ == '__main__':
    run()
    
