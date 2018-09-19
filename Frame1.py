#Boa:Frame:Frame1

import wx
from wx.lib.anchors import LayoutAnchors

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1PANEL1, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1STATICTEXT10, wxID_FRAME1STATICTEXT11, wxID_FRAME1STATICTEXT2, 
 wxID_FRAME1STATICTEXT3, wxID_FRAME1STATICTEXT4, wxID_FRAME1STATICTEXT5, 
 wxID_FRAME1STATICTEXT6, wxID_FRAME1STATICTEXT7, wxID_FRAME1STATICTEXT8, 
 wxID_FRAME1STATICTEXT9, wxID_FRAME1STATUSBAR1, wxID_FRAME1TEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(15)]

[wxID_FRAME1FILEMENUITEMSCLOSE, wxID_FRAME1FILEMENUITEMSEXIT, 
 wxID_FRAME1FILEMENUITEMSOPEN, wxID_FRAME1FILEMENUITEMSSAVE, 
 wxID_FRAME1FILEMENUITEMSSAVEAS, 
] = [wx.NewId() for _init_coll_FileMenu_Items in range(5)]

[wxID_FRAME1HELPMENUITEMSABOUT] = [wx.NewId() for _init_coll_HelpMenu_Items in range(1)]

class Frame1(wx.Frame):
    def _init_coll_gridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText1, 0, border=1, flag=0)
        parent.AddWindow(self.textCtrl1, 0, border=3, flag=0)
        parent.AddWindow(self.staticText2, 0, border=0, flag=0)
        parent.AddWindow(self.staticText3, 0, border=0, flag=0)
        parent.AddWindow(self.staticText4, 0, border=0, flag=0)
        parent.AddWindow(self.staticText5, 0, border=0, flag=0)
        parent.AddWindow(self.staticText6, 0, border=0, flag=0)
        parent.AddWindow(self.staticText7, 0, border=0, flag=0)
        parent.AddWindow(self.staticText8, 0, border=0, flag=0)
        parent.AddWindow(self.staticText9, 0, border=0, flag=0)
        parent.AddWindow(self.staticText10, 0, border=0, flag=0)
        parent.AddWindow(self.staticText11, 0, border=0, flag=0)

    def _init_coll_menuBar1_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.FileMenu, title='&File')
        parent.Append(menu=self.HelpMenu, title='&About')

    def _init_coll_HelpMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='Display General Information About pyMap',
              id=wxID_FRAME1HELPMENUITEMSABOUT, kind=wx.ITEM_NORMAL,
              text='&About')
        self.Bind(wx.EVT_MENU, self.OnHelpMenuItemsaboutMenu,
              id=wxID_FRAME1HELPMENUITEMSABOUT)

    def _init_coll_FileMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='Open a data file', id=wxID_FRAME1FILEMENUITEMSOPEN,
              kind=wx.ITEM_NORMAL, text='&Open')
        parent.Append(help='Save a data file', id=wxID_FRAME1FILEMENUITEMSSAVE,
              kind=wx.ITEM_NORMAL, text='&Save')
        parent.Append(help='Save the data file as...',
              id=wxID_FRAME1FILEMENUITEMSSAVEAS, kind=wx.ITEM_NORMAL,
              text='Save&As')
        parent.Append(help='Close the data file',
              id=wxID_FRAME1FILEMENUITEMSCLOSE, kind=wx.ITEM_NORMAL,
              text='&Close')
        parent.Append(help='Exit pyMap', id=wxID_FRAME1FILEMENUITEMSEXIT,
              kind=wx.ITEM_NORMAL, text='&Exit')
        self.Bind(wx.EVT_MENU, self.OnFileMenuItemsopenMenu,
              id=wxID_FRAME1FILEMENUITEMSOPEN)
        self.Bind(wx.EVT_MENU, self.OnFileMenuItemssaveMenu,
              id=wxID_FRAME1FILEMENUITEMSSAVE)
        self.Bind(wx.EVT_MENU, self.OnFileMenuItemssaveasMenu,
              id=wxID_FRAME1FILEMENUITEMSSAVEAS)
        self.Bind(wx.EVT_MENU, self.OnFileMenuItemscloseMenu,
              id=wxID_FRAME1FILEMENUITEMSCLOSE)
        self.Bind(wx.EVT_MENU, self.OnFileMenuItemsexitMenu,
              id=wxID_FRAME1FILEMENUITEMSEXIT)

    def _init_coll_statusBar1_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(1)

        parent.SetStatusText(number=0, text='Status')

        parent.SetStatusWidths([-1])

    def _init_sizers(self):
        # generated method, don't edit
        self.gridSizer1 = wx.GridSizer(cols=2, hgap=3, rows=6, vgap=3)

        self._init_coll_gridSizer1_Items(self.gridSizer1)

        self.panel1.SetSizer(self.gridSizer1)

    def _init_utils(self):
        # generated method, don't edit
        self.FileMenu = wx.Menu(title='File')

        self.HelpMenu = wx.Menu(title='Help')

        self.menuBar1 = wx.MenuBar()

        self._init_coll_FileMenu_Items(self.FileMenu)
        self._init_coll_HelpMenu_Items(self.HelpMenu)
        self._init_coll_menuBar1_Menus(self.menuBar1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='Frame1', parent=prnt,
              pos=wx.Point(560, 252), size=wx.Size(493, 279),
              style=wx.DEFAULT_FRAME_STYLE, title='pyMap')
        self._init_utils()
        self.SetClientSize(wx.Size(485, 245))
        self.SetMenuBar(self.menuBar1)
        self.SetBackgroundStyle(0)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1,
              name='statusBar1', parent=self, style=wx.RAISED_BORDER)
        self.statusBar1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(485, 203),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetAutoLayout(False)
        self.panel1.SetBackgroundStyle(0)
        self.panel1.Enable(False)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label='staticText4', name='staticText4', parent=self.panel1,
              pos=wx.Point(0, 68), size=wx.Size(73, 16), style=0)
        self.staticText4.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
        self.staticText4.SetMinSize(wx.Size(-1, -1))

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label='staticText5', name='staticText5', parent=self.panel1,
              pos=wx.Point(244, 68), size=wx.Size(73, 16), style=0)
        self.staticText5.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
        self.staticText5.SetMinSize(wx.Size(-1, -1))

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label='staticText2', name='staticText2', parent=self.panel1,
              pos=wx.Point(0, 34), size=wx.Size(73, 16), style=0)
        self.staticText2.SetMinSize(wx.Size(-1, -1))
        self.staticText2.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label='staticText3', name='staticText3', parent=self.panel1,
              pos=wx.Point(244, 34), size=wx.Size(73, 16), style=0)
        self.staticText3.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
        self.staticText3.SetMinSize(wx.Size(-1, -1))

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label='staticText1', name='staticText1', parent=self.panel1,
              pos=wx.Point(0, 0), size=wx.Size(73, 16), style=0)
        self.staticText1.SetAutoLayout(True)
        self.staticText1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
        self.staticText1.SetConstraints(LayoutAnchors(self.staticText1, True,
              True, True, True))
        self.staticText1.SetExtraStyle(1)
        self.staticText1.SetThemeEnabled(False)
        self.staticText1.SetMinSize(wx.Size(-1, -1))

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=wx.Point(244, 0), size=wx.Size(100, 21),
              style=0, value='textCtrl1')

        self.staticText6 = wx.StaticText(id=wxID_FRAME1STATICTEXT6,
              label='staticText6', name='staticText6', parent=self.panel1,
              pos=wx.Point(0, 102), size=wx.Size(54, 13), style=0)

        self.staticText7 = wx.StaticText(id=wxID_FRAME1STATICTEXT7,
              label='staticText7', name='staticText7', parent=self.panel1,
              pos=wx.Point(244, 102), size=wx.Size(54, 13), style=0)

        self.staticText8 = wx.StaticText(id=wxID_FRAME1STATICTEXT8,
              label='staticText8', name='staticText8', parent=self.panel1,
              pos=wx.Point(0, 136), size=wx.Size(56, 13), style=0)

        self.staticText9 = wx.StaticText(id=wxID_FRAME1STATICTEXT9,
              label='staticText9', name='staticText9', parent=self.panel1,
              pos=wx.Point(244, 136), size=wx.Size(54, 13), style=0)

        self.staticText10 = wx.StaticText(id=wxID_FRAME1STATICTEXT10,
              label='staticText10', name='staticText10', parent=self.panel1,
              pos=wx.Point(0, 170), size=wx.Size(60, 13), style=0)

        self.staticText11 = wx.StaticText(id=wxID_FRAME1STATICTEXT11,
              label='staticText11', name='staticText11', parent=self.panel1,
              pos=wx.Point(244, 170), size=wx.Size(60, 13), style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnFileMenuItemsopenMenu(self, event):
        event.Skip()

    def OnFileMenuItemssaveMenu(self, event):
        event.Skip()

    def OnFileMenuItemssaveasMenu(self, event):
        event.Skip()

    def OnFileMenuItemscloseMenu(self, event):
        event.Skip()

    def OnFileMenuItemsexitMenu(self, event):
        event.Skip()

    def OnHelpMenuItemsaboutMenu(self, event):
        event.Skip()
