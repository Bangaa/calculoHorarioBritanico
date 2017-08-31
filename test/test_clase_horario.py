import unittest
import app.horario as H
from random import randint

class TestClassHorario(unittest.TestCase):

    def test_comparar_lt(self):

        horario1 = H.Horario(0, 1030, 1200) # Lunes entre las 10:30-12:00
        horario2 = H.Horario(0, 1100, 1200) # Lunes entre las 11:00-12:00

        self.assertLess(horario1, horario2)

        horario1 = H.Horario(1, 1030, 1100) # Martes entre las 10:30-12:00
        horario2 = H.Horario(1, 1030, 1100) # Martes entre las 10:30-12:00

        self.assertFalse(horario1 < horario2)

        horario1 = H.Horario(0, 1030, 1100) # Lunes entre las 10:30-11:00
        horario2 = H.Horario(1, 1000, 1030) # Martes entre las 10:00-10:30

        self.assertLess(horario1, horario2)

    def test_comparar_gt(self):

        horario1 = H.Horario(0, 1030, 1200) # Lunes entre las 10:30-12:00
        horario2 = H.Horario(0, 1100, 1200) # Lunes entre las 11:00-12:00

        self.assertGreater(horario2, horario1)

        horario1 = H.Horario(1, 1030, 1100) # Martes entre las 10:30-12:00
        horario2 = H.Horario(1, 1030, 1100) # Martes entre las 10:30-12:00

        self.assertFalse(horario1 > horario2)

        horario1 = H.Horario(0, 1030, 1100) # Lunes entre las 10:30-11:00
        horario2 = H.Horario(1, 1000, 1030) # Martes entre las 10:00-10:30

        self.assertGreater(horario2, horario1)

    def test_comparar_eq(self):

        horario1 = H.Horario(0, 1030, 1200) # Lunes entre las 10:30-12:00
        horario2 = H.Horario(0, 1100, 1200) # Lunes entre las 11:00-12:00

        self.assertNotEqual(horario1, horario2)

        horario1 = H.Horario(1, 1030, 1100) # Martes entre las 10:30-12:00
        horario2 = H.Horario(4, 1030, 1100) # Martes entre las 10:30-12:00

        self.assertNotEqual(horario1, horario2)

        horario1 = H.Horario(1, 1030, 1100) # Martes entre las 10:30-12:00
        horario2 = H.Horario(1, 1030, 1100) # Martes entre las 10:30-12:00

        self.assertEqual(horario1, horario2)

    def test_duracion_horario(self):
        horario = H.Horario(1, 1030, 1100) # Martes entre las 10:30-12:00

        self.assertEqual(horario.duracion(), 30)

        horario = H.Horario(1, 1030, 1215) # Martes entre las 10:30-12:00

        self.assertEqual(horario.duracion(), 105)

    def test_creacion_horario_con_strings(self):
        hrss = H.Horario(0, 1000, 1130)
        hrcs = H.Horario(0, "10:00", "11:30")

        self.assertEqual(hrss, hrcs)

        hrss = H.Horario(0, 900, 1130)
        hrcs = H.Horario(0, "09:00", "11:30")

        self.assertEqual(hrss, hrcs)

        hrss = H.Horario(0, 45, 325)
        hrcs = H.Horario(0, "00:45", "03:25")

        self.assertEqual(hrss, hrcs)
