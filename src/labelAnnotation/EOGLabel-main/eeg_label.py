import os
import numpy as np
from numpy import save, load
from scipy import signal
from scipy.signal import butter, lfilter, sosfilt
import pyedflib
# import codecs
# import re

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLabel, QRadioButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import MouseButton, KeyEvent
import matplotlib.pyplot as plt
import random

class DataLoadAndPlot :

    def __init__( self, efdFileName ):

        self.minPlot = 0
        self.maxPlot = self.minPlot + 1000*20
        self.dataEDF = self.loadData( efdFileName )

    def readEDF( self, fileName ) :
        
        f = pyedflib.EdfReader( fileName )
        n = f.signals_in_file
        signal_labels = f.getSignalLabels()
        sigbufs = np.zeros((n, f.getNSamples()[0]))
        for i in np.arange(n):
            sigbufs[i, :] = f.readSignal(i)
        
        return sigbufs, signal_labels, f, n

    # def readASCII( self, asciiArray ) :
        
    #     dataArray = []
    #     patternEmpty = re.compile( "^\.$" )
            
    #     for line in asciiArray :
            
    #         testEmpty = not any( bool( patternEmpty.match( s ) ) for s in line )
            
    #         if any("32765" in s for s in line ) and testEmpty :
                
    #             tmp = []
                
    #             for word in line :
                    
    #                 w = word.replace(',', '')
                    
    #                 try:
                        
    #                     tmp.append(float( w ))
                        
    #                 except ValueError:
                        
    #                     tmp.append( 0. )
                        
    #             dataArray.append( tmp )
                
    #     dataArray = np.array( dataArray )
    #     dataArray = dataArray[ :, 1 ]
    #     return dataArray

    # def loadTxt( self, fileNameTxt ) :

    #     with codecs.open( fileNameTxt, encoding='utf-8-sig') as f:
    #                 X = [[x for x in line.split()] for line in f]
            
    #     Xnp = np.array(X)
    #     dataArray = self.readASCII( Xnp )

    #     return  self.formatLoadedSaccade( dataArray )

    # def formatLoadedSaccade( self, dataArray ) :

    #     saccadeList = []

    #     for saccade in dataArray :

    #         start = int ( ( saccade - 0.2 ) * 1000 )
    #         end = int ( ( saccade + 0.6 ) * 1000 )
    #         saccadeList.append( [ start, end ] )
        
    #     return saccadeList
            

    def changeHzTo( self, eogIn, fromHz, toHz ) :
        
        newEOG = []
        
        for sig in eogIn :
        
            newSig = []

            hzDiv = fromHz / toHz

            for i in range( 0, sig.shape[ 0 ], fromHz ) :

                j = 0.

                while ( j < fromHz and i + j + round( hzDiv ) < sig.shape[ 0 ] ) :

                    start = i + round( j )
                    newSig.append( np.mean( sig[ start : start + round( hzDiv ) ] ) )
                    j += hzDiv
            
            newEOG.append( newSig )
                
        return np.array( newEOG )
    
    def loadData( self, fileNameEDF ) :

        sigbufs, _, _, _ = self.readEDF( fileNameEDF )
        eyesData = sigbufs[ [ 256, 257, 258, 259, 68, 69, 70, 71, 72 ] ]

        eyesData[ 6 ] = eyesData[ 0 ] - eyesData[ 1 ]
        eyesData[ 7 ] = eyesData[ 1 ] - eyesData[ 0 ]
        eyesData[ 8 ] = eyesData[ 3 ] - eyesData[ 2 ]
        print(eyesData.shape)
        
        return eyesData

    def getDataToPlot( self ) :
        data = self.dataEDF[ [ 6, 7, 8 ] , : ]
        data = self.changeHzTo( data, 2048, 1000 )
        print( data.shape )

        sfreq = 1000
        nyq = 0.5 * sfreq
        high = 10 / nyq
        filter_order = 5
        b, a = signal.butter(filter_order, high, btype='low')
        data = signal.filtfilt(b, a, data[:])

        data = np.swapaxes( data, 0, 1 )

        return data


# used to start : https://www.geeksforgeeks.org/how-to-embed-matplotlib-graph-in-pyqt5/
# main window
# which inherits QDialog
class Window(QDialog):
       
    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.saccadeListLoaded = []
        self.blinkListLoaded = []
        
        fileNameEDF = '.\eegDataSet.edf'
        self.myData = DataLoadAndPlot( fileNameEDF )

        fileNameNPYSaccade = '.\exampleSaccade.npy'
        self.saccadeListLoaded = load( fileNameNPYSaccade )
        
        fileNameNPYBlink = '.\exampleBlink.npy'
        self.blinkListLoaded = load( fileNameNPYBlink )

        # fileNameTxtSaccade = '..\..\Work\elocans\data Anais\DataWassim\\Testdatawassim2.txt'
        # self.saccadeListLoaded = self.myData.loadTxt( fileNameTxtSaccade )

        self.blinkList = []
        self.blinkSpanList = []
        self.saccadeList = []
        self.saccadeSpanList = []
        self.modeTag = ''

        self.keyTagList = [
            [ 'right', '→' ],
            [ 'left', '←' ],
            [ 'up', '↑' ],
            [ 'down', '↓' ]
            ]
   
        # a figure instance to plot on
        self.figure = plt.figure()
   
        # this is the Canvas Widget that 
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
        # self.canvas.setFocus()
        self.cid_enter = self.canvas.mpl_connect('axes_enter_event', self.on_enter_event)

        self.toolbar = NavigationToolbar(self.canvas, self)
   
        self.buttonForward = QPushButton('Forward')
        self.buttonForward.clicked.connect( lambda: self.forwardBtn())

        self.buttonBackward = QPushButton('Backward')
        self.buttonBackward.clicked.connect( lambda: self.backwardBtn())

        self.buttonSave = QPushButton('Save')
        self.buttonSave.clicked.connect( lambda: self.saveBtn())
        

        self.labelTag = QLabel( 'Events :' )
        self.rdBtnBlink = QRadioButton( 'Blink' )
        self.rdBtnSaccade = QRadioButton( 'Saccade' )
        self.rdBtnBlink.toggled.connect( self.onClikedRdBtn )
        self.rdBtnSaccade.toggled.connect( self.onClikedRdBtn )

   
        layout = QVBoxLayout()
           
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.buttonForward)
        layout.addWidget(self.buttonBackward)
        layout.addWidget(self.buttonSave)
        layout.addWidget(self.labelTag)
        layout.addWidget(self.rdBtnBlink)
        layout.addWidget(self.rdBtnSaccade)
           
        self.setLayout(layout)

        self.plot( fileNameEDF )

        self.spanFromSaccadeList( self.saccadeListLoaded )
        self.spanFromBlinkList( self.blinkListLoaded )

        self.tagState = "Idle"
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_move)
        self.canvas.mpl_connect("key_press_event", self.on_keyPressed)



    def on_enter_event(self, _):
        self.canvas.setFocus()

    def onClikedRdBtn( self ) :

        radioBtn = self.sender()
        if radioBtn.isChecked() :
            self.modeTag = radioBtn.text()

    def on_press(self, event):

        if self.tagState == "Idle" :

            if event.xdata is not None :

                if event.button is MouseButton.LEFT :

                    if self.modeTag == 'Blink' : 

                        indiceSpan = self.testSpanBlinkUnderCursor( event.xdata )

                        if indiceSpan is not None :

                            self.on_pressBlinkModify( event, indiceSpan )

                        else :
                            
                            self.on_pressBlinkCreate( event )

                    elif self.modeTag == 'Saccade' :

                        indiceSpan = self.testSpanSaccadeUnderCursor( event.xdata )

                        if indiceSpan is not None :
                            
                            self.on_pressSaccadeModify( event, indiceSpan )

                        else :

                            self.on_pressSaccadeCreate( event )

    def on_pressBlinkCreate( self, event ) :
        self.tagState = "Create"
        self.mySpanstart = event.xdata
        end = event.xdata + 1
        self.blinkSpanList.append( self.plot.axvspan( self.mySpanstart, end, color='green', alpha=0.2 ) )
        self.canvas.draw()

    def on_pressSaccadeCreate( self, event ) :
        self.tagState = "Create"
        self.mySpanstart = event.xdata
        end = event.xdata + 1
        self.saccadeSpanList.append( self.plot.axvspan( self.mySpanstart, end, color='blue', alpha=0.2 ) )
        self.canvas.draw()


    def on_pressBlinkModify( self, event, indiceSpan ) :
        self.tagState = "Modify"
        self.indiceSpan = indiceSpan
        self.firstX = event.xdata

    def on_pressSaccadeModify( self, event, indiceSpan ) :
        self.tagState = "Modify"
        self.indiceSpan = indiceSpan
        self.firstX = event.xdata


    def on_release(self, event):

        if event.button is MouseButton.LEFT :

            if self.tagState == "Create" :

                if self.modeTag == 'Blink' : 
                    self.on_releaseBlinkCreate( event )
                elif self.modeTag == 'Saccade' :
                    self.on_releaseSaccadeCreate( event )
                    
            if self.tagState == "Modify" :

                if self.modeTag == 'Blink' : 
                    self.on_releaseBlinkModify( event )
                elif self.modeTag == 'Saccade' :
                    self.on_releaseSaccadeModify( event )
                    
        elif event.button is MouseButton.RIGHT :

            if event.xdata is not None :

                if self.modeTag == 'Blink' : 
                    self.deleteSpanBlinkAt( event.xdata )
                elif self.modeTag == 'Saccade' :
                    self.deleteSpanSaccadeAt( event.xdata )

    def on_releaseBlinkCreate( self, event ) :

        self.tagState = "Idle"
        mySpan = self.blinkSpanList[ -1 ]
        mySpan.remove()
        del self.blinkSpanList[ - 1 ]
        
        end = event.xdata
        
        if end is not None and abs( end - self.mySpanstart ) > 9 :

            self.blinkSpanList.append( [ self.plot.axvspan( self.mySpanstart, end, color='green', alpha=0.2 ), self.plot.text( 0, -400, "" ) ] )

            if self.mySpanstart < end :
                center = self.mySpanstart + ( end - self.mySpanstart ) / 2
                self.blinkList.append( [ self.mySpanstart, end, center, "" ] )
            else :
                center = end + ( self.mySpanstart - end ) / 2
                self.blinkList.append( [ end, self.mySpanstart, center, "" ] )

        self.canvas.draw()

    def on_releaseSaccadeCreate( self, event ) :

        self.tagState = "Idle"
        mySpan = self.saccadeSpanList[ -1 ]
        mySpan.remove()
        del self.saccadeSpanList[ - 1 ]

        end = event.xdata
        
        if end is not None and abs( end - self.mySpanstart ) > 9 :
            
            self.saccadeSpanList.append( [ self.plot.axvspan( self.mySpanstart, end, color='blue', alpha=0.2 ), self.plot.text( 0, -400, "" ) ] )

            if self.mySpanstart < end :
                center = self.mySpanstart + ( end - self.mySpanstart ) / 2
                self.saccadeList.append( [ self.mySpanstart, end, center, "" ] )
            else :
                center = end + ( self.mySpanstart - end ) / 2
                self.saccadeList.append( [ end, self.mySpanstart, center, "" ] )

        self.canvas.draw()


    def on_releaseBlinkModify( self, event ) :

        self.tagState = "Idle"
        start = self.blinkList[ self.indiceSpan ][ 0 ] + event.xdata - self.firstX
        end = self.blinkList[ self.indiceSpan ][ 1 ] + event.xdata - self.firstX
        mySpan = self.blinkSpanList[ self.indiceSpan ][ 0 ]
        mySpan.remove()
        self.blinkSpanList[ self.indiceSpan ][ 0 ] = self.plot.axvspan( start, end, color='green', alpha=0.2 )
        center = start + ( end - start ) / 2
        self.blinkList[ self.indiceSpan ] = [ start, end, center, self.blinkList[ self.indiceSpan ][ 3 ] ]
        self.writeInBlink( self.indiceSpan, center - 100 )
        self.canvas.draw()

    def on_releaseSaccadeModify( self, event ) :

        self.tagState = "Idle"
        start = self.saccadeList[ self.indiceSpan ][ 0 ] + event.xdata - self.firstX
        end = self.saccadeList[ self.indiceSpan ][ 1 ] + event.xdata - self.firstX
        mySpan = self.saccadeSpanList[ self.indiceSpan ][ 0 ]
        mySpan.remove()
        self.saccadeSpanList[ self.indiceSpan ][ 0 ] = self.plot.axvspan( start, end, color='blue', alpha=0.2 )
        center = start + ( end - start ) / 2
        self.saccadeList[ self.indiceSpan ] = [ start, end, center, self.saccadeList[ self.indiceSpan ][ 3 ] ]
        self.writeInSaccade( self.indiceSpan, center - 100 )
        self.canvas.draw()


    def on_move(self, event):
        
        if event.xdata is not None :

            if self.tagState == "Create" :

                if self.modeTag == 'Blink' : 
                    self.on_moveBlinkCreate( event )
                elif self.modeTag == 'Saccade' :
                    self.on_moveSaccadeCreate( event )

            elif self.tagState == "Modify" :

                if self.modeTag == 'Blink' : 
                    self.on_moveBlinkModify( event )
                elif self.modeTag == 'Saccade' :
                    self.on_moveSaccadeModify( event )

    def on_moveBlinkCreate( self, event ) :

        mySpan = self.blinkSpanList[ -1 ]
        mySpan.remove()
        del self.blinkSpanList[ - 1 ]
        end = event.xdata
        self.blinkSpanList.append( self.plot.axvspan( self.mySpanstart, end, color='green', alpha=0.2 ) )
        self.canvas.draw()
        
    def on_moveSaccadeCreate( self, event ) :

        mySpan = self.saccadeSpanList[ -1 ]
        mySpan.remove()
        del self.saccadeSpanList[ - 1 ]
        end = event.xdata
        self.saccadeSpanList.append( self.plot.axvspan( self.mySpanstart, end, color='blue', alpha=0.2 ) )
        self.canvas.draw()


    def on_moveBlinkModify( self, event ) :

        start = self.blinkList[ self.indiceSpan ][ 0 ] + event.xdata -self.firstX
        end = self.blinkList[ self.indiceSpan ][ 1 ] + event.xdata - self.firstX
        mySpan = self.blinkSpanList[ self.indiceSpan ][ 0 ]
        mySpan.remove()
        self.blinkSpanList[ self.indiceSpan ][ 0 ] = self.plot.axvspan( start, end, color='green', alpha=0.2 )
        center = start + ( end - start ) / 2
        self.writeInBlink( self.indiceSpan, center - 100 )
        self.canvas.draw()

    def on_moveSaccadeModify( self, event ) :

        start = self.saccadeList[ self.indiceSpan ][ 0 ] + event.xdata -self.firstX
        end = self.saccadeList[ self.indiceSpan ][ 1 ] + event.xdata -self.firstX
        mySpan = self.saccadeSpanList[ self.indiceSpan ][ 0 ]
        mySpan.remove()
        self.saccadeSpanList[ self.indiceSpan ][ 0 ] = self.plot.axvspan( start, end, color='blue', alpha=0.2 )
        center = start + ( end - start ) / 2
        self.writeInSaccade( self.indiceSpan, center - 100 )
        self.canvas.draw()


    def on_keyPressed( self, event ) :

        if self.tagState == "Idle" :

            if self.modeTag == 'Blink' :

                indiceSpan = self.testSpanBlinkUnderCursor( event.xdata )

                if indiceSpan is not None :
                    
                    self.on_keyBlink( event, indiceSpan )

            if self.modeTag == 'Saccade' :

                indiceSpan = self.testSpanSaccadeUnderCursor( event.xdata )

                if indiceSpan is not None :
                    
                    self.on_keySaccade( event, indiceSpan )

    def on_keyBlink( self, event, indiceSpan ) :

        for keyTag in self.keyTagList :

            if keyTag[ 0 ] == event.key :

                if keyTag[ 0 ] in self.blinkList[ indiceSpan ][ 3 ] :

                    self.blinkList[ indiceSpan ][ 3 ] = self.blinkList[ indiceSpan ][ 3 ].replace( keyTag[ 0 ], "" )
                
                else :

                    self.blinkList[ indiceSpan ][ 3 ] = self.blinkList[ indiceSpan ][ 3 ] + keyTag[ 0 ]

                self.blinkList[ indiceSpan ][ 3 ] = self.rewriteKeyTag( self.blinkList[ indiceSpan ][ 3 ] )
                self.writeInBlink( indiceSpan, self.blinkList[ indiceSpan ][ 2 ] - 100 )
                self.canvas.draw()
                break

    def on_keySaccade( self, event, indiceSpan ) :

        for keyTag in self.keyTagList :

            if keyTag[ 0 ] == event.key :

                if keyTag[ 0 ] in self.saccadeList[ indiceSpan ][ 3 ] :

                    self.saccadeList[ indiceSpan ][ 3 ] = self.saccadeList[ indiceSpan ][ 3 ].replace( keyTag[ 0 ], "" )
                
                else :

                    self.saccadeList[ indiceSpan ][ 3 ] = self.saccadeList[ indiceSpan ][ 3 ] + keyTag[ 0 ]

                self.saccadeList[ indiceSpan ][ 3 ] = self.rewriteKeyTag( self.saccadeList[ indiceSpan ][ 3 ] )
                self.writeInSaccade( indiceSpan, self.saccadeList[ indiceSpan ][ 2 ] - 100 )
                self.canvas.draw()
                break
   

    def writeInBlink( self, indiceSpan, xText ) :

        textToWrite = self.getTextToWrite( self.blinkList[ indiceSpan ][ 3 ] )
        self.blinkSpanList[ indiceSpan ][ 1 ].set_text( textToWrite )
        self.blinkSpanList[ indiceSpan ][ 1 ].set_position( ( xText, -400 ) )

    def writeInSaccade( self, indiceSpan, xText ) :

        textToWrite = self.getTextToWrite( self.saccadeList[ indiceSpan ][ 3 ] )
        self.saccadeSpanList[ indiceSpan ][ 1 ].set_text( textToWrite )
        self.saccadeSpanList[ indiceSpan ][ 1 ].set_position( ( xText, -400 ) )

    def getTextToWrite( self, keyString ) :

        result = ""

        for keyTag in self.keyTagList :

            if keyTag[ 0 ] in keyString :

                result = result + keyTag[ 1 ]
            
        return result

    def rewriteKeyTag( self, keytagString ) :

        result = ""

        for keyTag in self.keyTagList :

            if keyTag[ 0 ] in keytagString :

                result = result + keyTag[ 0 ]

        return result

    def forwardBtn( self ) : 

        diff = self.myData.maxPlot - self.myData.minPlot
        self.myData.minPlot = self.myData.minPlot + int( diff * 3 / 4 )
        self.myData.maxPlot = self.myData.minPlot + diff
        self.plot.set_xlim( left = self.myData.minPlot, right = self.myData.maxPlot )
        self.plot.set_ylim( bottom = -500, top = 500 )
        self.canvas.draw()
        
    def backwardBtn( self ) : 

        diff = self.myData.maxPlot - self.myData.minPlot
        self.myData.minPlot = self.myData.minPlot - int( diff * 3 / 4 )
        self.myData.maxPlot = self.myData.minPlot + diff
        self.plot.set_xlim( left = self.myData.minPlot, right = self.myData.maxPlot )
        self.plot.set_ylim( bottom = -500, top = 500 )
        self.canvas.draw()

    def saveBtn( self ) : 

        # save to npy file
        blinkSave = np.array( self.blinkList )
        saccadeSave = np.array( self.saccadeList )
        print( blinkSave.shape )
        save( './blinkTimeStamp.npy', blinkSave )
        print( saccadeSave.shape )
        save( './saccadeTimeStamp.npy', saccadeSave )


    def deleteSpanAt( self, xdata ) :

        self.deleteSpanBlinkAt( xdata )
        self.deleteSpanSaccadeAt( xdata )
        
    def deleteSpanBlinkAt( self, xdata ) :

        for i in range ( len( self.blinkList ) ) :

            if self.blinkList[ i ][ 0 ] < xdata and  xdata < self.blinkList[ i ][ 1 ] :

                span = self.blinkSpanList[ i ][ 0 ]
                span.remove()
                text = self.blinkSpanList[ i ][ 1 ]
                if text is not None :
                    text.remove()
                del self.blinkList[ i ]
                del self.blinkSpanList[ i ]

                self.canvas.draw()
                break

    def deleteSpanSaccadeAt( self, xdata ) :

        for i in range ( len( self.saccadeList ) ) :

            if self.saccadeList[ i ][ 0 ] < xdata and  xdata < self.saccadeList[ i ][ 1 ] :

                span = self.saccadeSpanList[ i ][ 0 ]
                span.remove()
                text = self.saccadeSpanList[ i ][ 1 ]
                if text is not None :
                    text.remove()
                del self.saccadeList[ i ]
                del self.saccadeSpanList[ i ]

                self.canvas.draw()
                break


    def testSpanBlinkUnderCursor( self, xdata ) :

        for i in range ( len( self.blinkList ) ) :

            if self.blinkList[ i ][ 0 ] < xdata and  xdata < self.blinkList[ i ][ 1 ] :

                return i

    def testSpanSaccadeUnderCursor( self, xdata ) :

        for i in range ( len( self.saccadeList ) ) :

            if self.saccadeList[ i ][ 0 ] < xdata and  xdata < self.saccadeList[ i ][ 1 ] :

                return i
        

    def plot( self, title ) :

        self.figure.clear()
        data = self.myData.getDataToPlot()
        ax = self.figure.add_subplot( 111, title = title)
        ax.set_xlim( left = self.myData.minPlot, right = self.myData.maxPlot )
        ax.set_ylim( bottom = -500, top = 500 )
        
        ax.plot( data[ :, 0 ], label="right" )
        ax.plot( data[ :, 1 ], label="left" )
        ax.plot( data[ :, 2 ], label="vertical" )
        ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
        # ax.plot(data)
        self.plot = ax
        self.canvas.draw()


    def spanFromBlinkList( self, blinkListLoaded ) :

        for i in range( len( blinkListLoaded ) ) :
            
            start = int( float( blinkListLoaded[ i ][ 0 ] ) )
            end = int( float( blinkListLoaded[ i ][ 1 ] ) )
            center = int( float( blinkListLoaded[ i ][ 2 ] ) )
            self.blinkList.append( [ start, end, center, blinkListLoaded[ i ][ 3 ] ] )
            self.blinkSpanList.append( [ self.plot.axvspan( start, end, color='green', alpha=0.2 ), self.plot.text( 0, -400, "" ) ] )
            self.writeInBlink( i, self.blinkList[ i ][ 2 ] - 100 )

    def spanFromSaccadeList( self, saccadeListLoaded ) :

        for i in range( len( saccadeListLoaded ) ) :
            
            start = int( float( saccadeListLoaded[ i ][ 0 ] ) )
            end = int( float( saccadeListLoaded[ i ][ 1 ] ) )
            center = int( float( saccadeListLoaded[ i ][ 2 ] ) )
            self.saccadeList.append( [ start, end, center, saccadeListLoaded[ i ][ 3 ] ] )
            self.saccadeSpanList.append( [ self.plot.axvspan( start, end, color='blue', alpha=0.2 ), self.plot.text( 0, -400, "" ) ] )
            self.writeInSaccade( i, self.saccadeList[ i ][ 2 ] - 100 )


   
# driver code
if __name__ == '__main__':
       
    # creating apyqt5 application
    app = QApplication(sys.argv)
   
    # creating a window object
    main = Window()
       
    # showing the window
    main.show()
   
    # loop
    sys.exit(app.exec_())