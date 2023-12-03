import socket
import tqdm
import os
import threading

def received(address,port):
    #传输数据间隔符
    SEPARATOR='<SEPARATOR>'
    #文件缓冲区
    Buffersize=4096*10
    while True:
        print('准备接受新的文件....')
        
        udp_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udp_socket.bind((address,port))
        recv_data=udp_socket.recvfrom(Buffersize)
        recv_file_info=recv_data[0].decode('utf-8')#存储接受到的数据，文件名
        print(f'接受到的文件信息{recv_file_info}')
        c_address=recv_data[1]#存储客户的地址信息
        #打印客户端ip
        print(f'客户端{c_address}连接')
        
        filename,file_size=recv_file_info.split(SEPARATOR)
        file_size=int(file_size)

        #文件接受处理
        progress=tqdm.tqdm(range(file_size),f'接受{filename}',unit_scale=True)

        with open('8_18'+filename,'wb') as f:
            for _ in progress:
                #从客户端读取数据

                bytes_read=udp_socket.recv(Buffersize)
                #如果没有数据传输内容
                print('完成传输！')
                print(bytes_read)
                break
            #读取写入
            f.write(bytes_read)
            #更新进度条
            progress.update(len(bytes_read))
        udp_socket.close()

if __name__ == '__main__':

    port=int(input('请输入服务器端口号：'))
    t = threading.Thread(target=received, args=('', port))
    t.start()
    # send(address)
