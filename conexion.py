from PyQt5 import QtWidgets, QtSql
# import  pymongo
import var, time
import ventas


class Conexion():
    def db_connect(filename):
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

    def altaCli(cliente):
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
            Conexion.mostarClientes(None)
            var.ui.lblstatus.setText('Cliente con dni ' + str(cliente[0]) + ' dado de alta, dia ' + time.strftime("%x"))
            print('Insercion correcta')
        else:
            print("Error alta: ", query.lastError().text())

    def mostrarClientes(self):
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
            print('Error mostrar clientes: ' + query.lastError().text())

    def cargarCliente(self):
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

    def bajaCliente(dni):
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
            var.ui.lblstatus.setText('Cliente con dni ' + dni + ' dado de baja, dia' + time.strftime("%x"))
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    def modCliente(codigo, newdata):
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
            print('Error modificar cliente: ', query.lastError().text())

    def buscarCliente(dni):
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

                var.ui.tablaCli.setRowCount(index + 1)  # crea la fila y a continuacion mete los datos
                var.ui.tablaCli.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(1))))
                var.ui.tablaCli.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(2))))
                var.ui.tablaCli.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(3))))

    def altaPro(producto):
        query = QtSql.QSqlQuery()
        query.prepare('insert into articulos (nombre, precio, stock)'
                      'VALUES (:nombre, :precio, :stock)')
        query.bindValue(':nombre', str(producto[0]))
        # cambiamos la coma por el punto
        producto[1] = producto[1].replace(',', '.')
        query.bindValue(':precio', round(float(producto[1]), 2))
        query.bindValue(':stock', int(producto[2]))
        if query.exec_():
            Conexion.mostarProductos(None)
            var.ui.lblstatus.setText(
                'Producto con nombre ' + str(producto[0]) + ' dado de alta, dia ' + time.strftime("%x"))
            print('Insercion correcta')
        else:
            print("Error producto: ", query.lastError().text())

    def mostrarProductos(self):
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
                var.ui.tablaPro.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio)))
                index += 1
        else:
            print('Error mostrar producto ddd: ' + query.lastError().text())

    def cargarProducto(self):
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

    def bajaProducto(nombre):
        query = QtSql.QSqlQuery()
        query.prepare('delete from articulos where nombre = :nombre')
        query.bindValue(':nombre', nombre)
        if query.exec_():
            print('Baja producto')
            var.ui.lblstatus.setText('Producto con nombre ' + nombre + ' dado de baja, dia' + time.strftime("%x"))
        else:
            print("Error eliminar producto: ", query.lastError().text())

    def modProducto(codigo, newdata):
        print(newdata)
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        print(codigo, newdata)
        query.prepare('update articulos set nombre=:nombre, precio=:precio, stock=:stock where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':nombre', str(newdata[0]))
        newdata[1] = newdata[1].replace(',', '.')
        query.bindValue(':precio', round(float(newdata[1]), 2))
        query.bindValue(':stock', int(newdata[2]))
        if query.exec_():
            print('Producto modificado')
            var.ui.lblstatus.setText(
                'Producto con nombre ' + str(newdata[0]) + ' modificado, dia ' + time.strftime("%x"))
        else:
            print('Error modificar producto: ', query.lastError().text())

    '''FACTURACION'''

    def cargarCmbVentas(cmbventa):
        var.cmbventa.clear()
        query = QtSql.QSqlQuery()
        var.cmbventa.addItem('')
        query.prepare('select codigo, nombre from articulos order by nombre')
        if query.exec_():
            while query.next():
                var.cmbventa.addItem(str(query.value(1)))

    def altaFac(dni, fecha, apel):
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into facturas (dniCliente, fechaFactura, apellidos) VALUES (:dniCliente, :fechaFactura, :apellidos)')
        query.bindValue(':dniCliente', str(dni))
        query.bindValue(':fechaFactura', str(fecha))
        query.bindValue(':apellidos', str(apel))
        if query.exec_():
            var.ui.lblstatus.setText('Factura creada')
        query1 = QtSql.QSqlQuery()
        query1.prepare('select max(numFac) from facturas')
        if query1.exec_():
            while query1.next():
                var.ui.lblCodFac.setText(str(query1.value(0)))

    def mostrarFacturas(self):
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select numFactura, fechaFactura from facturas order by numFactura desc')
        if query.exec_():
            while query.next():
                # creamos fila
                var.ui.tabFactura.setRowCount(index + 1)
                # vamos metiendo los datos en cada celda de la fila
                var.ui.tabFactura.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                var.ui.tabFactura.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                index += 1
            Conexion.limpiarFac(self)
            var.ui.tabFactura.selectRow(0)
            var.ui.tabFactura.setFocus()
        else:
            print("Error mostrar facturas: ", query.lastError().text())
        if index == 0:
            var.ui.tabFactura.clearContents()

    def mostrarFacturasCli():
        index = 0
        cont = 0
        dni = var.ui.editDniFac.text()
        query = QtSql.QSqlQuery()
        query.prepare('select numFactura, fechaFactura from facturas where dniCliente = :dni order by fechaFactura desc')
        query.bindValue(':dni', str(dni))
        if query.exec_():
            while query.next():
                # cojo valores
                cont =+ 1
                codFac = query.value(0)
                fecha = query.value(1)
                # crear fila
                var.ui.tabFactura.setRowCount(index + 1)
                # vamos metiendo los datos en cada celda de la fila
                var.ui.tabFactura.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codFac)))
                var.ui.tabFactura.setItem(index, 1, QtWidgets.QTableWidgetItem(str(fecha)))
                index += 1
            if cont == 0:
                var.ui.tabFactura.selectRow(0)
                var.ui.lblstatus.setText('Cliente sin facturas')
        else:
            print("Error mostrar facturas cliente: ", query.lastError().text())


    def limpiarFac(self):
        datosFac = [var.ui.editDniFac, var.ui.editApellidosFac, var.ui.lblCodFac, var.ui.editFechaFac]
        for i, data in enumerate(datosFac):
            datosFac[i].setText('')

    def cargarFacturas(cod):
        query = QtSql.QSqlQuery()
        query.prepare('select dniCliente, apellidos from facturas where numFac = :numFac)')
        query.bindValue(':numFac', int(cod))
        if query.exec_():
            while query.next():
                var.ui.editApellidosFac.setText(str(query.value(1)))
                var.ui.editDniFac.setText(str(query.value(0)))

    def cargarFacturas2(self):
        query = QtSql.QSqlQuery()
        query.prepare('select numFac, dniCliente, fechaFactura, apellidos from facturas order by numFac desc LIMIT 1)')
        if query.exec_():
            while query.next():
                var.ui.lblCodFac.setText(str(query.value(0)))
                var.ui.editDniFac.setText(str(query.value(1)))
                var.ui.editFechaFac.setText(str(query.value(2)))
                var.ui.editApellidosFac.setText(query.value(3))

    def borrarFactura(cod):
        query = QtSql.QSqlQuery()
        query.prepare('delete from facturas where numFac = :numFac)')
        query.bindValue(':numFac', int(cod))
        if query.exec_():
            var.ui.lblstatus.setText('Factura anulada')
            Conexion.mostrarFacturas()
        else:
            print('Error anular factura en borrarFactura ', query.lastError().text())

        query1 = QtSql.QSqlQuery()
        query1.prepare('delete from ventas where codFacVenta = :numFac)')
        query1.bindValue(':numFac', int(cod))
        if query1.exec_():
            var.ui.lblstatus.setText('Factura anulada')

    def obtenerCodPrecio(articulo):
        dato = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio, stock from articulos where nombre = :articulo')
        query.bindValue(':articulo', str(articulo))
        if query.exec_():
            while query.next():
                dato = [str(query.value(0)), str(query.value(1))]
        return dato

    def altaVenta(self):
        # insertamos en venta codFac, codPro, nombreArt, cantidad, precio, subtotal, row
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into ventas (codFacVenta, codArtVenta, cantidad, precio) VALUES (:codFacVenta, :codArtVenta, :cantidad, :precio)')
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
            Conexion.cargarCmbVentas(var.cmbventa)
        else:
            print('Error alta venta: ', query.lastError().text())


    def listadoVentasFacturas(codFac):
        '''Modulo lista ventas contenidas en una factura
            :param codfac: valor factura a la que se incluirán las líneas de venta
            :type codfac: int

            Recibe el código de la factura para seleccionar los datos de las ventas cargadas a esta.
        De la BB.DD toma el nombre del producto y su precio para cada línea de venta. El precio lo multiplica
        por las unidades y se obtiene el subtotal de cada línea. Después en cada línea de la tabla irá
        el código de la venta, el nombre del producto, las unidades y dicho subotal.
        Finalmente, va sumando el subfact, que es la suma de todas las ventas de esa factura, le aplica el IVA y
        el importe total de la factura. Los tres valores, subfact, iva y fac los muestra en los label asignados.

        En excepciones se recoge cualquier error que se produzca en la ejecución del módulo.
        '''
        try:
            var.subfac = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codFacVenta, codArtVenta, cantidad from ventas where codFacVenta = :codFac')
            query.bindValue(':codFac', int(codFac))
            if query.exec_():
                index = 0
                while query.next():
                    codVenta = query.value(0)
                    codArtVenta = query.value(1)
                    cantidad = query.value(2)
                    var.ui.tabVenta.setRowCount(index + 1)
                    var.ui.tabVenta.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codVenta)))
                    query1.prepare('select articulo, precio from articulos where codigo = :codArtVenta')
                    query1.bindValue(':codArtVenta', int(codArtVenta))
                    if query1.exec_():
                        while query1.next():
                            articulo = query1.value(0)
                            precio = query1.value(1)
                            var.ui.tabVenta.setItem(index, 1, QtWidgets.QTableWidgetItem(str(articulo)))
                            var.ui.tabVenta.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
                            subtotal = round(float(cantidad) * float(precio), 2)
                            var.ui.tabVenta.setItem(index, 3, QtWidgets.QTableWidgetItem(str(precio)))
                            var.ui.tabVenta.setItem(index, 4, QtWidgets.QTableWidgetItem(str(subtotal)))
                    index += 1
                    var.subfac = round(float(subtotal) + float(var.subfac), 2)

            if int(index) > 0:
                ventas.Ventas.prepararTablaventas(index)
            else:
                print(index)
                var.ui.tabVenta.setRowCount(0)
                ventas.Ventas.TablaVentas(0)
            var.ui.lblSubtotal.setText(str(var.subfac))
            var.iva = round(float(var.subfac) * 0.21, 2)
            var.ui.lblIva.setText(str(var.iva))
            var.fac = round(float(var.iva) + float(var.subfac), 2)
            var.ui.lblTotal.setText(str(var.fac))
        except Exception as error:
            print('Error Listado de la tabla de ventas: %s ' % str(error))


    def anulaVenta(codVenta):
        query = QtSql.QSqlQuery()
        query.prepare('delete from ventas where codVenta = :codVenta')
        query.bindValue(':codVenta', codVenta)
        if query.exec_():
            var.ui.lblstatus.setText('Venta Anulada')
        else:
            print("Error baja venta: ", query.lastError().text())

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
