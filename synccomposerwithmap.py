# -*- coding: utf-8 -*-
"""
/***************************************************************************
 syncComposerWithMap
                                 A QGIS plugin
 Sync the map canvas extents with composer map
                              -------------------
        begin                : 2014-07-08
        copyright            : (C) 2014 by Ed Boesenberg
        email                : boesiii@yahoo.com
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
# To do:
# Test for active composers
# Below helped me to figure out where to start
# http://gis.stackexchange.com/questions/2515/altering-composer-label-items-in-qgis-with-python

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
# from synccomposerwithmapdialog import syncComposerWithMapDialog
import os.path
import sys


class syncComposerWithMap:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'synccomposerwithmap_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        # self.dlg = syncComposerWithMapDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/synccomposerwithmap/icon.png"),
            u"Sync Composer With Map", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Sync Composer With Map", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Sync Composer With Map", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        #TO DO: Add something for signal and slot
        
        #get canvas
        canvas = self.iface.mapCanvas()
        
        #get active composers in a list
        composerList = self.iface.activeComposers()
        
        #check for Active Composers
        if len(composerList) > 0:
        
            #get first object in list
            composerView = composerList[0]
            
            #get the composition object
            composition = composerView.composition()
            
            #http://gis.stackexchange.com/questions/109335/how-to-test-for-multiple-map-items-in-composer-using-python
            #get all maps in composer
            maps = [item for item in composition.items() if item.type() == QgsComposerItem.ComposerMap and item.scene()]
            if len(maps) > 0:
            
                #get all selected map in composer
                selMaps = [item for item in composition.selectedItems() if item.type() == QgsComposerItem.ComposerMap and item.scene()]
                
                #check for selected maps
                if len(selMaps) > 0:
                
                    #Set map to first selected map found
                    map = selMaps[0]
                    message = "Map Canvas extents and scale have been synchronized with Selected Map in Composer"
                else:
                    #If no maps are selected than set map to first found
                    map = maps[0]
                    message = "Map Canvas extents and scale have been synchronized with first map found in Composer"
                #print str(map)
                
                #calculate x move distance
                moveX = map.extent().center().x()-canvas.extent().center().x()
                #print "Move X = " + str(moveX)
                
                #calculate y move distance
                moveY = map.extent().center().y()-canvas.extent().center().y()
                #print "Move Y = " + str(moveY)
                
                #Get units conversion
                unitCon = map.mapUnitsToMM()
                #print "Conversion: " + str (unitCon)
                
                try:
                    #Move composer map to equal canvas map
                    map.moveContent(-moveX * unitCon, moveY * unitCon)
                    #map.moveContent(-100 * unitCon, 100 * unitCon)
                    
                    #set new composer scale
                    map.setNewScale(canvas.scale())
                    
                    #put a nice message on canvas
                    iface.messageBar().pushMessage("Sync Composer with Map",message , QgsMessageBar.INFO, 2)
                    
                except:
                    iface.messageBar().pushMessage("Sync Composer with Map","Something went wrong", QgsMessageBar.WARNING, 3)
            
            #No Composers
            else:
                iface.messageBar().pushMessage("Sync Composer with Map","There are no maps in Composer", QgsMessageBar.WARNING, 3)            
         
        #No Active Composer Found         
        else:
            iface.messageBar().pushMessage("Sync Composer with Map","There are no active composers", QgsMessageBar.WARNING, 3)
                