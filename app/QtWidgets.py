# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian Mejias
#
# Distributed under terms of the GPL license.

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
from app.widgets.calendar import CalendarWidget

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

