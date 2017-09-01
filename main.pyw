#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian

import sys
from PyQt5.QtCore import QDate, QVariant, QAbstractTableModel, QModelIndex, Qt, QTime, QTimer, qDebug
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QDateEdit, QSpinBox, QPushButton, QTableView, QDialog, QComboBox, QTimeEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtWidgets import QAction

from app.horario import Horario

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.setGeometry(600, 300, 450, 400)
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
        self.horarios = []

        self.initUi()

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

        self.tablaHorarios = QTableView()
        self.tablaHorarios.setModel(HorarioTableModel(self.horarios))

        ## Botones para hacer el calculo de las clases

        btnCalcular = QPushButton('Calcular')
        btnCalcular.clicked.connect(self.listarClases)

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

        btnsCalHorLayout = QHBoxLayout()
        btnsCalHorLayout.addStretch(1)
        btnsCalHorLayout.addWidget(btnCalcular)
        generalLayout.addLayout(btnsCalHorLayout)

        self.setLayout(generalLayout)

    def listarClases(self):
        """
        Se muestra un dialogo que muestra el primer dia de clases, el ultimo
        dia de clases y la lista de todos los dias de clases que debe tomar el
        alumno, incluyendo el primer y ultimo día
        """
        pass

    def agregarHorario(self):
        dialogo = NuevoHorarioDialog(self)
        if dialogo.exec() == QDialog.Accepted:
            newhorario = Horario(dialogo.POST['dia'], dialogo.POST['desde'], dialogo.POST['hasta'])
            self.horarios.append(newhorario)


class HorarioTableModel(QAbstractTableModel):

    def __init__(self, horariosList, parent=None):
        super().__init__(parent)
        self.horarios = horariosList

    def rowCount(self, parent=QModelIndex()):
        return 6

    def columnCount(self, parent=QModelIndex()):
        return 3

    def data(self, index, role):
        row = index.row()
        col = index.column()
        if row > len(self.horarios) - 1:
            return QVariant()
        horario = self.horarios[row]
        horData = [horario.diaStr().capitalize(), horario.desde(), horario.hasta()]

        if role == Qt.DisplayRole:
            return horData[col]

        return QVariant()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                headers = ['Dia', 'Desde', 'Hasta']
                return headers[section]
            else:
                return section + 1

        return QVariant()


class NuevoHorarioDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.POST = {}
        self.initUi()

    def initUi(self):

        ## formulario

        self.cbDia = QComboBox(self)
        for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']:
            self.cbDia.addItem(dia)

        self.desdeTP = QTimeEdit(self)
        self.hastaTP = QTimeEdit(self)

        ## botones

        btnOk = QPushButton('Agregar')
        btnOk.clicked.connect(self.accept)
        btnCancelar = QPushButton('Cancelar')
        btnCancelar.clicked.connect(self.reject)

        ## posision widgets

        formLayout = QHBoxLayout()
        formLayout.addWidget(self.cbDia)
        formLayout.addWidget(self.desdeTP)
        formLayout.addWidget(self.hastaTP)

        btnsLayout = QHBoxLayout()
        btnsLayout.addWidget(btnOk)
        btnsLayout.addWidget(btnCancelar)

        generalLayout = QVBoxLayout()
        generalLayout.addLayout(formLayout)
        generalLayout.addLayout(btnsLayout)
        self.setLayout(generalLayout)

    def accept(self):
        self.POST['dia'] = self.cbDia.currentIndex()
        self.POST['desde'] = self.desdeTP.time().toString()
        self.POST['hasta'] = self.hastaTP.time().toString()
        super().accept()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Aplicacion()
    sys.exit(app.exec_())
