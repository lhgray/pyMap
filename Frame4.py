#Boa:Frame:Frame4

import wx
from wx.lib.anchors import LayoutAnchors
import Map_db_IO.WaypointTarget_IO as wpio
import os

##def create(parent, dbfile):
##    return Frame4(parent, dbfile)
def create(parent, dbfile, list_type, list):
    return Frame4(parent, dbfile, list_type, list)

[wxID_FRAME4, wxID_FRAME4LISTBOX1, wxID_FRAME4STATUSBAR1, 
] = [wx.NewId() for _init_ctrls in range(3)]

[wxID_FRAME4MENU1ITEMS0] = [wx.NewId() for _init_coll_menu1_Items in range(1)]

class Frame4(wx.Frame):
    def _init_coll_menuBar1_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menu1, title='Fields')

    def _init_coll_menu1_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='Select the Display Fields', id=wxID_FRAME4MENU1ITEMS0,
              kind=wx.ITEM_NORMAL, text='Select')

    def _init_coll_statusBar1_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(2)

        parent.SetStatusText(number=0, text='Fields0')
        parent.SetStatusText(number=1, text='Fields1')

        parent.SetStatusWidths([-1, 75])

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar1 = wx.MenuBar()

        self.menu1 = wx.Menu(title='Fields')

        self._init_coll_menuBar1_Menus(self.menuBar1)
        self._init_coll_menu1_Items(self.menu1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME4, name='', parent=prnt, pos=wx.Point(591, 348),
              size=wx.Size(255, 234),
              style=wx.FRAME_TOOL_WINDOW | wx.STAY_ON_TOP | wx.NO_FULL_REPAINT_ON_RESIZE | wx.DEFAULT_FRAME_STYLE,
              title='Frame4')
        self._init_utils()
        self.SetClientSize(wx.Size(247, 200))
        self.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.SetBackgroundStyle(1)
        self.SetBestFittingSize(wx.Size(255, 234))
        self.SetMinSize(wx.Size(191, 234))
        self.Show(True)
        self.SetMenuBar(self.menuBar1)
        self.SetStatusBarPane(-1)
        self.Enable(True)
        self.Bind(wx.EVT_ICONIZE, self.OnFrame4Iconize)
        self.Bind(wx.EVT_CLOSE, self.OnFrame4Close)

        self.listBox1 = wx.ListBox(choices=[], id=wxID_FRAME4LISTBOX1, name='listBox1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(247, 158),
              style=wx.LB_SORT | wx.LB_SINGLE | wx.CAPTION | wx.VSCROLL)
        self.listBox1.SetAutoLayout(True)
        self.listBox1.SetBackgroundColour(wx.Colour(255, 255, 128))
        self.listBox1.SetLabel('')
        self.listBox1.SetSelection(-1)
        self.listBox1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        self.listBox1.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListBox1ListboxDclick,
              id=wxID_FRAME4LISTBOX1)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME4STATUSBAR1, name='statusBar1', parent=self,
              style=0)
        self.statusBar1.SetAutoLayout(True)
        self.statusBar1.SetConstraints(LayoutAnchors(self.statusBar1, True, True, False, False))
        self.statusBar1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        self.statusBar1.SetFieldsCount(2)
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

    def __init__(self, parent, dbfile, list_type, list):
        self._init_ctrls(parent)
        # end of generated code
        self.dbfile = dbfile
        self.input_type = list_type
        self.list = list
        # place the database filename in the statusbar
        txt = '%s - %s' %(os.path.basename(self.dbfile), self.input_type)
        self.statusBar1.SetLabel(txt)
        # update the Title of the frame object
        txt = '%s - %s' %(self.input_type.upper(), 'Database')
        self.SetTitle(txt)
        if self.input_type == 'Sites':
            self.listBox1.SetBackgroundColour(wx.Colour(192, 255, 255)) # cyan
            self.SetStatusText(number=1, text='Sites')
        elif self.input_type == 'Plan':
            self.listBox1.SetBackgroundColour(wx.Colour(192, 255, 192)) # pale green
            self.SetStatusText(number=1, text='Plans')
        elif self.input_type == 'config':
            self.listBox1.SetBackgroundColour(wx.Colour(255, 192, 192)) # pale pink
            self.SetStatusText(number=1, text='Config')
        else:
            pass
        # sort the list
        self.list.sort()
        # print the list for testing
        print self.list
        # populate the listBox control
        self.listBox1.InsertItems(self.list, 0)
        
##        if self.input_type == 'Sites':
##            return(site_dlg)
##        elif self.input_type == 'Plan':
##            return(plan_dlg)
##        elif self.input_type == 'config':
##            return(config_dlg)
##        else:
##            return
        
    def __del__(self):
        print 'Frame4 Destructor'
        print 'Frame2.wxID_FRAME2DATAMENUITEMS0 =',
        print wxID_FRAME2DATAMENUITEMS0
##        Frame2.Check(Frame2.wxID_FRAME2DATAMENUITEMS0, check=False)
##        application.DataMenu.Check(id=Frame2.wxID_FRAME2DATAMENUITEMS0, check=False)
        Frame2.DataMenu.Check(id=Frame2.wxID_FRAME2DATAMENUITEMS0, check=False)
        print 'Frame4 Destructor'
        

    def OnListBox1ListboxDclick(self, event):
        print 'Here I am - (LeftDClick).'
        if self.input_type == 'Sites':
            Message = 'Item Selected from Site ListBox'
        elif self.input_type == 'Plan':
            Message = 'Item Selected from Plan ListBox'
        elif self.input_type == 'config':
            Message = 'Item Selected from Configuration ListBox'
        else:
            pass
        self.key = event.GetString()
        
        txt = ''.join([Message, '\n', self.key])
        txt1 = 'Selection Message'
        dlg = wx.MessageDialog(self, txt, txt1, wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def OnFrame4Close(self, event):
        print 'Closing Frame4'
##        print 'GetKey called on closing', Frame2.site_dlg.getkey()
##        Frame2.DataMenu.Check(id=Frame2.wxID_FRAME2DATAMENUITEMS0, check=False)
        self.Destroy()
        
    def OnFrame4Iconize(self, event):
        print 'Iconize'
        event.Skip()
        
    def getKey(self):
        print 'Frame4.getKey called'
        return self.key

        
