# -*- coding: utf-8 -*-

"""

/***************************************************************************

 npg

                                 A QGIS plugin

 npg des

                             -------------------

        begin                : 2017-08-31

        git sha              : $Format:%H$

        copyright            : (C) 2019 by Moritz Mennenga

        email                : mennenga@nihk.de

 ***************************************************************************/



/***************************************************************************

 *                                                                         *

 *   This program is free software; you can redistribute it and/or modify  *

 *   it under the terms of the GNU General Public License as published by  *

 *   the Free Software Foundation; either version 2 of the License, or     *

 *   (at your option) any later version.                                   *

 *                                                                         *

 ***************************************************************************/

"""

from __future__ import print_function

from qgis.gui import QgsMessageBar

from qgis.core import *
from .messageWrapper import *

def criticalMessageToBar (self, header, text):

    self.iface.messageBar().pushMessage(header, text, level=Qgis.Critical)


def warningMessageToBar (self, header, text):

    self.iface.messageBar().pushMessage(header, tex, level=Qgis.Info)


def exportError (self):

    # fix_print_with_import
    print("Error when creating shapefile: ")

    criticalMessageToBar(self, 'Export Error', 'Error when creating shapefile')


def printLogMessage(self,message,tab):

    QgsMessageLog.logMessage(message, tab)
