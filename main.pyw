#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ian

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import assets.resources

from app.QtExtendedWidgets import Formulario, CalendarWidget, AgregarFeriadosDialog
from app.calculo_horario import strToDate
import pickle

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

        ## Cargar archivo de configuracion

        conf = self.cargarConfiguracion()

        if conf:
            self.calendar_w.agregarLosFeriados(conf['feriados'])
            self.statusBar().showMessage("Archivo de configuracion cargado")

    def initUi(self):
        self.calendar_w = CalendarWidget()
        self.formulario = Formulario(self.calendar_w)
        self.setCentralWidget(self.formulario)

        menubar = self.menuBar()

        feriadosMenu = menubar.addMenu('Feriados')
        feriadosMenu.setStatusTip('Muestra y edita los dias feriados')

        editarFeriados = QAction('Editar feriados', self)
        editarFeriados.triggered.connect(self.mostrarDialogoFeriados)
        editarFeriados.setStatusTip('Abre un calendario para agregar/eliminar dias feriados')
        cargarFeriados = QAction('Cargar feriados', self)
        cargarFeriados.triggered.connect(self.cargarFeriadosDesdeArchivo)
        cargarFeriados.setStatusTip('Agrega dias feriados desde un archivo de texto')

        feriadosMenu.addAction(editarFeriados)
        feriadosMenu.addAction(cargarFeriados)

    def mostrarDialogoFeriados(self):
        dialogo = AgregarFeriadosDialog(self.calendar_w.feriados(), self)
        dialogo.exec()

        feriados_antes = self.calendar_w.feriados()
        feriados_despues = dialogo.calendar_w.feriados()

        eliminar = feriados_antes - feriados_despues
        agregar = feriados_despues - feriados_antes

        self.calendar_w.agregarLosFeriados(agregar)
        self.calendar_w.eliminarLosFeriados(eliminar)

    def cargarFeriadosDesdeArchivo(self):
        fname = QFileDialog.getOpenFileName(self, 'Cargar feriados', os.environ['pwd'], 'Text files (*.txt)')

        if fname[0]:
            feriados = set()
            with open(fname[0], 'r') as f:
                for linea in f:
                    feriados.add(strToDate(linea))
                f.close()

            self.calendar_w.agregarLosFeriados(feriados)

            success = QMessageBox(QMessageBox.Information, 'Carga completa', 'Se cargaron %d feriados' % len(feriados), parent=self)
            success.exec()

    def closeEvent(self, event):
        self.guardarConfiguracion()
        event.accept()

    def guardarConfiguracion(self, fname="horaculo.conf.data"):
        """Guarda la configuracion en un archivo binario.

        Esta accion se gatilla automaticamente al cerrar la aplicacion."""
        conf = {"feriados": self.calendar_w.feriados()}

        with open(fname, 'wb') as fb:
            fb.write(pickle.dumps(conf))

        return True

    def cargarConfiguracion(self, fname="horaculo.conf.data"):
        """Carga la configuracion desde un archivo binario.

        Esta accion se gatilla automaticamente cuando empieza la
        aplicacion.

        Args:
            fname: Nombre del archivo de respaldo (default
                'horaculo.conf.data')
        Returns:
            Si es que existe el archivo de configuracion, devuelve un
            diccionario que contiene las configuraciones de la aplicacion.
            Entre las llaves del diccionario se encuentra: 'feriados'

            Devuelve 'None' si es que no existe un archivo de respaldo.
        """
        try:
            conff = open(fname, "rb")
            conf = pickle.loads(conff.read())

            return conf
        except IOError:
            return None
        except Exception:
            conff.close()
            return None

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    ex = Aplicacion()
    sys.exit(app.exec_())
