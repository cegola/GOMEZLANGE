from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from PyQt5 import QtSql
import os,var

class Printer():
    def cabecera(self):
        try:
            logo=".\\img\logo.jpg"
            #var.rep.drawImage(logo, 540,752)
            var.rep.setTitle('INFORMES')
            var.rep.setAuthor('Administracion Teis')
            var.rep.setFont('Helvetica', size=10)
            var.rep.line(45,820,525,820  )
            var.rep.line(45,750,525,750)
            textcif = 'CIF: A0000000N'
            textnom = 'IMPORTACIONES Y EXPORTACIONES TEIS S.L'
            textdir = 'Avda. Galicia, 101 - Vigo C.P.: 36216'
            texttel = 'Telefono: 886 12 04 64'
            var.rep.drawString(50,805, textcif)
            var.rep.drawString(50, 790, textnom)
            var.rep.drawString(50, 775, textdir)
            var.rep.drawString(50, 760, texttel)
            var.rep.drawImage(logo, 450, 752)
        except Exception as error:
            print('error en el cabecera de informe: %s' % str(error))

    def pie(textlistado):
        try:
            var.rep.line(50,50,525,50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d.%m.%Y %H.%M.%S')
            var.rep.setFont('Helvetica-Oblique', size=6)
            var.rep.drawString(460,40, str(fecha))
            var.rep.drawString(270,40, str('Página %s' % var.rep.getPageNumber()))
            var.rep.drawString(50, 40, str(textlistado))
        except Exception as error:
            print('error en el pie de informe: %s' % str(error))

    def cabeceraCli(self):
        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE CLIENTES'
            var.rep.drawString(255, 735, textlistado)
            var.rep.line(45, 730, 525, 730)
            itemcli = ['Cod', 'DNI', 'APELLIDOS', 'NOMBRE', 'FECHA ALTA']
            var.rep.drawString(45, 710, itemcli[0])
            var.rep.drawString(90, 710, itemcli[1])
            var.rep.drawString(180, 710, itemcli[2])
            var.rep.drawString(325, 710, itemcli[3])
            var.rep.drawString(465, 710, itemcli[4])
            var.rep.line(45, 703, 525, 703)
        except Exception as error:
            print('error en el cabecera cli de informe: %s' % str(error))

    def cabeceraPro(self):
        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE PRODUCTOS'
            var.rep.drawString(255, 735, textlistado)
            var.rep.line(45, 730, 525, 730)
            itempro = ['Cod', 'ARTÍCULO', 'PRECIO', 'STOCK']
            var.rep.drawString(45, 710, itempro[0])
            var.rep.drawString(170, 710, itempro[1])
            var.rep.drawString(360, 710, itempro[2])
            var.rep.drawString(490, 710, itempro[3])
            var.rep.line(45, 703, 525, 703)
        except Exception as error:
            print('error en el cabecera pro de informe: %s' % str(error))

    def reportCli(self):
        try:
            textlistado='LISTADO DE CLIENTES'
            var.rep= canvas.Canvas('informes/listadoClientes.pdf')
            Printer.cabecera(self)
            Printer.cabeceraCli(self)
            Printer.pie(textlistado)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, dni, apellidos, nombre, fechaAlta from clientes order by apellidos, nombre')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 50 #valores eje X
                j = 690 #valores eje Y
                while query.next():
                    if j <= 80:
                        var.rep.drawString(440,70,'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera(self)
                        Printer.pie(textlistado)
                        Printer.cabeceraCli(self)
                        i = 50
                        j = 690
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i+30, j, str(query.value(1)))
                    var.rep.drawString(i+130, j, str(query.value(2)))
                    var.rep.drawString(i+280, j, str(query.value(3)))
                    var.rep.drawRightString(i+470, j, str(query.value(4)))
                    j = j - 25

            var.rep.save()
            roothPath = ".\\informes"
            cont = 0
            for file in os.listdir(roothPath):
                if file.endswith('listadoClientes.pdf'):
                    os.startfile("%s/%s" % (roothPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reportcli %s' % str(error))

    def reportPro(self):
        try:
            textlistado='LISTADO DE PRODUCTOS'
            var.rep= canvas.Canvas('informes/listadoProductos.pdf')
            Printer.cabecera(self)
            Printer.cabeceraPro(self)
            Printer.pie(textlistado)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio, stock from articulos order by nombre')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 50 #valores eje X
                j = 690 #valores eje Y
                while query.next():
                    if j <= 80:
                        var.rep.drawString(440,70,'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera(self)
                        Printer.pie(textlistado)
                        Printer.cabeceraPro(self)
                        i = 50
                        j = 690
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i+100, j, str(query.value(1)))
                    var.rep.drawRightString(i+335, j, str(query.value(2)))
                    var.rep.drawRightString(i+470, j, str(query.value(3)))
                    j = j - 25

            var.rep.save()
            roothPath = ".\\informes"
            cont = 0
            for file in os.listdir(roothPath):
                if file.endswith('listadoProductos.pdf'):
                    os.startfile("%s/%s" % (roothPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reportpro %s' % str(error))