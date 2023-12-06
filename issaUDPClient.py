# github:  https://github.com/Isaaaaaaaaaaaaaa/Computer-Network

import os
import select
from socket import *

timeout = 5

#判断ip是否合法
def isValidIp(ip):
    parts = ip.split(".")   #将ip以'.'为分隔，分隔成一个列表parts
    if len(parts) != 4:     #判断parts的长度是否为4,不是则证明输入有误
        return False
    for part in parts:      #遍历parts列表 判断每个part是否符合规则
        if not part.isdigit():
            return False
        i = int(part)
        if i < 0 or i > 255:
            return False
    return True

while True:
    #判断是否继续传输文件
    flag = input("Continue to transfer file? Y/n :")
    if flag == "n":
        break
    
    #输入目标端口号       
    while True:
        serverPort = input("Please input server Port number :")
        if serverPort.isdigit() and int(serverPort)>=0 and int(serverPort)<=65535:
            serverPort = int(serverPort)
            break
        else:
            print("Please input a valid Port number!")
            
    #输入目标ip地址
    while True:
        serverName = input("Please input server IP :")
        if isValidIp(serverName):
            break
        else:
            print("Please input a valid IP!")

    #创建socket
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    print("Trying to establish connection ...")
    
    #判断是否建立连接
    connectionEstablish = False
    #记录超时重传次数
    cnt = 0
    
    #模拟建立TCP连接,三次握手
    while True:
        clientSocket.sendto("SYN".encode(),(serverName,serverPort))
        ready = select.select([clientSocket],[],[],timeout)
        #引入超时重传机制
        if ready[0]:
            ack = clientSocket.recv(1024)
            print(ack)
            if ack == b"ACK":
                #print("Received ack from server,sending ack ...")
                clientSocket.sendto("ACK".encode(),(serverName,serverPort))
                print(f"Connection established to server, IP: {serverName}, Port Number: {serverPort}")
                connectionEstablish = True
                break
        elif cnt>2:
            break
        else:
            cnt += 1
            print(f"Timeout, trying again ... times = {cnt}")
    
    if not connectionEstablish:
        print("Connection failed, please try again!")
        continue
    
    #开始传输文件
    while True:
        #输入传输类型
        type = input("Please input transfer type: s/r(send or receive), input q to quit :")
        
        #判断传输类型是否合法
        if type != "s" and type != "r" and type != "q":
            print("Please input a valid transfer type!")
            continue
        
        #向服务器端发送传输类型
        clientSocket.sendto(type.encode(),(serverName,serverPort))
        
        #接收ACK
        while True:
            ack = clientSocket.recv(1024)
            if ack == b"ACK":
                #print("The server gets ready")
                break
        
        if type == "q":
            #模拟释放TCP连接
            while True:
                print("Trying to release connection ...")
                clientSocket.sendto("FIN".encode(),(serverName,serverPort))
                ack = clientSocket.recv(1024)
                if ack == b"ACK":
                    #print("Received ack from server")
                    break
            #接收FIN
            while True:
                fin = clientSocket.recv(1024)
                if fin == b"FIN":
                    #print("Received fin from server,sending ack ...")
                    break
            #发送ACK
            clientSocket.sendto("ACK".encode(),(serverName,serverPort))
            #关闭socket
            clientSocket.close()
            print("Connection released")
            break
        
        #向Server端发送文件
        elif type == "s":
            while True:
                #输入文件名
                fileName = input("Please input file name :")
                #判断文件是否存在
                if os.path.exists(fileName):
                    #处理文件名
                    filePath = fileName.split('/')
                    #发送文件名
                    clientSocket.sendto(filePath[len(filePath)-1].encode(),(serverName,serverPort))
                    #接收ACK
                    while True:
                        ack = clientSocket.recv(1024)
                        if ack == b"ACK":
                            #print("Received ack from server,ready to send file  ...")
                            break
                    #打开文件
                    file = open(fileName,"rb")
                    #分块读取和发送整个文件
                    while True:
                        data = file.read(1024)
                        if not data:
                            clientSocket.sendto("ACK".encode(), (serverName, serverPort))
                            print("File sent!")
                            break
                        clientSocket.sendto(data, (serverName, serverPort))
                    #关闭文件
                    file.close()
                    break
                else:
                    print("File does not exist!")
        elif type == "r":
            #指定接收文件名并发送至服务器端
            while True:
                fileName = input("Please input file name :")
                clientSocket.sendto(fileName.encode(),(serverName,serverPort))
                #接收服务器端返回结果
                ack = clientSocket.recv(1024)
                if ack == b"ACK":
                    #print("Received ack from server,ready to receive file ...")
                    break
                else:
                    print("File does not exist!")
            file = open(fileName,"wb")
            #接收文件
            while True:
                data,addr = clientSocket.recvfrom(1024)
                if data == b"ACK":
                    print("File received!")
                    break
                file.write(data)
            #关闭文件
            file.close()