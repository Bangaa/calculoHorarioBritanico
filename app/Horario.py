#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, time, timedelta
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
        self.hora_i = time(initial/100, initial%100)
        self.hora_f = time(final/100, final%100)

        mfinal = final/100 * 60 + final%100
        minitial = initial/100 * 60 + initial%100
        self.duration = mfinal - minitial # cantidad de minutos del horario

        self.weekday = weekday

    def __lt__(self, horario):
        d = self.weekday - horario.weekday
        if d < 0 or self.hora_i < horario.hora_i and d == 0:
            return True
        return False

    def __gt__(self, horario):
        d = self.weekday - horario.weekday
        if d > 0 or self.hora_i > horario.hora_i and d == 0:
            return True
        return False

    def __eq__(self, horario):
        d = self.weekday - horario.weekday
        if d == 0 and self.hora_i == horario.hora_i and self.hora_f == horario.hora_f:
            return True
        return False

    def __str__(self):
        dia = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        return "%9s de %s a %s" % (dia[self.weekday], self.hora_i.isoformat(), self.hora_f.isoformat())

    # devuelve la proxima fecha en la cual se pueda cumplir el horario
    def sig_clase(self, afterdate = date.today()):
        difdias = afterdate.weekday() - self.weekday

        if difdias > 0:
            delay = timedelta(days=6-afterdate.weekday()+self.weekday+1)
        elif difdias < 0:
            delay = timedelta(days=-difdias)
        else:
            delay = timedelta()

        return afterdate + delay

