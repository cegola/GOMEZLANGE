import xlrd
import xlwt

class Importar():

    def importar(self, doc):
        documento=xlrd.open_workbook(str(doc))

        frutas = documento.sheet_by_index(0)
        lacteos = documento.sheet_by_index(1)

        filas_fruta = frutas.nrows
        col_fruta = frutas.ncols
        print("Frutas tiene "+str(filas_fruta)+" filas y "+str(col_fruta)+ " columnas")

        # Gardamos a información de la celda (0,1) da folla de lacteos
        # Os tipos de celda son: 0-Vacia, 1-Texto, 2-Numero, 3-Data, 4-Booleano, 5-Erro

        tipo_celda = frutas.cell_type(0,1)
        print
