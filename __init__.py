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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load syncComposerWithMap class from file syncComposerWithMap
    from synccomposerwithmap import syncComposerWithMap
    return syncComposerWithMap(iface)
