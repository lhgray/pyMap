#Boa:FramePanel:Panel2

import wx
from wx.lib.anchors import LayoutAnchors

[wxID_PANEL2, wxID_PANEL2SCROLLEDWINDOW1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class Panel2(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL2, name='', parent=prnt, pos=wx.Point(666, 439),
              size=wx.Size(353, 218), style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(345, 184))

        self.scrolledWindow1 = wx.ScrolledWindow(id=wxID_PANEL2SCROLLEDWINDOW1,
              name='scrolledWindow1', parent=self, pos=wx.Point(16, 24), size=wx.Size(200, 100),
              style=wx.STATIC_BORDER | wx.ALWAYS_SHOW_SB | wx.HSCROLL | wx.VSCROLL)
        self.scrolledWindow1.SetConstraints(LayoutAnchors(self.scrolledWindow1, True, True,
              False, False))

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
