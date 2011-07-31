#!/usr/bin/env python

'''
svgPianoScale.py
Inkscape generator plugin for automatic creation schemes of musical scales and chords.

Copyright (C) 2011 Iljin Alexender <piroxiljin(a)gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

__version__ = "1.0"

import inkex, simplestyle, re, math
from datetime import *

notes =       ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
keys_color =  ('W', 'B', 'W',  'B', 'W', 'W',  'B',  'W', 'B',  'W', 'B',  'W')
keys =  {'C':'W', 'C#':'B',  'D':'W', 'D#':'B',  'E':'W', 'F':'W', 'F#':'B', 'G':'W', 'G#':'B',  'A':'W', 'A#':'B',  'B':'W'}
keys_numbers =  {'C':'0', 'C#':'0',  'D':'1', 'D#':'1',  'E':'2', 'F':'3', 'F#':'3', 'G':'4', 'G#':'4',  'A':'5', 'A#':'5',  'B':'6'}
keys_order =    {'C':'0', 'C#':'1',  'D':'2', 'D#':'3',  'E':'4', 'F':'5', 'F#':'6', 'G':'7', 'G#':'8',  'A':'9', 'A#':'10',  'B':'11'}

intervals = ("2212221", "2122212", "1222122", "2221221", "2212212", "2122122", "1221222")
#intervals = {1:"2212221", 2:"2122212", 3:"1222122", 4:"2221221", 5:"2212212", 6:"2122122", 7:"1221222"}

def keyNumberFromNote(note):
    note = note.upper()
    note = note.strip()
    octave = 1
    dies = '#' in note
    if dies :
        if (len(note) > 2) and note[2].isdigit():
                octave = int(note[2])
        note = note[0:2]
    else:
        if (len(note) > 1) and note[1].isdigit():
                octave = int(note[1])
        note = note[0]
    
    return int(keys_order[note])+(octave-1)*12

def noteFromKeyNumber(keyNumber):
    octave = floor(keyNumber / 12) + 1
    note = keyNumber % 12
    return notes[note]+str(octave)

def whiteKeyCountInRange(firstNote, lastNote):
    count = 0
    for key in range(firstNote, lastNote+1):
        if keys_color[key%12] == "W":
            count += 1
    return count

def colorFromKey(keyNumber):
    return keys_color[keyNumber%12]
    
class SVGPianoScale (inkex.Effect):
    black_key_width = inkex.unittouu('3.6 mm');
    white_key_width = inkex.unittouu('6 mm');
    black_key_height = inkex.unittouu('18 mm');
    white_key_height = inkex.unittouu('30 mm');
    doc_width = 0
    doc_height = 0
        
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--firstNote",
          action="store", type="string", default="C1",
          dest="firstNote")
        self.OptionParser.add_option("--lastNote",
          action="store", type="string", default="B2",
          dest="lastNote")
        self.OptionParser.add_option("--tab",
          action="store", type="string",
          dest="tab")
        self.OptionParser.add_option("--intervals",
          action="store", type="string",
          dest="intervals")
        self.OptionParser.add_option("--keynote",
          action="store", type="string",
          dest="keynote")
        self.OptionParser.add_option("--scale",
          action="store", type="int",
          dest="scale")
        self.OptionParser.add_option("--helpSheet",
          action="store", type="int",
          dest="helpSheet")
        
   
    def validate_options(self):
        return

    def calculate_size_and_positions(self):
        self.doc_width = inkex.unittouu(self.document.getroot().get('width'))
        self.doc_height = inkex.unittouu(self.document.getroot().get('height'))        
        self.black_key_width = inkex.unittouu('3.6 mm');
        self.white_key_width = inkex.unittouu('6 mm');
        self.black_key_height = inkex.unittouu('18 mm');
        self.white_key_height = inkex.unittouu('30 mm');

    def createBlackKey(self, parent, number):
        key_atts = {'x':str(self.white_key_width * number + self.white_key_width - self.black_key_width/2), 'y':'0.0', 'width':str(self.black_key_width), 'height':str(self.black_key_height),
            'ry':str(inkex.unittouu('0.7 mm')),
			'style':'fill:#000000;stroke:#000000;stroke-width:'+str(inkex.unittouu('0.1 mm'))+';stroke-opacity:1;fill-opacity:1' }
        white_key = inkex.etree.SubElement(parent, 'rect', key_atts)

    def createWhiteKey(self, parent, number):
        key_atts = {'x':str(self.white_key_width * number), 'y':'0.0', 'width':str(self.white_key_width), 'height':str(self.white_key_height),
            'ry':str(inkex.unittouu('0.7 mm')),
			'style':'fill:#ffffff;stroke:#000000;stroke-width:'+str(inkex.unittouu('0.25 mm'))+';stroke-opacity:1;fill-opacity:1' }
        white_key = inkex.etree.SubElement(parent, 'rect', key_atts)

    def createKeyByNumber(self, parent, keyNumber):
        octave = math.floor(keyNumber / 12) + 1
        note = keyNumber % 12
        key =  int(keys_numbers[notes[note]])
        if keys_color[note] == "W":
            self.createWhiteKey(parent, key+7*(octave-1))
        else:
            self.createBlackKey(parent, key+7*(octave-1))
        
    def createKey(self, parent, key):
        key = key.upper()
        key = key.strip()
        octave = 1
        dies = '#' in key
        if dies :
            if (len(key) > 2):
                if  key[2].isdigit():
                    octave = int(key[2])
            note = key[0:2]
        else:
            inkex.debug("len(key) = " + str(len(key)))
            if (len(key) > 1) :
                if key[1].isdigit():
                    octave = int(key[1])
            note = key[0]
            
        # if key in notes:
            # inkex.debug('key is a note (' + note + ')')
        # else:
            # inkex.debug('key is not a note (' + note + ')')
        # inkex.debug("note = " + note)
        # inkex.debug("keys[note]  = " + keys[note] )
        if keys[note] == "W":
            self.createWhiteKey(parent, int(keys_numbers[note])+7*(octave-1))
        else:
            self.createBlackKey(parent, int(keys_numbers[note])+7*(octave-1))
       
    def createKeyInRange(self, parent, firstKeyNum, lastKeyNum):
        for key in range(firstKeyNum, lastKeyNum+1):
            if keys_color[key % 12] == 'W':
                self.createKeyByNumber(parent, key)
        for key in range(firstKeyNum, lastKeyNum+1):
            if keys_color[key % 12] == 'B':
                self.createKeyByNumber(parent, key)
            
    def createPiano(self, parent):
        firstKeyNumber = keyNumberFromNote(self.options.firstNote)
        lastKeyNumber = keyNumberFromNote(self.options.lastNote)
        self.createKeyInRange(parent, firstKeyNumber, lastKeyNumber)

        rectBump = (self.white_key_width - self.black_key_width/2)
        rectBump = inkex.unittouu('1 mm')
        rect_x1 = self.white_key_width * (whiteKeyCountInRange(0, firstKeyNumber)-1)- rectBump
        rect_y1 = inkex.unittouu('-3 mm')
        rect_width = self.white_key_width * (whiteKeyCountInRange(firstKeyNumber, lastKeyNumber)) + rectBump*2
        rect_height = inkex.unittouu('4 mm')
        rect_atts = {'x':str(rect_x1), 
                    'y':str(rect_y1), 
                    'width':str(rect_width), 
                    'height':str(rect_height),
            'ry':str(0),
			'style':'fill:#ffffff;stroke:none;fill-opacity:1' }
        rect = inkex.etree.SubElement(parent, 'rect', rect_atts)
        path_atts = {'style':'fill:#ffffff;stroke:#000000;stroke-width:'+str(inkex.unittouu('0.25 mm'))+';stroke-opacity:1',
            'd':'m '+str(rect_x1)+", "+str(rect_y1)+ 
                 " l "+str(0)+", "+str(rect_height)+
                 " "  +str(rect_width)+", "+ str(0) +
                 " "+str(0)+", "+str(-rect_height)}
        path = inkex.etree.SubElement(parent, 'path', path_atts)
        
    def createMarkerAt(self, parent, x, y, radius, markerText):
        markerGroup = inkex.etree.SubElement(parent, 'g')
    
        ellipce_atts = {
            inkex.addNS('cx','sodipodi'):str(x),
            inkex.addNS('cy','sodipodi'):str(y),
            inkex.addNS('rx','sodipodi'):str(radius),
            inkex.addNS('ry','sodipodi'):str(radius),
            inkex.addNS('type','sodipodi'):'arc',
            'd':'m '+str(x+radius)+','+str(y)+' a '+
                    str(x)+','+str(y)+'  0 1 1 ' + str(-radius*2)+',0 '+ 
                    str(x)+','+str(y)+'  0 1 1 ' + str(radius*2)+',0 z',
            'style':'fill:#b3b3b3;stroke:#000000;stroke-width:'+str(inkex.unittouu('0.125 mm'))+';stroke-opacity:1;fill-opacity:1' }
        ellipse = inkex.etree.SubElement(markerGroup, 'path', ellipce_atts)
        
        textstyle = { 'font-size': '11 px',
          'font-family': 'arial',
          'text-anchor': 'middle',
          'text-align': 'center',
          'fill': '#000000'
          }
        text_atts = { 'style':simplestyle.formatStyle(textstyle),
                    'x': str( x ),
                    'y': str( y + radius*0.5) }
        text = inkex.etree.SubElement(markerGroup, 'text', text_atts)
        text.text = str(markerText)
        
    def createMarkerOnWhite(self, parent, whiteNumber, markerText):
        radius = self.white_key_width * 0.42
        center_x = self.white_key_width * (whiteNumber + 0.5)
        center_y = self.white_key_height * 0.92 - radius 
        self.createMarkerAt(parent, center_x, center_y, radius, markerText)
        return

    def createMarkerOnBlack(self, parent, whiteNumber, markerText):
        radius = self.white_key_width * 0.42
        center_x = self.white_key_width * (whiteNumber + 1)
        center_y = self.black_key_height * 0.92 - radius 
        self.createMarkerAt(parent, center_x, center_y, radius, markerText)
        return
        
    def createMarkers(self, parent, keyNumberList, markerTextList):
        current=0
        for key in keyNumberList:
            octave = math.floor(key/12)
            if colorFromKey(key) == "W":
                self.createMarkerOnWhite(parent, int(keys_numbers[notes[key%12]])+(octave)*7, markerTextList[current])
            else:
                self.createMarkerOnBlack(parent, int(keys_numbers[notes[key%12]])+(octave)*7, markerTextList[current])
            current += 1;
        return
        
    def createMarkersFromIntervals(self, parent, intervals):
        intervalSumm = 0
        for i in intervals:
            intervalSumm += int(i)
        if intervalSumm != 12:
            inkex.debug("Warning! Scale have not 12 half-tones")
            
        firstKeyNum = keyNumberFromNote(self.options.firstNote)
        lastKeyNum  = keyNumberFromNote(self.options.lastNote)

        markedKeys = ()
        markerText = ()
        if keyNumberFromNote(self.options.keynote) in range(firstKeyNum, lastKeyNum+1):
            currentKey = keyNumberFromNote(self.options.keynote)
            markedKeys = (currentKey,)
            markerText = ('1',)
            currentInterval = 0
            for key in range(keyNumberFromNote(self.options.keynote), lastKeyNum+1):
                if key-currentKey == int(intervals[currentInterval]):
                    markedKeys += (key,)
                    currentInterval += 1
                    markerText += (str(currentInterval+1),)
                    if currentInterval == len(intervals):
                        currentInterval = 0
                    currentKey = key
                    
            currentKey = keyNumberFromNote(self.options.keynote)
            currentInterval = len(intervals)-1
            for key in range(keyNumberFromNote(self.options.keynote), firstKeyNum-1, -1):
                if currentKey - key == int(intervals[currentInterval]):
                    markedKeys += (key,)
                    markerText += (str(currentInterval+1),)
                    currentInterval -= 1
                    if currentInterval == -1:
                        currentInterval = len(intervals)-1
                    currentKey = key
                    
                    
        self.createMarkers(parent, markedKeys, markerText)
    
    def createHelpSheetIonianScale(self, parent):
        textstyle = { 'font-size': '64px',
          'font-family': 'arial',
          'text-anchor': 'middle',
          'text-align': 'center',
          'fill': '#000000'
          }
        text_atts = { 'style':simplestyle.formatStyle(textstyle),
                    'x': str( self.doc_width/2 ),
                    'y': str( inkex.unittouu('18 mm') ) }
        text = inkex.etree.SubElement(parent, 'text', text_atts)
        text.text = str("Ionian scale")
        for i in range(0, 12):
            self.options.keynote = notes[i]
            if keys_color[i] == "W":
                t = 'translate(' + str( self.doc_width/2 ) + ','\
                    + str( self.doc_height-self.white_key_height*1.5-(self.white_key_height+inkex.unittouu('7 mm')) * int(keys_numbers[self.options.keynote]) ) + ')'
            else:
                t = 'translate(' + str( inkex.unittouu('7 mm') ) + ',' \
                    + str( self.doc_height-self.white_key_height*1.5-(self.white_key_height+inkex.unittouu('7 mm')) * int(keys_numbers[self.options.keynote])-self.white_key_height*0.5 ) + ')'
            group = inkex.etree.SubElement(parent, 'g', { 'transform':t})
            self.createPiano(group)
            self.createMarkersFromIntervals(group, intervals[self.options.helpSheet-1])

    def createHelpSheet(self, parent, helpSheetNumber):
        self.createHelpSheetIonianScale(parent)
        return
        
    def effect(self):
        self.validate_options()
        self.calculate_size_and_positions()
        
        
        parent = self.document.getroot()

        if str(self.options.tab) == '"scale"':
            t = 'translate(' + str( self.view_center[0] ) + ',' + str( self.view_center[1] ) + ')'
            group = inkex.etree.SubElement(parent, 'g', { 'transform':t})
            self.createPiano(group)
            self.createMarkersFromIntervals(group, intervals[self.options.scale-1])
        elif str(self.options.tab) == '"helpSheet"':
            t = 'translate(' + str( inkex.unittouu('5 mm') ) + ',' + str( inkex.unittouu('5 mm') ) + ')'
            group = inkex.etree.SubElement(parent, 'g', { 'transform':t})
            self.createHelpSheet(group, self.options.helpSheet)
        else:
            t = 'translate(' + str( self.view_center[0] ) + ',' + str( self.view_center[1] ) + ')'
            group = inkex.etree.SubElement(parent, 'g', { 'transform':t})
            self.createPiano(group)
            self.createMarkersFromIntervals(group, self.options.intervals)

if __name__ == '__main__':   #pragma: no cover
    e = SVGPianoScale()
    e.affect()
