from ventana import *
from venSalir import *
from venCalendar import *
from datetime import datetime
import sys, var, events,clients

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        '''Coleccion de datos'''
        var.rbtsex= (var.ui.rbtFemenino, var.ui.rbtMasculino)
        var.chkpago=(var.ui.chkEfectivo, var.ui.chkTarjeta, var.ui.chkTransferencia)
        var.avisoSalir = DialogSalir()
        #var.dlgCalendar =DialogCalendar()
        '''Conexión de eventos con los objetos'''
        '''Estamos conectando el codigo con la interfaz grafica'''
        QtWidgets.QAction(self).triggered.connect(self.close)
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.editDni.editingFinished.connect(clients.Clientes.validoDni)
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)
        var.ui.cmbProvincia.activated[str].connect(clients.Clientes.selProv)

        '''Llamada a modulos iniciales'''
        events.Eventos.cargarProv();

class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.avisoSalir = Ui_venSalir()
        var.avisoSalir.setupUi(self)
        var.avisoSalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
        var.avisoSalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.No).clicked.connect(events.Eventos.Salir)


class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgCalendar = Ui_calendar
        var.dlgCalendar.setupUi(self)
        mesActual = datetime.now().month
        anoActual = datetime.now().year
        var.dlgCalendar.Calendar.setSelectedDate(QtCore.QDate(anoActual,mesActual,1))
        var.dlgCalendar.Calendar.clicked.connected(clients.Clientes.cargarFecha)






    def closeEvents(self, event):
        event.Eventos.Salir()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())