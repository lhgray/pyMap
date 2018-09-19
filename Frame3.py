#Boa:Frame:Frame3

import wx
from wx.lib.anchors import LayoutAnchors
import wx.gizmos
##import wx.images
import Map_db_IO.WaypointTarget_IO as wpio


##def create(parent, dbfile): # 2nd parameter dbfile passes the database filename
##    return Frame3(parent, dbfile)

def create(parent, dbfile, list_type): # 2nd parameter dbfile passes the database filename
    return Frame3(parent, dbfile, list_type)

[wxID_FRAME3, wxID_FRAME3STATUSBAR1, wxID_FRAME3TREELISTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(3)]

[wxID_FRAME3MENU1ITEMS0, wxID_FRAME3MENU1ITEMS1, wxID_FRAME3MENU1ITEMS2, 
] = [wx.NewId() for _init_coll_menu1_Items in range(3)]

class Frame3(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME3, name='', parent=prnt, pos=wx.Point(438, 326),
              size=wx.Size(686, 372), style=wx.DEFAULT_FRAME_STYLE,
              title='Target / Plan Database')
        self.SetClientSize(wx.Size(678, 338))
        self.SetBackgroundColour(wx.Colour(128, 128, 128))
        self.SetBackgroundStyle(0)
        self.SetCursor(wx.CROSS_CURSOR)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME3STATUSBAR1, name='statusBar1', parent=self,
              style=0)
        self.statusBar1.SetLabel('Status')
        self.statusBar1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.SetStatusBar(self.statusBar1)

        self.treeListCtrl1 = wx.gizmos.TreeListCtrl(id=wxID_FRAME3TREELISTCTRL1,
              name='treeListCtrl1', parent=self, pos=wx.Point(0, 0), size=wx.Size(678, 315),
              style=wx.DOUBLE_BORDER | wx.TR_SINGLE | wx.THICK_FRAME | wx.TR_HAS_BUTTONS | wx.HSCROLL | wx.VSCROLL | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HIDE_ROOT| wx.TR_NO_LINES)
        self.treeListCtrl1.SetAutoLayout(False)
        self.treeListCtrl1.SetMainColumn(0)
        self.treeListCtrl1.SetForegroundColour(wx.Colour(0, 0, 0))
        self.treeListCtrl1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,False, 'Tahoma'))
        self.treeListCtrl1.SetBackgroundColour(wx.Colour(159, 255, 159))
        self.treeListCtrl1.SetBackgroundStyle(1)
        self.treeListCtrl1.Enable(True)
        self.treeListCtrl1.SetIndent(18)
        self.treeListCtrl1.SetLineSpacing(2)
        self.treeListCtrl1.SetCursor(wx.STANDARD_CURSOR)
        self.treeListCtrl1.Show(True)
        self.treeListCtrl1.Bind(wx.EVT_LEFT_UP, self.OnTreeListCtrl1LeftUp)
        self.treeListCtrl1.Bind(wx.EVT_RIGHT_UP, self.OnTreeListCtrl1RightUp)
        self.treeListCtrl1.Bind(wx.EVT_TREE_GET_INFO, self.OnTreeListCtrl1TreeGetInfo,
              id=wxID_FRAME3TREELISTCTRL1)
        self.treeListCtrl1.Bind(wx.EVT_TREE_ITEM_ACTIVATED,
              self.OnTreeListCtrl1TreeItemActivated, id=wxID_FRAME3TREELISTCTRL1)
        self.treeListCtrl1.Bind(wx.EVT_TREE_ITEM_COLLAPSED,
              self.OnTreeListCtrl1TreeItemCollapsed, id=wxID_FRAME3TREELISTCTRL1)
        self.treeListCtrl1.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnTreeListCtrl1TreeItemExpanded,
              id=wxID_FRAME3TREELISTCTRL1)

    def __init__(self, parent, dbfile, list_type):
        self._init_ctrls(parent)
        self.dbfile = dbfile
        self.input_type = list_type
                        
##        self.treeListCtrl1.SetItemImage(self.root, fldridx, which = wx.TreeItemIcon_Normal)
##        self.treeListCtrl1.SetItemImage(self.root, fldropenidx, which = wx.TreeItemIcon_Expanded)

        temp_db = wpio.ReadDatabase(self.dbfile)
        # code here to determine the type of database file
        self.input_type = temp_db['Captions'][0][0].strip()
        # place the database filename in the statusbar
        txt = '%s - %s' %(self.dbfile, self.input_type)
        self.statusBar1.SetLabel(txt)
##        self.Frame3.title = self.input_type
        if self.input_type == 'Sites':
            input_db = wpio.generic2site_db(temp_db)
            self.treeListCtrl1.SetBackgroundColour(wx.Colour(192, 255, 255)) # cyan
        elif self.input_type == 'Plan':
            input_db = wpio.generic2plan_db(temp_db)
            self.treeListCtrl1.SetBackgroundColour(wx.Colour(192, 255, 192)) # pale green
        elif self.input_type == 'config':
            input_db = wpio.generic2sensor_db(temp_db)
            self.treeListCtrl1.SetBackgroundColour(wx.Colour(255, 192, 192)) # pale pink
        else:
            pass
        
        # create treeList columns using Caption fields for titles
        for x in range(1,len(input_db['Captions'][0])):
            txt = '%s' %(input_db['Captions'][0][x])
            self.treeListCtrl1.AddColumn(text=txt)
            self.treeListCtrl1.SetColumnWidth(x, 250)

        # test case with a real input file
        txt = '%s' %input_db['Captions'][0][1]
        self.root = self.treeListCtrl1.AddRoot(txt)
        for key in input_db.keys():
            if key == 'Captions':continue # bypass the caption fields 
            txt = '%s' %key
            level_0 = self.treeListCtrl1.AppendItem(self.root, txt)
            for x in range(len(input_db[key])):
                txt = '%s' %x
                level_1 = self.treeListCtrl1.AppendItem(level_0, txt)
                for y in range(len(input_db[key][x])):
                    field = input_db[key][x][y]
                    '''
                    The following section ensures that field values that are floats
                    are displayed as a string representation of a float in the
                    treeCtrlList, integers are displayed as integers and other
                    types are displayed as strings.
                    '''
                    try:
                        if round(field,0)==field:
                            # field is an integer
                            txt = '%d' %field
                        else:
                            # field is a float
                            txt = '%6.2f' %field
                    except (TypeError, ValueError):
                        txt = '%s' %repr(field)
                    self.treeListCtrl1.SetItemText(level_1, txt, y+1) 
                                   
        self.treeListCtrl1.Expand(self.root)

    def OnTreeListCtrl1TreeItemActivated(self, event):
        item = event.GetItem()
##        field = self.treeListCtrl1.GetItemText(item,9)
##        if field == '':
##            print 'Null',
##        else:
##            print field,
##        field = self.treeListCtrl1.GetItemText(item,15)
##        print field
        field_num = 0
        field = 0
        while field != '':
            field = self.treeListCtrl1.GetItemText(item,field_num)
            print field,
            field_num += 1
        print
        
        if self.input_type == 'Sites':
            Message = 'Item Selected from Site TreeList'
        elif self.input_type == 'Plan':
            Message = 'Item Selected from Plan TreeList'
        elif self.input_type == 'config':
            Message = 'Item Selected from Configuration TreeList'
        else:
            pass 
        txt = ''.join(['Message from Hell\n', Message])
        txt1 = 'Caption from Hell'
        dlg = wx.MessageDialog(self, txt, txt1, wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
        
    def OnTreeListCtrl1RightUp(self, event):
        print 'Here I am.'
        pos = event.GetPosition()
        item, flags, col = self.treeListCtrl1.HitTest(pos)
        if item:
            msg = ('Flags: %s, Col:%s, Text: %s' %
                           (flags, col, self.treeListCtrl1.GetItemText(item, col)))
        txt1 = 'Caption'
        dlg = MessageDialog(self, msg, txt1, wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
            
    def OnTreeListCtrl1RightDclick(self, event):
        print 'Here I am - (RightDClick).'
        pos = event.GetPosition()
        item, flags, col = self.treeListCtrl1.HitTest(pos)
        if item:
            msg = ('Flags: %s, Col:%s, Text: %s' %
                           (flags, col, self.treeListCtrl1.GetItemText(item, col)))
        txt1 = 'Caption'
        dlg = MessageDialog(self, msg, txt1, wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def OnTreeListCtrl1TreeItemExpanded(self, event):
        print 'Item Expanded'
        txt = 'Item Expanded'
        txt1 = 'Expanded Caption'
        dlg = wx.MessageDialog(self, txt, txt1, wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def OnTreeListCtrl1TreeItemCollapsed(self, event):
        print 'Item Collapsed'
        txt = 'Item Collapsed'
        txt1 = 'Collapsed Caption'
        dlg = wx.MessageDialog(self, txt, txt1, wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def OnTreeListCtrl1LeftDclick(self, event):
        print 'Here I am - (LeftDClick).'
        if self.input_type == 'Sites':
            Message = 'Item Selected from Site TreeList'
        elif self.input_type == 'Plan':
            Message = 'Item Selected from Plan TreeList'
        elif self.input_type == 'config':
            Message = 'Item Selected from Configuration TreeList'
        else:
            pass 
        txt = ''.join(['Message from Hell\n', Message])
        txt1 = 'Caption from Hell'
        dlg = wx.MessageDialog(self, txt, txt1, wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def OnTreeListCtrl1LeftUp(self, event):
        print 'Left Mouse Button Up'
        pos = event.GetPosition()
        item, flags, col = self.treeListCtrl1.HitTest(pos)
        print item, flags, col

    def OnTreeListCtrl1TreeSelChanged(self, event):
        print 'New Selection'
##        pos = event.GetPosition()
##        item, flags, col = self.treeListCtrl1.HitTest(pos)
##        if item:
##            msg = ('Flags: %s, Col:%s, Text: %s' %
##                           (flags, col, self.treeListCtrl1.GetItemText(item, col)))
##        txt1 = 'Caption'
##        dlg = MessageDialog(self, msg, txt1, wx.OK | wx.ICON_INFORMATION)
##        try:
##            dlg.ShowModal()
##        finally:
##            dlg.Destroy()

    def OnTreeListCtrl1TreeGetInfo(self, event):
        pos = event.GetPosition()
        item, flags, col = self.treeListCtrl1.HitTest(pos)
        print item, flags, col
        if item:
            msg = ('Flags: %s, Col:%s, Text: %s' %
                           (flags, col, self.treeListCtrl1.GetItemText(item, col)))
        txt1 = 'Caption'
        dlg = MessageDialog(self, msg, txt1, wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

