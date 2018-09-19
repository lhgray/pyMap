#!/usr/bin/env python
#Boa:App:BoaApp

import wx

import Frame5

modules ={'Frame5': [1, 'Main frame of Application', 'Frame5.py']}

class BoaApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.main = Frame5.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
