#Boa:Frame:Frame5

import wx

def create(parent):
    return Frame5(parent)

[wxID_FRAME5] = [wx.NewId() for _init_ctrls in range(1)]

class Frame5(wx.Frame):
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, style=wx.DEFAULT_FRAME_STYLE, name='', parent=prnt, title='Frame5', pos=wx.Point(-1, -1), id=wxID_FRAME5, size=wx.Size(-1, -1))

    def __init__(self, parent):
        self._init_ctrls(parent)
