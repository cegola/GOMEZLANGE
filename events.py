import sys, var

class Eventos():
    def Salir(self):
        '''Evento modulo salir'''
        try:
            var.lblMensaje.setText('¿Está seguro que quiere salir de la aplicación?')
            var.dlgAviso.show()
            if var.dlgAviso.exec_() and var.Salir:
                sys.exit()
            else:
                var.dlgAviso.close()
        except Exception as error:
            print('Error salir %s'% str(error))

    def Backup(self):
        try:
            print('Backup')
        except Exception as error:
            print('Error backup %s' % str(error))

    def AbrirDir(self):
        try:
            var.filedlgAbrir.setWindowTitle('Abrir archivo')
            var.filedlgAbrir.setModal(True)
            var.filedlgAbrir.show()
        except Exception as error:
            print('Error abrir dir: %d' % str(error))

    def AbrirAviso(mensaje):
        try:
            var.lblMensaje.setText(mensaje)
            var.dlgAviso.show()
        except Exception as error:
            print('Error salir %s' % str(error))


    def Imprimir(self):
        try:
            var.dglImprimir.setModal(True)
            var.dglImprimir.show()
        except Exception as error:
            print('Error abrir dir: %d' % str(error))


    def cargarProv():
        '''Carga las provincias al iniciar el programa'''
        try:
            prov = ['', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            for i in prov:
                var.ui.cmbProvincia.addItem(i)
        except Exception as error:
            print('Error %s' % str(error))


