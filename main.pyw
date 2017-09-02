#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian

import sys
from PyQt5.QtWidgets import *

from app.widgets.formulario import Formulario

import locale

locale.setlocale(locale.LC_ALL, 'esp_esp')

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.setGeometry(600, 300, 425, 512)
        self.setWindowTitle('Calculo horario')
        self.statusBar()
        self.show()

    def initUi(self):
        self.formulario = Formulario()
        self.setCentralWidget(self.formulario)

        feriadosMenu = QAction('Feriados', self)
        feriadosMenu.setStatusTip('Muestra y edita los dias feriados')

        menubar = self.menuBar()
        menubar.addAction(feriadosMenu)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Aplicacion()
    sys.exit(app.exec_())
