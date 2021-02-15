from PyQt5 import QtWidgets, QtSql, QtCore
# import  pymongo
import var, time
import ventas


class Conexion():

    def db_connect(self, filename):
        """

        Módulo que realiza la conexion de la aplicacion con la bd

        :param filename: nombre de la base de datos
        :type filename: string
        :return: bool
        :rtype: True/False

        Utiliza la libreria de QtSql y el gestor de la BBDD es SqLite. En caso de error muestra pantalla de aviso

        """
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filename)
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos',
                                           'No se puede establecer conexion.\n'
                                           'Haz click para cancelar', QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexion establecida')
        return True

    def altaCli(self, cliente):
        """

        Módulo que da de alta un cliente con los datos pasados por lista. Muestra mensaje de resultado en la statusbar.
        Rescarga la tablaCli

        :param cliente: datos del cliente
        :type cliente: lista
        :return: None
        :rtype: None

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into clientes (dni, apellidos, nombre, fechaAlta, direccion, provincia, sexo, edad, formasPago)'
            'VALUES (:dni, :apellidos, :nombre, :fechaAlta, :direccion, :provincia, :sexo, :edad, :formasPago)')
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechaAlta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        query.bindValue(':edad', str(cliente[7]))
        query.bindValue(':formasPago', str(cliente[8]))
        if query.exec_():
            Conexion.mostrarClientes(None)
            var.ui.lblstatus.setText('Cliente con dni ' + str(cliente[0]) + ' dado de alta, dia ' + time.strftime("%x"))
            print('Insercion correcta')
        else:
            print("Error conexion: alta: ", query.lastError().text())

    def cargarDatos(self):
        """

        Carga los datos iniciales del programa

        :return: None
        :rtype: None

        """
        Conexion.db_connect(self, var.filebd)
        Conexion.mostrarClientes(self)
        Conexion.mostrarProductos(self)
        Conexion.mostrarFacturas(self)

    def mostrarClientes(self):
        """

        Carga los clientes de la base de datos en la tablaCli

        :return: None
        :rtype: None

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos, nombre from clientes')
        if query.exec_():
            while query.next():
                dni = query.value(0)
                apellidos = query.value(1)
                nombre = query.value(2)
                var.ui.tablaCli.setRowCount(index + 1)  # crea la fila y a continuacion mete los datos
                var.ui.tablaCli.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tablaCli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tablaCli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print('Error conexion: mostrar clientes: ' + query.lastError().text())

    def cargarCliente(self):
        """

        Carga los datos de un cliente cuando se clicka en la tabla

        :return: None
        :rtype: None

        """
        dni = var.ui.editDni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodCli.setText(str(query.value(0)))
                var.ui.editDniFac.setText(str(query.value(1)))
                var.ui.editApellidosFac.setText(str(query.value(2)))
                var.ui.editCliAlta.setText(query.value(4))
                var.ui.editDireccion.setText(str(query.value(5)))
                var.ui.cmbProvincia.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFemenino.setChecked(True)
                    var.ui.rbtMasculino.setChecked(False)
                else:
                    var.ui.rbtFemenino.setChecked(False)
                    var.ui.rbtMasculino.setChecked(True)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(9):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(9):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(9):
                    var.chkpago[2].setChecked(True)
                var.ui.spinEdad.setValue(int(query.value(8)))

    def bajaCliente(self, dni):
        """

        Módulo que da de baja a un cliente.

        :param dni: dni del cliente
        :type dni: string
        :return: None
        :rtype: None

         Da de baja a un cliente con el dni pasado. Muestra los datos pasados. Muestra un mensaje en la barra de estado.

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
            var.ui.lblstatus.setText('Cliente con dni ' + dni + ' dado de baja, dia' + time.strftime("%x"))
        else:
            print("Error conexion: mostrar clientes: ", query.lastError().text())

    def modCliente(self, codigo, newdata):
        """

        Modulo que modifica los datos del cliente

        :param codigo: codigo del cliente
        :type codigo: string
        :param newdata: datos actualizados
        :type newdata: lista
        :return: None
        :rtype: None

        Se actualizan los datos pasados en la lista del cliente con el codigo dado. En realidad coge todos los datos que
         hay en los widgets. Muestra mensaje en la barra de estado.

        """
        print(newdata)
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        print(codigo, newdata)
        query.prepare('update clientes set dni=:dni, apellidos=:apellidos, nombre=:nombre, fechaAlta=:fechaAlta,'
                      'direccion=:direccion, provincia=:provincia, sexo=:sexo, edad=:edad, formasPago=:formasPago where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':dni', str(newdata[0]))
        query.bindValue(':apellidos', str(newdata[1]))
        query.bindValue(':nombre', str(newdata[2]))
        query.bindValue(':fechaAlta', str(newdata[3]))
        query.bindValue(':direccion', str(newdata[4]))
        query.bindValue(':provincia', str(newdata[5]))
        query.bindValue(':sexo', str(newdata[6]))
        query.bindValue(':edad', int(newdata[7]))
        query.bindValue(':formasPago', str(newdata[8]))
        if query.exec_():
            print('Cliente modificado')
            var.ui.lblstatus.setText('Cliente con dni ' + str(newdata[0]) + ' modificado, dia ' + time.strftime("%x"))
        else:
            print('Error conexion: modificar cliente: ', query.lastError().text())

    def buscarCliente(self, dni):
        """

        Módulo que busca cliente y carga sus datos en la pantalla cliente.

        :param dni: dni del cliente a buscar
        :type dni: string
        :return: None
        :rtype: None

        Busca en la base de datos el cliente con ese dni y carga los datos en los widgets, si existe.

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodCli.setText(str(query.value(0)))
                var.ui.editApellidos.setText(str(query.value(2)))
                var.ui.editNombre.setText(str(query.value(3)))
                var.ui.editCliAlta.setText(query.value(4))
                var.ui.editDireccion.setText(str(query.value(5)))
                var.ui.cmbProvincia.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFemenino.setChecked(True)
                    var.ui.rbtMasculino.setChecked(False)
                else:
                    var.ui.rbtFemenino.setChecked(False)
                    var.ui.rbtMasculino.setChecked(True)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(9):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(9):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(9):
                    var.chkpago[2].setChecked(True)
                var.ui.spinEdad.setValue(int(query.value(8)))

                var.ui.tablaCli.setRowCount(index + 1)
                var.ui.tablaCli.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(1))))
                var.ui.tablaCli.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(2))))
                var.ui.tablaCli.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(3))))

    """PRODUCTOS"""

    def altaPro(self, producto):
        """

        Módulo que da de alta un producto.

        :param producto: datos del producto
        :type producto: lista
        :return: None
        :rtype: None

        Muestra mensaje de resultado en la statusbar.
        Rescarga la tablaPro

        """
        query = QtSql.QSqlQuery()
        query.prepare('insert into articulos (nombre, precio, stock)'
                      'VALUES (:nombre, :precio, :stock)')
        query.bindValue(':nombre', str(producto[0]))
        # cambiamos la coma por el punto
        producto[1] = producto[1].replace(',', '.')
        query.bindValue(':precio', round(float(producto[1]), 2))
        query.bindValue(':stock', int(producto[2]))
        if query.exec_():
            Conexion.mostrarProductos(None)
            var.ui.lblstatus.setText(
                'Producto con nombre ' + str(producto[0]) + ' dado de alta, dia ' + time.strftime("%x"))
        else:
            print("Error conexion: alta producto: ", query.lastError().text())

    def mostrarProductos(self):
        """

        Módulo que carga los productos en la tablaPro

        :return: None
        :rtype: None

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, nombre, precio from articulos')
        if query.exec_():
            while query.next():
                codigo = query.value(0)
                nombre = query.value(1)
                precio = query.value(2)
                var.ui.tablaPro.setRowCount(index + 1)  # crea la fila y a continuacion mete los datos
                var.ui.tablaPro.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                var.ui.tablaPro.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
                var.ui.tablaPro.setItem(index, 2, QtWidgets.QTableWidgetItem("{0:.2f}".format(float(precio)) + ' €'))

                var.ui.tablaPro.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                var.ui.tablaPro.item(index, 2).setTextAlignment(QtCore.Qt.AlignRight)
                index += 1
        else:
            print('Error conexion mostrar producto: ' + query.lastError().text())

    def cargarProducto(self):
        """

        Módulo carga los datos de un producto

        :return: None
        :rtype: None

        """
        nombre = var.ui.editNombrePro.text()
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio, stock from articulos where nombre = :nombre')
        query.bindValue(':nombre', nombre)
        print('cargar prducto')
        if query.exec_():
            while query.next():
                var.ui.lblCodPro.setText(str(query.value(0)))
                var.ui.editNombrePro.setText(nombre)
                var.ui.editPrecio.setText(str(query.value(1)))
                var.ui.editStock.setText(str(query.value(2)))

    def nombreProducto(self, cod):
        """

        Módulo que devuelve el nombre de un producto

        :param cod: codigo del producto
        :type cod: int
        :return: nombre del producto
        :rtype: string

        """
        query = QtSql.QSqlQuery()
        query.prepare('select nombre from articulos where codigo = :codigo')
        query.bindValue(':codigo', int(cod))
        if query.exec_():
            while query.next():
                nombre = query.value(0)
                return str(nombre)

    def existeProducto(self, nombre):
        """

        Módulo que busca si existe un producto por su nombre

        :param nombre: nombre del producto
        :type nombre: string
        :return: lista con datos del producto
        :rtype: lista

        Busca en la bd si existe el producto. Si existe devuelve una lista con todos los datos de este.
        Si no existe devuelve una lista vacia

        """
        producto = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio, stock from articulos where nombre = :nombre')
        query.bindValue(':nombre', str(nombre))
        if query.exec_():
            while query.next():
                producto.append(query.value(0))
                producto.append(nombre)
                producto.append(query.value(1))
                producto.append(query.value(2))
                return producto
        else:
            return False

    def bajaProducto(self, nombre):
        """

        Módulo que da de baja un producto

        :param nombre: nombre del producto
        :type nombre: string
        :return: None
        :rtype: None

        Borra de la base de datos el producto con ese nombre. Muestra mensaje en la barra de estado.

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from articulos where nombre = :nombre')
        query.bindValue(':nombre', nombre)
        if query.exec_():
            var.ui.lblstatus.setText('Producto con nombre ' + nombre + ' dado de baja, dia' + time.strftime("%x"))
        else:
            print("Error conexion: eliminar producto: ", query.lastError().text())

    def modProducto(self, codigo, newdata):
        """

        Módulo que modifica un producto.

        :param codigo: codigo del producto a modificar
        :type codigo: int
        :param newdata: datos actualizados del producto
        :type newdata: lista
        :return: None
        :rtype: None

        Se actualizan los datos pasados en la lista del producto con el codigo dado. En realidad coge todos los datos que
        hay en los widgets. Muestra mensaje en la barra de estado.

        """
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update articulos set nombre=:nombre, precio=:precio, stock=:stock where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':nombre', str(newdata[0]))
        newdata[1] = str(newdata[1]).replace(',', '.')
        query.bindValue(':precio', round(float(newdata[1]), 2))
        query.bindValue(':stock', int(newdata[2]))
        if query.exec_():
            var.ui.lblstatus.setText(
                'Producto con nombre ' + str(newdata[0]) + ' modificado, dia ' + time.strftime("%x"))
        else:
            print('Error conexion: modificar producto: ', query.lastError().text())

    '''FACTURACION/VENTA'''

    def cargarCmbVentas(self):
        """

        Módulo que carga los productos en el combo de ventas de la pantalla facturación

        :return: None
        :rtype: None

        Recoge los productos de la base de datos y los carga en el cmbVenta

        """
        var.cmbventa.clear()
        query = QtSql.QSqlQuery()
        var.cmbventa.addItem('')
        query.prepare('select codigo, nombre from articulos order by nombre')
        if query.exec_():
            while query.next():
                var.cmbventa.addItem(str(query.value(1)))

    def altaFac(self, dni, fecha, apel, estado):
        """

        Módulo que da de alta una factura de un cliente

        :param dni: dni del cliente
        :type dni: string
        :param fecha: fecha de alta
        :type fecha: string
        :param apel: apellidos del cliente
        :type apel: string
        :return: None
        :rtype: None

        Inserta en la base de datos una nueva factura con los datos pasados.
        Escribe un mensaje en la barra de estado.
        Busca en la base de datos la ultima factura, que será la del código mayor, y carga el código en el widget de
        código de la factura.


        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into facturas (dniCliente, fechaFactura, apellidos, estado) VALUES (:dniCliente, :fechaFactura, :apellidos, :estado)')
        query.bindValue(':dniCliente', str(dni))
        query.bindValue(':fechaFactura', str(fecha))
        query.bindValue(':apellidos', str(apel))
        query.bindValue(':estado', str(estado))
        if query.exec_():
            var.ui.lblstatus.setText('Factura creada')
        else:
            print("Error conexion: alta facturas: ", query.lastError().text())
        query1 = QtSql.QSqlQuery()
        query1.prepare('select max(numFactura) from facturas')
        if query1.exec_():
            while query1.next():
                var.ui.lblCodFac.setText(str(query1.value(0)))
                print(query1.value(0))
        else:
            print("Error conexion: alta facturas codFac ", query.lastError().text())

    def mostrarFacturas(self):
        """

        Módulo que carga las facturas en la tabFactura

        :return: None
        :rtype: None

        Carga la tabla de facturas. Cuando acaba limpia los widgets de los datos de las facturas y pone el foco
        en la primera factura de la tabla.

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select numFactura, fechaFactura from facturas order by numFactura desc')
        if query.exec_():
            while query.next():
                var.ui.tabFactura.setRowCount(index + 1)
                var.ui.tabFactura.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                var.ui.tabFactura.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                index += 1
            Conexion.limpiarFac(self)
            var.ui.tabFactura.selectRow(0)
            var.ui.tabFactura.setFocus()
        else:
            print("Error conexion: mostrar facturas: ", query.lastError().text())
        if index == 0:
            var.ui.tabFactura.clearContents()

    def mostrarFacturasCli(self):
        """

        Módulo que muestra las facturas de un cliente

        :return: None
        :rtype: None

        Lee el dni del cliente del widget de dni del cliente y busca las facturas de dicho dni. Limpia la tabFactura
        y va cargando los datos de las facturas.
        Muestra mensaje en la barra de estado.

        """
        index = 0
        cont = 0
        var.ui.tabFactura.clearContents()
        dni = var.ui.editDniFac.text()
        query = QtSql.QSqlQuery()
        query.prepare(
            'select numFactura, fechaFactura from facturas where dniCliente = :dni order by fechaFactura desc')
        query.bindValue(':dni', str(dni))
        if query.exec_():
            while query.next():
                cont += 1
                codFac = query.value(0)
                fecha = query.value(1)
                var.ui.tabFactura.setRowCount(index + 1)
                var.ui.tabFactura.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codFac)))
                var.ui.tabFactura.setItem(index, 1, QtWidgets.QTableWidgetItem(str(fecha)))
                index += 1
            if cont == 0:
                var.ui.tabFactura.selectRow(0)
                var.ui.lblstatus.setText('Cliente sin facturas')
            else:
                var.ui.lblstatus.setText('Facturas del cliente con dni ' + str(dni) + ' cargadas en la tabla')
        else:
            print("Error conexion: mostrar facturas cliente: ", query.lastError().text())

    def limpiarFac(self):
        """

        Módulo que limpia datos de factura

        :return: None
        :rtype: None

        Limpia los widgets de datos del cliente en la pantalla factura.

        """
        datosFac = [var.ui.editDniFac, var.ui.editApellidosFac, var.ui.lblCodFac, var.ui.editFechaFac]
        for i, data in enumerate(datosFac):
            datosFac[i].setText('')
        var.ui.chkFacPagada.setChecked(False)

    def cargarDatosClienteFactura(self, cod):
        """

        Módulo que carga los datos del cliente con factura

        :param cod: codigo de la factura
        :type cod: int
        :return: None
        :rtype: None

        Busca en la base de datos el cliente al que pertenece la factura con el codigo pasado. Carga los datos en los
        widgets de datos de cliente de la pantalla facturacion.

        """
        query = QtSql.QSqlQuery()
        query.prepare('select dniCliente, apellidos, estado from facturas where numFactura = :numFac')
        query.bindValue(':numFac', int(cod))
        if query.exec_():
            while query.next():
                var.ui.editApellidosFac.setText(str(query.value(1)))
                var.ui.editDniFac.setText(str(query.value(0)))
                if str(query.value(2)) == 'Pagada':
                    var.ui.chkFacPagada.setChecked(True)
                else:
                    var.ui.chkFacPagada.setChecked(False)

    def cargarFacturas(self):
        """

        Módulo que carga todas las facturas (juraria que es inutil pero ahí está=)

        :return: None
        :rtype: None

        no hace nada xd

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'select numFac, dniCliente, fechaFactura, apellidos, estado from facturas order by numFac desc LIMIT 1)')
        if query.exec_():
            while query.next():
                var.ui.lblCodFac.setText(str(query.value(0)))
                var.ui.editDniFac.setText(str(query.value(1)))
                var.ui.editFechaFac.setText(str(query.value(2)))
                var.ui.editApellidosFac.setText(query.value(3))
                if str(query.value(2)) == 'Pagada':
                    var.ui.chkFacPagada.setChecked(True)
                else:
                    var.ui.chkFacPagada.setChecked(False)

    def actualizarFactura(self, cod, estado):
        """

        Módulo que borra una factura

        :param cod: codigo de la factura
        :type cod: int
        :return: None
        :rtype: None

        Elimina de la base de datos la factura con ese código. Muestra un mensaje en la barra de estado.

        """
        query = QtSql.QSqlQuery()
        # print(int(cod))
        query.prepare('update facturas set estado=:estado where numFactura = :codfac')
        query.bindValue(':estado', str(estado))
        query.bindValue(':codfac', int(cod))
        if query.exec_():
            var.ui.lblstatus.setText('Factura actualizada')
            Conexion.mostrarFacturas(self)
        else:
            print('Error conexion: borrar factura en borrarFactura ', query.lastError().text())

    def borrarFactura(self, cod):
        """

        Módulo que borra una factura

        :param cod: codigo de la factura
        :type cod: int
        :return: None
        :rtype: None

        Elimina de la base de datos la factura con ese código. Muestra un mensaje en la barra de estado.

        """
        query = QtSql.QSqlQuery()
        # print(int(cod))
        query.prepare('delete from facturas where numFactura = :codfac')
        query.bindValue(':codfac', int(cod))
        if query.exec_():
            var.ui.lblstatus.setText('Factura anulada')
            Conexion.mostrarFacturas(self)
        else:
            print('Error conexion: borrar factura en borrarFactura ', query.lastError().text())

        query1 = QtSql.QSqlQuery()
        query1.prepare('delete from ventas where codFacVenta = :numFac)')
        query1.bindValue(':numFac', int(cod))
        if query1.exec_():
            var.ui.lblstatus.setText('Factura anulada')

    def obtenerCodPrecio(self, articulo):
        """

        Módulo que devuelve informacion de un producto

        :param articulo: nombre del articulo
        :type articulo: string
        :return: dato
        :rtype: lista

        Busca en la base de datos un articulo con el nombre pasado y devuelve una lista con el código y el precio de ese
        artículo.

        """
        dato = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio, stock from articulos where nombre = :articulo')
        query.bindValue(':articulo', str(articulo))
        if query.exec_():
            while query.next():
                dato = [str(query.value(0)), str(query.value(1))]
        return dato

    def altaVenta(self):
        """

        Módulo que da de alta una venta

        :return: None
        :rtype: None

        Se guarda en la base de datos una venta nueva recogiendo los datos:
            codFac, codPro, nombreArt, cantidad, precio, subtotal
        que están en la variable venta.
        Luego carga los datos en la tabVentas y carga el cmbVentas llamando al método cargarCmbVentas.

        """
        query = QtSql.QSqlQuery()
        query.prepare('insert into ventas (codFacVenta, codArtVenta, cantidad, precio) VALUES'
                      '(:codFacVenta, :codArtVenta, :cantidad, :precio)')
        query.bindValue(':codFacVenta', int(var.venta[0]))
        query.bindValue(':codArtVenta', int(var.venta[1]))
        query.bindValue(':cantidad', int(var.venta[3]))
        query.bindValue(':precio', float(var.venta[4]))

        row = var.ui.tabVenta.currentRow()
        if query.exec_():
            var.ui.lblstatus.setText('Venta Realizada')
            var.ui.tabVenta.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var.venta[2])))
            var.ui.tabVenta.setItem(row, 2, QtWidgets.QTableWidgetItem(str(var.venta[3])))
            var.ui.tabVenta.setItem(row, 3, QtWidgets.QTableWidgetItem(str(var.venta[4])))
            var.ui.tabVenta.setItem(row, 4, QtWidgets.QTableWidgetItem(str(var.venta[5])))
            row = row + 1
            var.ui.tabVenta.insertRow(row)
            var.ui.tabVenta.setCellWidget(row, 1, var.cmbventa)
            var.ui.tabVenta.scrollToBottom()
            Conexion.cargarCmbVentas(self)
        else:
            print('Error conexion: alta venta: ', query.lastError().text())

    def listadoVentasFacturas(self, codFac):
        """

        Modulo que lista ventas contenidas en una factura

        :param codFac: codigo de la factura a la que se incluirán las lineas de venta
        :type codFac: int
        :return: None
        :rtype: None

        Recibe el código de la factura para seleccionar los datos de las ventas cargadas a esta.
        De la BB.DD toma el nombre del producto y su precio para cada línea de venta.
        El precio lo multiplica por las unidades y se obtiene el subtotal de cada línea.
        Después en cada línea de la tabla irá el código de la venta, el nombre del producto, las unidades y dicho subotal.
        Finalmente, va sumando el subfact, que es la suma de todas las ventas de esa factura, le aplica el IVA y
        el importe total de la factura.
        Los tres valores, subfact, iva y fac los muestra en los label asignados.

        En excepciones se recoge cualquier error que se produzca en la ejecución del módulo.

        """
        try:
            var.ui.tabVenta.clearContents()
            var.subfac = 0.00
            subtotal = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codVenta, codArtVenta, cantidad from ventas where codFacVenta = :codFac')
            query.bindValue(':codFac', int(codFac))
            if query.exec_():
                index = 0
                while query.next():
                    codVenta = query.value(0)
                    codArtVenta = query.value(1)
                    cantidad = query.value(2)
                    var.ui.tabVenta.setRowCount(index + 1)
                    var.ui.tabVenta.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codVenta)))
                    query1.prepare('select nombre, precio from articulos where codigo = :codArtVenta')
                    query1.bindValue(':codArtVenta', int(codArtVenta))
                    if query1.exec_():
                        while query1.next():
                            articulo = query1.value(0)
                            precio = query1.value(1)
                            var.ui.tabVenta.setItem(index, 1, QtWidgets.QTableWidgetItem(str(articulo)))
                            var.ui.tabVenta.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
                            subtotal = round(float(cantidad) * float(precio), 2)
                            var.ui.tabVenta.setItem(index, 3,
                                                    QtWidgets.QTableWidgetItem("{0:.2f}".format(float(precio)) + ' €'))
                            var.ui.tabVenta.setItem(index, 4, QtWidgets.QTableWidgetItem(
                                "{0:.2f}".format(float(subtotal)) + ' €'))
                            var.ui.tabVenta.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                            var.ui.tabVenta.item(index, 2).setTextAlignment(QtCore.Qt.AlignCenter)
                            var.ui.tabVenta.item(index, 3).setTextAlignment(QtCore.Qt.AlignRight)
                            var.ui.tabVenta.item(index, 4).setTextAlignment(QtCore.Qt.AlignRight)

                    index += 1
                    var.subfac = round(float(subtotal) + float(var.subfac), 2)

            if int(index) > 0:
                ventas.Ventas.tablaVentas(index)
            else:
                # print(index)
                var.ui.tabVenta.setRowCount(0)
                ventas.Ventas.tablaVentas(0)
            var.ui.lblSubtotal.setText(str(var.subfac))
            var.iva = round(float(var.subfac) * 0.21, 2)
            var.ui.lblIva.setText(str(var.iva))
            var.fac = round(float(var.iva) + float(var.subfac), 2)
            var.ui.lblTotal.setText(str(var.fac))
        except Exception as error:
            print('Error conexion: Listado de la tabla de ventas: %s ' % str(error))

    def anulaVenta(self, codVenta):
        """

        Módulo que borra una venta

        :param codVenta: codigo de la venta a borrar
        :type codVenta: int
        :return: None
        :rtype: None

        Borra la venta con dicho código de la base de datos. Muestra un mensaje en la barra de estados.

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from ventas where codVenta = :codVenta')
        query.bindValue(':codVenta', codVenta)
        if query.exec_():
            var.ui.lblstatus.setText('Venta Anulada')
        else:
            print("Error conexion: baja venta: ", query.lastError().text())

    def totalPrecioFactura(self, codfac):
        """

        Módulo que calcula el precio total de una factura

        :param codFac: codigo de la factura
        :type codFac: int
        :return: total factura
        :rtype: lista

        Recibe el codigo de una factura. Busca sus ventas, las va recorriendo y sumando el total de estas.
        Devuelve el precio total de la factura.

        """
        try:
            venta = 0
            subtotal = 0
            query = QtSql.QSqlQuery()
            query.prepare('select cantidad, precio from ventas where codFacVenta = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                while query.next():
                    venta = round(float(query.value(0)) * float(query.value(1)), 2)
                    subtotal = float(subtotal) + float(venta)

                iva = round(float(subtotal) * 0.21, 2)
                total= round(float(iva) + float(subtotal), 2)

                precio = [float(subtotal), float(iva), float(total)]
                return precio
        except Exception as error:
            print('Error conexion calculo precio total : %s ' % str(error))

# class Conexion():
#     HOST =  'localhost'
#     PORT = '27017'
#     URI_CONECTION = 'mongodb://' + HOST + ':' + PORT + '/'
#     var.DATABASE = 'empresa'
#     try:
#         var.client = pymongo.MongoClient(URI_CONECTION)
#         var.client.server_info()
#         print('OK -- Conexion realizada al servidor %s' % HOST)
#     except:
#         print('Error conexion')
