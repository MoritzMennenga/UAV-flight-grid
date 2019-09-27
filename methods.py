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
from .messageWrapper import *


def specialCaseFunc(self, extend, coord, start):

    # proof how many coordinates have the max min coordinates for the direction
    count_ymax = 0
    count_ymin = 0
    count_xmax = 0
    count_xmin = 0
    for x in range(len(coord)):
        printLogMessage(self, str(coord[x][1]), 'test')
        printLogMessage(self, str(extend[0]), 'test')
        if coord[x][1] == extend[3]:
            count_ymax = count_ymax + 1
        if coord[x][1] == extend[2]:
            count_ymin = count_ymin + 1
        if coord[x][0] == extend[1]:
            count_xmax = count_xmax + 1
        if coord[x][0] == extend[0]:
            count_xmin = count_xmin + 1

    specialCase = False
    if count_ymax > 1 and count_xmin > 1 and count_xmax > 1 and count_ymin > 1:
        specialCase = True

    return specialCase

def getExtendFunc(self, layer):
    ext = layer.extent()
    xmin = round(ext.xMinimum(), 3)
    xmax = round(ext.xMaximum(), 3)
    ymin = round(ext.yMinimum(), 3)
    ymax = round(ext.yMaximum(), 3)
    extend = [xmin, xmax, ymin, ymax]


    return extend

def calculateGridX(self, start_coord, x_steps, y_steps, extent):
    xcoord = start_coord[0]
    ycoord = start_coord[1]
    coord_grid =[]
    id = 1
    coord_grid.append([xcoord, ycoord, 0, id])
    #extent = [xmin, ymin, xmax, ymax]
    extent[0] = round(extent[0], 3)#xmin
    extent[1] = round(extent[1], 3)#ymin
    extent[2] = round(extent[2], 3)#xmax
    extent[3] = round(extent[3], 3)#ymax

    columns = (extent[3] - extent[1]) / abs(y_steps)
    rows = (extent[2] - extent[0]) / abs(x_steps)

    while (columns >= 0):
        local_rows = rows
        while (local_rows > 0):
            xcoord = xcoord + x_steps
            id = id + 1
            coord_grid.append([xcoord, ycoord, 0, id])
            local_rows = local_rows - 1

        ycoord = ycoord - y_steps
        id = id + 1
        coord_grid.append([xcoord, ycoord, 0, id])
        x_steps = x_steps * -1

        columns = columns - 1


    del coord_grid[-1]

    return coord_grid

def calculateGridY(self, start_coord, x_steps, y_steps, extent):
    xcoord = start_coord[0]
    ycoord = start_coord[1]
    coord_grid =[]
    id = 1
    coord_grid.append([xcoord, ycoord, 0, id])
    #extent = [xmin, ymin, xmax, ymax]
    extent[0] = round(extent[0], 3)#xmin
    extent[1] = round(extent[1], 3)#ymin
    extent[2] = round(extent[2], 3)#xmax
    extent[3] = round(extent[3], 3)#ymax

    columns = (extent[3] - extent[1]) / abs(y_steps)
    rows = (extent[2] - extent[0]) / abs(x_steps)

    while (rows >= 0):
        local_columns = columns
        while (local_columns > 0):
            ycoord = ycoord + y_steps
            id = id + 1
            coord_grid.append([xcoord, ycoord, 0, id])
            local_columns = local_columns - 1

        xcoord = xcoord - x_steps
        id = id + 1
        coord_grid.append([xcoord, ycoord, 0, id])
        y_steps = y_steps * -1

        rows = rows - 1


    del coord_grid[-1]

    return coord_grid