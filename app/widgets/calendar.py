# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian Mejias
#
# Distributed under terms of the GPL license.

from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtCore import Qt, QDate
from datetime import date

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

    def feriados(self): return self._feriados

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

