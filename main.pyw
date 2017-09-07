#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import assets.resources

from app.QtExtendedWidgets import Formulario, CalendarWidget, AgregarFeriadosDialog

import locale

locale.setlocale(locale.LC_ALL, 'esp_esp')

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.setGeometry(600, 300, 425, 512)
        self.setWindowTitle('Calculo horario')
        self.statusBar()
        self.setWindowIcon(QIcon(":/app-icon"))
        self.show()

    def initUi(self):
        self.calendar_w = CalendarWidget()
        self.formulario = Formulario(self.calendar_w)
        self.setCentralWidget(self.formulario)

        feriadosMenu = QAction('Feriados', self)
        feriadosMenu.setStatusTip('Muestra y edita los dias feriados')
        feriadosMenu.triggered.connect(self.mostrarDialogoFeriados)

        menubar = self.menuBar()
        menubar.addAction(feriadosMenu)

    def mostrarDialogoFeriados(self):
        dialogo = AgregarFeriadosDialog(self.calendar_w.feriados(), self)
        dialogo.exec()

        feriados_antes = self.calendar_w.feriados()
        feriados_despues = dialogo.calendar_w.feriados()


        eliminar = feriados_antes - feriados_despues
        agregar = feriados_despues - feriados_antes

        self.calendar_w.agregarLosFeriados(agregar)
        self.calendar_w.eliminarLosFeriados(eliminar)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    ex = Aplicacion()
    sys.exit(app.exec_())
