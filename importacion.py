import xlrd
from PyQt5 import QtWidgets
import var, events, conexion
import xlwt

class Importar():

    def dirImportar(self):
        """

        Módulo que busca un archivo xls para importar datos

        :return: None
        :rtype: None

        Abre una ventana para elegir el archivo tipo xls donde están los datos.
        Muestra una ventana de aviso preguntando si esta seguro que quiere importar datos.
        Recarga los datos llamando al método conexio.cargarDatos.
        Muestra un mensaje en la barra de estado.

        """
        try:
            mensaje = '¿Seguro que desea importar datos de productos?'
            option = QtWidgets.QFileDialog.Options()
            filename = var.filedlgAbrir.getOpenFileName(None, 'Importar datos', '', '*.xls',
                                                        options=option)
            imp = events.Eventos.AbrirAviso(mensaje)
            if var.filedlgAbrir.Accepted and filename != '' and imp:
                print(str(filename[0]))
                Importar.importar(self, filename[0])
            var.ui.lblstatus.setText('Datos de productos importados')

        except Exception as error:
            print('Error importar datos %s' % str(error))

    def importar(self, doc):
        """

        Módulo que importa datos desde un archivo xls

        :param doc: nombre del archivo
        :type doc: string
        :return: None
        :rtype: None

        Recibe el archivo y, linea a linea, lee los productos del archivo. Si existe ese producto, lo actualiza.
        Si no existe, lo crea.

        """
        documento=xlrd.open_workbook(str(doc))

        frutas = documento.sheet_by_index(0)
        fila = frutas.nrows
        col = frutas.ncols

        for i in range(1, fila):  # froitas.ncols é o número columnas
            producto = []
            for j in range(col):
                producto.append(frutas.cell_value(i,j))
            producto[1]=str(producto[1])
            aux = conexion.Conexion.existeProducto(self, producto[0])
            if aux == None:
                conexion.Conexion.altaPro(self, producto)
            else:
                producto[2]=int(producto[2])+int(aux[3])
                conexion.Conexion.modProducto(self, aux[0], producto)
                conexion.Conexion.mostrarProductos(self)

        conexion.Conexion.mostrarProductos