#https://github.com/www-light/theNetwork-ofComputerlab5
#运行环境为python解释器3.10.6 64—bit,开发工具为visual stdio code

import socket
import threading
from socket import *

def send(serverSocket,address):
    while True:
        #
        msg=serverSocket.recv(1024)#接受信息
        #print("msg")
        #print(msg)
        serverSocket.sendto("ACK".encode(),address)#回复的是msg的ack
        if msg==b"N": #模拟四次挥手,断开与client的连接
            while True:#接受FIN
                FIN=serverSocket.recv(1024)
                #print("1xcbdbd")
                #print(FIN)
                if FIN==b"FIN":
                    serverSocket.sendto("ACK".encode(),address)
                    break
            #serverSocket.sendto("ACK".encode(),address)
            serverSocket.sendto("FIN".encode(),address)
            while True:#接受ack
                ACK=serverSocket.recv(1024)
                #print("2")
                #print(ACK)
                if ACK==b"ACK":
                    print("已释放连接")
                    break
            break#跳出接受信息的循环
        elif msg==b"Y":#客户机发送确认开始发送文件的"Y",服务器端开始准备接受对方发送的文件
            filename=serverSocket.recv(1024).decode()#接收到服务端发来的文件名
            serverSocket.sendto("ACK".encode(),address)#回应接收到的msg的ack
            file=open(filename,"wb")
            #循环接收文件
            while True:
                data=serverSocket.recv(1024)
                if data==b"ACK":
                    print("已经收到发来的文件")
                    break
                file.write(data)
            file.close()

if __name__ == '__main__':
    while True:
        while True:#确定端口号和client地址
            serverPort=int(input("请输入服务器的端口号："))
            if serverPort>0 and serverPort<65536 :
                break
            else:
                print("输入的端口号无效")
        while True:#准备建立连接和传输文件
            #创建socket
            serverSocket=socket(AF_INET,SOCK_DGRAM)
            serverSocket.bind(('',serverPort))
            serverPort+=1
            while True:
                syn=serverSocket.recvfrom(1024)#接受client发送的信息
                clientname,clientport=syn[1]
                #print(syn[0])
                if syn[0]==b"SYN":#客户机接收到了服务器发送的SYN
                    #print("ack")
                    serverSocket.sendto("ACK".encode(),(clientname,clientport))#区别encode和decode
                    while True:
                        ack=serverSocket.recv(1024)
                        #print(ack)
                        if(ack==b"ACK"):#收到client端发送的ACK,准备发送文件
                            print("The connetion is established")
                            break
                    break
            address=(clientname,clientport)
            t=threading.Thread(target=send,args=(serverSocket,address))
            t.start()


                    

            
        


