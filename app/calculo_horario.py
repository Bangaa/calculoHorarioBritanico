#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian Mejias
#
# Distributed under terms of the GPL license.

from Horario import Horario

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
    # Expresión regular de una fecha (yyyy-mm-dd)
    datematch = re.match(r'(?P<y>\d{4})\s*(?P<sep>[-/])\s*0*?(?P<m>[1-9]\d?)\s*(?P=sep)\s*0*?(?P<d>[1-9]\d?)',fecha_str)

    year = int(datematch.group("y"))
    month = int(datematch.group("m"))
    day = int(datematch.group("d"))

    return date(year, month, day)

