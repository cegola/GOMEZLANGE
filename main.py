from ventana import *
from venSalir import *
import sys, var, events,clients

class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dialog = Ui_venSalir
        var.dialog.setupUi(self)
        var.dialog.btnBox.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
        var.dialog.btnBox.button(QtWidgets.QDialogButtonBox.No).clicked.connect(events.Eventos.Salir)
        QtWidgets.QAction(self).triggered.connect(self.close)

    def closeEvent(self, event):
        events.Eventos.Salir



class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        '''Coleccion de datos'''
        var.rbtsex= (var.ui.rbtFemenino, var.ui.rbtMasculino)
        var.chkpago=(var.ui.chkEfectivo, var.ui.chkTarjeta, var.ui.chkTransferencia)
        '''Conexión de eventos con los objetos'''
        '''Estamos conectando el codigo con la interfaz grafica'''
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.editDni.editingFinished.connect(clients.Clientes.validoDni)
        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)
        var.ui.cmbProvincia.activated[str].connect(clients.Clientes.selProv)

        '''Llamada a modulos iniciales'''
        events.Eventos.cargarProv();

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())