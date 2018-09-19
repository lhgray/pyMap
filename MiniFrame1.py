#Boa:MiniFrame:MiniFrame1

import wx
from wx.lib.anchors import LayoutAnchors
import Map_db_IO.WaypointTarget_IO as wpio


def create(parent):
    return MiniFrame1(parent)

[wxID_MINIFRAME1, wxID_MINIFRAME1BUTTON1, wxID_MINIFRAME1BUTTON2, wxID_MINIFRAME1BUTTON3, 
 wxID_MINIFRAME1CHOICE1, wxID_MINIFRAME1CHOICE2, wxID_MINIFRAME1CHOICE3, 
 wxID_MINIFRAME1PANEL1, 
] = [wx.NewId() for _init_ctrls in range(8)]

class MiniFrame1(wx.MiniFrame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MiniFrame.__init__(self, id=wxID_MINIFRAME1, name='', parent=prnt, pos=wx.Point(650,
              455), size=wx.Size(327, 233), style=wx.DEFAULT_FRAME_STYLE,
              title='Targetting & Configuration')
        self.SetClientSize(wx.Size(319, 199))
        self.SetAutoLayout(False)
        self.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,'MS Shell Dlg 2'))
        self.Center(wx.BOTH)

        self.panel1 = wx.Panel(id=wxID_MINIFRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(319, 199),
              style=wx.NO_BORDER | wx.TAB_TRAVERSAL)
        self.panel1.SetBackgroundColour(wx.Colour(226, 222, 194))
        self.panel1.SetThemeEnabled(False)
        self.panel1.SetAutoLayout(False)

        self.button1 = wx.Button(id=wxID_MINIFRAME1BUTTON1, label='Targets', name='button1',
              parent=self.panel1, pos=wx.Point(16, 40), size=wx.Size(136, 23), style=0)
        self.button1.SetHelpText('Select a Target Database')
        self.button1.SetToolTipString('Select a Target Database')
        self.button1.SetBackgroundColour(wx.Colour(255, 255, 191))
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button, id=wxID_MINIFRAME1BUTTON1)
        self.button1.Bind(wx.EVT_ENTER_WINDOW, self.OnButton1EnterWindow)
        self.button1.Bind(wx.EVT_LEAVE_WINDOW, self.OnButton1LeaveWindow)

        self.button2 = wx.Button(id=wxID_MINIFRAME1BUTTON2, label='Plans', name='button2',
              parent=self.panel1, pos=wx.Point(16, 80), size=wx.Size(136, 23), style=0)
        self.button2.SetToolTipString('Select a Planning Database')
        self.button2.SetBackgroundColour(wx.Colour(255, 255, 191))
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button, id=wxID_MINIFRAME1BUTTON2)
        self.button2.Bind(wx.EVT_ENTER_WINDOW, self.OnButton2EnterWindow)
        self.button2.Bind(wx.EVT_LEAVE_WINDOW, self.OnButton2LeaveWindow)

        self.button3 = wx.Button(id=wxID_MINIFRAME1BUTTON3, label='Sensor Configuration',
              name='button3', parent=self.panel1, pos=wx.Point(16, 120), size=wx.Size(136, 23),
              style=0)
        self.button3.SetToolTipString('Select a Sensor Configuration Database')
        self.button3.SetBackgroundColour(wx.Colour(255, 255, 191))
        self.button3.Bind(wx.EVT_BUTTON, self.OnButton3Button, id=wxID_MINIFRAME1BUTTON3)
        self.button3.Bind(wx.EVT_ENTER_WINDOW, self.OnButton3EnterWindow)
        self.button3.Bind(wx.EVT_LEAVE_WINDOW, self.OnButton3LeaveWindow)

        self.choice1 = wx.Choice(choices=['Empty'], id=wxID_MINIFRAME1CHOICE1, name='choice1',
              parent=self.panel1, pos=wx.Point(160, 40), size=wx.Size(135, 21), style=0)
        self.choice1.SetSelection(0)
        self.choice1.Bind(wx.EVT_CHOICE, self.OnChoice1Choice, id=wxID_MINIFRAME1CHOICE1)

        self.choice2 = wx.Choice(choices=['Empty'], id=wxID_MINIFRAME1CHOICE2, name='choice2',
              parent=self.panel1, pos=wx.Point(160, 80), size=wx.Size(135, 21), style=0)
        self.choice2.SetSelection(0)
        self.choice2.Bind(wx.EVT_CHOICE, self.OnChoice2Choice, id=wxID_MINIFRAME1CHOICE2)

        self.choice3 = wx.Choice(choices=['Empty'], id=wxID_MINIFRAME1CHOICE3, name='choice3',
              parent=self.panel1, pos=wx.Point(160, 120), size=wx.Size(135, 21), style=0)
        self.choice3.SetSelection(0)
        self.choice3.Bind(wx.EVT_CHOICE, self.OnChoice3Choice, id=wxID_MINIFRAME1CHOICE3)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        wildcard = "Site Database (*sites.txt)|*sites.txt|" \
                   "All Database files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=".",
                defaultFile="", wildcard=wildcard, style=wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                sites_filename = dlg.GetPath()
                # Your code
                temp_db = wpio.ReadDatabase(sites_filename)
                input_db = wpio.generic2site_db(temp_db)
                choice1_Data = [key for key in input_db.keys() if key != 'Captions']
                choice1_Data.sort()
                # remove all items in the control list
                self.choice1.Clear()
                # input the Data into the choice box
                for item in choice1_Data:
                    self.choice1.Append(item)
                self.choice1.SetSelection(0)
        finally:
            dlg.Destroy()

    def OnButton2Button(self, event):
        wildcard = "Plan Database (*plan.txt)|*plan.txt|" \
                   "All Database files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=".",
                defaultFile="", wildcard=wildcard, style=wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                plan_filename = dlg.GetPath()
                # Your code
                temp_db = wpio.ReadDatabase(plan_filename)
                input_db = wpio.generic2plan_db(temp_db)
                choice2_Data = [key for key in input_db.keys() if key != 'Captions']
                choice2_Data.sort()
                # remove all items in the control list
                self.choice2.Clear()
                # input the Data into the choice box
                for item in choice2_Data:
                    self.choice2.Append(item)
                self.choice2.SetSelection(0)
        finally:
            dlg.Destroy()

    def OnButton3Button(self, event):
        wildcard = "Sensor Database(*config.txt)|*config.txt|" \
                   "All Database files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=".",
                defaultFile="", wildcard=wildcard, style=wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                config_filename = dlg.GetPath()
                # Your code
                temp_db = wpio.ReadDatabase(config_filename)
                input_db = wpio.generic2sensor_db(temp_db)
                choice3_Data = [key for key in input_db.keys() if key != 'Captions']
                choice3_Data.sort()
                # remove all items in the control list
                self.choice3.Clear()
                # input the Data into the choice box
                for item in choice3_Data:
                    self.choice3.Append(item)
                self.choice3.SetSelection(0)
        finally:
            dlg.Destroy()

    def OnChoice1Choice(self, event):
        txt = ''.join(['Selected Site\n', event.GetString()])
        txt1 = 'Site Selection'
        dlg = wx.MessageDialog(self, txt, txt1, wx.OK | wx.ICON_INFORMATION)  
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def OnChoice2Choice(self, event):
        txt = ''.join(['Selected Plan\n', event.GetString()])
        txt1 = 'Plan Selection'
        dlg = wx.MessageDialog(self, txt, txt1, wx.OK | wx.ICON_INFORMATION)  
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def OnChoice3Choice(self, event):
        txt = ''.join(['Selected Configuration\n', event.GetString()])
        txt1 = 'Configuration Selection'
        dlg = wx.MessageDialog(self, txt, txt1, wx.OK | wx.ICON_INFORMATION)  
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def OnButton1EnterWindow(self, event):
        self.button1.SetBackgroundColour(wx.Colour(255, 255, 0))
        
    def OnButton1LeaveWindow(self, event):
        self.button1.SetBackgroundColour(wx.Colour(255, 255, 191))

    def OnButton2EnterWindow(self, event):
        self.button2.SetBackgroundColour(wx.Colour(255, 255, 0))

    def OnButton2LeaveWindow(self, event):
        self.button2.SetBackgroundColour(wx.Colour(255, 255, 191))

    def OnButton3EnterWindow(self, event):
        self.button3.SetBackgroundColour(wx.Colour(255, 255, 0))

    def OnButton3LeaveWindow(self, event):
        self.button3.SetBackgroundColour(wx.Colour(255, 255, 191))
