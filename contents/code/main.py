##########################################################################
#                                                                        #
# Copyright (C) 2010 Felix Rohrbach <fxrh@gmx.de>                        #
#                                                                        #
# This program is free software; you can redistribute it and/or          #
# modify it under the terms of the GNU General Public License            #
# as published by the Free Software Foundation; either version 3         #
# of the License, or (at your option) any later version.                 #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
########################################################################## 

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import aur_py2
import subprocess

class AurApplet(plasmascript.Applet):
    def __init__(self, parent):
        plasmascript.Applet.__init__(self, parent)
        
    def _getData(self):
        try:
            self.data = aur_py2.aurUpdates()
        except subprocess.CalledProcessError:
            self.errorMsg = "Could not run pacman"
            self.data = None
        except IOError:
            self.errorMsg = "Could not access the AUR"
            self.data = None
            
    def _writeData(self):
        print self.data
        string = ""
        for line in self.data[0]:
            string = string+line[0]+"\t"+line[1]+" -> "+line[2]+"\n"
        self.updateData.setText(string)
        string = ""
        for line in self.data[1]:
            string = string+line[0]+"\t"+line[1]+"\n"
        self.oodData.setText(string)
        string = ""
        for line in self.data[2]:
            string = string+line[0]+"\t"+line[1]+"\n"
        self.orphanData.setText(string)
        string = ""
        for line in self.data[3]:
            string = string+line[0]+"\t"+line[1]+"\n"
        self.notFoundData.setText(string)
        
        
    def _checkForNone(self):
        if self.data == None:
            self.updateInfo.setText("<h1>"+self.errorMsg+"</h1>")
        else:
            self.updateInfo.setText("<h1>Updates</h1>")
            self.oodInfo.setText("<h1>Out Of Date</h1>")
            self.orphanInfo.setText("<h1>Orphans</h1>")
            self.notFoundInfo.setText("<h1>Not Found</h1>")
            self._writeData()
        
    def init(self):
        self.updateInfo = Plasma.Label(self.applet)
        self.updateData = Plasma.Label(self.applet)
        self.oodInfo = Plasma.Label(self.applet)
        self.oodData = Plasma.Label(self.applet)
        self.orphanInfo = Plasma.Label(self.applet)
        self.orphanData = Plasma.Label(self.applet)
        self.notFoundInfo = Plasma.Label(self.applet)
        self.notFoundData = Plasma.Label(self.applet)
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
        self.layout.addItem(self.updateInfo)
        self.layout.addItem(self.updateData)
        self.layout.addItem(self.oodInfo)
        self.layout.addItem(self.oodData)
        self.layout.addItem(self.orphanInfo)
        self.layout.addItem(self.orphanData)
        self.layout.addItem(self.notFoundInfo)
        self.layout.addItem(self.notFoundData)
        
        self._getData()
        
        self._checkForNone()
        
        

def CreateApplet(parent):
    return AurApplet(parent)
