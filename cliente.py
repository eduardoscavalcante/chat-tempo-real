import socket
import threading

#pra criar a interface grafica
from tkinter import *
import tkinter
from tkinter import simpledialog

class Chat:
    def __init__(self):

        HOST = 'localhost'
        PORT = 55555

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #inicia uma conexão
        self.client.connect((HOST, PORT)) #cria uma conexão
        login = Tk()
        login.withdraw()

        self.janela_carregada = False
        self.ativo = True

        self.nome = simpledialog.askstring('Nome', 'Digite seu nome:', parent=login) #interface que pede pelo nome
        self.sala = simpledialog.askstring('sala', 'Digite a sala:', parent=login) #interface que pede o nome da sala
        
        thread = threading.Thread(target=self.conecta) #cria a thread do conecta
        thread.start() #inicia a thread
        self.janela() #chama a função da janela


    def janela(self): #interface do chat
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title('Chat')

        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600)
        
        self.envia_mensagem = Entry(self.root) #caixa de envio da mensagem
        self.envia_mensagem.place(relx=0.05, rely=0.8, width=500, height=20)
        
        self.botao_enviar = Button(self.root, text='Enviar', command=self.enviarMensagem) #botao de envio
        self.botao_enviar.place(relx=0.7, rely=0.8, width=100, height=20)
        self.root.protocol("WM_DELETE_WINDOW", self.fechar) #funçao de fechar
        
        self.root.mainloop() #faz a janela continuar aberta

    def fechar(self): #função de destruir a janela
        self.root.destroy() 
        self.client.close()

    def conecta(self):
        while True: #enquanto a janela está aberta
            recebido = self.client.recv(1024)
            if recebido == b'SALA':
                self.client.send(self.sala.encode()) #envia o nome da sala
                self.client.send(self.nome.encode()) #envia o nome
            else: #se nao for o login, entao é uma mensagem
                try:
                    self.caixa_texto.insert('end', recebido.decode())
                except:
                    pass

    def enviarMensagem (self): #funcao do botao de envio
        mensagem = self.envia_mensagem.get() #recebe a mensagem que é enviada
        self.client.send(mensagem.encode()) #envia a mensagem para ser enviada

chat = Chat()