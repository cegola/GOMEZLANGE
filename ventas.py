import var, conexion, events
from PyQt5 import QtWidgets
from ventana import *

class Ventas():
    def tablaVentas(self):
        try:
            index=0
            var.cmbventa = QtWidgets.QComboBox()
            conexion.Conexion.cargarCmbVentas(var.cmbventa)
            var.ui.tabVentas.setRowCount(index + 1)  # crea la fila y a continuacion mete los datos
            var.ui.tablaPro.setItem(index, 0, QtWidgets.QTableWidgetItem())
            var.ui.tablaPro.setItem(index, 1, QtWidgets.QTableWidgetItem(var.cmbventa))
            var.ui.tablaPro.setItem(index, 2, QtWidgets.QTableWidgetItem())
            var.ui.tablaPro.setItem(index, 3, QtWidgets.QTableWidgetItem())
        except Exception as error:
            print('Error Preparar tabla ventas %s' % str(error) )