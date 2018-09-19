#!/usr/bin/env python
#Boa:App:BoaApp

##comment added to test TortoiseSVN in pyMap/branches/task1
## 2nd comment added to test TortoiseSVn in pyMap/trunk

import os, sys      # added 4Aug2005

modules ={'Ephemerus': [0,
               'Solar Ephemerus Calculator by LHGray',
               'Ephemerus/Ephemerus.py'],
 'Frame2': [1, 'Main frame of Application', 'Frame2.py'],
 'Frame3': [0, 'Database TreeList Display Frame', 'Frame3.py'],
 'Frame4': [0, 'Database ListBox Display Frame', 'Frame4.py'],
 'MiniFrame1': [0, 'Database Selection Button & CheckBox', 'MiniFrame1.py'],
 'RouteGenerator': [0, '', 'Map_db_IO/RouteGenerator.py'],
 'WaypointTarget_IO': [0, '', 'Map_db_IO/WaypointTarget_IO.py'],
 'geodesy': [0, '', 'Geodesy/geodesy.py'],
 'plot_tools': [0, '', 'plot_tools.py']}
    
import wx
import Frame2

class BoaApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.main = Frame2.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():

    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
