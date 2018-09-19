#Boa:Dialog:Dialog1

import wx
import wx.gizmos
from wx.lib.anchors import LayoutAnchors

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1TREELISTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class Dialog1(wx.Dialog):
    def _init_coll_treeListCtrl1_Columns(self, parent):
        # generated method, don't edit

        parent.AddColumn(text='Site')
        parent.AddColumn(text='Datum')
        parent.AddColumn(text='Northing')
        parent.AddColumn(text='Easting')
        parent.AddColumn(text='Zone')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(451, 322), size=wx.Size(432, 300),
              style=wx.DEFAULT_DIALOG_STYLE | wx.DIALOG_MODAL,
              title='Database Listing')
        self.SetClientSize(wx.Size(424, 266))
        self.Show(True)
        self.SetExtraStyle(0)
        self.SetAutoLayout(True)

        self.treeListCtrl1 = wx.gizmos.TreeListCtrl(id=wxID_DIALOG1TREELISTCTRL1,
              name='treeListCtrl1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(384, 208),
              style=wx.HSCROLL | wx.VSCROLL | wx.TR_HAS_BUTTONS)
        self.treeListCtrl1.SetAutoLayout(True)
        self.treeListCtrl1.SetMainColumn(2)
        self._init_coll_treeListCtrl1_Columns(self.treeListCtrl1)

    def __init__(self, parent):
        self._init_ctrls(parent)
        # My method for filling the tree list

    def OnDialog1InitDialog(self, event):
        event.Skip()
        
