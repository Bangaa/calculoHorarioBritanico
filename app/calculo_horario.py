# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian Mejias
#
# Distributed under terms of the GPL license.

from app.horario import Horario
from datetime import timedelta, date
import re

# Devuelve la fecha del siguiente día 'dayofweek'. Por ejemplo, si hoy, 6 de
# junio, es jueves, entonces 'nextDayOfWeek(0)' devuelve '10 de julio'.
# @param dayofweek Es el número del día de la semana (lunes es 0, martes es 1,
# etc)
# @param afterdate Es la fecha a partir de la cual se buscará el proximo
# 'dayofweek'. Es opcional (default: hoy).
def nextDayOfWeek(dayofweek, afterdate = date.today()):
    difdias = afterdate.weekday() - dayofweek

    if difdias > 0:
        delay = timedelta(days=6-afterdate.weekday()+dayofweek+1)
    elif difdias < 0:
        delay = timedelta(days=-difdias)
    else:
        delay = timedelta(days=7)

    return afterdate + delay

##
# Devuelve una lista de fechas en las cuales el alumno deberá asistir a
# clases.
# @param fecha_inicio Es la fecha en la que comienzan las clases
# @param horarios Horarios elegido por el alumno
# @param num_horas Cantidad de horas contratadas
# @param feriados Lista con las fechas en las que no se puede hacer clases.
def construirItinerario(fecha_inicio, horarios, num_horas, feriados=[]):

    if len(horarios) == 0:
        raise ValueError("Se debe entregar al menos 1 horario")
    elif num_horas == 0:
        raise ValueError("Las horas contratadas no pueden ser cero")

    wdinicial = fecha_inicio.weekday()
    num_minutos = num_horas*60
    horarios.sort()

    itinerario = []

    index = 0   # por donde parto recorriendo la lista de horarios
    while index < len(horarios):
        if horarios[index].weekday == wdinicial:
            break
        index += 1

    if index >= len(horarios):
        dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
        raise RuntimeError(f'El dia inicial cae un dia {dias[wdinicial]} pero no se pudo encontrar ningun {dias[wdinicial]} dentro de los horarios')

    apartirdeldia = fecha_inicio - timedelta(days=1)
    while num_minutos > 0:
        # buscar el siguiente dia de clases
        hr = horarios[index]
        diaclases = nextDayOfWeek(hr.weekday, apartirdeldia)

        # Se busca el siguiente día para hacer clases que no sea feriado
        while diaclases in feriados:
            index = (index + 1)%len(horarios)
            hr = horarios[index]
            diaclases = nextDayOfWeek(hr.weekday, apartirdeldia)

        num_minutos -= hr.duracion()
        itinerario.append(diaclases)
        apartirdeldia = diaclases

        index = (index + 1)%len(horarios)

    return itinerario

def strToDate(fecha_str):
    # Expresión regular de una fecha (yyyy-mm-dd)
    # datematch = re.match(r'(?P<y>\d{4})\s*(?P<sep>[-/])\s*0*?(?P<m>[1-9]\d?)\s*(?P=sep)\s*0*?(?P<d>[1-9]\d?)',fecha_str)
    dateregex = re.compile(r"""^0?(?P<d>\d+)         #dia
                                \s*(?P<sep>[-/])\s*
                                0?(?P<m>\d+)         #mes
                                \s*(?P=sep)\s*
                                (?P<y>\d{4})$           #año
                                """, re.X)
    datematch = dateregex.match(fecha_str)
    year = int(datematch.group("y"))
    month = int(datematch.group("m"))
    day = int(datematch.group("d"))

    return date(year, month, day)

