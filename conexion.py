from PyQt5 import QtWidgets, QtSql
#import  pymongo
import var

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
        query.prepare('insert into clientes (dni, apellidos, nombre, fechaAlta, direccion, provincia, sexo, formasPago)'
                      'VALUES (:dni, :apellidos, :nombre, :fechaAlta, :direccion, :provincia, :sexo, :formasPago)')
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechaAlta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        query.bindValue(':formasPago', str(cliente[7]))
        if query.exec_():
            Conexion.mostarClientes()
            print('Insercion correcta')
        else:
            print("Error: ", query.lastError().text())

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

    def bajaCli(dni):
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
           # var.ui.lblstatus.setText('Cliente con dni '+dni+' dado de baja')
        else:
            print("Error mostrar clientes: ", query.lastError().text())

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