import socket
import os
import threading
from time import ctime, sleep
from socket import *
timeout = 8
def send(clientSocket,address):
    #三次握手
    conncetion=False#用来判断是否建立连接
    while True:
        while True:
            clientSocket.sendto("SYN".encode(),address)
            ack=clientSocket.recv(1024)
            #print(ack)
            #print(ack==b"ACK")
            if ack==b"ACK":#收到的是二进制
                #print("ack")
                clientSocket.sendto("ACK".encode(),address)
                print("成功建立连接")
                conncetion=True
                break
        if conncetion==False:
            print("尝试重新再次连接......")
            continue
        #开始传输文件
        while True:
            type=input("是否要传输文件(Y/N):")
            if type=="Y":
                clientSocket.sendto("Y".encode(),address)
                while True:
                    ack=clientSocket.recv(1024)
                    if ack==b"ACK" :#确认
                        break
                while True:
                    filename=input("请输入传送文件的路径：")
                    if os.path.exists(filename):#如果存在这个文件
                    #处理文件路径
                        filePath = filename.split('//')
                        #发送文件名
                        clientSocket.sendto(filePath[len(filePath)-1].encode(),address)
                        while True:
                            ack=clientSocket.recv(1024)
                            if ack==b"ACK":
                                break
                        #打开文件,并且分开发送
                        file=open(filename,"rb")
                        while True:
                            data=file.read(1024)
                            if not data:
                                clientSocket.sendto("ACK".encode(),address)
                                print("文件已经发送完毕")
                                break
                            clientSocket.sendto(data,address)
                        file.close()
                        break
                    else:
                        print("不存在该文件，请重新输入")
            elif type=="N":#跳出发送文件的循环，准备询问是否断开连接
                clientSocket.sendto("N".encode(),address)
                break
        break

#释放连接,模拟tcp的四次挥手
def close(clientSocket,address):
    while True:
        print("正在准备释放连接")
        clientSocket.sendto("FIN".encode(),address)
        while True:
            ack=clientSocket.recv(1024)
            #print(ack)
            if ack==b"ACK":
                print("即将释放连接")
                break
        while True:
            fin=clientSocket.recv(1024)
            #print("第二次挥手")
            #print(fin)
            if fin==b"FIN":
                break
        clientSocket.sendto("ACK".encode(),address)
        clientSocket.close()
        print("已关闭连接")
        break

if __name__=='__main__':#用于判断当前模块是否作为主程序直接运行。
    while True:
        serverAddress = input("Please input server IP(例如:192.168.226.129):")
        while True:
            port=int(input("请输入服务器端口号(例如:10000)"))
            if port>0 and port<65536:#判断输入的端口号的合法性
                break
            print("你输入的端口号无效")
        address=(serverAddress,port)
        print(address)
        clientSocket=socket(AF_INET,SOCK_DGRAM)
        send(clientSocket,address)
        #t=threading.Thread(target=send,args=(clientSocket,address))
        #t.start()
        flag=input("是否要继续连接其他的主机(Yes/No)")
        if flag=="Yes":
            continue
        else:
            break
    close(clientSocket,address)
    
