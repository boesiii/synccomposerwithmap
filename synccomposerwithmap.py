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
 *   (at your option) any later version .                                  *
 *                                                                         *
 ***************************************************************************/
 
 
"""
# To do:
# get rid of not needed code from plugin builder
# Test for active composers
# Test for map in composers
# Research moveContent

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
        #The link below helped me get started
        #http://gis.stackexchange.com/questions/2515/altering-composer-label-items-in-qgis-with-python
        
        #TO DO: ADD SIGNAL AND SLOT
        
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
        #print "Canvas X = " + str(curMapCenterX)
        
        #get map canvas center y coordinate
        curMapCenterY = canvas.extent().center().y()
        #print "Canvas Y = " + str(curMapCenterY)
        
        #get map canvas width
        curMapWidth = canvas.extent().width()
        
        #get map canvas height
        curMapHeight = canvas.extent().height()
        
        #get map canvas xmin
        curMapXmin = canvas.extent().xMinimum()
        
        #get map canvas xmax
        curMapXmax = canvas.extent().xMaximum()
        
        #TO DO: ADD CHECK FOR COMPOSERS
        #get active composers in a list
        composerList = self.iface.activeComposers()
        
        #get first list object
        composerView = composerList[0]
        
        #get the composition object
        composition = composerView.composition()
        
        #old version to get list of maps didn't work in win 32 bit
        #for item in composition.composerMapItems():
        
        #TO DO: CHECK FOR MORE THAN ONE MAP
        #get first map object in composer
        map = composition.getComposerMapById(0)
                
        try:
            #get composer map width
            compMapWidth = map.currentMapExtent().width()
                
            #get composer map height
            compMapHeight = map.currentMapExtent().height()
            
            compMapCenterX = map.extent().center().x()
            #print "Composer X = " + str(compMapCenterX)
            
            compMapCenterY = map.extent().center().y()
            #print "Composer Y= " + str(compMapCenterY)
            
            #old version to calc composer extents
            #calculate new Y min
            #newCompExtentYmin = curMapCenterY - ((curMapWidth / 2) * (compMapHeight / compMapWidth))
            #calculate new y max
            #newCompExtentYmax = curMapCenterY + ((curMapWidth / 2) * (compMapHeight / compMapWidth))
            #new composer extents
            #newCompExtent = QgsRectangle(curMapXmin, newCompExtentYmin, curMapXmax, newCompExtentYmax)
            #set composed new extents
            #map.setNewExtent(newCompExtent)
            #set composer scale to equal map scale
            #map.setNewScale(curMapScale)
            #end of old version stuff
            
            #calculate x move distance
            moveX = compMapCenterX-curMapCenterX
            #print "Move X = " + str(moveX)
            
            #calculate y move distance
            moveY = compMapCenterY-curMapCenterY
            #print "Move Y = " + str(moveY)
            
            #Get units conversion
            unitCon = map.mapUnitsToMM()
            
            #Move composer map to equal canvas map
            map.moveContent(-moveX * unitCon, moveY * unitCon)
            
            #set new composer scale
            map.setNewScale(curMapScale)
            
            #put a nice message on canvas
            iface.messageBar().pushMessage("Sync Composer with Map","Map center and scale have been synced with ComposerMessage", QgsMessageBar.INFO, 2)

                
        except:
                iface.messageBar().pushMessage("Sync Composer with Map","Something went wrong", QgsMessageBar.WARNING, 3)
                