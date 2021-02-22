import conexion
import events
import var
from ventana import *


class Productos:

    @staticmethod
    def altaProducto():
        """

        Módulo que da de alta un producto

        :return: None
        :rtype: None

        Recoge los datos de los widgets. Cuando conecta con el modúlo conexion.altaPro manda un mensaje para asegurar
        que quiere continuar la operación.

        """
        try:
            newpro = []
            protab = []
            product = [var.ui.editNombrePro, var.ui.editPrecio, var.ui.editStock]
            k = 0
            for i in product:
                newpro.append(i.text())
                if k < 3:
                    protab.append(i.text())
                    k += 1

            print(newpro)
            print(protab)
            mensaje = 'Seguro que desea añadir este producto'
            mod = events.Eventos.AbrirAviso(mensaje)
            if mod:
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
                Productos.limpiarDatos()
        except Exception as error:
            print('Error products: alta pro: %s' % str(error))

    @staticmethod
    def limpiarDatos():
        """

        Módulo que limpia los datos

        :return: None
        :rtype: None

        Limpia los widgets de la pantalla productos

        """
        try:
            # client son todas las cajas de texto
            product = [var.ui.editNombrePro, var.ui.editPrecio, var.ui.editStock]
            for i in range(len(product)):
                product[i].setText('')
            var.ui.lblCodPro.setText('')
        except Exception as error:
            print('Error products: en limpiar datos : %s' % str(error))

    @staticmethod
    def cargarPro():
        """

        Módulo que carga los productos en la tablaPro

        :return: None
        :rtype: None

        Al generarse el evento se llama al módulo de conexion.cargarProducto que devuelve los datos haciendo una llamada
        a la base de datos

        """
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
            conexion.Conexion.cargarProducto()
        except Exception as error:
            print('Error products: cargar datos producto: %s' % str(error))

    @staticmethod
    def bajaPro():
        """

        Módulo que da de baja un producto a partir del nombre del dni. Además recarga el widget tablaPro con los
        datos actualizados desde la base de datos

        :return: None
        :rtype: None

        Toma el nombre cargado en el widget editNombre, se lo pasa al módulo Conexion.bajaProducto y da de baja
        el producto.
        Limpia los datos del formulario y recarga tablaPro

        """
        try:
            nombre = var.ui.editNombrePro.text()
            mensaje = '¿Seguro que desea dar de baja a este producto?'
            borrar = events.Eventos.AbrirAviso(mensaje)
            if borrar:
                conexion.Conexion.bajaProducto(nombre)
                conexion.Conexion.mostrarProductos()
                Productos.limpiarDatos()
        except Exception as error:
            print('Error products: baja producto: %s ' % str(error))

    @staticmethod
    def modPro():
        """

        Módulo para modificar los datos de un producto a partir del codigo

        :return: None
        :rtype: None

        A partir del código del producto, lee los nuevos datos de los widgets que se han cargado y modificado,
        llama al módulo modProducto para actualizar los datos pasandole una lista con los nuevos datos en la base de
        datos. Vuelve a mostrar la tablaCli actualizada pero no limpia los datos.
        """
        try:
            newdata = []
            product = [var.ui.editNombrePro, var.ui.editPrecio, var.ui.editStock]
            for i in product:
                newdata.append(i.text())
            cod = var.ui.lblCodPro.text()
            mensaje = 'Seguro que desea modificar este producto'
            mod = events.Eventos.AbrirAviso(mensaje)
            if mod:
                conexion.Conexion.modProducto(cod, newdata)
                conexion.Conexion.mostrarProductos()
            else:
                Productos.limpiarDatos()
        except Exception as error:
            print('Error products: modificar producto: %s ' % str(error))
