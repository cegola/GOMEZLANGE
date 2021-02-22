import unittest

from PyQt5 import QtSql

import clients, conexion, var


class MyTestCase(unittest.TestCase):
    def test_conexion(self):
        value = conexion.Conexion.db_connect(var.filebd)
        msg = 'Conexion no válida'
        self.assertTrue(value, msg)

    def test_dni(self):
        dni = '00000000T'
        value = clients.Clientes.validarDni(str(dni))
        msg = 'Prueba dni errónea'
        self.assertTrue(value, msg)

    def test_factura(self):
        valor = 5.32
        codFac = 50
        try:
            msg = 'Prueba factura errónea, calculos incorrectos'
            var.subfac = 0.00
            subtotal = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codVenta, codArtVenta, cantidad from ventas where codFacVenta = :codFac')
            query.bindValue(':codFac', int(codFac))
            if query.exec_():
                index = 0
                while query.next():
                    codArtVenta = query.value(1)
                    cantidad = query.value(2)
                    query1.prepare('select nombre, precio from articulos where codigo = :codArtVenta')
                    query1.bindValue(':codArtVenta', int(codArtVenta))
                    if query1.exec_():
                        while query1.next():
                            precio = query1.value(1)
                            subtotal = round(float(cantidad)*float(precio), 2)
                    var.subfac = round(float(subtotal) + float(var.subfac), 2)
            var.iva = round(float(var.subfac) * 0.21, 2)
            var.fac = round(float(var.iva) + float(var.subfac), 2)
        except Exception as error:
            print('Error conexion: Listado de la tabla de ventas: %s ' % str(error))
        self.assertEqual(round(float(valor), 2), round(float(var.fac), 2), msg)



if __name__ == '__main__':
    unittest.main()
