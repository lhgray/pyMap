#Boa:FramePanel:Panel1

import wx
import wx.grid
import wx.gizmos
from wx.lib.anchors import LayoutAnchors

[wxID_PANEL1, wxID_PANEL1TREELISTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class Panel1(wx.Panel):
    def _init_coll_treeListCtrl1_Columns(self, parent):
        # generated method, don't edit

        parent.AddColumn(text='Columns0')
        parent.AddColumn(text='Columns1')
        parent.AddColumn(text='Columns2')
        parent.AddColumn(text='Columns3')
        parent.AddColumn(text='Columns4')
        parent.AddColumn(text='Columns5')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt, pos=wx.Point(398, 269),
              size=wx.Size(810, 580), style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(802, 546))
        self.SetMaxSize(wx.Size(1280, 1024))
        self.SetAutoLayout(True)

        self.treeListCtrl1 = wx.gizmos.TreeListCtrl(id=wxID_PANEL1TREELISTCTRL1,
              name='treeListCtrl1', parent=self, pos=wx.Point(24, 20), size=wx.Size(744, 496),
              style=wx.THICK_FRAME | wx.ALWAYS_SHOW_SB | wx.HSCROLL | wx.VSCROLL | wx.TR_HAS_BUTTONS)
        self.treeListCtrl1.Center(wx.BOTH)
        self._init_coll_treeListCtrl1_Columns(self.treeListCtrl1)

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
