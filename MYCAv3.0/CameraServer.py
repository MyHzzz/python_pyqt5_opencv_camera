'''
     美颜相机服务端
     利用类将函数封装
     处理业务逻辑
     1.建立网络通信模型
'''
from socket import *
from threading import Thread
from settings import *
import sys
import pymysql
#利用UDP作为信息传输通道

#将服务器具备的功能封装成类
class CameraServer(object):
    def __init__(self):
        #添加对象属性
        self.server_address = SERVER_ADDR
        self.ip = SERVER_HOST
        self.port = SERVER_PORT
        # self.user = {}
        #创建套接字
        self.db = pymysql.connect('localhost','root','','mycamera')
        print(self.server_address)
        self.create_socket()
    def create_socket(self):
        self.sockfd = socket(AF_INET,SOCK_DGRAM)
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(self.server_address)
    def serve_forever(self):
        print("------多线程--------")
        while True:
            try:
                data,addr = self.sockfd.recvfrom(1024)
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit("服务器退出")
            except Exception as e:
                print("Error:",e)
                continue
            #创建线程处理客户端请求

            clientThread = Thread(target=self.handle,args = (data.decode(),addr))    
            clientThread.setDaemon(True)
            clientThread.start()
    #具体处理客户端请求
    def handle(self,data,addr):
        #接收客户端请求
        # print(c.getpeername(),':',data)
        print(data,"!!!!")
        print(addr,"---",data[0])
        if data[0] == 'L':
            self.do_login(addr,data)
        elif data[0] == 'R':
            self.do_register(addr,data)
        # elif data[0] == 'L':
        #     do_login(c,db,data)
        # elif data[0] == 'Q':
        #     do_query(c,db,data)
        # elif data[0] == 'H':
        #     do_hist(c,db,data)
    def do_login(self,addr,data):
        l = data.split(' ')
        name = l[1]
        passwd = l[2]
        cursor = self.db.cursor()
        self.db.ping(reconnect=True)
        sql="select * from user where \
        name='%s' and passwd='%s'"%(name,passwd)

        #查找用户

        cursor.execute(sql)
        r = cursor.fetchone()
        if r == None:
            self.sockfd.sendto(b'FALL',addr)
        else:
            self.sockfd.sendto(b'OK',addr)
    def do_register(self,addr,data):
        l = data.split(' ')
        name = l[1]
        passwd = l[2]  
        cursor = self.db.cursor()
        print(name,"--",passwd)
        self.db.ping(reconnect=True)

        sql="select * from user where name='%s'"%name  
        cursor.execute(sql)
        r = cursor.fetchone()

        if r != None:
            self.sockfd.sendto(b"EXISTS",addr) 
        else:
            #插入用户
            sql="insert into user (name,passwd) values \
            ('%s','%s')"%(name,passwd)

            try:
                print(1)
                cursor.execute(sql)
                self.db.commit()
                self.sockfd.sendto(b'OK',addr)
                self.db.close()
            except:
                print(2)
                self.db.rollback()
                self.sockfd.sendto(b'FALL',addr)       





if __name__ == "__main__":    
    #创建服务器对象
    Ser_One = CameraServer()
    #启动服务器
    Ser_One.serve_forever()









