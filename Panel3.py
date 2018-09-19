#Boa:FramePanel:Panel3

import wx
import wx.grid

[wxID_PANEL3, wxID_PANEL3GRID1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class Panel3(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL3, name='', parent=prnt, pos=wx.Point(454, 338),
              size=wx.Size(365, 269), style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(357, 235))

        self.grid1 = wx.grid.Grid(id=wxID_PANEL3GRID1, name='grid1', parent=self,
              pos=wx.Point(16, 16), size=wx.Size(304, 200),
              style=wx.STATIC_BORDER | wx.ALWAYS_SHOW_SB | wx.HSCROLL | wx.VSCROLL)

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
