import tkinter
from PIL import ImageTk, Image
from bd_utils import traer_carta_random
from urllib.request import Request, urlopen
#import login
from functools import partial
#from itertools import cycle
from soqeteServer import Servidor
#l = login.Login()

class Pantalla:
    def __init__(self):
        self.j1 = Jugador()
        print(f'j1 vida = {self.j1.vida}')
        
        self.j2 = Jugador()
        print(f'j2 vida = {self.j2.vida}')
        self.ventana = tkinter.Tk()
        self.ventana.title("Battle cards Roluby<3")
        self.ventana.config(bg = "thistle")
        
        self.f1 = tkinter.Frame(self.ventana)
        self.f1.grid(column=0, row=0, sticky=tkinter.W+tkinter.N+tkinter.S)
        f2 = tkinter.Frame(self.f1)
        f2.grid(column=0, row=0)
        f12 = tkinter.Frame(f2)
        f12.grid(column=0, row=0)
        f13 = tkinter.Frame(f2)
        f13.grid(column=1, row=0)
        f3 = tkinter.Frame(self.ventana, bg = "thistle")
        f3.grid(column=1, row=0, sticky=tkinter.W)
        
        self.f4 = tkinter.Frame(self.ventana, bg = "thistle")
        self.f4.grid(column=0, row=1)
        self.f5 = tkinter.Frame(self.f4)
        self.f5.grid(column=0, row=0)
        f6 = tkinter.Frame(self.f4)
        f6.grid(column=1, row=0)
        f7 = tkinter.Frame(self.f4)
        f7.grid(column=2, row=0)
        
        self.f8 = tkinter.Frame(self.ventana, bg = "thistle")
        self.f8.grid(column=0, row=2)
        self.f9 = tkinter.Frame(self.f8, bg = "thistle")
        self.f9.grid(column=0, row=0)
        f10 = tkinter.Frame(self.f8)
        f10.grid(column=1, row=0)
        self.f11 = tkinter.Frame(self.f8, bg = "thistle")
        self.f11.grid(column=2, row=0)
        
        lomo = ImageTk.PhotoImage(Image.open('lomo_clash.png'))
        self.photo = self.sacar_cartas(self.j1)
        self.l1 = tkinter.Label(self.f5)
        self.l1.grid(column=0, row=0)
        self.l2 = tkinter.Label(f7, image=lomo)
        self.l2.grid(column=0, row=0)
        self.poner_foto(self.l1,1)
       
        boton1 = tkinter.Button(f6, text = "Vida", command = partial(self.jugar_mano, self.j1.comp_vida, self.j2), padx = 27, pady = 10, bg = "mediumorchid1")
        boton1.pack()
        boton2 = tkinter.Button(f6, text = "Daño", command = partial(self.jugar_mano, self.j1.comp_danio, self.j2), padx = 25, pady = 10, bg = "mediumorchid1")
        boton2.pack()
        boton3 = tkinter.Button(f6, text = "Velocidad", command = partial(self.jugar_mano, self.j1.comp_velocidad, self.j2), padx = 12, pady = 10, bg = "mediumorchid1")
        boton3.pack()
        self.boton4 = tkinter.Button(f6, text = "Rendirse", command = partial(self.jugar_mano, self.j1.rendirse, None), padx = 15, pady = 10, bg = "mediumorchid1")
        self.boton4.pack()
        boton5 = tkinter.Button(self.f1, text = "Servidor", padx = 35.59, pady = 10, bg = "mediumorchid1", command = self.crear_servidor)
        boton5.grid(column=0, row=0)
        boton6 = tkinter.Button(self.f1, text = "Cliente", padx = 35.59, pady = 10, bg = "mediumorchid1")
        boton6.grid(column=1, row=0)
        
        self.etiqueta1 = tkinter.Label(self.f9, text = f'NOMBRE: {self.j1.nombre}', bg = "thistle")
        self.etiqueta1.pack()
        self.etiqueta2 = tkinter.Label(self.f9, text = f'DAÑO: {self.j1.danio}', bg = "thistle")
        self.etiqueta2.pack()
        self.etiqueta3 = tkinter.Label(self.f9, text = f'VIDA: {self.j1.vida}', bg = "thistle")
        self.etiqueta3.pack()
        self.etiqueta4 = tkinter.Label(self.f9, text = f'VELOCIDAD: {self.j1.velocidad}', bg = "thistle")
        self.etiqueta4.pack()
        self.etiqueta5 = tkinter.Label(self.f9, text = f'PUNTOS: {self.j1.puntos}', bg = "thistle")
        self.etiqueta5.pack()
        self.etiqueta6 = tkinter.Label(self.f11, text = "", bg = "thistle")
        self.etiqueta6.pack()
        self.etiqueta7 = tkinter.Label(f3, text = "IP: ", bg = "thistle")
        self.etiqueta7.grid(column=0, row=0)
        self.etiqueta8 = tkinter.Label(f3, text = "Puerto: ", bg = "thistle")
        self.etiqueta8.grid(column=0, row=1)
        
        self.ventana.mainloop()
    
    def jugar_mano(self,funcion_jugador, atributo_jugada):
        respuesta = funcion_jugador(atributo_jugada)
        self.j1.preparar_carta()
        self.j2.preparar_carta()
        self.etiqueta1.config(text = f'NOMBRE: {self.j1.nombre}')
        self.etiqueta2.config(text = f'DAÑO: {self.j1.danio}')
        self.etiqueta3.config(text = f'VIDA: {self.j1.vida}')
        self.etiqueta4.config(text = f'VELOCIDAD: {self.j1.velocidad}')
        self.etiqueta5.config(text = f'PUNTOS: {self.j1.puntos}')
        self.etiqueta6.config(text = f'MENSAJE: {respuesta["mensaje"]}')
        print(self.j1.url_final)
        self.boton4.config(state=tkinter.DISABLED)
        self.photo = self.sacar_cartas(self.j1)
        self.photo2 = self.sacar_cartas(self.j2)
        self.poner_foto(self.l1,1)
    
    def sacar_cartas(self, jugador):
        req = Request(jugador.url_final, headers={'User-Agent': 'Mozilla/5.0'})
        raw_data = urlopen(req).read()
        p = ImageTk.PhotoImage(data=raw_data)
        return p
        
    def poner_foto(self, label, jug):
        if jug == 1:
            label.config(image=self.photo)
        else:
            label.config(image=self.photo2)
            
    def crear_servidor(self):
        self.modo = Servidor()
        self.etiqueta7.config (text = f"IP: {self.modo.MiIP}")
        self.etiqueta8.config (text = f"Puerto: {self.modo.Port}")
        self.modo.abrir_conexion()
    
class Jugador:
    def __init__(self):
        self.puntos = 0
        self.preparar_carta()
        self.respuesta = {
            "puntos": 0,
            "mensaje": "",
            }
    def comp_vida(self, oponente):
        if self.vida > oponente.vida:       
            self.puntos += 20            
            self.respuesta["mensaje"] = "Ganó por: " + str(self.vida - oponente.vida)
            print("Ganó por: " + str(self.vida - oponente.vida))
        else:
            oponente.puntos += 20
            print("Perdió por: " + str(oponente.vida - self.vida))
            self.respuesta["mensaje"] = "Perdió por: " + str(oponente.vida - self.vida)
        self.respuesta["puntos"] = self.puntos
        return self.respuesta
    
    def comp_danio(self, oponente):
        if self.danio > oponente.danio:       
            self.puntos += 20            
            self.respuesta["mensaje"] = "Ganó por: " + str(self.danio - oponente.danio)
            print("Ganó por: " + str(self.danio - oponente.danio))
        else:
            oponente.puntos += 20
            print("Perdió por: " + str(oponente.danio - self.danio))
            self.respuesta["mensaje"] = "Perdió por: " + str(oponente.danio - self.danio)
        self.respuesta["puntos"] = self.puntos
        return self.respuesta
            
    def comp_velocidad(self, oponente):
        if self.velocidad > oponente.velocidad:       
            self.puntos += 20            
            self.respuesta["mensaje"] = "Ganó por: " + str(self.velocidad - oponente.velocidad)
            print("Ganó por: " + str(self.velocidad - oponente.velocidad))
        else:
            oponente.puntos += 20
            print("Perdió por: " + str(oponente.velocidad - self.velocidad))
            self.respuesta["mensaje"] = "Perdió por: " + str(oponente.velocidad - self.velocidad)
        self.respuesta["puntos"] = self.puntos
        return self.respuesta
            
    def rendirse(self):
        if True:
            self.puntos -= 10
            print("Se rindió. El juego empieza de nuevo")
            self.preparar_carta
            
            
    def preparar_carta(self):
        datos = traer_carta_random()
        self.url_final = datos[0]
        self.vida = datos[1]
        self.danio = datos[2]
        self.velocidad = datos[3]
        self.nombre = datos[4]

if __name__ == "__main__":
    p = Pantalla()