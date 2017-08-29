#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian

import sys
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QDateEdit, QSpinBox, QPushButton, QTableWidget, QDialog, QComboBox, QTimeEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtWidgets import QAction

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.setGeometry(600, 300, 400, 300)
        self.setWindowTitle('Calculo horario')
        self.show()

    def initUi(self):
        self.formulario = Formulario()
        self.setCentralWidget(self.formulario)

        feriadosMenu = QAction('Feriados', self)
        feriadosMenu.setStatusTip('Muestra y edita los dias feriados')

        menubar = self.menuBar()
        menubar.addAction(feriadosMenu)


class Formulario(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()
        self.horarios = []

    def initUi(self):
        fechaInicio = QDateEdit(QDate.currentDate(), self)
        fechaInicio.setCalendarPopup(True)

        hrsCont = QSpinBox(self)
        hrsCont.setMinimum(0)

        ## Agregar o eliminar horarios

        btnAddHorario = QPushButton("Agregar Horario")
        btnAddHorario.clicked.connect(self.agregarHorario)
        btnDelHorario = QPushButton("Eliminar Horario")

        ## Tabla de horarios

        self.tablaHorarios = QTableWidget(0, 3, self)
        self.tablaHorarios.setHorizontalHeaderLabels(['Dia', 'Desde', 'Hasta'])

        ## Ordenamiento de widgets

        generalLayout = QVBoxLayout()

        formLayout = QFormLayout()
        formLayout.addRow("Fecha inicio", fechaInicio)
        formLayout.addRow("Horas contratadas", hrsCont)
        generalLayout.addLayout(formLayout)

        btnsTablaLayout = QHBoxLayout()
        btnsTablaLayout.addWidget(btnAddHorario)
        btnsTablaLayout.addWidget(btnDelHorario)
        btnsTablaLayout.addStretch(1)
        generalLayout.addLayout(btnsTablaLayout)

        generalLayout.addWidget(self.tablaHorarios)

        self.setLayout(generalLayout)

    def agregarHorario(self):
        dialogo = NuevoHorarioDialog(self)
        dialogo.exec()


class NuevoHorarioDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()

    def initUi(self):

        ## formulario

        cbDia = QComboBox(self)
        for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']:
            cbDia.addItem(dia)

        desdeTP = QTimeEdit(self)
        hastaTP = QTimeEdit(self)

        ## botones

        btnOk = QPushButton('Agregar')
        btnOk.clicked.connect(self.accept)
        btnCancelar = QPushButton('Cancelar')
        btnCancelar.clicked.connect(self.reject)

        ## posision widgets

        formLayout = QHBoxLayout()
        formLayout.addWidget(cbDia)
        formLayout.addWidget(desdeTP)
        formLayout.addWidget(hastaTP)

        btnsLayout = QHBoxLayout()
        btnsLayout.addWidget(btnOk)
        btnsLayout.addWidget(btnCancelar)

        generalLayout = QVBoxLayout()
        generalLayout.addLayout(formLayout)
        generalLayout.addLayout(btnsLayout)
        self.setLayout(generalLayout)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Aplicacion()
    sys.exit(app.exec_())
