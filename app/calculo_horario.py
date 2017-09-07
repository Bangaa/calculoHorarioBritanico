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
        raise RuntimeError('El dia inicial cae un dia %s pero no se pudo encontrar ningun %s dentro de los horarios' % (dias[wdinicial],dias[wdinicial]))

    apartirdeldia = fecha_inicio - timedelta(days=1)
    while num_minutos > 0:
        # buscar el siguiente dia de clases
        hr = horarios[index]
        diaclases = nextDayOfWeek(hr.weekday, apartirdeldia)

        # Se busca el siguiente día para hacer clases que no sea feriado
        while diaclases in feriados:
            apartirdeldia = diaclases
            index = (index + 1)%len(horarios)
            hr = horarios[index]
            diaclases = nextDayOfWeek(hr.weekday, apartirdeldia)

        num_minutos -= hr.duracion()
        itinerario.append(diaclases)
        apartirdeldia = diaclases

        index = (index + 1)%len(horarios)

    return itinerario

def construirItinerario_qtdates(fecha_inicio, horarios, num_horas, feriados):
    """
    Funciona de la misma manera que construirItinerario pero los feriados se
    entregan con objetos del tipo QDate
    """
    feriados = [date(*qtdate.getDate()) for qtdate in feriados]
    return construirItinerario(fecha_inicio, horarios, num_horas, feriados)

def strToDate(fecha_str):

    meses = "enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre".split('|')

    date_regex = [re.compile(r"0*(?P<d>\d{1,2}) \s* (?P<s>[-/.]) \s* 0*(?P<m>\d{1,2}) \s* (?P=s) 0*(?P<a>\d{4}|\d{2})",re.X), # nn/nn/nn[nn]
            re.compile(r"0*(?P<d>\d{1,2}) \s* (?P<s>[-/.]) \s* 0*(?P<m>\d{1,2})",re.X), # nn/nn
            re.compile(r"0*(?P<d>\d{1,2}) .* (?P<m>enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre) .* (?P<a>\d{4})", re.I|re.X),
            re.compile(r"0*(?P<d>\d{1,2}) .* (?P<m>enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)", re.I|re.X),
            ]

    match = None

    for regex in date_regex:
        match = regex.search(fecha_str)
        if match:
            break

    if match is None:
        raise ValueError("No se pudo parsear <%s>" % fecha_str)

    dt = match.groupdict()

    dia = int(dt['d'])

    try:
        mes = int(dt['m'])
        if mes > 12:
            aux = dia
            dia = mes
            mes = aux
    except ValueError:
        mes = meses.index(dt['m'].lower()) + 1

    try:
        anyo = int(dt['a'])
        if anyo < 100:
            anyo += 2000
    except KeyError:
        anyo = date.today().year

    return date(anyo, mes, dia)

