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
 
 #icon Arrow by P.J. Onori from The Noun Project
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from synccomposerwithmapdialog import syncComposerWithMapDialog
import os.path


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
        self.dlg = syncComposerWithMapDialog()

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
        #get canvas
        canvas = self.iface.mapCanvas()
        
        #get map canvas scale
        curMapScale = canvas.scale()
        
        #get map canvas current extent
        curMapExtent = canvas.extent()
        
        #get map canvas center
        curMapCenter = canvas.extent().center()
        
        #get map canvas center x coordinate
        curMapCenterX = canvas.extent().center().x()
        
        #get map canvas center y coordinate
        curMapCenterY = canvas.extent().center().y()
        
        #get map canvas width
        curMapWidth = canvas.extent().width()
        
        #get map canvas height
        curMapHeight = canvas.extent().height()
        
        #get map canvas xmin
        curMapXmin = canvas.extent().xMinimum()
        
        #get map canvas xmax
        curMapXmax = canvas.extent().xMaximum()
        
        #get active composers in a list
        composerList = self.iface.activeComposers()
        
        #get first list object
        composerView = composerList[0]
        
        #get the composition object
        composition = composerView.composition()
        
        #iterate over each map in composer
        #Should change this so it will only work on one map
        for item in composition.composerMapItems():
            
            try:
                #get composer map width
                compMapWidth = item.currentMapExtent().width()
                
                #get composer map height
                compMapHeight = item.currentMapExtent().height()
                
                #calculate new Y min
                newCompExtentYmin = curMapCenterY - ((curMapWidth / 2) * (compMapHeight / compMapWidth))
                
                #calculate new y max
                newCompExtentYmax = curMapCenterY + ((curMapWidth / 2) * (compMapHeight / compMapWidth))
                
                #new composer extents
                newCompExtent = QgsRectangle(curMapXmin, newCompExtentYmin, curMapXmax, newCompExtentYmax)
                
                #set composed new extents
                item.setNewExtent(newCompExtent)
                
                #set composer scale to equal map scale
                item.setNewScale(curMapScale)
                
                #put a nice message on canvas
                iface.messageBar().pushMessage("Sync Composer with Map","Map center and scale have been synced with ComposerMessage", QgsMessageBar.INFO, 2)
                
                #not sure why moveContent does not work as expected will investigate
                #moveX = compMapCenterX-curMapCenterX
                #moveY = compMapCenterY-curMapCenterY
                #item.moveContent(moveX, moveY)
                #item.moveContent(0, 1)
                
            except:
                iface.messageBar().pushMessage("Sync Composer with Map","Something went wrong", QgsMessageBar.WARNING, 3)
                print "No Composers!!!"