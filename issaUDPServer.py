# github:  https://github.com/Isaaaaaaaaaaaaaa/Computer-Network

import os
from socket import *
from threading import Thread

# 判断数据报是否来自正确的源client
# def isFromCorrectClient(clientName,clientPort,data):
#     addr = data[1]
#     Name, Port = addr
#     if clientName == Name and clientPort == Port:
#         return True
#     else:
#         return False
    
#传输文件
def transfer(serverSocket,clientName,clientPort):   
    while True:
        #接收传输类型
        # while True:            
        #     type = serverSocket.recvfrom(1024)
        #     if isFromCorrectClient(clientName,clientPort,type):
        #         type = type[0]
        #         break
        
        #接收传输类型
        type = serverSocket.recv(1024)
        #发送ACK
        serverSocket.sendto("ACK".encode(), (clientName,clientPort))    
        
        if type == b"q":#断开连接
            #print(f"The client (IP: {clientName}  Port Number: {clientPort})  asked to release conneciton ...")
            #接收FIN
            while True:
                fin = serverSocket.recv(1024)
                if fin == b"FIN":
                    #print("Received fin from client,sending ack ...")
                    serverSocket.sendto("ACK".encode(), (clientName,clientPort))
                    break
            #发送ACK
            serverSocket.sendto("ACK".encode(), (clientName,clientPort))
            #发送FIN
            serverSocket.sendto("FIN".encode(), (clientName,clientPort))
            #接收ACK
            while True:
                ack = serverSocket.recv(1024)
                if ack == b"ACK":
                    print(f"Connection released from client IP: {clientName}, Port Number: {clientPort} !")
                    break
        elif type == b"r":   #接受文件
            #print(f"Ready to send file to IP: {clientName}, Port Number: {clientPort}")  
            while True:
                #接收客户端发送的文件名
                fileName = serverSocket.recv(1024).decode()
                #print(f"The client ask the file {fileName}")
                #判断文件是否存在
                if os.path.exists(fileName):
                    #发送ACK
                    serverSocket.sendto("ACK".encode(), (clientName,clientPort))
                    #打开文件
                    file = open(fileName,"rb")
                    #分块读取和发送整个文件
                    while True:
                        data = file.read(1024)
                        if not data:
                            print(f"The file {fileName} has sent to client (IP:{clientName}, Port Number: {clientPort})!")
                            #发送文件传输完成的ACK
                            serverSocket.sendto("ACK".encode(), (clientName,clientPort))
                            break
                        serverSocket.sendto(data, (clientName, clientPort))
                    #关闭文件
                    file.close()
                    break
                else:
                    #发送错误信息
                    serverSocket.sendto("Error".encode(), (clientName,clientPort))
                    print(f"The File {fileName} which client (IP:{clientName}, Port Number: {clientPort}) asked does not exist!")
        elif type == b"s":#发送文件
            #print("Ready to receive a file")
            #接收文件名
            fileName = serverSocket.recv(1024).decode()
            #返回ack
            serverSocket.sendto("ACK".encode(), (clientName,clientPort))
            file = open(fileName,"wb")
            #接收文件
            while True:
                data,addr = serverSocket.recvfrom(1024)
                clientName,clientPort=addr
                if data == b"ACK":
                    print(f"The file {fileName} received from client (IP:{clientName}, Port Number: {clientPort})!")
                    break
                file.write(data)
            #关闭文件
            file.close()
        
while True:
    #设定服务器端端口号
    while True:
        serverPort = input("Please input server Port number :")
        if serverPort.isdigit() and int(serverPort)>=0 and int(serverPort)<=65535:
            serverPort = int(serverPort)
            break#跳出循环
        else:
            print("Please input a valid Port number!")
    
    
    while True:
        #创建UDP socket
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('',serverPort))
        serverPort += 1
        
        #模拟建立TCP连接
        while True:
            #print("Trying to establish connection")
            syn = serverSocket.recvfrom(1024)
            clientName, clientPort = syn[1]
            #在使用Python中的socket库进行网络编程时，
            # 我们通常使用recvfrom方法来接收UDP协议的数据包。
            # 这个方法会返回一个元组，其中包含接收到的数据和发送方的地址信息。
            if syn[0] == b"SYN":
                #print("The server received syn from client,sending ack ...")
                serverSocket.sendto("ACK".encode(), (clientName,clientPort))
                while True:
                    ack = serverSocket.recv(1024)
                    if ack == b"ACK":#再次收到ACK，准备发送文件
                        print(f"Connection established from IP: {clientName} , Port Number: {clientPort}")
                        #transfer(serverSocket,clientName,clientPort)
                        break
                break
            
        Thread(target=transfer, args=(serverSocket,clientName,clientPort)).start()   