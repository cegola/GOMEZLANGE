import sys, var, shutil
from datetime import datetime
from PyQt5 import QtWidgets
import os, zipfile

import conexion


class Eventos():
    def Salir(event):
        '''Evento modulo salir'''

        try:
            # var.dlgSalir.show()
            var.dlgSalir.show()
            if var.dlgSalir.exec_():
                sys.exit()
            else:
                var.dlgSalir.close()
                event.ignore()
        except Exception as error:
            print('Error salir %s' % str(error))

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
            var.copia = (fecha.strftime('%d_%m_%Y_%H-%M') + '_backup.zip')
            option = QtWidgets.QFileDialog.Options()
            print(option)
            directorio, filename = var.filedlgAbrir.getSaveFileName(None, 'Guardar copia', var.copia, '.zip',
                                                                    options=option)
            if var.filedlgAbrir.Accepted and filename != '':
                ficheroZip = zipfile.ZipFile(var.copia, 'w')
                ficheroZip.write(var.filebd, os.path.basename(var.filebd), zipfile.ZIP_DEFLATED)
                ficheroZip.close()
                var.ui.lblstatus.setText('Backup realizada')
                shutil.move(str(var.copia), str(directorio))

        except Exception as error:
            print('Error backup %s' % str(error))

    def restaurarBD(self):
        try:
            option = QtWidgets.QFileDialog.Options()
            filename = var.filedlgAbrir.getOpenFileName(None, 'Restaurar copia de seguridad','','*.zip', options=option)
            if var.filedlgAbrir.Accepted and filename != '':
                print(str(filename[0]))
                bd = zipfile.ZipFile(str(filename[0]),'r')
                bd.extractall()
                bd.close()
            conexion.Conexion.cargarDatos(self)
            var.ui.lblstatus.setText('Copia de seguridad restaurada')

        except Exception as error:
            print('Error restaurar BD %s' % str(error))


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


    def AbrirAcercaDe(self):
        try:
            # var.dlgSalir.show()
            var.dlgAcercaDe.show()
            if var.dlgAcercaDe.exec_():
                var.dlgAcercaDe.close()
        except Exception as error:
            print('Error acerca de %s' % str(error))


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
