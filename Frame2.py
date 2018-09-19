#Boa:Frame:Frame2

import wx
import wx.lib.buttons
from wx.lib.anchors import LayoutAnchors
import wx.gizmos
import Frame3   # for TreeListCtrl Display
import Frame4   # for ListBox Display
import MiniFrame1   # for CheckButton & CheckBox Dialog

import Map_db_IO.WaypointTarget_IO as wpio
import Map_db_IO.RouteGenerator as rg

Buffered = 1

def create(parent):
    return Frame2(parent)

[wxID_FRAME2, wxID_FRAME2BUTTON1, wxID_FRAME2BUTTON2, wxID_FRAME2BUTTON3, wxID_FRAME2BUTTON4, 
 wxID_FRAME2BUTTON5, wxID_FRAME2BUTTON6, wxID_FRAME2BUTTON7, wxID_FRAME2BUTTON8, 
 wxID_FRAME2SCROLLEDWINDOW1, wxID_FRAME2STATUSBAR1, 
] = [wx.NewId() for _init_ctrls in range(11)]

[wxID_FRAME2FILEMENUDATA, wxID_FRAME2FILEMENUITEMS0, wxID_FRAME2FILEMENUITEMS1, 
 wxID_FRAME2FILEMENUITEMS2, wxID_FRAME2FILEMENUITEMS3, wxID_FRAME2FILEMENUITEMS4, 
] = [wx.NewId() for _init_coll_FileMenu_Items in range(6)]

[wxID_FRAME2TESTMENUITEMS0, wxID_FRAME2TESTMENUITEMS1, 
] = [wx.NewId() for _init_coll_TestMenu_Items in range(2)]

[wxID_FRAME2DATAMENUITEMS0, wxID_FRAME2DATAMENUITEMS1, wxID_FRAME2DATAMENUITEMS2, 
 wxID_FRAME2DATAMENUITEMS4, 
] = [wx.NewId() for _init_coll_DataMenu_Items in range(4)]

def check_DB_selections(self):
    print self.site_dlg.input_db[self.site_dlg.getKey()]
    print self.plan_dlg.input_db[self.plan_dlg.getKey()]
    print self.config_dlg.input_db[self.config_dlg.getKey()]
    return
    
[wxID_FRAME2HELPMENUITEMS0] = [wx.NewId() for _init_coll_HelpMenu_Items in range(1)]

class Frame2(wx.Frame):
    def _init_coll_gridBagSizer1_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(7)
        parent.AddGrowableCol(1)

    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.button5, (0, 0), border=5,
              flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, span=(1, 1))
        parent.AddWindow(self.button6, (1, 0), border=5,
              flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, span=(1, 1))
        parent.AddWindow(self.button7, (2, 0), border=5,
              flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, span=(1, 1))
        parent.AddWindow(self.button8, (3, 0), border=5,
              flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, span=(1, 1))
        parent.AddWindow(self.button1, (4, 0), border=5,
              flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, span=(1, 1))
        parent.AddWindow(self.button2, (5, 0), border=5,
              flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, span=(1, 1))
        parent.AddWindow(self.button3, (6, 0), border=5,
              flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, span=(1, 1))
        parent.AddWindow(self.button4, (7, 0), border=5, flag=wx.ALIGN_TOP | wx.TOP | wx.LEFT,
              span=(1, 1))
        parent.AddWindow(self.scrolledWindow1, (0, 1), border=5, flag=wx.GROW | wx.ALL, span=(8,
              1))

    def _init_coll_menuBar1_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.FileMenu, title='File')
        parent.Append(menu=self.TestMenu, title='Test')
        parent.Append(menu=self.HelpMenu, title='Help')

    def _init_coll_imageList1_Images(self, parent):
        # generated method, don't edit

        parent.Add(bitmap=wx.Bitmap('C:/Python24/Lib/site-packages/boa-constructor/Images/ZOA/Folder.png',
              wx.BITMAP_TYPE_PNG), mask=wx.NullBitmap)
        parent.Add(bitmap=wx.Bitmap('C:/Python24/Lib/site-packages/boa-constructor/Images/ZOA/FolderOpen.png',
              wx.BITMAP_TYPE_PNG), mask=wx.NullBitmap)
        parent.Add(bitmap=wx.Bitmap('C:/Python24/Lib/site-packages/boa-constructor/Images/ZOA/File.png',
              wx.BITMAP_TYPE_PNG), mask=wx.NullBitmap)
        parent.Add(bitmap=wx.Bitmap('C:/Python24/Lib/site-packages/boa-constructor/Images/CvsPics/Commit.png',
              wx.BITMAP_TYPE_PNG), mask=wx.NullBitmap)

    def _init_coll_DataMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='Retrieve Target Database', id=wxID_FRAME2DATAMENUITEMS0,
              kind=wx.ITEM_CHECK, text='&Target Database')
        parent.Append(help='Retrieve Planning Database', id=wxID_FRAME2DATAMENUITEMS1,
              kind=wx.ITEM_CHECK, text='&Planning Database')
        parent.Append(help='Retrieve Sensor Database', id=wxID_FRAME2DATAMENUITEMS2,
              kind=wx.ITEM_CHECK, text='&Sensor Database')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_FRAME2DATAMENUITEMS4, kind=wx.ITEM_NORMAL,
              text='&Generate Routing')
        self.Bind(wx.EVT_MENU, self.OnDataMenuItems0Menu, id=wxID_FRAME2DATAMENUITEMS0)
        self.Bind(wx.EVT_MENU, self.OnDataMenuItems1Menu, id=wxID_FRAME2DATAMENUITEMS1)
        self.Bind(wx.EVT_MENU, self.OnDataMenuItems2Menu, id=wxID_FRAME2DATAMENUITEMS2)
        self.Bind(wx.EVT_MENU, self.OnDataMenuItems4Menu, id=wxID_FRAME2DATAMENUITEMS4)

    def _init_coll_HelpMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='Display general information about pyMap',
              id=wxID_FRAME2HELPMENUITEMS0, kind=wx.ITEM_NORMAL, text='&About')
        self.Bind(wx.EVT_MENU, self.OnHelpMenuItems0Menu, id=wxID_FRAME2HELPMENUITEMS0)

    def _init_coll_FileMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='Open a file', id=wxID_FRAME2FILEMENUITEMS0, kind=wx.ITEM_NORMAL,
              text='&Open')
        parent.Append(help='Save the current file', id=wxID_FRAME2FILEMENUITEMS1,
              kind=wx.ITEM_NORMAL, text='&Save')
        parent.Append(help='Save the current file as...', id=wxID_FRAME2FILEMENUITEMS2,
              kind=wx.ITEM_NORMAL, text='Save &As')
        parent.AppendMenu(help='Open Database Retrieval Menus', id=wxID_FRAME2FILEMENUDATA,
              submenu=self.DataMenu, text='&Data')
        parent.Append(help='Close the current file', id=wxID_FRAME2FILEMENUITEMS3,
              kind=wx.ITEM_NORMAL, text='&Close')
        parent.AppendSeparator()
        parent.Append(help='Exit pyMap', id=wxID_FRAME2FILEMENUITEMS4, kind=wx.ITEM_NORMAL,
              text='&Exit')
        self.Bind(wx.EVT_MENU, self.OnFileMenuItems1Menu, id=wxID_FRAME2FILEMENUITEMS1)
        self.Bind(wx.EVT_MENU, self.OnFileMenuItems0Menu, id=wxID_FRAME2FILEMENUITEMS0)
        self.Bind(wx.EVT_MENU, self.OnFileMenuItems2Menu, id=wxID_FRAME2FILEMENUITEMS2)
        self.Bind(wx.EVT_MENU, self.OnFileMenuItems3Menu, id=wxID_FRAME2FILEMENUITEMS3)
        self.Bind(wx.EVT_MENU, self.OnFileMenuItems4Menu, id=wxID_FRAME2FILEMENUITEMS4)

    def _init_coll_TestMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='Test Button & CheckBox Dialog', id=wxID_FRAME2TESTMENUITEMS0,
              kind=wx.ITEM_NORMAL, text='&MiniFrame1')
        parent.Append(help='Tree List Control Dialogs', id=wxID_FRAME2TESTMENUITEMS1,
              kind=wx.ITEM_NORMAL, text='&TreeList Control')
        self.Bind(wx.EVT_MENU, self.OnTestMenuItems0Menu, id=wxID_FRAME2TESTMENUITEMS0)
        self.Bind(wx.EVT_MENU, self.OnTestMenuItems1Menu, id=wxID_FRAME2TESTMENUITEMS1)

    def _init_coll_statusBar1_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(4)

        parent.SetStatusText(number=0, text='Status')
        parent.SetStatusText(number=1, text='Site')
        parent.SetStatusText(number=2, text='Plan')
        parent.SetStatusText(number=3, text='Sensor Configuration')

        parent.SetStatusWidths([200, -1, -2, -2])

    def _init_sizers(self):
        # generated method, don't edit
        self.gridBagSizer1 = wx.GridBagSizer(hgap=5, vgap=5)

        self._init_coll_gridBagSizer1_Items(self.gridBagSizer1)
        self._init_coll_gridBagSizer1_Growables(self.gridBagSizer1)

        self.SetSizer(self.gridBagSizer1)

    def _init_utils(self):
        # generated method, don't edit
        self.FileMenu = wx.Menu(title='File')

        self.HelpMenu = wx.Menu(title='Help')
        self.HelpMenu.SetEvtHandlerEnabled(True)

        self.menuBar1 = wx.MenuBar()
        self.menuBar1.SetAutoLayout(True)
        self.menuBar1.SetTitle('Main MenuBar')

        self.imageList1 = wx.ImageList(height=16, width=16)
        self._init_coll_imageList1_Images(self.imageList1)

        self.TestMenu = wx.Menu(title='Test')
        self.TestMenu.SetEvtHandlerEnabled(True)

        self.DataMenu = wx.Menu(title='Database Selection')

        self._init_coll_FileMenu_Items(self.FileMenu)
        self._init_coll_HelpMenu_Items(self.HelpMenu)
        self._init_coll_menuBar1_Menus(self.menuBar1)
        self._init_coll_TestMenu_Items(self.TestMenu)
        self._init_coll_DataMenu_Items(self.DataMenu)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME2, name='', parent=prnt, pos=wx.Point(354, 210),
              size=wx.Size(919, 724), style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER,
              title='pyMap - A Flight Planning Utility')
        self._init_utils()
        self.SetClientSize(wx.Size(911, 690))
        self.SetMenuBar(self.menuBar1)
        self.SetAutoLayout(False)
        self.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.SetMinSize(wx.Size(680, 450))
        self.SetBackgroundColour(wx.Colour(0, 0, 160))
        self.Show(False)
        self.SetStatusBarPane(0)
        self.Center(wx.BOTH)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME2STATUSBAR1, name='statusBar1', parent=self,
              style=wx.ALWAYS_SHOW_SB | wx.HSCROLL | wx.ST_SIZEGRIP)
        self.statusBar1.SetStatusText('Status')
        self.statusBar1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        self.statusBar1.SetAutoLayout(False)
        self.statusBar1.Enable(True)
        self.statusBar1.SetExtraStyle(0)
        self.statusBar1.SetMinHeight(23)
        self.statusBar1.SetMinSize(wx.Size(712, 23))
        self.statusBar1.SetSizeHints(-1, -1, -1, -1)
        self.statusBar1.SetFieldsCount(4)
        self.statusBar1.SetHelpText('Status Bar')
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

        self.button5 = wx.Button(id=wxID_FRAME2BUTTON5, label='Sites', name='button5',
              parent=self, pos=wx.Point(5, 5), size=wx.Size(75, 23), style=0)
        self.button5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.button5.SetBackgroundColour(wx.Colour(192, 255, 255))
        self.button5.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.button5.SetToolTipString('Open a Target Database')
        self.button5.Bind(wx.EVT_BUTTON, self.OnButton5Button, id=wxID_FRAME2BUTTON5)
        self.button5.Bind(wx.EVT_ENTER_WINDOW, self.OnButton5EnterWindow)
        self.button5.Bind(wx.EVT_LEAVE_WINDOW, self.OnButton5LeaveWindow)

        self.button6 = wx.Button(id=wxID_FRAME2BUTTON6, label='Plans', name='button6',
              parent=self, pos=wx.Point(5, 38), size=wx.Size(75, 23), style=0)
        self.button6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.button6.SetBackgroundColour(wx.Colour(192, 255, 192))
        self.button6.SetToolTipString('Open a Planning Database')
        self.button6.Bind(wx.EVT_BUTTON, self.OnButton6Button, id=wxID_FRAME2BUTTON6)
        self.button6.Bind(wx.EVT_ENTER_WINDOW, self.OnButton6EnterWindow)
        self.button6.Bind(wx.EVT_LEAVE_WINDOW, self.OnButton6LeaveWindow)

        self.button7 = wx.Button(id=wxID_FRAME2BUTTON7, label='Config', name='button7',
              parent=self, pos=wx.Point(5, 71), size=wx.Size(75, 23), style=0)
        self.button7.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.button7.SetBackgroundColour(wx.Colour(255, 192, 192))
        self.button7.Show(True)
        self.button7.Bind(wx.EVT_BUTTON, self.OnButton7Button, id=wxID_FRAME2BUTTON7)
        self.button7.Bind(wx.EVT_ENTER_WINDOW, self.OnButton7EnterWindow)
        self.button7.Bind(wx.EVT_LEAVE_WINDOW, self.OnButton7LeaveWindow)

        self.button8 = wx.Button(id=wxID_FRAME2BUTTON8, label='Routing', name='button8',
              parent=self, pos=wx.Point(5, 104), size=wx.Size(75, 23), style=0)
        self.button8.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.button8.SetBackgroundColour(wx.Colour(255, 255, 192))
        self.button8.Bind(wx.EVT_BUTTON, self.OnButton8Button, id=wxID_FRAME2BUTTON8)
        self.button8.Bind(wx.EVT_ENTER_WINDOW, self.OnButton8EnterWindow)
        self.button8.Bind(wx.EVT_LEAVE_WINDOW, self.OnButton8LeaveWindow)

        self.button1 = wx.Button(id=wxID_FRAME2BUTTON1, label='Sites', name='button1',
              parent=self, pos=wx.Point(5, 137), size=wx.Size(75, 23), style=0)
        self.button1.SetConstraints(LayoutAnchors(self.button1, True, True, False, False))
        self.button1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,'MS Shell Dlg 2'))
        self.button1.SetAutoLayout(True)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button, id=wxID_FRAME2BUTTON1)

        self.button2 = wx.Button(id=wxID_FRAME2BUTTON2, label='Plans', name='button2',
              parent=self, pos=wx.Point(5, 170), size=wx.Size(75, 23), style=0)
        self.button2.SetConstraints(LayoutAnchors(self.button2, True, True, False, False))
        self.button2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,'MS Shell Dlg 2'))
        self.button2.SetAutoLayout(True)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button, id=wxID_FRAME2BUTTON2)

        self.button3 = wx.Button(id=wxID_FRAME2BUTTON3, label='Config', name='button3',
              parent=self, pos=wx.Point(5, 203), size=wx.Size(75, 23), style=0)
        self.button3.SetConstraints(LayoutAnchors(self.button3, True, True, False, False))
        self.button3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,'MS Shell Dlg 2'))
        self.button3.SetAutoLayout(True)
        self.button3.Bind(wx.EVT_BUTTON, self.OnButton3Button, id=wxID_FRAME2BUTTON3)

        self.button4 = wx.Button(id=wxID_FRAME2BUTTON4, label='Routing', name='button4',
              parent=self, pos=wx.Point(5, 236), size=wx.Size(75, 23), style=0)
        self.button4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,'MS Shell Dlg 2'))
        self.button4.SetAutoLayout(True)
        self.button4.SetMinSize(wx.Size(75, 23))
        self.button4.Bind(wx.EVT_BUTTON, self.OnButton4Button, id=wxID_FRAME2BUTTON4)

        self.scrolledWindow1 = wx.ScrolledWindow(id=wxID_FRAME2SCROLLEDWINDOW1,
              name='scrolledWindow1', parent=self, pos=wx.Point(90, 5), size=wx.Size(816, 680),
              style=wx.ALWAYS_SHOW_SB | wx.HSCROLL | wx.VSCROLL)
        self.scrolledWindow1.SetAutoLayout(True)
        self.scrolledWindow1.SetConstraints(LayoutAnchors(self.scrolledWindow1, True, True,
              False, False))
        self.scrolledWindow1.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.scrolledWindow1.SetBackgroundColour(wx.Colour(255, 255, 198))
        self.scrolledWindow1.SetForegroundColour(wx.Colour(255, 255, 255))
        self.scrolledWindow1.SetMaxSize(wx.Size(4000, 4000))
        self.scrolledWindow1.Bind(wx.EVT_PAINT, self.OnScrolledWindow1Paint)
        self.scrolledWindow1.Bind(wx.EVT_SCROLLWIN, self.OnScrolledWindow1Scrollwin)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        # My code
        self.DataMenu.Check(id=wxID_FRAME2DATAMENUITEMS0, check=False)
        self.DataMenu.Check(id=wxID_FRAME2DATAMENUITEMS1, check=False)
        self.DataMenu.Check(id=wxID_FRAME2DATAMENUITEMS2, check=False)
        # finish set up of scrolled window
        self.scrolledWindow1.maxWidth = 4000
        self.scrolledWindow1.maxHeight = 4000
        self.scrolledWindow1.x = 0
        self.scrolledWindow1.y = 0
##        self.scrolledWindow1.SetVirtualSize((self.scrolledWindow1.maxWidth, 
##                                            self.scrolledWindow1.maxHeight))
        self.scrolledWindow1.SetVirtualSize(wx.Size(4000,4000))
        self.scrolledWindow1.SetScrollRate(20,20)
        
    def OnFileMenuItems0Menu(self, event):
        filename = ''
        import Map_db_IO.WaypointTarget_IO as wpio
        wildcard = "Site Database (*sites.txt)|*sites.txt|"     \
                   "Plan Database (*plan.txt)|*plan.txt|" \
                   "Sensor Database(*config.txt)|*config.txt|"    \
                   "All Database files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=".",
                defaultFile="", wildcard=wildcard, style=wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                # Your code
        finally:
            dlg.Destroy()
        # view the database
        # determine the database type
        temp_db = wpio.ReadDatabase(filename)
        input_type = temp_db['Captions'][0][0].strip()
        try:
            if input_type == 'Sites':
                self.site_dlg = Frame4.create(None, filename)
                self.site_dlg.Show(True)
                print 'SiteDlg', isinstance(self.site_dlg, Frame4.Frame4), id(self.site_dlg)
            elif input_type == 'Plan':
                self.plan_dlg = Frame4.create(None, filename)
                self.plan_dlg.Show(True)
                print 'PlanDlg', isinstance(self.plan_dlg, Frame4.Frame4), id(self.plan_dlg)
            elif input_type == 'config':
                self.config_dlg = Frame4.create(None, filename)
                self.config_dlg.Show(True)
                print 'configDlg', isinstance(self.config_dlg, Frame4.Frame4), id(self.config_dlg)
            else:
                pass
        finally:
            self.DataMenu.Check(id=wxID_FRAME2DATAMENUITEMS0, check=False)
            dlg.Destroy()              

    def OnFileMenuItems1Menu(self, event):
        event.Skip()

    def OnFileMenuItems2Menu(self, event):
        event.Skip()

    def OnFileMenuItems3Menu(self, event):
        event.Skip()

    def OnFileMenuItems4Menu(self, event):
        event.Skip()

    def OnHelpMenuItems0Menu(self, event):
        event.Skip()

    def OnTestMenuItems0Menu(self, event):
        setup_dlg = MiniFrame1.create(None)
        setup_dlg.Show(True)

    def OnTestMenuItems1Menu(self, event):
        # Select the Planning Database
        wildcard = "Plan Database (*plan.txt)|*plan.txt|" \
                   "All Database files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=".",
                defaultFile="", wildcard=wildcard, style=wx.OPEN)
        input_type = 'Plan'
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetPath()
                # Your code
            else:
                # handles the case where the dialog is cancelled
                self.filename = ''
        finally:
            dlg.Destroy()

        if self.filename != '':
            try:
                # try to close an existing ListCtrl Object
                # ignore any errors
                # then create a new one
                self.plan_dlg.Destroy()
            finally:
                temp_db = wpio.ReadDatabase(self.filename)
                input_db = wpio.generic2plan_db(temp_db)
                # ListTree Dialog
                self.plan_dlg = Frame3.create(self, self.filename, input_type)
                self.plan_dlg.input_db = input_db
                self.plan_dlg.Show(True)

    def OnDataMenuItems0Menu(self, event):
        # select the Target Site Database
        wildcard = "Site Database (*sites.txt)|*sites.txt|"     \
                   "All Database files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=".",
                defaultFile="", wildcard=wildcard, style=wx.OPEN)
        input_type = 'Sites'
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetPath()
                # Your code
            else:
                # handles the case where the dialog is cancelled
                self.filename = ''
        finally:
            dlg.Destroy()

        if self.filename != '':
            try:
                # try to close an existing ListCtrl Object
                # ignore any errors
                # then create a new one
                self.DataMenu.Check(id=wxID_FRAME2DATAMENUITEMS0, check=False)
                print 'HERE I AM - DataMenuItem0'
                self.site_dlg.Destroy()
            finally:
                temp_db = wpio.ReadDatabase(self.filename)
                input_db = wpio.generic2site_db(temp_db)
                # create the list of data to populate the list
                self.DataList = [key for key in input_db.keys() if key != 'Captions']                
                # ListCtrl Dialog
                self.site_dlg = Frame4.create(None, self.filename, input_type, self.DataList)    
                self.DataMenu.Check(id=wxID_FRAME2DATAMENUITEMS0, check=True)
                self.site_dlg.input_db = input_db
                self.site_dlg.Show(True)
                print 'From Frame2 File/Data menu: %s' %(self.site_dlg.list)
                print self.site_dlg.GetId(), self.site_dlg.GetLabel()            

    def OnDataMenuItems1Menu(self, event):
        # Select the Planning Database
        wildcard = "Plan Database (*plan.txt)|*plan.txt|" \
                   "All Database files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=".",
                defaultFile="", wildcard=wildcard, style=wx.OPEN)
        input_type = 'Plan'
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetPath()
                # Your code
            else:
                # handles the case where the dialog is cancelled
                self.filename = ''
        finally:
            dlg.Destroy()

        if self.filename != '':
            try:
                # try to close an existing ListCtrl Object
                # ignore any errors
                # then create a new one
                self.DataMenu.Check(id=wxID_FRAME2DATAMENUITEMS1, check=False)
                self.plan_dlg.Destroy()
            finally:
                temp_db = wpio.ReadDatabase(self.filename)
                input_db = wpio.generic2plan_db(temp_db)
                # create the list of data to populate the list
                self.DataList = [key for key in input_db.keys() if key != 'Captions']                
                # ListCtrl Dialog
                self.plan_dlg = Frame4.create(None, self.filename, input_type, self.DataList)    
                self.DataMenu.Check(id=wxID_FRAME2DATAMENUITEMS1, check=True)
                self.plan_dlg.input_db = input_db
                self.plan_dlg.Show(True)

    def OnDataMenuItems2Menu(self, event):
        # Select the Configuration Database
        wildcard = "Sensor Database(*config.txt)|*config.txt|"     \
                   "All Database files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=".",
                defaultFile="", wildcard=wildcard, style=wx.OPEN)
        input_type = 'config'
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetPath()
                # Your code
            else:
                # handles the case where the dialog is cancelled
                self.filename = ''
        finally:
            dlg.Destroy()

        if self.filename != '':
            try:
                self.DataMenu.Check(id=wxID_FRAME2DATAMENUITEMS2, check=False)
                print 'HERE I AM - DataMenuItem2'
                self.config_dlg.Destroy()
            finally:
                temp_db = wpio.ReadDatabase(self.filename)
                input_db = wpio.generic2sensor_db(temp_db)
                # create the list of data to populate the list
                self.DataList = [key for key in input_db.keys() if key != 'Captions']                
                # ListCtrl Dialog
                self.config_dlg = Frame4.create(None, self.filename, input_type, self.DataList)
                self.DataMenu.Check(id=wxID_FRAME2DATAMENUITEMS2, check=True)
                self.config_dlg.input_db = input_db
                self.config_dlg.Show(True)

    def OnFileMenuDataMenu(self, event):
        event.Skip()

    def OnDataMenuItems4Menu(self, event):
        print 'HERE I AM - DataMenuItem4'
        try:
            txt = ''.join(['Message', '\n\n', 
            '\tSite Selection.............', self.site_dlg.getKey(), '\n', 
            '\tPlan Selection.............', self.plan_dlg.getKey(), '\n', 
            '\tConfiguration Selection....', self.config_dlg.getKey(), '\t'])
        except (NameError, AttributeError):
            txt = ''.join(['Message', '\n\n',
            'Database Selections are not complete.', '\n',
            'Please Try Again'])
        dlg = wx.MessageDialog(self, txt,
          'Caption', wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
        # this works and shows how to access the data
        print self.site_dlg.input_db[self.site_dlg.getKey()]
        print self.plan_dlg.input_db[self.plan_dlg.getKey()]
        print self.config_dlg.input_db[self.config_dlg.getKey()]
        
        # check that the selected site resides in the planning database
        if self.plan_dlg.input_db.has_key(self.site_dlg.getKey()):
            print 'Selected Site found in Planning Database'
        else:
            print 'Selected Site not located in Planning Database'
        
        # check for multiple plans for the selected site
        if len(self.plan_dlg.input_db[self.plan_dlg.getKey()]) > 1:
            print 'Multiple Plans exist for this site'
        else:
            print self.plan_dlg.input_db[self.plan_dlg.getKey()]
            
        # check that the plan configuration resides in the config database.
        

##        check_DB_selections(self)
    
##    def check_DB_selections(self):
##        print self.site_dlg.input_db[self.site_dlg.getKey()]
##        print self.plan_dlg.input_db[self.plan_dlg.getKey()]
##        print self.config_dlg.input_db[self.config_dlg.getKey()]
##        return

    def OnButton1Button(self, event):
        Frame2.OnDataMenuItems0Menu(self, event)

    def OnButton2Button(self, event):
        Frame2.OnDataMenuItems1Menu(self, event)

    def OnButton3Button(self, event):
        Frame2.OnDataMenuItems2Menu(self, event)

    def OnButton4Button(self, event):
        Frame2.OnDataMenuItems4Menu(self, event)

    def OnButton5Button(self, event):
        Frame2.OnDataMenuItems0Menu(self, event)

    def OnButton6Button(self, event):
        Frame2.OnDataMenuItems1Menu(self, event)

    def OnButton7Button(self, event):
        Frame2.OnDataMenuItems2Menu(self, event)

    def OnButton8Button(self, event):
        Frame2.OnDataMenuItems4Menu(self, event)

    def OnButton5EnterWindow(self, event):
        self.button5.SetBackgroundColour(wx.Colour(127, 192, 192))

    def OnButton5LeaveWindow(self, event):
        self.button5.SetBackgroundColour(wx.Colour(192, 255, 255))

    def OnButton6EnterWindow(self, event):
        self.button6.SetBackgroundColour(wx.Colour(127, 255, 127))

    def OnButton6LeaveWindow(self, event):
        self.button6.SetBackgroundColour(wx.Colour(192, 255, 192))

    def OnButton7EnterWindow(self, event):
        self.button7.SetBackgroundColour(wx.Colour(255, 127, 127))

    def OnButton7LeaveWindow(self, event):
        self.button7.SetBackgroundColour(wx.Colour(255, 192, 192))

    def OnButton8EnterWindow(self, event):
        self.button8.SetBackgroundColour(wx.Colour(255, 255, 127))

    def OnButton8LeaveWindow(self, event):
        self.button8.SetBackgroundColour(wx.Colour(255, 255, 192))
        
    def OnScrolledWindow1Paint(self, event):
        dc = wx.PaintDC(self.scrolledWindow1)
        dc.Clear()
        dc.DrawLine(0,0,100,100)
        dc.SetPen(wx.Pen("RED", width=3, style=wx.SOLID))
        dc.DrawRectangle(100,100,4,4)
        dc.SetPen(wx.Pen("RED", width=4, style=wx.SOLID))
        dc.DrawCircle(150,150,25)
        dc.SetBrush(wx.Brush("CYAN", style=wx.SOLID))
        dc.DrawEllipse(250,250,25,200)
        dc.SetPen(wx.Pen("BLUE", width=2, style=wx.SOLID))
        dc.SetBrush(wx.Brush("CYAN", style=wx.TRANSPARENT))
        dc.DrawEllipse(200,300,200,25)
        dc.SetBrush(wx.Brush("CYAN", style=wx.CROSSDIAG_HATCH))
        dc.DrawRoundedRectangle(700,800,150,50,20)
        dc.SetPen(wx.Pen("GREEN", width=1, style=wx.SOLID))
        dc.CrossHair(200,200)
        dc.SetBrush(wx.Brush("CYAN", style=wx.TRANSPARENT))
        dc.DrawCircle(200,200,3)
        dc.DrawCircle(200,200,10)
        dc.DrawCircle(200,200,33)
        dc.DrawCircle(200,200,100)
        dc.DrawCircle(200,200,333)
        dc.DrawCircle(200,200,1000)      
        print wx.Pen.GetColour(dc.GetPen())
        print wx.Pen.GetStyle(dc.GetPen())
        print wx.Brush.GetStyle(dc.GetBrush())

    def OnScrolledWindow1Scrollwin(self, event):
        event.Skip()



        
    
        
 
