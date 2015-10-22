# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
import os
#import resources



def name():
    return ("init","GdbPrint Plugin")

def description():
    return ("init","Beschriftung der GST-Eigentümer")

def icon():
	return "GdbPrint.png"

def version():
    return "1.0.1"

def qgisMinimumVersion():
  return "2.4"


def classFactory(iface):
    from GdbPrint import GdbPrint
    return GdbPrint(iface)
