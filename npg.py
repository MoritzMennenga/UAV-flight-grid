# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NPGflightMode
                                 A QGIS plugin
 This plugin numbers point grids
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-09-26
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
import os.path

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QFileInfo
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import QgsRectangle
from qgis.gui import QgsProjectionSelectionWidget
from .methods import *
from .messageWrapper import *
from .export import *
from .check import *

# Import the code for the dialog
from .npg_dialog import NPGflightModeDialog


# Initialize Qt resources from file resources.py


class NPGflightMode:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'NPGflightMode_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&NPG fliht mode')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('NPGflightMode', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/npg/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'NPG flight'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&NPG flight mode'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = NPGflightModeDialog()


        # show file dialog
        self.dlg.outputPath.clear()
        self.dlg.newOutputButton.clicked.connect(self.select_output_file)

        # show the dialog
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()
        if result:

            # Get the values for the start and the direction
            start = str(self.dlg.cornerCombo.currentText())
            direction = str(self.dlg.directionCombo.currentText())

            # get filename
            filename = self.dlg.outputPath.text()
            #CHECK filename

            # Read Extent
            xmax = QgsRectangle.xMaximum(self.dlg.groupBox.outputExtent())
            xmin = QgsRectangle.xMinimum(self.dlg.groupBox.outputExtent())
            ymin = QgsRectangle.yMinimum(self.dlg.groupBox.outputExtent())
            ymax = QgsRectangle.yMaximum(self.dlg.groupBox.outputExtent())

            extent = [xmin, ymin, xmax, ymax]

            # readCRS
            crs = self.dlg.projectionWidget.crs()
            check_crs = checkCRS(crs)


            if check_crs == True:
                printLogMessage(self, str('OK'), 'test')
                start_coord = []
                if (start == 'NW'):
                    start_coord = [round(xmin, 3), round(ymax, 3)]
                elif (start == 'NE'):
                    start_coord = [round(xmax, 3), round(ymax, 3)]
                elif (start == 'SE'):
                    start_coord = [round(xmax, 3), round(ymin, 3)]
                elif (start == 'SW'):
                    start_coord = [round(xmin, 3), round(ymin, 3)]

                x_steps = int(self.dlg.xText.text())
                y_steps = int(self.dlg.yText.text())


                temp = None
                if (direction == 'W' and start not in ['NE','SE']):
                    criticalMessageToBar(self, 'Error', 'Cannot go to west when start in the west ...')
                elif (direction == 'E' and start not in ['NW', 'SW']):
                    criticalMessageToBar(self, 'Error', 'Cannot go to east when start in the east ...')
                elif (direction == 'N' and start not in ['SE', 'SW']):
                    criticalMessageToBar(self, 'Error', 'Cannot go to north when start in the north ...')
                elif (direction == 'S' and start not in ['NE', 'NW']):
                    criticalMessageToBar(self, 'Error', 'Cannot go to south when start in the south ...')
                elif (direction == 'E' and start == 'NW'):
                    temp = calculateGridX(self, start_coord, x_steps, y_steps, extent)
                elif (direction == 'W' and start == 'NE'):
                    temp = calculateGridX(self, start_coord, (x_steps*-1), y_steps, extent)
                elif (direction == 'E' and start == 'SW'):
                    temp = calculateGridX(self, start_coord, x_steps, (y_steps*-1), extent)
                elif (direction == 'W' and start == 'SE'):
                    temp = calculateGridX(self, start_coord, (x_steps * -1), (y_steps * -1), extent)
                elif (direction == 'S' and start == 'NW'):
                    temp = calculateGridY(self, start_coord, (x_steps *-1),(y_steps*-1), extent)
                elif (direction == 'S' and start == 'NE'):
                    temp = calculateGridY(self, start_coord, (x_steps), (y_steps * -1), extent)
                elif (direction == 'N' and start == 'SW'):
                    temp = calculateGridY(self, start_coord, (x_steps * -1), y_steps, extent)
                elif (direction == 'N' and start == 'SE'):
                    temp = calculateGridY(self, start_coord, x_steps, y_steps, extent)


                if temp is not None:
                    exportFunc(self, temp, filename, crs)
                    layer = self.iface.addVectorLayer(self.dlg.outputPath.text(),
                                                  "",
                                                  "ogr")
            pass

    def select_output_file(self):
        prjfi = QFileInfo(QgsProject.instance().fileName())

        filename, __ = QFileDialog.getSaveFileName(self.dlg, "Select output file ", prjfi.absolutePath(), '*.shp')

        self.dlg.outputPath.setText(filename)
