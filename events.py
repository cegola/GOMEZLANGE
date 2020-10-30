import sys, var

class Eventos():
    def Salir(self):
        '''Evento modulo salir'''
        try:
            sys.exit()
        except Exception as error:
            print('Error %s'% str(error))


    def cargarProv():
        '''Carga las provincias al iniciar el programa'''
        try:
            prov = ['', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            for i in prov:
                var.ui.cmbProvincia.addItem(i)
        except Exception as error:
            print('Error %s' % str(error))
