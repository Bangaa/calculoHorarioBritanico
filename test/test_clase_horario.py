import unittest
import app.Horario as H
from random import randint

class TestUnitariosHorario(unittest.TestCase):

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