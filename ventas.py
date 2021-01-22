import var, conexion, events, products
from PyQt5 import QtWidgets
from ventana import *


class Ventas():

    def altaFactura(self):
        try:
            dni = var.ui.editDniFac.text()
            fecha = var.ui.editFechaFac.text()
            apel = var.ui.editApellidosFac.text()

            if dni != '' and fecha != '':
                conexion.Conexion.altaFac(dni, fecha, apel)
            conexion.Conexion.mostrarFacturas(self)
            conexion.Conexion.cargarFacturas2(self)
            Ventas.tablaVentas(0)

        except Exception as error:
            print('Error alta factura: %s' % str(error))

    def abrirCalendar(self):
        try:
            var.dlgCalendar.show()
        except Exception as error:
            print('Error cal: %s' % str(error))

    def cargarFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editFechaFac.setText(str(data))
            var.dlgCalendar.hide()
        except Exception as error:
            print('Error cargar fecha factura: %s' % str(error))

    def tablaVentas(index):
        try:
            var.cmbventa = QtWidgets.QComboBox()
            conexion.Conexion.cargarCmbVentas(var.cmbventa)
            var.ui.tabVenta.setRowCount(index + 1)
            var.ui.tablaPro.setItem(index, 0, QtWidgets.QTableWidgetItem())
            var.ui.tabVenta.setCellWidget(index, 1, var.cmbventa)
            var.ui.tablaPro.setItem(index, 2, QtWidgets.QTableWidgetItem())
            var.ui.tablaPro.setItem(index, 3, QtWidgets.QTableWidgetItem())
            var.ui.tablaPro.setItem(index, 4, QtWidgets.QTableWidgetItem())
        except Exception as error:
            print('Error ventas: Preparar tabla ventas %s' % str(error))

    def cargarFac(self):
        '''modulo que carga los datos de la factura y cliente'''
        try:
            var.subfac = 0.00
            var.fac = 0.00
            var.iva = 0.00
            fila = var.ui.tabFactura.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codF = fila[0]
            var.ui.lblCodFac.setText(str(codF[0]))
            var.ui.editFechaFac.setText(str(fila[1]))
            conexion.Conexion.cargarFacturas(str(codF))
            Ventas.mostrarVentasFac(self)
            conexion.Conexion.mostrarProductos(self)

        except Exception as error:
            print('Error ventas: cargar fac %s' % str(error))

    def borrarFac(self):
        try:
            cod = var.ui.lblCodFac.text()
            conexion.Conexion.borrarFac(cod)
            Ventas.tablaVentas(0)
        except Exception as error:
            print('Error ventas: borrar fac %s' % str(error))

    # def buscarCliVenta(self):
    #     try:
    #         dni = var.ui.editDniFac
    #         if Clientes.validarDni(dni):
    #             var.ui.editDni.setText(dni.upper())
    #         else:
    #
    #             var.ui.lblValidar.setStyleSheet('QLabel {color:red;}')
    #             var.ui.lblValidar.setText('X')
    #             var.ui.editDni.setText(dni.upper())
    #             mensaje = 'Ese DNI es erróneo'
    #             events.Eventos.AbrirAviso(mensaje)
    #             Clientes.limpiarDatos()
    #             dniOk=False
    #     except Exception as error:
    #         print('Error ventas: bucar cliente venta %s' % str(error))

    def procesoVenta(self):
        try:
            var.subfac = 0.00
            var.venta = []
            # insertamos en venta codFac, codPro, nombreArt, cantidad, precio, subtotal, row
            codFac = var.ui.lblCodFac.text()
            var.venta.append(int(codFac))
            articulo = var.cmbventa.currentText()
            dato = conexion.Conexion.obtenerCodPrecio(articulo)

            var.venta.append(int(dato[0]))  # codigo del producto
            var.venta.append(articulo)
            row = var.ui.tabVenta.currentRow()
            cantidad = var.ui.tabVenta.item(row, 2).text()
            cantidad = cantidad.replace(',', '.')
            var.venta.append(int(cantidad))
            precio = dato[1].replace(',', '.')
            var.venta.append(round(float(precio), 2))
            subtotal = round(float(cantidad) * float(dato[1]), 2)
            var.venta.append(subtotal)
            var.venta.append(row)
            #print(var.venta)
            if codFac != '' and articulo != '' and cantidad != '':
                conexion.Conexion.altaVenta()
                print(var.venta)
                var.subfac = round(float(subtotal) + float(var.subfac), 2)
                var.ui.lblSubtotal.setText(str(var.subfac))
                var.iva = round(float(var.subfac) * 0.21, 2)
                var.ui.lblIva.setText(str(var.iva))
                var.fac = round(float(var.iva) + float(var.subfac), 2)
                var.ui.lblTotal.setText(str(var.fac))
                Ventas.mostrarVentasFac(self)
                conexion.Conexion.mostrarProductos(self)
            else:
               var.ui.lblstatus.setText('Faltan Datos de la Factura')
        except Exception as error:
            print('Error ventas: proceso venta fac %s' % str(error))


    def mostrarVentasFac(self):
        try:
            var.cmbventa = QtWidgets.QComboBox()
            codfac = var.ui.lblCodFac.text()
            conexion.Conexion.listadoVentasFacturas(int(codfac))
            conexion.Conexion.cargarCmbVentas(var.cmbventa)
        except Exception as error:
            print('Error ventas: mostrar ventas de facturas %s' % str(error))

    def anularVenta(self):
        try:
            fila = var.ui.tabVenta.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codventa = int(fila[0])
            conexion.Conexion.anulaVenta(codventa)
            Ventas.mostrarVentasFac(self)

        except Exception as error:
            print('Error ventas: proceso anular venta de una factura: %s' % str(error))
