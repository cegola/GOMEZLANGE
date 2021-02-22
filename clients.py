import conexion
import events
import var
from ventana import *


class Clientes:

    @staticmethod
    def validarDni(dni):
        """

        Módulo que valida que la letra del dni sea nacional o extranjera

        :param dni: formato texto
        :type dni: string
        :return: bool
        :rtype: bool

        Pone la letra en mayuscula, comprueba que son caracteres. Toma los 8 primeros, si es extranjero
        cambia la letra por el numero, y aplica el algoritmo de comprobación de la letra basado en la normativa.
        Si es correcto--> true, falso-->False

        """
        try:
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'
            dig_ext = 'XYZ'
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = '0123456789'
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
            return False

        except Exception as error:
            print('Error clients modulo validar DNI %s' % str(error))
            return None

    @staticmethod
    def validoDni():
        """

        Módulo que según sea valido o no muestra imagen distinta

        :return: None

        Si es falso--> muestra cruz roja.
        Si es true--> muestra cruz verde.

        """
        try:
            dni = var.ui.editDni.text()
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
        except Exception as error:
            print('Error clients: modulo valido DNI%s' % str(error))
            return None

    @staticmethod
    def selSexo():
        """

        Módulo que según checkeemos el rtb fem/masc carga el texto correspondiente de mujer o hombre a la variable
        var.sex que luego se añade a la lista de los datos del cliente, a incluir en la base de datos

        :return: None
        :rtype: None

        """
        try:
            if var.ui.rbtFemenino.isChecked():
                var.sex = 'Mujer'
            if var.ui.rbtMasculino.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error clients: sexo: %s' % str(error))

    @staticmethod
    def selPago():
        """

        Módulo que checkea que valores de pago se seleccionan el el checkbox y los añade a una variable lista var.pay

        :return: None
        :rtype: None

        En QtDesigner se deben agrupar los checkbox en un buttongroup

        """
        try:
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

    @staticmethod
    def selProv(prov):
        """

        Al seleccionar una provincia en el combo de provincias llama al evento  cmbProv.activated
        que devuelve la provincia

        :param prov: provincia seleccionada
        :type prov: string
        :return: None
        :rtype: None
        """
        try:
            global vpro
            vpro = prov
        except Exception as error:
            print('Error clients: sel prov: %s' % str(error))

    @staticmethod
    def abrirCalendar():
        """

        Módulo que abre la ventana calendario

        :return: None
        :rtype: None

        """
        try:
            var.dlgCalendar.show()
        except Exception as error:
            print('Error clients: cal: %s' % str(error))

    @staticmethod
    def cargarFecha(qDate):
        """

        Módulo que carga la fecha marcada en el widget calendar

        :param qDate: libreria python para formateo de fechas
        :return: None
        :rtype: formato de fechas en python

        A partir de los eventos Calendar.clicked.connect, al clickar en una fecha, la captura y la carga en
        el widget edit que almacena la fecha

        """
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editCliAlta.setText(str(data))
            var.dlgCalendar.hide()
        except Exception as error:
            print('Error clients: cargar fecha: %s' % str(error))

    @staticmethod
    def altaCliente():
        """

        Módulo que carga los datos del cliente

        :return: None

        Se crea una lista newcli que contendrá todos los datos del cliente que se introduczca en los widgets,
        esta en la lista se pasa como argumento al modulo altaCli del módulo Conexión.
        El módulo llama al módulo altaCli para dar de alta el cliente en la base de datos.
        El módulo llama al módulo limpiarDatos para limpiar los datos de la ventana.

        """

        try:
            newcli = []
            clitab = []
            client = [var.ui.editDni, var.ui.editApellidos, var.ui.editNombre, var.ui.editCliAlta, var.ui.editDireccion]
            k = 0
            for i in client:
                newcli.append(i.text())
                if k < 3:
                    clitab.append(i.text())
                    k += 1
            newcli.append(vpro)
            newcli.append(var.sex)
            edad = var.ui.spinEdad.value()
            newcli.append(edad)
            var.pay2 = Clientes.selPago()
            newcli.append(var.pay2)
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
            Clientes.limpiarDatos()
        except Exception as error:
            print('Error clients: alta cli: %s' % str(error))

    @staticmethod
    def limpiarDatos():
        """

        Módulo que vacia los datos de la ventana cliente

        :return: None
        :rtype: None

        los checkbox y radiobuttons los pone a false

        """
        try:
            client = [var.ui.editDni, var.ui.editApellidos, var.ui.editNombre, var.ui.editCliAlta, var.ui.editDireccion]
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

    @staticmethod
    def cargarCli():
        """

        Módulo que se activa con el evento clicked.connected y setSelectionBehavior del widget TTablaCli

        :return: None
        :rtype: None

        Al generarse el evento se llama al módulo de conexion.cargarCliente que devuelve los datos haciendo una llamada
        a la base de datos

        """
        try:
            fila = var.ui.tablaCli.selectedItems()
            client = [var.ui.editDni, var.ui.editApellidos, var.ui.editNombre]
            if fila:
                fila = [dato.text() for dato in fila]

            i = 0
            for i, dato in enumerate(client):
                dato.setText(fila[i])
            conexion.Conexion.cargarCliente()
            conexion.Conexion.mostrarFacturasCli()
        except Exception as error:
            print('Error clients: cargar datos: %s' % str(error))

    @staticmethod
    def bajaCli():
        """

        Módulo que da de baja un cliente a partir del dni. Además recarga el widget TablaCli con los datos actualizados
        desde la base de datos

        :return: None
        :rtype: None

        Toma el dni cargado en el widget editDni, se lo pasa al módulo Conexion.bajaCliente y da de baja el cliente.
        Limpia los datos del formulario y recarga tablaCli

        """
        try:
            dni = var.ui.editDni.text()
            mensaje = '¿Seguro que desea dar de baja a este cliente?'
            borrar = events.Eventos.AbrirAviso(mensaje)
            if borrar:
                conexion.Conexion.bajaCliente(dni)
                conexion.Conexion.mostrarClientes()
                Clientes.limpiarDatos()
        except Exception as error:
            print('Error clients: cargar clientes: %s ' % str(error))

    @staticmethod
    def modCli():
        """

        Módulo para modificar los datos de un cliente a partir del dni

        :return: None
        :rtype: None

        A partir del código del cliente, lee los nuevos datos de los widgets que se han cargado y modificado,
        llama al módulo moCliente para actualizar los datos pasandole una lista con los nuevos datos en la base de
        datos. Vuelve a mostrar la tablaCli actualizada pero no limpia los datos.
        """
        try:
            newdata = []
            client = [var.ui.editDni, var.ui.editApellidos, var.ui.editNombre, var.ui.editCliAlta, var.ui.editDireccion]
            for i in client:
                newdata.append(i.text())
            newdata.append(var.ui.cmbProvincia.currentText())
            newdata.append(var.sex)
            edad = var.ui.spinEdad.value()
            newdata.append(edad)
            var.pay = Clientes.selPago()
            newdata.append(var.pay)
            cod = var.ui.lblCodCli.text()
            mensaje = 'Seguro que desea modificar este cliente'
            mod = events.Eventos.AbrirAviso(mensaje)
            if mod:
                conexion.Conexion.modCliente(cod, newdata)
                conexion.Conexion.mostrarClientes()
            else:
                Clientes.limpiarDatos()
        except Exception as error:
            print('Error clients: modificar clientes: %s ' % str(error))

    @staticmethod
    def reloadCli():
        """
        Limpia datos del formulario y recarga la tabla de clientes

        :return: None
        :rtype: None
        """
        try:
            Clientes.limpiarDatos()
            conexion.Conexion.mostrarClientes()
        except Exception as error:
            print('Error clients: recargar clientes: %s ' % str(error))

    @staticmethod
    def buscarCli():
        """

        Busca un cliente a partir de un dni que escribe el usuario

        :return: None
        :rtype: None

        Toma el dni del widget editDni y llama a la función Conexion.buscaCliente a la que le pasa el dni

        """
        try:
            dni = var.ui.editDni.text()
            conexion.Conexion.buscarCliente(dni)
        except  Exception as error:
            print('Error clients: recargar clientes: %s ' % str(error))

    @staticmethod
    def valoresSpin():
        """

        Módulo que se lanza con el programa cargando por defecto el valor 16

        :return: None
        :rtype: None
        """
        try:
            var.ui.spinEdad.setValue(16)
            print('Done')
        except Exception as error:
            print('Error clients: valores spin: %s' % str(error))
