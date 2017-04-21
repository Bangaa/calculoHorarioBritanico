#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, time, timedelta
import re

class Horario:

    # la hora inicial y final en formato "militar", ej: 940 para referirse a 
    # las 09:40 y 2140 para referirse a las 21:40
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

def calcularHorario(dia_inicio, horarios, num_horas, feriados):
    wdinicial = dia_inicio.weekday()
    num_minutos = num_horas*60

    itinerario = [dia_inicio]

    index = 0   # por donde parto recorriendo la lista de horarios
    diaclases = dia_inicio
    while index < len(horarios):
        if horarios[index].weekday == wdinicial:
            break
        index += 1


    while num_minutos > 0:
        # buscar el siguiente dia de clases
        hr = horarios[index]
        diaclases = hr.sig_clase(itinerario[-1])

        while diaclases in feriados:
            index = (index + 1)%len(horarios)
            hr = horarios[index]
            diaclases = hr.sig_clase(itinerario[-1])

        num_minutos -= hr.duration
        itinerario.append(diaclases)

        index = (index + 1)%len(horarios)

    return itinerario[1:]

def strToDate(fecha_str):
    datematch = re.match(r'(?P<y>\d{4})\s*(?P<sep>[-/])\s*0*?(?P<m>[1-9]\d?)\s*(?P=sep)\s*0*?(?P<d>[1-9]\d?)',fecha_str)

    year = int(datematch.group("y"))
    month = int(datematch.group("m"))
    day = int(datematch.group("d"))

    return date(year, month, day)

feriados = [date(2017,4,19), date(2017,4,25)]


# datos de entrada

canthr = 7                 # cantidad de horas contratadas
horarios = [Horario(0, 930, 1030), Horario(1, 1500, 1700), Horario(2, 1500, 1700)].sort()
fechai = date(2017, 4, 18)  # fecha inicio de clases



