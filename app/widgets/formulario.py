#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian Mejias

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QAbstractTableModel, QModelIndex, Qt, QVariant

from app.horario import Horario
from app.calculo_horario import construirItinerario

from datetime import date

class Formulario(QWidget):

    def __init__(self):
        super().__init__()
        self.horarios = []
        self.feriados = []

        self.initUi()

    def initUi(self):
        self.fechaIn_w = QDateEdit(QDate.currentDate(), self)
        self.fechaIn_w.setCalendarPopup(True)

        self.hrsCont_w = QSpinBox(self)
        self.hrsCont_w.setMinimum(0)

        ## Agregar o eliminar horarios

        btnAddHorario = QPushButton("Agregar Horario")
        btnAddHorario.clicked.connect(self.agregarHorario)
        btnDelHorario = QPushButton("Eliminar Horario")

        ## Tabla de horarios

        self.tablaHorarios = QTableView()
        self.tablaHorarios.setModel(HorarioTableModel(self.horarios))

        ## Informacion de ultimo dia de clases

        lblLastDay = QLabel('Ultimo día de clases')
        self.lastDay_w = QLineEdit()
        self.lastDay_w.setReadOnly(True)
        lblLastDay.setBuddy(self.lastDay_w)

        ## Botones para hacer el calculo de las clases

        btnCalcular = QPushButton('Calcular')
        btnCalcular.clicked.connect(self.listarClases)

        ## Ordenamiento de widgets

        generalLayout = QVBoxLayout()

        formLayout = QFormLayout()
        formLayout.addRow("Fecha inicio", self.fechaIn_w)
        formLayout.addRow("Horas contratadas", self.hrsCont_w)
        generalLayout.addLayout(formLayout)

        btnsTablaLayout = QHBoxLayout()
        btnsTablaLayout.addWidget(btnAddHorario)
        btnsTablaLayout.addWidget(btnDelHorario)
        btnsTablaLayout.addStretch(1)
        generalLayout.addLayout(btnsTablaLayout)

        generalLayout.addWidget(self.tablaHorarios)

        generalLayout.addWidget(lblLastDay)
        generalLayout.addWidget(self.lastDay_w)

        btnsCalHorLayout = QHBoxLayout()
        btnsCalHorLayout.addStretch(1)
        btnsCalHorLayout.addWidget(btnCalcular)
        generalLayout.addLayout(btnsCalHorLayout)

        self.setLayout(generalLayout)

    def listarClases(self):
        fecha_inicio = date(self.fechaIn_w.date().year(), self.fechaIn_w.date().month(), self.fechaIn_w.date().day())
        horarios = self.horarios
        num_horas = self.hrsCont_w.value()
        feriados = self.feriados

        clases = construirItinerario(fecha_inicio, horarios, num_horas, feriados)
        clases.sort()
        ultClase = clases[-1]

        self.lastDay_w.setText(ultClase.strftime("%A %d de %B del %Y"))

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

        if role == Qt.DisplayRole:
            if row < len(self.horarios):
                horario = self.horarios[row]
                horData = [horario.diaStr().capitalize(), horario.desde(), horario.hasta()]
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

