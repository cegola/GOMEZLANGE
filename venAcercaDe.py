# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'venAcercaDe.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_venAcercaDe(object):
    def setupUi(self, venAcercaDe):
        venAcercaDe.setObjectName("venAcercaDe")
        venAcercaDe.setWindowModality(QtCore.Qt.NonModal)
        venAcercaDe.resize(400, 189)
        venAcercaDe.setModal(True)
        self.lblLogo = QtWidgets.QLabel(venAcercaDe)
        self.lblLogo.setGeometry(QtCore.QRect(290, 20, 81, 31))
        self.lblLogo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblLogo.setStyleSheet("font: 14pt \"Snap ITC\";color:rgb(103, 105, 255)")
        self.lblLogo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblLogo.setObjectName("lblLogo")
        self.lblVersion = QtWidgets.QLabel(venAcercaDe)
        self.lblVersion.setGeometry(QtCore.QRect(120, 70, 171, 21))
        self.lblVersion.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.lblVersion.setObjectName("lblVersion")
        self.lblNombre = QtWidgets.QLabel(venAcercaDe)
        self.lblNombre.setGeometry(QtCore.QRect(120, 100, 171, 21))
        self.lblNombre.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.lblNombre.setObjectName("lblNombre")
        self.btnSalir = QtWidgets.QPushButton(venAcercaDe)
        self.btnSalir.setGeometry(QtCore.QRect(300, 150, 75, 23))
        self.btnSalir.setObjectName("btnSalir")

        self.retranslateUi(venAcercaDe)
        QtCore.QMetaObject.connectSlotsByName(venAcercaDe)

    def retranslateUi(self, venAcercaDe):
        _translate = QtCore.QCoreApplication.translate
        venAcercaDe.setWindowTitle(_translate("venAcercaDe", "Acerca De"))
        self.lblLogo.setText(_translate("venAcercaDe", "LOGO"))
        self.lblVersion.setText(_translate("venAcercaDe", "Versión del programa: 0.0.1"))
        self.lblNombre.setText(_translate("venAcercaDe", "Celia Gómez Lange"))
        self.btnSalir.setText(_translate("venAcercaDe", "Salir"))
