from ventana import *
from venSalir import *
from venCalendar import *
from datetime import datetime
import sys, var, events, clients, conexion


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dlgSalir = Ui_venSalir()
        var.dlgSalir.setupUi(self)
        var.dlgSalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
        #var.dlgSalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.No).clicked.connect(events.Eventos.Salir)


class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgCalendar = Ui_dlgCalendar()
        var.dlgCalendar.setupUi(self)
        diaActual = datetime.now().day
        mesActual = datetime.now().month
        anoActual = datetime.now().year
        var.dlgCalendar.Calendar.setSelectedDate((QtCore.QDate(anoActual,mesActual,diaActual)))
        var.dlgCalendar.Calendar.clicked.connect(clients.Clientes.cargarFecha)



class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.dlgSalir = DialogSalir()
        var.dlgCalendar = DialogCalendar()
        QtWidgets.QAction(self).triggered.connect(self.close)

        '''Coleccion de datos'''
        var.rbtsex= (var.ui.rbtFemenino, var.ui.rbtMasculino)
        var.chkpago=(var.ui.chkEfectivo, var.ui.chkTarjeta, var.ui.chkTransferencia)

        '''Conexión de eventos con los objetos'''
        '''Estamos conectando el codigo con la interfaz grafica'''

        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.editDni.editingFinished.connect(clients.Clientes.validoDni)
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnAltaCli.clicked.connect(clients.Clientes.altaCliente)
        var.ui.btnLimpiarCli.clicked.connect(clients.Clientes.limpiarDatos)
        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)
        var.ui.cmbProvincia.activated[str].connect(clients.Clientes.selProv)
        var.ui.tablaCli.clicked.connect(clients.Clientes.cargarCli)
        var.ui.tablaCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        '''Llamada a modulos iniciales'''
        events.Eventos.cargarProv();

        '''modulos del principal'''
        conexion.Conexion.db_connect(var.filebd)
        #conexion.Conexion()


    def closeEvents(self, event):
        event.Eventos.Salir()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    #window.maximumSize()
    window.show()
    sys.exit(app.exec())