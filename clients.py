
import var, conexion, events
from PyQt5 import QtWidgets
from ventana import *

class Clientes():
    '''eventos clientes'''
    def validarDni(dni):
        '''codigo que controla la validez del dni'''

        try:
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'
            dig_ext = 'XYZ'
            reemp_dig_ext ={'X':'0', 'Y':'1', 'Z':'2'}
            numeros = '0123456789'
            dni=dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
                '''Va construyendo una lista, almacena el dato en ella si es un numero, al final comprueba que la lista creada tenga len=8'''
                '''Comprueba que la letra del dni corresponde con la de la tabla'''
            return False
        except:
            print('Error clients: modulo validar DNI')
            return None


    def validoDni():
        try:
            dni = var.ui.editDni.text()
            #print(dni)
            if Clientes.validarDni(dni):
                var.ui.lblValidar.setStyleSheet('QLabel {color:green;}')
                var.ui.lblValidar.setText('V')
                var.ui.editDni.setText(dni.upper())
            else:

                var.ui.lblValidar.setStyleSheet('QLabel {color:red;}')
                var.ui.lblValidar.setText('X')
                var.ui.editDni.setText(dni.upper())
                mensaje = 'Ese DNI es erróneo'
                events.Eventos.AbrirAviso(mensaje)
                Clientes.limpiarDatos()
                dniOk=False
        except:
            print('Error clients: modulo valido DNI')
            return None

    def selSexo(self):
        try:
            if var.ui.rbtFemenino.isChecked():
                var.sex = 'Mujer'
            if var.ui.rbtMasculino.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error clients: sexo: %s' % str(error))

    def selPago():
        try:
            '''se llama al final, tiene la lista vacia y la llena según estén clickados los botones'''
            var.pay = []
            for i, data in enumerate(var.ui.grpBtnPay.buttons()):
                if data.isChecked() and i == 0:
                    var.pay.append('Efectivo')
                if data.isChecked() and i == 1:
                    var.pay.append('Tarjeta')
                if data.isChecked() and i == 2:
                    var.pay.append('Transferencia')
            return var.pay
        except Exception as error:
            print('Error clients: pago: %s' % str(error))


    def valoresSpin(self):
        try:
            var.ui.spinEdad.setValue(18)
            print('Done')
        except Exception as error:
            print('Error clients: valores spin: %s' % str(error))

    def selProv(prov):
        try:
            global vpro
            vpro = prov
        except Exception as error:
            print('Error clients: sel prov: %s' % str(error))


    def abrirCalendar(self):
        try:
            var.dlgCalendar.show()
        except Exception as error:
            print('Error clients: cal: %s' % str(error))

    def cargarFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editCliAlta.setText(str(data))
            var.dlgCalendar.hide()
        except Exception as error:
            print('Error clients: cargar fecha: %s' % str(error))

    def altaCliente(self):
        '''cargara los clientes en la tabla'''
        try:
            newcli = [] #donde están todos los datos
            clitab = [] #sera lo que carguemos
            client = [var.ui.editDni, var.ui.editApellidos, var.ui.editNombre, var.ui.editCliAlta, var.ui.editDireccion]
            k=0
            for i in client:
                newcli.append(i.text()) #cargamos los valores que hay en los edits
                if k < 3:
                    clitab.append(i.text())
                    k += 1
            newcli.append(vpro)
            #elimina duplicados
            newcli.append(var.sex)
            edad = var.ui.spinEdad.value()
            newcli.append(edad)
            var.pay2 = Clientes.selPago()
            newcli.append(var.pay2)
            '''var.pay = set(var.pay)
            for j in var.pay:
                newcli.append(j)'''

            #print(newcli)
            #print(clitab)
            #como trabajar con la tableWidget
            if newcli:
                row = 0
                column = 0
                var.ui.tablaCli.insertRow(row)
                for registro in clitab:
                    cell = QtWidgets.QTableWidgetItem(registro)
                    var.ui.tablaCli.setItem(row, column, cell)
                    column += 1
                conexion.Conexion.altaCli(newcli)
            else:
                print('Faltan datos')
            '''limpiamos los datos'''
            Clientes.limpiarDatos(self)
        except Exception as error:
            print('Error clients: alta cli: %s' % str(error))

    def limpiarDatos(self):
        '''limpia los datos del formulario'''
        try:
            #client son todas las cajas de texto
            client  = [var.ui.editDni, var.ui.editApellidos, var.ui.editNombre, var.ui.editCliAlta, var.ui.editDireccion]
            for i in range(len(client)):
                client[i].setText('')
            var.ui.grpBtnSex.setExclusive(False)
            for data in var.rbtsex:
                data.setChecked(False)
            for data in var.chkpago:
                data.setChecked(False)
            var.ui.cmbProvincia.setCurrentIndex(0)
            var.ui.lblValidar.setText('')
            var.ui.lblCodCli.setText('')
            var.ui.spinEdad.setValue(18)

        except Exception as error:
                print('Error clients: en limpiar datos : %s' % str(error))


    def cargarCli(self):
        try:
            fila = var.ui.tablaCli.selectedItems()
            client = [var.ui.editDni, var.ui.editApellidos, var.ui.editNombre]
            if fila:
                fila = [dato.text() for dato in fila ]#dato recorre la fila y va almacenando el texto que haya en esa fila
            #print(fila)
            i = 0
            for i, dato in enumerate(client):
                dato.setText(fila[i])
            conexion.Conexion.cargarCliente(None)
            conexion.Conexion.mostrarFacturasCli(self)
        except Exception as error:
                print('Error clients: cargar datos: %s' % str(error))


    def bajaCli(self):
        try:
            dni = var.ui.editDni.text()
            mensaje='¿Seguro que desea dar de baja a este cliente?'
            borrar = events.Eventos.AbrirAviso(mensaje)
            if borrar == True:
                conexion.Conexion.bajaCliente(dni)
                conexion.Conexion.mostrarClientes(self)
                Clientes.limpiarDatos()
        except Exception as error:
            print('Error clients: cargar clientes: %s ' % str(error))

    def modCli(self):
        try:
            newdata = []
            client = [var.ui.editDni, var.ui.editApellidos, var.ui.editNombre, var.ui.editCliAlta, var.ui.editDireccion]
            for i in client:
                newdata.append(i.text())
            newdata.append(var.ui.cmbProvincia.currentText())
            newdata.append(var.sex)
            edad= var.ui.spinEdad.value()
            newdata.append(edad)
            var.pay = Clientes.selPago()
            newdata.append(var.pay)
            cod = var.ui.lblCodCli.text()
            mensaje = 'Seguro que desea modificar este cliente'
            mod = events.Eventos.AbrirAviso(mensaje)
            if mod == True:
                conexion.Conexion.modCliente(cod, newdata)
                conexion.Conexion.mostrarClientes(self)
            else:
                Clientes.limpiarDatos()
        except Exception as error:
            print('Error clients: modificar clientes: %s ' % str(error))


    def reloadCli(self):
        try:
            Clientes.limpiarDatos()
            conexion.Conexion.mostrarClientes(None)
        except  Exception as error:
            print('Error clients: recargar clientes: %s ' % str(error))

    def buscarClie(self):
        try:
            dni = var.ui.editDni.text()
            cliente = conexion.Conexion.buscarCliente(dni)
        except  Exception as error:
            print('Error clients: recargar clientes: %s ' % str(error))
