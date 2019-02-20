# -*- coding: utf-8 -*-

#from PyQt4.QtCore import *
#import os
#import resources
#from __future__ import absolute_import


def name():
    return ("init","GdbPrint Plugin")

def description():
    return ("init","Beschriftung der GST-Eigentümer")

def icon():
	return "GdbPrint.png"

def version():
    return "1.1"

def qgisMinimumVersion():
  return "3.2"


def classFactory(iface):
    from .GdbPrint import GdbPrint
    return GdbPrint(iface)
