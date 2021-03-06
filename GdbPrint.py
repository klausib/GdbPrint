# -*- coding: utf-8 -*-


#from qgis.PyQt import QtCore, QtGui, QtXml, QtNetwork, QtWebKit
from qgis.PyQt import QtCore, QtGui, QtXml, QtNetwork, QtWebKitWidgets
from qgis.gui import *
from qgis.core import *
from qgis.analysis import *
import math, copy, string, os

from .grpEig_ui import *
from .resources import *



class GdbPrint():
    def __init__(self,iface):

        #Reference to the QGIS Interface
        self.iface = iface
        self.mc = self.iface.mapCanvas()    #Map Canvas variable
        self.layer = QgsVectorLayer()
        #self.tool_vorher = None
        self.x = int
        self.y = int


        # Annotation Manager! Um die Annotations
        # mit dem Annotation Tool dann auch löschen zu können!!!
        self.am = QgsProject.instance().annotationManager()



    ##############################################
    # Verbindung zu QGIS initialisieren
    ##############################################
    def initGui(self):

        # action for starting the plugin
        self.GdbPrint = QtWidgets.QAction( QtGui.QIcon(":/plugins/GdbPrint/GdbPrint.png"),  ("GDB Beschriftung"),  self.iface.mainWindow() )
        #QtCore.QObject.connect(self.GdbPrint, QtCore.SIGNAL("triggered()"), self.initial)
        self.GdbPrint.triggered.connect(self.initial)
        self.GdbPrint.setCheckable(True)

        # toolbar button and menue item
        self.iface.addToolBarIcon( self.GdbPrint )
        self.iface.addPluginToVectorMenu(("GDB Beschriftung"),  self.GdbPrint)


        #Variable enthält das vorherigen Maptool (z.B. Lupe...). Das wird
        #hier weggesichter um es wieder zurückstellen zu können
        #if self.tool_vorher == None:
            #self.tool_vorher = self.iface.mapCanvas().mapTool()

        #----------------------------------------------------------------------



    ###################################################
    # Die eigentliche Initialisierung des Plugincodes
    ###################################################
    def initial(self):

        # Connect des Map Tool Change Events mit der MEthode digiclick (schließt GDB Fenster)
        self.mc.mapToolSet.connect(self.digklick)

        #Ein eigenes Maptool erzeugen das den Punkt zurückgibt (wenn man ins Kartnfenster klickt)
        self.GstTooli = tooli(self.mc)
        self.GstTooli.setObjectName( 'GDB_Print')    # so finden wir unser tooli immer wieder....

        #und QGIS auf das neue Maptool einstellen
        self.iface.mapCanvas().setMapTool(self.GstTooli)

        # ein Signal/Slot Verbindung herstellen zwischen dem eigenen Maptool
        # und der Methode mapclick
        self.GstTooli.punkte.connect(self.mapklick)


        # die Objekte die für die Kommunikationm mit dem Webserver
        # und dessen Antwort benötigt werden
        self.anfrage = QtNetwork.QNetworkRequest()  # enthät die URL für die Anfrage an den Webserver
        self.server = QtNetwork.QNetworkAccessManager() # für die Verbindung mit dem Webserver
        # ein signal/slot verbindung herstellen: die methode self.serverantwort wird aufgerufen
        # sobald der webserver (bei noch bestehender verbindung) das erfolgreiche beantworten
        # der anfrage meldet
        self.server.finished.connect(self.serverantwort)
        self.pagi = QtWebKitWidgets.QWebPage()    # die Webseite die zurückkommt
        self.frame = self.pagi.mainFrame()


        # das Anzeigefenster des Plugins und ein paar von
        # dessen Eigenschaften setzen
        self.eig_frm = EigAuswahl(self.iface.mainWindow())
        poli = QtWidgets.QSizePolicy()
        poli.setHorizontalPolicy(0)
        self.eig_frm.setSizePolicy(poli)
        self.eig_frm.setSizePolicy(poli)
        zeichens = self.eig_frm.btnOK.font()
        zeichens.setBold(True)
        zeichens.setUnderline(True)
        self.eig_frm.btnOK.setFont(zeichens)


        # eine signal/slot verbindung herstellen
        # für die beiden Buttens des Anzeigefensters
        self.eig_frm.btnSel.clicked.connect(self.change_selection)
        self.eig_frm.btnOK.clicked.connect(self.write_selected)

        self.gst_klick = False  # verwenden wir später als flag für eine neue Blase



    #######################################################
    # SLOT wird nache dem Klick in das Mapwindow
    # ausgeführt. x und y sind die Mauskoordinaten
    # und werden vom SIGNAL mit übrgeben
    #######################################################
    def mapklick (self,x, y):

        self.gst_klick = True   # der user hat einen Klick ins Mapwindow gemacht

        # die Mauskoordinaten
        self.x = x
        self.y = y
        # mauskoordinaten ind Kartenkoordinaten umwandeln
        #mappe = QgsMapCanvasMap(self.mc)
        mappe = QgsMapToolIdentify(self.mc)
        klickpunkt = mappe.toMapCoordinates(QtCore.QPoint(x,y))
        liste = self.GstTooli.identify(x,y,QgsMapToolIdentify.ActiveLayer)  # liste mit den Features die angeklickt wurden
                                                                            # das sind je nach Massstab und eingestellten Suchradius durchaus
                                                                            # auch mehre als eines von QGIS zurückgegeben werden
                                                                            # ACHTUNG: Modus Active Layer

        if not len(liste) > 0:
            QtWidgets.QMessageBox.information(None, "Hinweis", 'Keine Daten gefunden.\nBitte prüfen ob ein Grundstückslayer ausgewählt ist!')
            return


        # prüfen ob die für eine gdb abfrage
        # notwendigen felder überhaupt vorhanden sind
        # bei den angeklickten features
        for list in liste:
                if (list.mFeature.fields().indexFromName('kg') < 0 or list.mFeature.fields().indexFromName('gnr') < 0) and (list.mFeature.fields().indexFromName('KG') < 0 or list.mFeature.fields().indexFromName('GNR') < 0):
                    QtWidgets.QMessageBox.information(None, "Hinweis", 'Eines der benötigten Felder KG und GNR nicht gefunden.\nBitte prüfen ob ein Grundstückslayer ausgewählt ist!')
                    return
                # und ob der Klickpunkt innerhalb des
                # Grundstücks liegt. Da je nach MAsstab von QGIS immer
                # etwas mehr Features identifiziert werden. Aber nur eines enthält
                # den tatsächlichen Klickpunkt!
                if list.mFeature.geometry().contains(klickpunkt):
                    self.kg = list.mFeature['kg']
                    self.gnr = list.mFeature['gnr']
                    break


        # ein http anfrageobjekt befüllen
        self.anfrage.setUrl(QtCore.QUrl('http://geodaten.intra.cnv.at/wg4/dbi_cmd.aspx?command=CustomForm&arguments=gdb_vbg|kg_gnr|KG=' + str(self.kg) + '|GNR=' + str(self.gnr)))
        #anfrage an den server schicken
        self.server.get(self.anfrage)



    ###########################################################
    # dieser slot wird aufgerufen wenn das verbindungsobjekt
    # vom webserver die antwort auf die anfrage erhält
    ##########################################################
    def serverantwort(self, reply=None):

        baReply = reply.readAll()   # die Antwort ist ein QBytearray

        boxliste = []
        ckBox = object
        i = 0
        self.textinhalt = ''

        # Muss ausgeschaltet werden vor der Aktualisierung
        # sonst gibts Probleme, keine Ahnung wieso
        self.eig_frm.tblEig.setSortingEnabled(False)


        # den Inhalt der Tabelle vor dem Neubefüllen löschen
        for i in range(self.eig_frm.tblEig.rowCount()):
            self.eig_frm.tblEig.removeRow(0)    # immer nur die oberste löschen weil die Lines von unten nachrücken!!



        # Eigenschafte der Tabelle setzen (auch wenn sie schon vorhanden ist)
        self.eig_frm.tblEig.setHorizontalHeaderLabels(['Eigentümer', 'Anteil', 'Fläche'])
        self.eig_frm.tblEig.setSelectionBehavior(1)
        self.eig_frm.tblEig.setSelectionMode(2)


        i = 0 # !!
        # Tabelle mit (bereits formatmäßig vorbereitetem) Inhalt füllen
        for eig in self.auslesen(baReply):  # self auslesen gibt eine Liste mit objekten vom typ rueckgabe zurück
                                            # (eigentümer, anteil fläche)

            #iti = QtGui.QTableWidgetItem()
            iti = QtWidgets.QTableWidgetItem()

            # spalte 1
            iti.setText(eig.eigentuemer)
            self.eig_frm.tblEig.insertRow(i)
            self.eig_frm.tblEig.setItem(i,0,iti)

            # spalte 2
            iti = QtWidgets.QTableWidgetItem()
            iti.setText(eig.anteil)
            self.eig_frm.tblEig.setItem(i,1,iti)

            # spalte 3
            iti = QtWidgets.QTableWidgetItem()
            iti.setText(eig.flaeche)
            self.eig_frm.tblEig.setItem(i,2,iti)

            self.eig_frm.tblEig.selectRow(i)    # alle werden vorab auf ausgewählt gestellt

            i = i + 1


        # noch etwas Kosmetik
        self.eig_frm.tblEig.resizeColumnsToContents()
        self.eig_frm.tblEig.horizontalHeader().stretchLastSection()

        if not self.eig_frm.isVisible():
            self.eig_frm.move(self.iface.mainWindow().pos())
            self.eig_frm.show()


        # das Widget immer nach vorne holen
        self.eig_frm.raise_()
        self.eig_frm.activateWindow()
        self.eig_frm.tblEig.setFocus()
        self.eig_frm.tblEig.setSelectionMode(3) # standard selections methode für die interaktive Auswahl


        self.eig_frm.tblEig.setSortingEnabled(True)     # Sorting wieder aktivieren


    ####################################################################
    # Methode extrahiert aus dem Bytearray der Antwort des Webservers
    # die gewünschte Information (eigentümer, anteil, fläche). Das Bytearray
    # enthält eigentlich (da Webserver) eine HTML Seite mit Tabelle
    # aus dieser Tabelle müssen eigentümer, anteil und fläche genommen werden
    ###################################################################
    def auslesen(self, ba):

        rueckliste = [] # liste initialisieren

        # Bytearray in String umwandeln und Codierung zuweisen nicht vergessen
        stringlist = str(ba,'utf-8')

        # ein HTML Frame damit füllen
        self.frame.setHtml(stringlist)

        # erstmal die Anzahl der Tabellen bestimmen
        all_elem = self.frame.findAllElements('table')

        # da wir wissen dass dort das gewünschte
        # drin ist nehmen wir die zweite Tabelle (=Element)
        elem = all_elem.at(1)

        # dort alle tr einträge - also alle Zeilen
        elem = elem.findAll('tr')
        anz_zeilen = elem.count()   # Anzahl der Eigentümer

        # die erste Zeile mit den Überschriften
        elem_ue = elem.at(0)
        # von dieser alle Felder (=spalten)
        elem_ue = elem_ue.findAll('td')


        # in einer Schleife prüfen, an welcher Stelle die Felder mit den Namen
        # Eigentuemer, Anteil und Flaeche laut GDB (m²) stehen
        i = 0
        pos_e = 0   # Index mit den Feldpositionen der gesuchten Daten
        pos_a = 0
        pos_f = 0
        while i < elem_ue.count():

            if ('Eigentuemer' in str(elem_ue[i].toPlainText())):
                pos_e = i
            if ('Anteil' in str(elem_ue[i].toPlainText())):
                pos_a = i
            if ('Flaeche laut GDB (m²)' in str(elem_ue[i].toPlainText())):
                pos_f = i


            i = i + 1

        # wieviel eigentümer gibt es -> anzahl der zeilen (tr)
        i = 1
        eig_t = []
        anteil_t = []
        area_t = []
        # nun unsere rueck-objektliste befüllen
        # alle Zeilen der HTML TAbelle durchgehen
        #f = open('d:\dodl.txt','w')
        while i < anz_zeilen:
            # unsere Strukturvariable
            rueck = rueckgabe()

            elem_daten = elem.at(i)
            elem_daten = elem_daten.findAll('td')


            # werte aus der HTML Zeile entnehmen (und die \n entfernen)
            eig = elem_daten[pos_e].toPlainText().replace('\\n','')
            anteil = elem_daten[pos_a].toPlainText().replace('\\n','')
            area = elem_daten[pos_f].toPlainText().replace('\\n','')


            # rueckgabeobjekt befüllen
            rueck.alles = (eig + ' - Anteil: ' + anteil + ' - Fläche: ' + area + ' m²')
            rueck.eigentuemer = (eig)
            rueck.anteil = (anteil)
            rueck.flaeche = (area)
            # rueckobjekt der rückgabeliste hinzufügen
            rueckliste.append(rueck)
            i = i + 1
            #debug output
            #f.write(elem_daten[pos_e].toPlainText().replace('\\n','').encode('latin1') + ' ' + elem_daten[pos_a].toPlainText().replace('\\n','').encode('latin1') + ' ' + elem_daten[pos_f].toPlainText().replace('\\n','').encode('latin1') +'\n')
        #f.close()

        return rueckliste

    #########################################################
    # slot for the map tool change event of the map canvas
    # wird ein anderes Tool ausgewählt, wird das
    # GDB Print Fenster geschlossen
    ########################################################
    def digklick(self,Aktion_neu,Aktion_alt):

        if not (Aktion_neu is None) and Aktion_neu.objectName() != 'GDB_Print':
            self.GdbPrint.setChecked(False)
            self.close_dialog()



    ##########################
    # deactivating the plugin
    ##########################
    def unload(self):

        self.mc.disconnect()

        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&GdbPrint", self.GdbPrint)
        self.iface.removeToolBarIcon(self.GdbPrint)


    ##########################################
    # close button clicked - send close event
    ##########################################
    def close_dialog(self):
        self.eig_frm.close()


    ###############################################
    # Dieser Slot wechselt die Ausgewählten Zeilen
    # in der Tabelle mit den Eigentümern. Alles
    # selektieren oder selektieren
    ##############################################
    def change_selection(self):

        # selection mode umschalten
        self.eig_frm.tblEig.setSelectionMode(2)
        auswahl_mod = self.eig_frm.tblEig.selectionModel()
        list_mod_index = auswahl_mod.selectedRows()

        # die selektionen/deselektionen vornehmen
        if len(list_mod_index) == 0:
            for row in range(self.eig_frm.tblEig.rowCount()):
                self.eig_frm.tblEig.selectRow(row)
        else:
            for row in range(self.eig_frm.tblEig.rowCount()):
                self.eig_frm.tblEig.clearSelection()

        # selection mode wiederherstellen
        self.eig_frm.tblEig.setSelectionMode(3)
        self.eig_frm.tblEig.setFocus()



    ###########################################################################
    # nachdem wir die gewünschten Daten vom Webserver geholt haben und
    # in die Tabelle des Fensters GDB Print eingefügt haben, können wir
    # die Daten in eine Beschriftungstext Blase ins  QGIS MAp Window Schreiben
    ###########################################################################
    def write_selected(self):

        erstezeile = False

        # hier entscheiden ob eine neue Blase erzeugt werden
        # oder Daten in eine bestehende hinzugeführt werden sollen
        if self.gst_klick:  # Eine neue Blase machen
            self.gdb_text = QgsTextAnnotation(self.mc)
            self.textinhalt = ''
            self.indexliste = []    # ist ganz wichtig: Enthält dann den Index der Lines der Tabelle die bereits beschriftet sind
            erstezeile = True # wegen dem Absatzsteuerzeichen \n


        # nur ausgewählte (selected) rows werden beschriftet
        # und hier extrahiert
        auswahl_mod = self.eig_frm.tblEig.selectionModel()
        list_mod_index = auswahl_mod.selectedRows()

        # wenn nichts ausgeählt -> return
        if len(list_mod_index) == 0:
            return

        # Schleife geht die ausgewählten
        # Tabellenzeilen durch
        for index in list_mod_index:
            if  self.indexliste.count(index) == 0:    # Index wird in der Indexliste nicht gefunden -> Inhalt ist nicht schon angezeigt - Verhindern von Mehrfachbeschriftung mit gleichem Inhalt!!
                if erstezeile:
                    if not (self.eig_frm.tblEig.item(index.row(), 0) == None or self.eig_frm.tblEig.item(index.row(), 1) == None):
                        self.textinhalt = self.textinhalt + self.eig_frm.tblEig.item(index.row(), 0).text() + ' - ' + self.eig_frm.tblEig.item(index.row(), 1).text()
                        erstezeile = False
                else:
                    if not (self.eig_frm.tblEig.item(index.row(), 0) == None or self.eig_frm.tblEig.item(index.row(), 1) == None):
                        self.textinhalt = self.textinhalt + '\n'
                        self.textinhalt = self.textinhalt + self.eig_frm.tblEig.item(index.row(), 0).text() + ' - ' + self.eig_frm.tblEig.item(index.row(), 1).text()
                self.indexliste.append(index)   # index ist in die BLase aufgenommen und wird so als angeziegt registriert


        # nun können wir die Blase mit Text erzeugen

        # Ein Textdokument instanzieren ->
        # enthält den T ext und die Formatierung
        text = QtGui.QTextDocument()
        # Das Fontobjekt fürs Textobjekt
        font = QtGui.QFont()
        font.setPointSize(8)
        text.setDefaultFont(font)
        text.setPlainText(self.textinhalt)
        # Benötigte Framgröße
        frame_groesse = text.size()
        #maximalgroesse = self.mc.map().contentImage().size()
        maximalgroesse = self.mc.sceneRect()
        #QtWidgets.QMessageBox.information(None, "Hinweis", str(maximalgroesse.width()))


        # Wie gross wird die Blase?
        if (frame_groesse.height() > maximalgroesse.height() / 2) or (frame_groesse.width() > maximalgroesse.width() / 2):
            Qret = QtWidgets.QMessageBox.critical(None, "Achtung", 'Die Anzeige der ausgewählten Eigentümer wird 50% des QGIS Kartenfensters überdecken.\nTrotzdem anzeigen?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)

            if not Qret == QtWidgets.QMessageBox.Yes:
                return

        #Hintergrund transparent und Rahmen soll weiss sein
        fs = self.gdb_text.fillSymbol()
        sl = fs.symbolLayer(0)
        sl.setFillColor(QtGui.QColor(255,255,255))
        sl.setStrokeColor(QtGui.QColor(0,0,0))
        fs.setOpacity(0.8)

        mappe = QgsMapToolIdentify(self.mc)
        einsetzpunkt = mappe.toMapCoordinates(QtCore.QPoint(self.x,self.y)) # zuerst die mauskoordineten der scene in map koordinaten umwandeln

        if self.gst_klick:  # Eine neue Blase
            self.gdb_text.setMapPosition(einsetzpunkt)

         # Benötigte Framgröße
        self.gdb_text.setDocument(text)
        self.gdb_text.setFrameSize(frame_groesse)
        self.gdb_text.setMarkerSymbol(None) # wir möchten keinen roten Knödel


        # Den Text dem Map Canvas hinzufügen nicht vergessen!
        self.gdb_text_item = QgsMapCanvasAnnotationItem(self.gdb_text,self.mc)

        # Und unbedingt auch zum Annotation Manager,
        # sonst können sie mit dem Annotation Tool nicht gelöscht werden!!
        self.am.addAnnotation(self.gdb_text)



        # Reicht die Blase über das Mapfenster raus,
        # dann muss sie nach innen verschoben werden. das machen wir nun
        # offset from reference pont ist das shift der Blase bezogen auf den Klickpunkt
        # in Pixelkoordinaten des View Image (system ist von links oben nach rechts unten)
        rechtsx = self.x + self.gdb_text_item.boundingRect().width() # Koordinaten im View geht von links oben nach rechts unten
        min_rechtsy = self.y - abs(self.gdb_text.frameOffsetFromReferencePoint().y())    # offset ist negativ
        max_rechtsy = min_rechtsy + self.gdb_text_item.boundingRect().height()




        if self.gst_klick:  # Eine neue Blase - QGIS dreht sie standardmäßig nach rechts oben -
                            # blase muss verschoben werden
                            # wenn sie über das Mapfenster hinausgeht
            shift = 0
            if rechtsx > maximalgroesse.width():  # prüfen ob Blase über den rechten Rand hinausragt
                shift = rechtsx - maximalgroesse.width()
                self.gdb_text.setFrameOffsetFromReferencePoint(QtCore.QPointF(self.gdb_text.frameOffsetFromReferencePoint().x()- shift, self.gdb_text.frameOffsetFromReferencePoint().y()))

            shift = 0
            if min_rechtsy < 0: # prüfen ob Blase über den oberen Rand hinausragt - obere Mapfenstergrenze ist 0 und positiv ist nach unten, also kleiner 0!
                shift =  min_rechtsy
                self.gdb_text.setFrameOffsetFromReferencePoint(QtCore.QPointF(self.gdb_text.frameOffsetFromReferencePoint().x(), self.gdb_text.frameOffsetFromReferencePoint().y()- shift))

            shift = 0
            if max_rechtsy > maximalgroesse.height(): # prüfen ob Blase über den unteren Rand hinausragt
                shift =  max_rechtsy - maximalgroesse.height()
                self.gdb_text.setFrameOffsetFromReferencePoint(QtCore.QPointF(self.gdb_text.frameOffsetFromReferencePoint().x(), self.gdb_text.frameOffsetFromReferencePoint().y()- shift))



        self.gst_klick = False  # gst_klick zurücksetzten. Erst bei neuem Klick ins
                                # Mapwindow wird das wieder True



#############################################
# Klassendefinition dient eigentlich
# als Struktuvariable für die Rückgabewerte
############################################
class rueckgabe():

    def __init__(self):
        alles = ''
        eigentuemer = ''
        anteil = ''
        flaeche = ''

#########################################################################
# Klassendefinition unseres eigenen Maptools fürs Plugin
# GDB Print - es erbt alles von der Klasse QgsMapToolIdentify
# erhält lediglich eine eigenes SIGNAL das über die Reimplementierung
# das canvas press events die Mausposition zurückgibt
########################################################################
class tooli(QgsMapToolIdentify):

    # Ein individuelles Signal deklarieren
    punkte = QtCore.pyqtSignal(float,float)

    def __init__(self,mc):
        QgsMapToolIdentify.__init__(self, mc)

        # Instanzvariablen
        self.x = int
        self.y = int




    # canvas press event wird reimplementiert
    def canvasPressEvent(self, ev):
        self.x = ev.pos().x()
        self.y = ev.pos().y()

        self.punkte.emit(self.x,self.y) # eigenes SIGNAL mit Namen punkte wird emittiert (beim canvas klick)
                                        # das die Mausposition mitübermittelt


###########################################
# Klassendefinition für das Anzeigefenster
###########################################
class EigAuswahl(QtWidgets.QDialog,QtWidgets.QMainWindow, Ui_frmEig):

    def __init__(self,parent): #,iface,pfad = None):
        QtWidgets.QDialog.__init__(self,parent)
        Ui_frmEig.__init__(self)


        self.setupUi(self)  # WICHTIG, sonst kommt das Widget oder der Dialog nicht vollständig, hier wird alles so
                            # initalisiert wie im Designer dargestellt!!!!

    # beim klicken auf das kreuzchen
    # wird der closeevent gesendet. hier die reimplementation
    def closeEvent(self,event = None):
        self.close()
