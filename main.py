from ventana import *
from venSalir import *
from venCalendar import *
from venAviso import *
from venAcercaDe import *
from PyQt5.QtPrintSupport import QPrintDialog
import sys, var, events, clients, conexion, products, printer, ventas
from datetime import datetime, date
import locale

locale.setlocale(locale.LC_ALL, 'es-ES')


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana salir

        """
        super(DialogSalir, self).__init__()
        var.dlgSalir = Ui_venSalir()
        var.dlgSalir.setupUi(self)
        var.dlgSalir.btnAceptar.clicked.connect(events.Eventos.Salir)
        var.dlgSalir.btnCancelar.clicked.connect(events.Eventos.closeSalir)

class DialogAviso(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana avisos

        """
        super(DialogAviso, self).__init__()
        var.dlgAviso = Ui_venAviso()
        var.dlgAviso.setupUi(self)

class DialogAcercaDe(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana AcercaDe

        """
        super(DialogAcercaDe, self).__init__()
        var.dlgAcercaDe = Ui_venAcercaDe()
        var.dlgAcercaDe.setupUi(self)
        var.dlgAcercaDe.btnSalir.clicked.connect(events.Eventos.AbrirAcercaDe)

class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana calendario

        """
        super(DialogCalendar, self).__init__()
        var.dlgCalendar = Ui_dlgCalendar()
        var.dlgCalendar.setupUi(self)
        diaActual = datetime.now().day
        mesActual = datetime.now().month
        anoActual = datetime.now().year
        var.dlgCalendar.Calendar.setSelectedDate((QtCore.QDate(anoActual, mesActual, diaActual)))
        var.dlgCalendar.Calendar.clicked.connect(clients.Clientes.cargarFecha)
        var.dlgCalendar.Calendar.clicked.connect(ventas.Ventas.cargarFecha)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de abrir directorios

        """
        super(FileDialogAbrir, self).__init__()

class DialogImprimir(QPrintDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de impresión

        """
        super(DialogImprimir, self).__init__()

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        """

        Instancia todas las ventanas que utilizamos del programa.
        Genera y  conecta todos los eventos de los botones y los widgets.
        Cunado se lanza se conecta con la base de datos.
        Cuando se lanza, el programa carga todos los artículos, facturas y clientes de la base de datos,
        en las ventanas correspondientes.

        """
        super(Main, self).__init__()
        '''
        
        Instancia de ventanas auxiliares
        
        '''
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.dlgSalir = DialogSalir()
        var.dlgAviso = DialogAviso()
        var.dlgAcercaDe = DialogAcercaDe()
        var.dlgCalendar = DialogCalendar()
        var.filedlgAbrir = FileDialogAbrir()
        var.dglImprimir = DialogImprimir()
        QtWidgets.QAction(self).triggered.connect(self.close)

        '''
        
        Listas que contienen los checkbox y radioButton
        
        '''
        var.rbtsex = (var.ui.rbtFemenino, var.ui.rbtMasculino)
        var.chkpago = (var.ui.chkEfectivo, var.ui.chkTarjeta, var.ui.chkTransferencia)
        var.chkfacpago =var.ui.chkFacPagada

        '''
        
        Conexión de eventos con los objetos
        Estamos conectando el codigo con la interfaz grafica
                
        '''
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.btnSalirPro.clicked.connect(events.Eventos.Salir)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.actiontoolBarSalir.triggered.connect(events.Eventos.Salir)
        var.ui.actionBackup.triggered.connect(events.Eventos.Backup)
        var.ui.toolBarAbrirCarpeta.triggered.connect(events.Eventos.AbrirDir)
        var.ui.actionAbrir.triggered.connect(events.Eventos.AbrirDir)
        var.ui.toolBarImpresora.triggered.connect(events.Eventos.Imprimir)
        var.ui.actionImprimir.triggered.connect(events.Eventos.Imprimir)
        var.ui.actionRestaurarBD.triggered.connect(events.Eventos.restaurarBD)

        var.ui.actionAbout.triggered.connect(events.Eventos.AbrirAcercaDe)

        var.ui.editDni.editingFinished.connect(clients.Clientes.validoDni)

        '''botones Cli'''
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnAltaCli.clicked.connect(clients.Clientes.altaCliente)
        var.ui.btnAltaPro.clicked.connect(products.Productos.altaProducto)
        var.ui.btnBajaCli.clicked.connect(clients.Clientes.bajaCli)
        var.ui.btnRecargar.clicked.connect(clients.Clientes.reloadCli)
        var.ui.btnBuscar.clicked.connect(clients.Clientes.buscarClie)
        '''Botones Pro'''
        var.ui.btnBajaPro.clicked.connect(products.Productos.bajaPro)
        var.ui.btnLimpiarCli.clicked.connect(clients.Clientes.limpiarDatos)
        var.ui.btnLimpiarPro.clicked.connect(products.Productos.limpiarDatos)
        var.ui.btnModCli.clicked.connect(clients.Clientes.modCli)
        var.ui.btnModPro.clicked.connect(products.Productos.modPro)
        clients.Clientes.valoresSpin(self)
        '''Botones Fac'''
        var.ui.btnFacturar.clicked.connect(ventas.Ventas.altaFactura)
        var.ui.btnCalendarFac.clicked.connect(ventas.Ventas.abrirCalendar)
        var.ui.btnAnular.clicked.connect(ventas.Ventas.borrarFac)
        var.ui.btnBuscarCli.clicked.connect(conexion.Conexion.mostrarFacturasCli)
        var.ui.btnRecargarCli.clicked.connect(conexion.Conexion.mostrarFacturas)
        var.ui.btnAceptarVenta.clicked.connect(ventas.Ventas.procesoVenta)
        var.ui.btnBorrarVenta.clicked.connect(ventas.Ventas.anularVenta)
        var.ui.btnActualizar.clicked.connect(ventas.Ventas.actualizarFac)

        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)
        # for i in var.chkfacpago:
        #     i.stateChanged.connect(ventas.Ventas.selFacPagada)
        var.chkfacpago.stateChanged.connect(ventas.Ventas.selFacPagada)

        var.ui.cmbProvincia.activated[str].connect(clients.Clientes.selProv)
        var.ui.tablaCli.clicked.connect(clients.Clientes.cargarCli)
        var.ui.tablaCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tablaPro.clicked.connect(products.Productos.cargarPro)
        var.ui.tablaPro.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabFactura.clicked.connect(ventas.Ventas.cargarFac)
        var.ui.tabFactura.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabVenta.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        '''
        
        Llamada a modulos iniciales
        
        '''
        events.Eventos.cargarProv(self)

        var.ui.statusbar.addPermanentWidget(var.ui.lblstatus, 5)
        var.ui.statusbar.addPermanentWidget(var.ui.lblfecha, 1)
        var.ui.lblstatus.setText('Bienvenido a 2º DAM')
        fecha = date.today()
        var.ui.lblfecha.setText(fecha.strftime('%A %d de %B del %Y'))
        var.ui.tabWidget.setCurrentIndex(0)

        '''
        
        modulos de impresion
        
        '''
        var.ui.actionListado_clientes.triggered.connect(printer.Printer.reportCli)
        var.ui.actionListado_productos.triggered.connect(printer.Printer.reportPro)
        var.ui.actionImprimir_factura.triggered.connect(printer.Printer.reportFac)

        '''
        
        modulos del principal
        
        '''
        conexion.Conexion.cargarDatos(self)

    def closeEvent(self, event):
        if event:
            events.Eventos.Salir(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    # window.show()
    sys.exit(app.exec())
