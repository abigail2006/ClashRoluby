from tkinter import *
import socket
import json

class Cliente:
    def __init__(self, ip, port ):
        self.ip = ip
        self.puerto = port
        self.servidor = socket.socket()
        self.running = True  
                    

    def conectar(self):
        self.nombre_host = self.ip
        self.servidor.connect((self.nombre_host, self.puerto)) #Conecta al servidor
        print("Conectado al servidor")

    def enviar(self, mensaje = ""):
        mensJson = json.dumps(mensaje)
        self.servidor.send(mensJson.encode()) #Codifica y envía mensajes
        print("Mensaje enviado")
        
    def recibir(self):
        while self.running:
            message = self.servidor.recv(1024).decode() #Recibe el nuevo mensaje
            if not message == "":
                print(message)
                print(type(json.loads(message)))
                self.running = False
        self.running = True
        return json.loads(message)