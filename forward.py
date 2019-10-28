#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import threading
import traceback
import errno
import sys
import base64
import Queue
import md5
 
class QueueMsg():
    def __init__(self):        
        self.MsgLength = None
        self.SocketNO = None
        self.CMD = None
        self.MsgData = bytearray()

    def ConvertToBytes(self):
        result = []
        result.extend(Common.Int162Bytes(self.MsgLength))
        result.extend(Common.Int162Bytes(self.SocketNO))
        result.append(self.CMD)
        result.extend(self.MsgData)

        return bytearray(result)
    @staticmethod
    def CreateQueueMsg(data):
        result = []
        useLen = 0
        
        currIndex = 0
        catcheLen = len(data)
        while (catcheLen - currIndex) >= 5 :
            msgLen = (ord(data[currIndex]) << 8) + ord(data[currIndex + 1]) + 2
            if (catcheLen - currIndex) >= msgLen:
                msg = QueueMsg()
                msg.MsgLength = (ord(data[currIndex]) << 8) + ord(data[currIndex + 1])
                currIndex += 2
                msg.SocketNO = (ord(data[currIndex]) << 8) + ord(data[currIndex + 1])
                currIndex += 2
                msg.CMD = ord(data[currIndex])
                currIndex += 1
                msgDataLen = msgLen - 5
                msg.MsgData = bytearray(data[currIndex:currIndex + msgDataLen])
                currIndex += msgDataLen
                result.append(msg)
                useLen += msgLen
            else:
                break

        return result,useLen

class Common():
    def __init__(self):  
        pass
    @staticmethod
    def Int162Bytes(num):
       return [(num >> 8) & 0xFF,num & 0xFF]

class SocketInfo():
    def __init__(self):  
        self.Sockt_Server = None
        self.SocketNO = None
        self.RecvQueue = Queue.Queue()
        self.RecvQueue.maxsize = 30
        self.IsClose = False


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

def Thread_RemoteRecv_Fun(conn,remoteSock,threadFlageKey): 
    remoteSockName = str(remoteSock.getpeername())
    while True:
        try:
            data = remoteSock.recv(8192)
            if not data:
                print(threadFlageKey + 'server remoteSock:' + remoteSockName + ' recv 0 will Close.')
                break
            conn.send(data)
        except Exception as e:
            print(threadFlageKey + str(e))
            print(threadFlageKey + errno.errorcode[e.errno])
            print(threadFlageKey + 'format_exc():\r\n',traceback.format_exc())
            break
    remoteSock.close()
    print(threadFlageKey + 'server remoteSock.close()')
    remoteSock = None
    conn.close()
    print(threadFlageKey + 'client conn.close()')
    conn = None
    return

def Thread_RecvFromServer_V2(conn,socketInfo):
    while True:
        try:
            data = conn.recv(8192)
            #print("从服务器收到数据 "+str(len(data))+"B\r\n")
            if not data:
                print("server recv 0B,close socket to server\r\n")
                print('server ServerSocket: recv 0 will Close.')
                closeMsg = QueueMsg()
                closeMsg.SocketNO = socketInfo.SocketNO
                closeMsg.CMD = 1
                closeMsg.MsgLength = 3
                socketInfo.RecvQueue.put(closeMsg)
                socketInfo.IsClose = True
                break
            forwardMsg = QueueMsg()
            forwardMsg.SocketNO = socketInfo.SocketNO
            forwardMsg.CMD = 2
            forwardMsg.MsgData = bytearray(data) #最大缓存不超过消息最大长度,无需分割
            forwardMsg.MsgLength = 3 + len(data)
            socketInfo.RecvQueue.put(forwardMsg)
            #print("向队列加入消息 2 ,准备发往客户端\r\n")
        except Exception as e:
            print("recv Exception from server,close socket to server\r\n")
            print(str(e))
            print(errno.errorcode[e.errno])
            print('format_exc():\r\n',traceback.format_exc())

            socketInfo.IsClose = True
            closeMsg = QueueMsg()
            closeMsg.SocketNO = socketInfo.SocketNO
            closeMsg.CMD = 1
            closeMsg.MsgLength = 3
            socketInfo.RecvQueue.put(closeMsg)
            print("add msg to Queue type 1 CloseMsg,wait Send \r\n")
            break
    return        

def Thread_SendMsgToClient_V2(conn,socketNODict):
    #lastSendTime = time.time()
    heartbeatMsg = QueueMsg()
    heartbeatMsg.SocketNO = 0
    heartbeatMsg.CMD = 3
    #print "lastTime:" + str(lastSendTime)
    while True:
        isHasMsg = False
        keys = socketNODict.keys()
        for k in keys:
            if socketNODict.has_key(k):
                socketInfo = socketNODict[k]
                isEmpty = socketInfo.RecvQueue.empty()
                if socketInfo.IsClose:
                    print("socket to client Flage Close\r\n")
                    if not isEmpty:
                        while not socketInfo.RecvQueue.empty():
                            closeMsg = socketInfo.RecvQueue.get()
                            if closeMsg.CMD == 1:
                                print("Find Close Msg \r\n")
                                closeData = closeMsg.ConvertToBytes()
                                try:
                                    isHasMsg = True
                                    print("Send Close Msg \r\n")
                                    conn.send(closeData)
                                except Exception as e:
                                    print('Thread_SendMsgToClient_V2 conn.send' + str(e))
                                    print(errno.errorcode[e.errno])
                                    print('format_exc():\r\n',traceback.format_exc())
                                    return
                                break
                        if socketNODict.has_key(k):
                            del socketNODict[k]
                            print("delete closed SocketNo\r\n")
                    else:
                        if socketNODict.has_key(k):
                            del socketNODict[k]
                            print("delete closed SocketNo\r\n")
                else:
                    if not isEmpty:
                        otherMsg = socketInfo.RecvQueue.get()
                        otherData = otherMsg.ConvertToBytes()
                        #print("取得待发送消息 "+ str(otherMsg.CMD) +"\r\n")
                        try:
                            isHasMsg = True
                            conn.send(otherData)
                            #lastSendTime = time.time()
                            #print "conn.send lastTime:" + str(lastSendTime)
                            #print("发送消息 send to Client: " + str(len(otherData))+"B\r\n")
                        except Exception as e:
                            print("send Msg Exception\r\n")
                            print('Thread_SendMsgToClient_V2 conn.send' + str(e))
                            print('format_exc():\r\n',traceback.format_exc())
                            print(errno.errorcode[e.errno])
                            return

        if not isHasMsg:
            #if 3 < (time.time() - lastSendTime):
                #heartbeatMsg.MsgData = Common.Int162Bytes(int(time.time() * 1000) & 0xffff)
                #heartbeatMsg.MsgLength = 3 + len(heartbeatMsg.MsgData)
                #heartbeatData = heartbeatMsg.ConvertToBytes()
                #conn.send(heartbeatData)
                #lastSendTime = time.time()
                #print "heartbeatData lastTime:" + str(lastSendTime)
            time.sleep(0.001)
    return

def Thread_CreateConnect_V2(msg,SocketNODict):#创建连接单独开一个线程,不然会阻塞其他请求

    socketInfo = SocketInfo()
    SocketNODict[msg.SocketNO] = socketInfo
    socketInfo.SocketNO = msg.SocketNO
    socketInfo.Sockt_Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketInfo.Sockt_Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    epStr =  ''.join(chr(x) for x in msg.MsgData)
    epArr = epStr.split(':')
    forward_EP = (epArr[0],int(epArr[1]))
    print("0 == msg.CMD,Create Scoket"+str(forward_EP)+"\r\n")

    try:
        socketInfo.Sockt_Server.connect(forward_EP)
        print('connected to Server'+str(forward_EP)+'\r\n')
        threading.Thread(target=Thread_RecvFromServer_V2,args=(socketInfo.Sockt_Server,socketInfo)).start()
        print('create thread for Read Server Data\r\n')
        createMsg = QueueMsg()
        createMsg.SocketNO = msg.SocketNO
        createMsg.CMD = 0
        createMsg.MsgData = msg.MsgData
        createMsg.MsgLength = 3 + len(createMsg.MsgData)
        socketInfo.RecvQueue.put(createMsg)
        #print('返回客户端已连接到服务器消息\r\n')
    except Exception as e:
        print('Err:create thread for Read Server\r\n')
        socketInfo.Sockt_Server.close()
        socketInfo.Sockt_Server = None
        print(str(e))
        print('format_exc():\r\n',traceback.format_exc())
        print(errno.errorcode[e.errno])
        closeMsg = QueueMsg()
        closeMsg.SocketNO = msg.SocketNO
        closeMsg.CMD = 1
        closeMsg.MsgLength = 3
        socketInfo.RecvQueue.put(closeMsg)
        socketInfo.IsClose = True
    pass


#主线程(conn 客户端连接后拿到的Socket)
def Main_Thread_Fun(conn):
    try:
        print('Main_Thread_Fun Hand clietn Data And Socket\r\n')
        data = conn.recv(1024)
        print('recv from bytes: '+str(len(data))+'B\r\n')
    except:
        print('format_exc():\r\n',traceback.format_exc())
        conn.close()
        return
    headers = get_headers(data)
    response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade: websocket\r\n" \
                   "Connection: Upgrade\r\n" \
                   "Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=\r\n" \
                   "\r\n"
                   #"Sec-WebSocket-Protocol: chat\r\n" \
                   #"WebSocket-Location: ws://%s%s\r\n"
 
    #response_str = response_tpl % (headers['Host'], headers['url'])
    response_str = response_tpl
    if '1' == headers['JustTest']:
        conn.send(bytes(response_str))
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        print('conn.close()')
        conn = None
        print('return')
        return
    print('send websocket Header\r\n')
    conn.send(bytes(response_str))

    clientFlage = headers['ClientFlage']
    SocketNODict = {}
    print('Create thread for Send msg to client\r\n')
    threading.Thread(target=Thread_SendMsgToClient_V2,args=(conn,SocketNODict)).start()
    cacheData = []
    while True:
        try:
            data = conn.recv(8192)
            #print('recv from Client '+str(len(data))+'B\r\n')
            if not data:
                print('client conn:' + str(conn.getpeername()) + ' recv 0 will Close.')
                break
        except Exception as e:
            print(str(e))
            print('format_exc():\r\n',traceback.format_exc())
            #print(errno.errorcode[e.errno])
            break

        cacheData.extend(data)
        msgArr,useLen = QueueMsg.CreateQueueMsg(cacheData)
        #print('转换为 '+str(len(msgArr))+'个消息\r\n')
        cacheData = cacheData[useLen:]

        for msg in msgArr:
            #print('recv from Client,SocketNO '+str(msg.SocketNO)+',CMD '+str(msg.CMD)+'\r\n')
            if not msg:
                continue
            if 0 == msg.CMD:    #创建连接
                
                threading.Thread(target=Thread_CreateConnect_V2,args=(msg,SocketNODict)).start()
            elif 1 == msg.CMD:  #关闭连接
                #print("1 == msg.CMD 关闭连接\r\n")
                if not SocketNODict.has_key(msg.SocketNO):
                    #print("1 SocketNODict找不到socketNO\r\n")
                    continue
                socketInfo = SocketNODict[msg.SocketNO]
                socketInfo.IsClose = True
                if socketInfo:
                    #print("关闭连接"+str(msg.SocketNO)+"\r\n")
                    socketInfo.Sockt_Server.close()
                    if SocketNODict.has_key(msg.SocketNO):
                        del SocketNODict[msg.SocketNO]

            elif 2 == msg.CMD:  #传输数据
                #print("2 == msg.CMD 传输数据\r\n")
                if not SocketNODict.has_key(msg.SocketNO):
                    #print("2 SocketNODict找不到socketNO\r\n")
                    continue
                socketInfo = SocketNODict[msg.SocketNO]
                if socketInfo:
                    #print("发送数据到服务器"+str(msg.SocketNO)+"\r\n")
                    bytesData = msg.MsgData
                    socketInfo.Sockt_Server.send(bytesData)


            elif 3 == msg.CMD:  #心跳包
                conn.send(msg.ConvertToBytes())
                pass
            elif 4 == msg.CMD:  #无用的消息
                pass

    conn.close()
    print('client conn.close()')
    conn = None
    return
 
def run():
    #print('CodePage:'+sys.getdefaultencoding()+'\r\n')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverPort = 36000
    try:
        sock.bind(('127.0.0.1', serverPort))
        sock.listen(5)
        print('wait connect ' + str(sock.getsockname()))
    except Exception as e:
        print(str(e))
        print(errno.errorcode[e.errno])
        print('format_exc():\r\n',traceback.format_exc())
        return
        
    while True:
        try:
            conn, address = sock.accept()
        except KeyboardInterrupt:
            print('Input KeyboardInterrupt')
            break
        except:
            print('format_exc():\r\n',traceback.format_exc())
            continue
        mainThr = threading.Thread(target=Main_Thread_Fun,args=(conn,))
        mainThr.start()
        print('accept' + str(address))
        
    print('close && exit\r\n')
    sock.close()
    sys.exit()
if __name__ == '__main__':
    run()