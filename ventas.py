import conexion
import var
from ventana import *


class Ventas:

    @staticmethod
    def selFacPagada():
        """

        Módulo que checkea que valores de pago de factura se seleccionan el el checkbox y los añade a una variable
        lista var.facpagada

        :return: None
        :rtype: None

        En QtDesigner se deben agrupar los checkbox en un buttongroup

        """
        try:
            if var.ui.chkFacPagada.isChecked():
                var.facPagada = 'Pagada'
            else:
                var.facPagada = ''
        except Exception as error:
            print('Error clients: pago: %s' % str(error))

    @staticmethod
    def altaFactura():
        """

        Módulo que graba una factura previa al proceso de ventas

        :return: None
        :rtype: None

        Una vez grabada prepara la tabla factura y recarga la tabla ventas

        """
        try:
            dni = var.ui.editDniFac.text()
            fecha = var.ui.editFechaFac.text()
            apel = var.ui.editApellidosFac.text()
            estado = var.facPagada
            if dni != '' and fecha != '':
                conexion.Conexion.altaFac(str(dni), str(fecha), str(apel), str(estado))
            conexion.Conexion.mostrarFacturas()
            Ventas.tablaVentas(0)

        except Exception as error:
            print('Error ventas: alta factura 333: %s' % str(error))

    @staticmethod
    def abrirCalendar():
        """

        Módulo que abre la ventana calendario para cargar la fecha

        :return: None
        :rtype: None

        """
        try:
            var.dlgCalendar.show()
        except Exception as error:
            print('Error cal: %s' % str(error))

    @staticmethod
    def cargarFecha(qDate):
        """

        Módulo que se ejecuta cuando clickamos en un dia en el calendat

        :param qDate: fecha de la factura
        :type qDate: QtCore.QDate
        :return: None
        :rtype: None

        Cuando clickamos en el calendario carga la fecha en el editFechaFac

        """
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editFechaFac.setText(str(data))
            var.dlgCalendar.hide()
        except Exception as error:
            print('Error ventas: cargar fecha factura: %s' % str(error))

    @staticmethod
    def tablaVentas(index):
        """

        Módulo prepara la tabla ventas

        :param index: fila de la tabla en la que insertar
        :type index: entero
        :return: None
        :rtype: None

        Carga la venta en la venta

        """
        try:
            var.cmbventa = QtWidgets.QComboBox()
            conexion.Conexion.cargarCmbVentas()
            var.ui.tabVenta.setRowCount(index + 1)
            var.ui.tablaPro.setItem(index, 0, QtWidgets.QTableWidgetItem())
            var.ui.tabVenta.setCellWidget(index, 1, var.cmbventa)
            var.ui.tablaPro.setItem(index, 2, QtWidgets.QTableWidgetItem())
            var.ui.tablaPro.setItem(index, 3, QtWidgets.QTableWidgetItem())
            var.ui.tablaPro.setItem(index, 4, QtWidgets.QTableWidgetItem())
        except Exception as error:
            print('Error ventas: Preparar tabla ventas %s' % str(error))

    @staticmethod
    def cargarFac():
        """

        Modulo que carga los datos de la factura y cliente

        :return: None
        :rtype: None
        
        """
        ''''''
        try:
            var.subfac = 0.00
            var.fac = 0.00
            var.iva = 0.00
            fila = var.ui.tabFactura.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            var.ui.lblCodFac.setText(str(fila[0]))
            var.ui.editFechaFac.setText(str(fila[1]))
            conexion.Conexion.cargarDatosClienteFactura(int(fila[0]))
            Ventas.mostrarVentasFac()
            conexion.Conexion.mostrarProductos()

        except Exception as error:
            print('Error ventas: cargar fac %s' % str(error))

    @staticmethod
    def borrarFac():
        """

        Módulo que borra una factua

        :return: None
        :rtype: None

        Coge el código de la factura del widget lblCodFac y conecta con el módulo conexion.borrarFactura
        Luego recarga la tablaVentas

        """
        try:
            cod = var.ui.lblCodFac.text()
            conexion.Conexion.borrarFactura(cod)
            Ventas.tablaVentas(0)
        except Exception as error:
            print('Error ventas: borrar fac %s' % str(error))

    @staticmethod
    def actualizarFac():
        """

        Módulo que actualiza el estado (pagada o no) de una factua

        :return: None
        :rtype: None

        Coge el código de la factura del widget lblCodFac y conecta con el módulo conexion.actualizarFactura
        Luego recarga la tablaVentas

        """
        try:
            cod = var.ui.lblCodFac.text()
            estado = var.facPagada
            conexion.Conexion.actualizarFactura(cod, estado)
        except Exception as error:
            print('Error ventas: borrar fac %s' % str(error))

    @staticmethod
    def procesoVenta():
        """

        Módulo que procesa una venta de una factura

        :return: None
        :rtype: None

        Recoge todos los datos de la venta y los mete en la variable var.venta. Da de alta la venta llamando al
        módulo conexion.altaVenta. Calcula el subtotal de la factura, el iva y el total y lo muestra en los widgets
        correspondientes.
        Recarga la tabla ventas y la tabla productos.
        Si falta algún dato en la factura o la venta, muestra mensaje en la barra de estado.

        """
        try:
            var.subfac = 0.00
            var.venta = []
            codFac = var.ui.lblCodFac.text()
            var.venta.append(int(codFac))
            articulo = var.cmbventa.currentText()
            dato = conexion.Conexion.obtenerCodPrecio(articulo)
            var.venta.append(int(dato[0]))
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
            if codFac != '' and articulo != '' and cantidad != '':
                conexion.Conexion.altaVenta()
                var.subfac = round(float(subtotal) + float(var.subfac), 2)
                var.ui.lblSubtotal.setText(str(var.subfac))
                var.iva = round(float(var.subfac) * 0.21, 2)
                var.ui.lblIva.setText(str(var.iva))
                var.fac = round(float(var.iva) + float(var.subfac), 2)
                var.ui.lblTotal.setText(str(var.fac))
                Ventas.mostrarVentasFac()
                conexion.Conexion.mostrarProductos()
            else:
                var.ui.lblstatus.setText('Faltan Datos de la Factura')
        except Exception as error:
            print('Error ventas: proceso venta fac %s' % str(error))

    @staticmethod
    def mostrarVentasFac():
        """

        Método que muestra las ventas de una factura

        :return: None
        :rtype:None

        Carga el combo de ventas y recoge el codigo de la factura. Conecta con el método listadoVentasFacturas
        pasandole el codigo y luego recarga el combo.

        """
        try:
            var.cmbventa = QtWidgets.QComboBox()
            codfac = var.ui.lblCodFac.text()
            conexion.Conexion.listadoVentasFacturas(int(codfac))
            conexion.Conexion.cargarCmbVentas()
        except Exception as error:
            print('Error ventas: mostrar ventas de facturas %s' % str(error))

    @staticmethod
    def anularVenta():
        """

        Módulo que borra una venta

        :return: None
        :rtype: None

        Recoge el codigo de la venta y se lo pasa al módulo conexion.anularVenta que lo borrará de la base de datos

        """
        try:
            fila = var.ui.tabVenta.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codventa = int(fila[0])
            conexion.Conexion.anulaVenta(codventa)
            Ventas.mostrarVentasFac()

        except Exception as error:
            print('Error ventas: proceso anular venta de una factura: %s' % str(error))
