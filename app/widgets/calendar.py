#! /usr/bin/env python
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

    def __init__(self):
        super().__init__()
        # Se inicializa el calendario con el dia lunes como dia inicial y se 
        # quita el numero de semana
        self.setFirstDayOfWeek(Qt.Monday)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader) 

    def agregarFeriado(self, fecha):
        if type(fecha) is date:
            fecha = QDate(fecha.year, fecha.month, fecha.day)
        self.setDateTextFormat(fecha, self.holidayFormat()) 

    def holidayFormat(self):
        return super().weekdayTextFormat(Qt.Saturday)

