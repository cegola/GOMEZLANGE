import sys, var, datetime
import os, zipfile

class Eventos():
    def Salir(event):
        '''Evento modulo salir'''

        try:
            #var.dlgSalir.show()
            var.dlgSalir.show()
            if var.dlgSalir.exec_():
                sys.exit()
            else:
                var.dlgSalir.close()
                event.ignore()
        except Exception as error:
            print('Error salir %s'% str(error))

    def closeSalir(event):
        try:
            if var.dlgSalir.exec_():
                var.dlgSalir.hide()
        except Exception as error:
            print('Error salir %s' % str(error))

    def Backup(self):
        try:
            print('Backup')
            fecha = datetime.now()
            ficheroZip = zipfile.Zipefile(str(self.fecha)+'_backup.zip','w')
            ficheroZip.write(var.filebd, os.path.basename(var.filebd), zipfile.ZIP_DEFLATED)

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
            if var.dlgAviso.exec_():
                return True
            else:
                var.dlgSalir.close()
                return False
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


