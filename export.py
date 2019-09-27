# -*- coding: utf-8 -*-

"""

/***************************************************************************

 npg

                                 A QGIS plugin

 npg des

                             -------------------

        begin                : 2019-02-06

        git sha              : $Format:%H$

        copyright            : (C) 2019 by Moritz Mennenga

        email                : mennenga@nihk.de

 ***************************************************************************/

"""
from __future__ import absolute_import


from builtins import str
from builtins import range

from qgis.PyQt.QtCore import QVariant

from qgis.core import *
from .messageWrapper import *

def exportFunc(self, coord, filename, corrdinate_system):
    '''Create Vector Layer'''

    export_fields = QgsFields()

    export_fields.append(QgsField("x", QVariant.Double))

    export_fields.append(QgsField("y", QVariant.Double))

    export_fields.append(QgsField("z", QVariant.Double))

    export_fields.append(QgsField("id", QVariant.Int))

    writer = QgsVectorFileWriter(filename,
                                 "utf-8",
                                 export_fields,
                                 QgsWkbTypes.Point,
                                 corrdinate_system,
                                 "ESRI Shapefile")

    if writer.hasError() != QgsVectorFileWriter.NoError:
        exportError(self)

    export_feature = QgsFeature()
    for x in range(len(coord)):
        printLogMessage(self, str(coord[x]), 'coord')
        printLogMessage(self, str(coord[x][0]), 'coord')
        printLogMessage(self, str(coord[x][1]), 'coord')
        export_feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(coord[x][0],
                                                                          coord[x][1])))

        export_feature.setAttributes([float(coord[x][0]), float(coord[x][1]),
                                          float(coord[x][2]), str(coord[x][3])])

        writer.addFeature(export_feature)

    del writer