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
                var.ui.editCliAlta.setText(query.value(4))
                var.ui.editDireccion.setText(str(query.value(5)))
                var.ui.cmbProvincia.setCurrentText(str(query.value(6)))
                if str(query.value(7)=='Mujer'):
                    var.ui.rbtFemenino.setChecked(True)
                    var.ui.rbtMasculino.setChecked(False)
                else:
                    var.ui.rbtFemenino.setChecked(False)
                    var.ui.rbtMasculino.setChecked(True)
                var.ui.spinEdad.setText(str(query.value(8)))
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)

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
        query.bindValue(':edad', str(newdata[7]))
        query.bindValue(':formasPago', str(newdata[8]))
        if query.exec_():
            print('Cliente modificado')
            var.ui.lblstatus.setText('Cliente con dni '+str(newdata[0])+' modificado, dia '+time.strftime("%x"))
        else:
            print('Error modificar cliente: ', query.lastError().text())

    def buscarCliente(dni):
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)

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