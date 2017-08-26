#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import time
import re

class Horario:

    # Constructor de un Horario. Las horas inicial y final se deben especificar
    # en formato "militar", es decir,  940 para referirse a las 09:40 y 2140
    # para referirse a las 21:40, etc.
    # @param weekday Es el número del día de la semana. 0 es lunes y 6 es
    # domingo.
    # @param initial La hora inicial en formato "militar"
    # @param final La hora final en formato "militar"
    def __init__(self, weekday, initial, final):
        self.__hora_i = time(initial//100, initial%100)
        self.__hora_f = time(final//100, final%100)

        self.weekday = weekday

    def duracion(self):
        mfinal = self.__hora_f.hour * 60 + self.__hora_f.minute
        minitial = self.__hora_i.hour * 60 + self.__hora_i.minute
        duration = mfinal - minitial # cantidad de minutos del horario

        return duration

    def __lt__(self, horario):
        d = self.weekday - horario.weekday
        if d < 0 or self.__hora_i < horario.__hora_i and d == 0:
            return True
        return False

    def __gt__(self, horario):
        d = self.weekday - horario.weekday
        if d > 0 or self.__hora_i > horario.__hora_i and d == 0:
            return True
        return False

    def __eq__(self, horario):
        d = self.weekday - horario.weekday
        if d == 0 and self.__hora_i == horario.__hora_i and self.__hora_f == horario.__hora_f:
            return True
        return False

    def __str__(self):
        dia = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        return "%9s de %s a %s" % (dia[self.weekday], self.__hora_i.isoformat(), self.__hora_f.isoformat())


