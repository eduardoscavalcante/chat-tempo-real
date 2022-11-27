import socket
import threading

HOST = 'localhost'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #inicia uma conexão
server.bind((HOST, PORT))
server.listen()

salas = {}

def broadcast(sala, mensagem):
    for i in salas[sala]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()
        
        i.send(mensagem)

def enviarMensagem(nome, sala, client):
    while True:
        mensagem = client.recv(1024) #fica recebendo as mensagens enviadas
        mensagem = f'{nome}: {mensagem.decode()}\n' #envia a mensagem recebida
        broadcast(sala, mensagem)

while True: #fica conectando os clientes dentro da sala
    client, addr = server.accept() #quando um cliente tentar se conectar
    client.send(b'SALA') #envia pro cliente uma mensagem chamada SALA para ele dizer qual sala é
    sala = client.recv(1024).decode()
    nome = client.recv(1024).decode()
    
    if sala not in salas.keys(): #se nao existir essa sala
        salas[sala] = [] #criamos essa sala
    salas[sala].append(client) #se existir, mandamos para a sala escolhida
    print(f'{nome} se conectou na {sala}! INFO {addr}')
    broadcast(sala, f'{nome}: Entrou na sala!\n')
    thread = threading.Thread(target=enviarMensagem, args=(nome, sala, client))
    thread.start()