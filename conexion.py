from PyQt5 import QtWidgets, QtSql
#import  pymongo
import var, time

class Conexion():
    def db_connect(filename):
        db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
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
        query.prepare('insert into clientes (dni, apellidos, nombre, fechaAlta, direccion, provincia, sexo, edad, formasPago)'
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
            var.ui.lblstatus.setText('Cliente con dni ' + str(cliente[0]) + ' dado de alta, dia '+time.strftime("%x"))
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
                var.ui.tablaCli.setRowCount(index+1) #crea la fila y a continuacion mete los datos
                var.ui.tablaCli.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tablaCli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tablaCli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print('Error mostrar clientes: '+query.lastError().text())


    def cargarCliente(self):
        dni = var.ui.editDni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodCli.setText(str(query.value(0)))
                var.ui.editCli.setText(str(query.value(1)))
                var.ui.editApellidosCli.setText(str(query.value(2)))
                var.ui.editCliAlta.setText(query.value(4))
                var.ui.editDireccion.setText(str(query.value(5)))
                var.ui.cmbProvincia.setCurrentText(str(query.value(6)))
                if str(query.value(7))=='Mujer':
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
            var.ui.lblstatus.setText('Cliente con dni '+dni+' dado de baja, dia'+time.strftime("%x"))
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
            var.ui.lblstatus.setText('Cliente con dni '+str(newdata[0])+' modificado, dia '+time.strftime("%x"))
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
                if str(query.value(7))=='Mujer':
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


                var.ui.tablaCli.setRowCount(index+1) #crea la fila y a continuacion mete los datos
                var.ui.tablaCli.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(1))))
                var.ui.tablaCli.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(2))))
                var.ui.tablaCli.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(3))))


    def altaPro(producto):
        query = QtSql.QSqlQuery()
        query.prepare('insert into articulos (nombre, precio, stock)'
                      'VALUES (:nombre, :precio, :stock)')
        query.bindValue(':nombre', str(producto[0]))
        #cambiamos la coma por el punto
        producto[1]  = producto[1].replace(',','.')
        query.bindValue(':precio', round(float(producto[1]),2))
        query.bindValue(':stock', int(producto[2]))
        if query.exec_():
            Conexion.mostarProductos(None)
            var.ui.lblstatus.setText('Producto con nombre ' + str(producto[0]) + ' dado de alta, dia ' + time.strftime("%x"))
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
                var.ui.tablaPro.setRowCount(index + 1) #crea la fila y a continuacion mete los datos
                var.ui.tablaPro.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                var.ui.tablaPro.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
                var.ui.tablaPro.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio)))
                index += 1
        else:
            print('Error mostrar producto ddd: '+query.lastError().text())

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
            var.ui.lblstatus.setText('Producto con nombre '+nombre+' dado de baja, dia'+time.strftime("%x"))
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
        newdata[1] = newdata[1].replace(',','.')
        query.bindValue(':precio', round(float(newdata[1]),2))
        query.bindValue(':stock', int(newdata[2]))
        if query.exec_():
            print('Producto modificado')
            var.ui.lblstatus.setText('Producto con nombre '+str(newdata[0])+' modificado, dia '+time.strftime("%x"))
        else:
            print('Error modificar producto: ', query.lastError().text())

    def cargarCmbVentas(cmbventa):
        cmbventa.clear()
        query = QtSql.QSqlQuery()
        cmbventa.addItem('')
        query.prepare('select codigo, nombre from articulos order by nombre')
        if query.exec_():
            while query.next():
                cmbventa.addItem(str(query.value(1)))

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