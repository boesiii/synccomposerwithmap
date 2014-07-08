# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_synccomposerwithmap.ui'
#
# Created: Tue Jul 08 10:53:06 2014
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_syncComposerWithMap(object):
    def setupUi(self, syncComposerWithMap):
        syncComposerWithMap.setObjectName(_fromUtf8("syncComposerWithMap"))
        syncComposerWithMap.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(syncComposerWithMap)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(syncComposerWithMap)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), syncComposerWithMap.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), syncComposerWithMap.reject)
        QtCore.QMetaObject.connectSlotsByName(syncComposerWithMap)

    def retranslateUi(self, syncComposerWithMap):
        syncComposerWithMap.setWindowTitle(QtGui.QApplication.translate("syncComposerWithMap", "syncComposerWithMap", None, QtGui.QApplication.UnicodeUTF8))

