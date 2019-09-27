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

def checkCRS(crs):
    #returns false if CRS is invalid
    checkReturn = False
    if crs.isValid():
        checkReturn = True
    else:
        criticalMessageToBar(self,'Error','CRS is not valid!')

    return checkReturn
