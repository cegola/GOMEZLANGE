import var, conexion, events
from PyQt5 import QtWidgets
from ventana import *

class Productos():
    def validarPrecio(precio):
        try:
            print(precio)
            #AQUI DEBERIA ESTAR LA VALIDACION DEL PRECIO PERO NO ME SALE
            # i=0
            # print(len(precio))
            # partes=[]
            # dig_ext = ','
            # numeros = '0123456789'
            # for n in precio:
            #     if n in dig_ext:
            #         partes.append(precio[:i])
            #         partes.append(precio[(i+1):])
            #     i += 1
            # print(partes)
            # if (partes[1])>2:
            #     partes[1][:2]
            # print(partes)
        except:
            print('Error modulo validar precio')
            return None

    def validoPrecio():
        try:
            precio = var.ui.editPrecio.text()
            print(precio)
            if Productos.validarPrecio(precio) == False:
                mensaje = 'Ese precio es erróneo'
                events.Eventos.AbrirAviso(mensaje)
                Productos.limpiarDatos()
                dniOk = False
        except:
            print('Error modulo valido DNI')
            return None



    def altaProducto(self):
        '''cargara los clientes en la tabla'''
        try:
            newpro = [] #donde están todos los datos
            protab = [] #sera lo que carguemos
            product = [var.ui.editNombrePro, var.ui.editPrecio, var.ui.editStock]
            #protab y newpro contienen lo mismo, pero lo dejamos asi por si en el futuro le añadimos mas items
            k=0
            for i in product:
                newpro.append(i.text()) #cargamos los valores que hay en los edits
                if k < 3:
                    protab.append(i.text())
                    k += 1

            print(newpro)
            print(protab)
            mensaje = 'Seguro que desea añadir este producto'
            mod = events.Eventos.AbrirAviso(mensaje)
            if mod == True:
                #como trabajar con la tableWidget
                if newpro:
                    row = 0
                    column = 0
                    var.ui.tablaPro.insertRow(row)
                    for registro in protab:
                        cell = QtWidgets.QTableWidgetItem(registro)
                        var.ui.tablaPro.setItem(row, column, cell)
                        column += 1
                    print(newpro)
                    conexion.Conexion.altaPro(newpro)

                else:
                    print('Faltan datos')
                '''limpiamos los datos'''
                Productos.limpiarDatos(self)
        except Exception as error:
            print('Error products: alta pro: %s' % str(error))

    def limpiarDatos(self):
        '''limpia los datos del formulario'''
        try:
            # client son todas las cajas de texto
            product = [var.ui.editNombrePro, var.ui.editPrecio, var.ui.editStock]
            for i in range(len(product)):
                product[i].setText('')
            var.ui.lblCodPro.setText('')
        except Exception as error:
            print('Error products: en limpiar datos : %s' % str(error))

    def cargarPro():
        try:
            fila = var.ui.tablaPro.selectedItems()
            product = [var.ui.lblCodPro, var.ui.editNombrePro, var.ui.editPrecio]
            if fila:
                fila = [dato.text() for dato in
                        fila]  # dato recorre la fila y va almacenando el texto que haya en esa fila
            print(fila)
            i = 0
            for i, dato in enumerate(product):
                dato.setText(fila[i])
            conexion.Conexion.cargarProducto(None)
        except Exception as error:
            print('Error products: cargar datos producto: %s' % str(error))

    def bajaPro(self):
        try:
            nombre = var.ui.editNombrePro.text()
            mensaje='¿Seguro que desea dar de baja a este producto?'
            borrar = events.Eventos.AbrirAviso(mensaje)
            if borrar == True:
                conexion.Conexion.bajaProducto(nombre)
                conexion.Conexion.mostrarProductos(self)
                Productos.limpiarDatos()
        except Exception as error:
            print('Error products: baja producto: %s ' % str(error))

    def modPro(self):
        try:
            newdata = []
            product = [var.ui.editNombrePro, var.ui.editPrecio, var.ui.editStock]
            for i in product:
                newdata.append(i.text())
            cod = var.ui.lblCodPro.text()
            mensaje = 'Seguro que desea modificar este producto'
            mod = events.Eventos.AbrirAviso(mensaje)
            if mod == True:
                conexion.Conexion.modProducto(cod, newdata)
                conexion.Conexion.mostrarProductos(self)
            else:
                Productos.limpiarDatos()
        except Exception as error:
            print('Error products: modificar producto: %s ' % str(error))
