import sys

class Eventos():
    def Salir(self):
        '''Evento modulo salir'''
        try:
            sys.exit()
        except Exception as error:
            print('Error %s'% str(error))