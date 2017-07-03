#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian Mejias
#
# Distributed under terms of the GPL license.


import unittest
import app.Horario as H
from app.calculo_horario import *
from datetime import date

class TestUnitariosConstruccionItinerario(unittest.TestCase):
    
    def test_nextDayOfWeek(self):

        # siguiente martes a partir del 20/07/2017
        siguientedia = nextDayOfWeek(1, date(2017, 7, 20))

        self.assertEqual(siguientedia, date(2017, 7, 25))

        # siguiente jueves a partir del 29/12/2017
        siguientedia = nextDayOfWeek(3, date(2017, 12, 29))

        self.assertEqual(siguientedia, date(2018, 1, 4))

        # siguiente miercoles a partir del 25/7/2017
        siguientedia = nextDayOfWeek(2, date(2017, 7, 25))

        self.assertEqual(siguientedia, date(2017, 7, 26))

    def test_construccion_itinerario_sin_feriados(self):
        # se empieza un día martes
        dia_inicio = date(2017, 7, 18)
        # lunes, martes y jueves, 1 hora por día
        horarios = [Horario(0, 1000, 1100), Horario(1, 1000, 1100), Horario(3, 1000, 1100)]
        feriados = []
        num_horas = 5
        resultado_esperado = [date(2017, 7, 18), date(2017, 7, 20), date(2017, 7, 24), date(2017, 7, 25), date(2017, 7, 27)]

        self.assertEqual(
                resultado_esperado,
                construirItinerario(dia_inicio, horarios, num_horas, feriados))

    def test_construccion_itinerario_con_feriados(self):
        # se empieza un día martes
        dia_inicio = date(2017, 7, 18)
        # lunes, martes y jueves, 1 hora por día
        horarios = [Horario(0, 1000, 1130), Horario(1, 1000, 1100), Horario(3, 1000, 1130)]
        feriados = [date(2017, 7, 25), date(2017, 7, 31)]
        num_horas = 7
        resultado_esperado = [date(2017, 7, 18), date(2017, 7, 20), date(2017, 7, 24), date(2017, 7, 27), date(2017, 8, 1), date(2017, 8, 3)]

        self.assertEqual(
                resultado_esperado,
                construirItinerario(dia_inicio, horarios, num_horas, feriados))
