#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian Mejias
#
# Distributed under terms of the GPL license.

from Horario import Horario
from datetime import timedelta, date

# Devuelve la fecha del siguiente día 'dayofweek'. Por ejemplo, si hoy, 6 de
# junio, es jueves, entonces 'nextDayOfWeek(0)' devuelve '10 de junio'.
# @param dayofweek Es el número del día de la semana
# @param afterdate Es la fecha a partir de la cual se buscará el proximo
# 'dayofweek'. Es opcional (default: datetime.date.today()).
def nextDayOfWeek(dayofweek, afterdate = date.today()):
    difdias = afterdate.weekday() - dayofweek

    if difdias > 0:
        delay = timedelta(days=6-afterdate.weekday()+dayofweek+1)
    elif difdias < 0:
        delay = timedelta(days=-difdias)
    else:
        delay = timedelta()

    return afterdate + delay

def construirItinerario(dia_inicio, horarios, num_horas, feriados):
    wdinicial = dia_inicio.weekday()
    num_minutos = num_horas*60

    itinerario = []

    index = 0   # por donde parto recorriendo la lista de horarios
    diaclases = dia_inicio
    while index < len(horarios):
        if horarios[index].weekday == wdinicial:
            break
        index += 1

    ultimodiaagregado = dia_inicio
    while num_minutos > 0:
        # buscar el siguiente dia de clases
        hr = horarios[index]
        diaclases = nextDayOfWeek(hr.weekday, ultimodiaagregado)

        # Se busca el siguiente día para hacer clases que no sea feriado
        while diaclases in feriados:
            index = (index + 1)%len(horarios)
            hr = horarios[index]
            diaclases = nextDayOfWeek(hr.weekday, ultimodiaagregado)

        num_minutos -= hr.duracion()
        itinerario.append(diaclases)

        index = (index + 1)%len(horarios)

    return itinerario

def strToDate(fecha_str):
    # Expresión regular de una fecha (yyyy-mm-dd)
    datematch = re.match(r'(?P<y>\d{4})\s*(?P<sep>[-/])\s*0*?(?P<m>[1-9]\d?)\s*(?P=sep)\s*0*?(?P<d>[1-9]\d?)',fecha_str)

    year = int(datematch.group("y"))
    month = int(datematch.group("m"))
    day = int(datematch.group("d"))

    return date(year, month, day)

