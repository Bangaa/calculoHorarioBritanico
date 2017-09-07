# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian Mejias
#
# Distributed under terms of the GPL license.

from PyQt5.QtCore import Qt, QDate, QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt5.QtWidgets import *
from datetime import date
from PyQt5.QtGui import QIcon

from app.horario import Horario
from app.calculo_horario import construirItinerario_qtdates


class AgregarFeriadosDialog(QDialog):

    def __init__(self, feriados, parent=None):
        super().__init__(parent)
        self.calendar_w = CalendarWidget(feriados)
        self.initUi()

    def initUi(self):
        """
        Inicializa los contenidos del widget
        """
        generalLayout = QVBoxLayout()

        self.calendar_w.setSelectedDate(QDate.currentDate())
        self.calendar_w.selectionChanged.connect(self.configurarRadioButtons)

        self.checkbtn_feriado_w = QCheckBox("Feriado", self)
        self.checkbtn_feriado_w.toggled.connect(self.configurarFeriado)


        ## posicion widgets

        generalLayout.addWidget(self.calendar_w)
        generalLayout.addWidget(self.checkbtn_feriado_w)

        self.setLayout(generalLayout)

    def configurarFeriado(self):
        fecha_elegida = self.calendar_w.selectedDate()

        if self.checkbtn_feriado_w.isChecked():
            self.calendar_w.agregarFeriado(fecha_elegida)
        else:
            self.calendar_w.eliminarFeriado(fecha_elegida)

    def configurarRadioButtons(self):
        fecha_elegida = self.calendar_w.selectedDate()
        if fecha_elegida in self.calendar_w.feriados():
            self.checkbtn_feriado_w.setChecked(True)
        else:
            self.checkbtn_feriado_w.setChecked(False)


class CalendarWidget(QCalendarWidget):

    def __init__(self, feriados=[]):
        super().__init__()
        self.initUi()
        self._feriados = set()

        for feriado in feriados:
            self.agregarFeriado(feriado)

    def initUi(self):
        # Se inicializa el calendario con el dia lunes como dia inicial y se
        # quita el numero de semana
        self.setFirstDayOfWeek(Qt.Monday)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setGridVisible(True)

    def feriados(self):
        return self._feriados

    def agregarFeriado(self, fecha):
        if type(fecha) is date:
            fecha = QDate(fecha.year, fecha.month, fecha.day)
        if fecha not in self._feriados:
            self.setDateTextFormat(fecha, self.holidayTextFormat())
            self._feriados.add(fecha)

    def agregarLosFeriados(self, lista_fechas):
        for fecha in lista_fechas:
            self.agregarFeriado(fecha)

    def eliminarFeriado(self, fecha):
        if type(fecha) is date:
            fecha = QDate(fecha.year, fecha.month, fecha.day)

        if fecha in self._feriados:
            self._feriados.discard(fecha)
            self.setDateTextFormat(fecha, self.weekdayTextFormat(Qt.Tuesday))

    def eliminarLosFeriados(self, lista_fechas):
        for fecha in lista_fechas:
            self.eliminarFeriado(fecha)

    def holidayTextFormat(self):
        return self.weekdayTextFormat(Qt.Saturday)


class Formulario(QWidget):

    def __init__(self, calendar=None):
        super().__init__()
        self.horarios = []
        self.calendar_w = calendar

        self.initUi()

    def initUi(self):
        self.fechaIn_w = QDateEdit(QDate.currentDate(), self)
        self.fechaIn_w.setCalendarPopup(True)
        self.fechaIn_w.setCalendarWidget(self.calendar_w)

        self.hrsCont_w = QSpinBox(self)
        self.hrsCont_w.setMinimum(0)

        ## Agregar o eliminar horarios

        btnAddHorario = QPushButton(QIcon(":/i/add_black"), "Agregar Horario")
        btnAddHorario.clicked.connect(self.agregarHorario)
        btnDelHorario = QPushButton(QIcon(":/i/loop_black"), "Empezar de nuevo")
        btnDelHorario.clicked.connect(self.empezarDeNuevo)

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

        ## Tips de ayuda

        self.fechaIn_w.setStatusTip('Fecha de la primera clase')
        btnAddHorario.setStatusTip('Agrega un nuevo horario a la lista')
        btnDelHorario.setStatusTip('Limpia el formulario para empezar de cero')
        self.hrsCont_w.setStatusTip('Numero de horas que dura el curso')

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
        feriados = [] if self.calendar_w is None else self.calendar_w.feriados()

        try:
            clases = construirItinerario_qtdates(fecha_inicio, horarios, num_horas, feriados)
            ultClase = clases[-1]

            self.lastDay_w.setText(ultClase.strftime("%A %d de %B del %Y"))
        except ValueError as ve:
            mensaje = QMessageBox(QMessageBox.Critical, 'Error', 'Error de parametros', parent=self)
            mensaje.setInformativeText(ve.args[0])
            mensaje.exec()
        except RuntimeError as rte:
            mensaje = QMessageBox(QMessageBox.Critical, 'Error', 'Error mientras se calculaba el horario', parent=self)
            mensaje.setInformativeText(rte.args[0])
            mensaje.exec()

    def empezarDeNuevo(self):
        self.horarios.clear()
        self.hrsCont_w.setValue(0)
        self.fechaIn_w.setDate(QDate.currentDate())
        self.tablaHorarios.model().update()

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

    def update(self, desde=(0,0), hasta=(5,2)):
        self.dataChanged.emit(self.createIndex(*desde), self.createIndex(*hasta))

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

