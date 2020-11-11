from PyQt5 import QtWidgets, QtSql
import  pymongo,var

# class Conexion():
#     def db_connect(filename):
#         db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
#         db.setDatabaseName(filename)
#         if not db.open():
#             QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos',
#                                            'No se puede establecer conexion.\n'
#                                            'Haz click para cancelar', QtWidgets.QMessageBox.Cancel)
#             return False
#         else:
#             print('Conexion establecida')
#         return True

class Conexion():
    HOST =  'localhost'
    PORT = '27017'
    URI_CONECTION = 'mongodb://' + HOST + ':' + PORT + '/'
    var.DATABASE = 'empresa'
    try:
        print('OK -- Conexion realizada al servidor %s' % HOST)
    except:
        print('Error conexion')