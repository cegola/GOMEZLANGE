import sys, var, shutil
from datetime import datetime
from PyQt5 import QtWidgets
import os, zipfile

import conexion


class Eventos():
    def Salir(self, event):
        """

        Método que cierra el programa

        :param event: evento salir
        :type event: event
        :return: None
        :rtype: None

        Abre la ventana salir y cierra el programa si se clicka el botón aceptar

        """

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

    def closeSalir(self):
        """

        Módulo que cierra la ventana salir

        :return: None
        :rtype: None

        """
        try:
            if var.dlgSalir.exec_():
                var.dlgSalir.hide()
        except Exception as error:
            print('Error salir %s' % str(error))

    def Backup(self):
        """

        Módulo que realiza una copia de seguridad de la base de datos

        :return: None
        :rtype: None

        Abre una ventana para elegir el directorio donde guardar la copia. Comprime el archivo de la base de datos
        en un archivo zip. Muestra un mensaje en la barra de estado.

        """
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
        """

        Módulo que restaura una copia de seguridad de la base de datos

        :return: None
        :rtype: None

        Abre una ventana para elegir el archivo tipo zip donde está la base de datos.
        Descomprime el archivo. Recarga los datos llamando al método conexio.cargarDatos.
        Muestra un mensaje en la barra de estado.

        """
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
        """

        Módulo que abre una ventana para elegir directorio

        :return: None
        :rtype: None

        """
        try:
            var.filedlgAbrir.setWindowTitle('Abrir archivo')
            var.filedlgAbrir.setModal(True)
            var.filedlgAbrir.show()
        except Exception as error:
            print('Error abrir dir: %d' % str(error))

    def AbrirAviso(mensaje):
        """

        Módulo que abre una ventana de aviso

        :param mensaje: mensaje que muestra la ventana
        :type mensaje: string
        :return: bool
        :rtype: True/False

        Abre una ventada de aviso con el mensaje pasado por parámetro. Devuelve un booleano dependiendo de si se ejecuta
        o no.

        """
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
        """

        Método que abre una ventada de Acerca De

        :return: None
        :rtype: None

        """
        try:
            # var.dlgSalir.show()
            var.dlgAcercaDe.show()
            if var.dlgAcercaDe.exec_():
                var.dlgAcercaDe.close()
        except Exception as error:
            print('Error acerca de %s' % str(error))

    def Imprimir(self):
        """

        Módulo que abre la ventana de impresión

        :return: None
        :rtype: None

        """
        try:
            var.dglImprimir.setModal(True)
            var.dglImprimir.show()
        except Exception as error:
            print('Error abrir dir: %d' % str(error))

    def cargarProv(self):
        """

        Módulo que carga las provincias al iniciar el programa

        :return: None
        :rtype: None

        Carga el comboBox de provincias en la pestaña clientes

        """
        try:
            prov = ['', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            for i in prov:
                var.ui.cmbProvincia.addItem(i)
        except Exception as error:
            print('Error %s' % str(error))
