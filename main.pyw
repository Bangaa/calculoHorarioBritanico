#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian

import sys
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QDateEdit, QSpinBox, QPushButton, QTableWidget, QDialog
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


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Aplicacion()
    sys.exit(app.exec_())
