from ventana import *
from venSalir import *
from venCalendar import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
import sys, var, events, clients, conexion
from datetime import datetime, date
import locale

locale.setlocale(locale.LC_ALL, 'es-ES')


class DialogAviso(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAviso, self).__init__()
        var.dlgAviso = Ui_venAviso()
        var.dlgAviso.setupUi(self)
        var.dlgAviso.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
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

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()

class DialogImprimir(QPrintDialog):
    def __init__(self):
        super(DialogImprimir, self).__init__()



class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.dlgAviso = DialogAviso()
        var.dlgCalendar = DialogCalendar()
        var.filedlgAbrir = FileDialogAbrir()
        var.dglImprimir = DialogImprimir()
        QtWidgets.QAction(self).triggered.connect(self.close)


        '''Coleccion de datos'''
        var.rbtsex= (var.ui.rbtFemenino, var.ui.rbtMasculino)
        var.chkpago=(var.ui.chkEfectivo, var.ui.chkTarjeta, var.ui.chkTransferencia)

        '''Conexión de eventos con los objetos'''
        '''Estamos conectando el codigo con la interfaz grafica'''

        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.actionBackup.triggered.connect(events.Eventos.Backup)
        var.ui.actiontoolBarSalir.triggered.connect(events.Eventos.Salir)
        var.ui.toolBarAbrirCarpeta.triggered.connect(events.Eventos.AbrirDir)
        var.ui.actionAbrir.triggered.connect(events.Eventos.AbrirDir)
        var.ui.toolBarImpresora.triggered.connect(events.Eventos.Imprimir)
        var.ui.actionImprimir.triggered.connect(events.Eventos.Imprimir)

        var.ui.editDni.editingFinished.connect(clients.Clientes.validoDni)
        '''botones'''
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnAltaCli.clicked.connect(clients.Clientes.altaCliente)
        var.ui.btnBajaCli.clicked.connect(clients.Clientes.bajaCli)
        var.ui.btnLimpiarCli.clicked.connect(clients.Clientes.limpiarDatos)
        var.ui.btnModCli.clicked.connect(clients.Clientes.modCli)
        var.ui.btnRecargar.clicked.connect(clients.Clientes.reloadCli)
        var.ui.btnBuscar.clicked.connect(clients.Clientes.buscarClie)
        clients.Clientes.valoresSpin(None)

        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)

        var.ui.cmbProvincia.activated[str].connect(clients.Clientes.selProv)
        var.ui.tablaCli.clicked.connect(clients.Clientes.cargarCli)
        var.ui.tablaCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        '''Llamada a modulos iniciales'''
        events.Eventos.cargarProv()

        var.ui.statusbar.addPermanentWidget(var.ui.lblstatus, 5)
        var.ui.statusbar.addPermanentWidget(var.ui.lblfecha, 1)
        var.ui.lblstatus.setText('Bienvenido a 2º DAM')
        var.ui.lblfecha.setText(str(datetime.now()))

        '''modulos del principal'''
        conexion.Conexion.db_connect(var.filebd)
        conexion.Conexion.mostrarClientes(self)


    def closeEvents(self, event):
        event.Eventos.Salir()
        salir = True


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    #window.show()
    sys.exit(app.exec())