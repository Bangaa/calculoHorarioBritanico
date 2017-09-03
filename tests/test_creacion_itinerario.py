# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian Mejias
#
# Distributed under terms of the GPL license.


import unittest
import app.horario as H
from app.calculo_horario import *
from datetime import date
from PyQt5.QtCore import QDate

class TestConstruccionItinerario(unittest.TestCase):

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

        # siguiente lunes a partir del 4/09/2017
        siguientedia = nextDayOfWeek(0, date(2017, 9, 4))

        self.assertEqual(siguientedia, date(2017, 9, 11))

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

    def test_construccion_itinerario_sin_feriados_un_solo_horario(self):

        dia_inicio = strToDate('04-09-2017')
        hrsCont = 2
        horarios = [Horario(0, '14:00', '15:00')]

        resultado = construirItinerario(dia_inicio, horarios, hrsCont, [])
        resultado_esperado = [strToDate('04-09-2017'), strToDate('11-09-2017')]

        self.assertEqual(resultado, resultado_esperado)

    def test_construccion_itinerario_con_feriados(self):
        # se empieza un día martes
        dia_inicio = date(2017, 7, 18)
        # lunes, martes y jueves, 1 hora por día
        horarios = [Horario(0, 1000, 1130), Horario(1, 1000, 1100), Horario(3, 1000, 1130)]
        feriados = [date(2017, 7, 25), date(2017, 7, 31)]
        num_horas = 7

        resultado = construirItinerario(dia_inicio, horarios, num_horas, feriados)
        resultado_esperado = [date(2017, 7, 18), date(2017, 7, 20), date(2017, 7, 24), date(2017, 7, 27), date(2017, 8, 1), date(2017, 8, 3)]

        self.assertEqual(resultado_esperado, resultado)

    def test_construccion_itinerario_con_feriados_caso2(self):

        dia_inicio = date(2017, 9, 4)
        horarios = [Horario(0, 1000, 1100)]
        feriados = [date(2017, 9, 11)]
        num_horas = 3

        resultado = construirItinerario(dia_inicio, horarios, num_horas, feriados)
        resultado_esperado = [date(2017, 9, 4), date(2017, 9, 18), date(2017, 9, 25)]

        self.assertEqual(resultado_esperado, resultado)


    def test_construccion_itinerario_dia_inicio_feriado(self):
        dia_inicio = date(2017,9,5)    # martes
        hrsCont = 7
        horarios = [Horario(0, 1400, 1500), Horario(1, 1000, 1100)]
        feriados = [date(2017,9,5)]

        resultado = construirItinerario(dia_inicio, horarios, hrsCont, feriados)

        self.assertEqual(resultado[-1], strToDate('2-10-2017'))

    def test_convertir_string_a_fecha(self):

        self.assertEqual(strToDate("26-08-2017"), date(2017, 8, 26))
        self.assertEqual(strToDate("06-8-2017"), date(2017, 8, 6))
        self.assertEqual(strToDate('2-10-2017'), date(2017, 10, 2))

    def test_const_itin_sin_horarios_raises_exception(self):
        diaI = date(2017, 9, 4)
        hrsCont = 35
        horarios = []

        self.assertRaisesRegex(ValueError, "Se debe entregar al menos 1 horario",
                construirItinerario, *(diaI, horarios, hrsCont, []))

    def test_const_itin_raise_exception_fecha_inicio_sin_horario(self):
        """
        No se debería poder elegir por ejemplo un dia inicial lunes si es que
        en los horarios no se elige el dia lunes.
        """
        diaI = date(2017, 9, 4)
        hrsCont = 35
        horarios = [Horario(1, 1000, 1100), Horario(2, 1000, 1100)]

        self.assertRaisesRegex(RuntimeError, r'El dia inicial cae un dia (\w+) pero no se pudo encontrar ningun \1 dentro de los horarios',
                construirItinerario, *(diaI, horarios, hrsCont))

    def test_const_itin_raise_exception_horas_contratadas_es_cero(self):
        diaI = date(2017,9,4)
        horarios = [Horario(0, 1000, 1100)]
        hrsCont = 0

        self.assertRaisesRegex(ValueError, 'Las horas contratadas no pueden ser cero',
                construirItinerario, *(diaI, horarios, hrsCont))

    def test_construccion_itinerario_feriados_qtdates(self):
        dia_inicio = date(2017, 9, 4)
        horarios = [Horario(0, 1000, 1100)]
        feriados = [QDate(2017, 9, 11)]
        num_horas = 3

        resultado = construirItinerario_qtdates(dia_inicio, horarios, num_horas, feriados)
        resultado_esperado = [date(2017, 9, 4), date(2017, 9, 18), date(2017, 9, 25)]

        self.assertEqual(resultado_esperado, resultado)
