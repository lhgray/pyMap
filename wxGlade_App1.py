#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4 on Fri Feb 03 10:41:45 2006

import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.notebook_1 = wx.Notebook(self, -1, style=0)
        self.notebook_1_pane_4 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_1 = wx.ScrolledWindow(self.notebook_1, -1, style=wx.TAB_TRAVERSAL)
        
        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_1_menubar)
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.NewId(), "Open", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.NewId(), "Save", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.NewId(), "Close", "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.NewId(), "MiniFrame", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.NewId(), "TreeListCtrl", "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "Menu")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.NewId(), "Help", "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "About")
        # Menu Bar end
        self.frame_1_statusbar = self.CreateStatusBar(3, 0)
        self.button_8 = wx.Button(self, -1, "button_8")
        self.button_9 = wx.Button(self, -1, "button_9")
        self.button_10 = wx.Button(self, -1, "button_10")
        self.button_11 = wx.Button(self, -1, "button_11")
        self.button_12 = wx.Button(self, -1, "button_12")
        self.button_13 = wx.Button(self, -1, "button_13")
        self.button_14 = wx.Button(self, -1, "button_14")
        self.button_15 = wx.Button(self, -1, "button_15")
        self.panel_1 = wx.Panel(self, -1, style=wx.RAISED_BORDER|wx.TAB_TRAVERSAL)
        self.panel_2 = wx.ScrolledWindow(self.notebook_1_pane_1, -1, style=wx.TAB_TRAVERSAL)
        self.tree_ctrl_1 = wx.TreeCtrl(self.notebook_1_pane_2, -1, style=wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)
        self.grid_1 = wx.grid.Grid(self.notebook_1_pane_3, -1, size=(1, 1))
        self.grid_2 = wx.grid.Grid(self.notebook_1_pane_4, -1, size=(1, 1))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((725, 485))
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))
        self.frame_1_statusbar.SetStatusWidths([-1, -1, -1])
        # statusbar fields
        frame_1_statusbar_fields = ["frame_1_statusbar", "Segment 2", "Segment 3"]
        for i in range(len(frame_1_statusbar_fields)):
            self.frame_1_statusbar.SetStatusText(frame_1_statusbar_fields[i], i)
        self.panel_1.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.panel_1.SetForegroundColour(wx.Colour(255, 0, 0))
        self.panel_2.SetScrollRate(10, 10)
        self.notebook_1_pane_1.SetMinSize((615, 374))
        self.notebook_1_pane_1.SetScrollRate(10, 10)
        self.grid_1.CreateGrid(10, 3)
        self.grid_2.CreateGrid(30, 4)
        self.grid_2.SetRowLabelSize(30)
        self.grid_2.SetColLabelSize(25)
        self.grid_2.SetColLabelValue(0, "Alpha")
        self.grid_2.SetColLabelValue(1, "Beta")
        self.grid_2.SetColLabelValue(2, "Gamma")
        self.grid_2.SetColLabelValue(3, "Delta")
        self.notebook_1.SetMinSize((200,200))
        self.notebook_1.SetFocus()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_2 = wx.FlexGridSizer(1, 2, 5, 5)
        grid_sizer_5 = wx.GridSizer(1, 1, 0, 0)
        grid_sizer_4 = wx.GridSizer(1, 1, 0, 0)
        grid_sizer_3 = wx.GridSizer(1, 1, 0, 0)
        grid_sizer_2 = wx.GridSizer(1, 1, 0, 0)
        grid_sizer_1 = wx.FlexGridSizer(9, 1, 5, 5)
        grid_sizer_1.Add(self.button_8, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_9, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_10, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_11, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_12, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_13, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_14, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_15, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        grid_sizer_1.AddGrowableRow(8)
        sizer_2.Add(grid_sizer_1, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_2.Add(self.panel_2, 1, wx.EXPAND, 0)
        self.notebook_1_pane_1.SetAutoLayout(True)
        self.notebook_1_pane_1.SetSizer(grid_sizer_2)
        grid_sizer_3.Add(self.tree_ctrl_1, 1, wx.EXPAND, 0)
        self.notebook_1_pane_2.SetAutoLayout(True)
        self.notebook_1_pane_2.SetSizer(grid_sizer_3)
        grid_sizer_3.Fit(self.notebook_1_pane_2)
        grid_sizer_3.SetSizeHints(self.notebook_1_pane_2)
        grid_sizer_4.Add(self.grid_1, 1, wx.EXPAND, 0)
        self.notebook_1_pane_3.SetAutoLayout(True)
        self.notebook_1_pane_3.SetSizer(grid_sizer_4)
        grid_sizer_4.Fit(self.notebook_1_pane_3)
        grid_sizer_4.SetSizeHints(self.notebook_1_pane_3)
        grid_sizer_5.Add(self.grid_2, 1, wx.EXPAND, 0)
        self.notebook_1_pane_4.SetAutoLayout(True)
        self.notebook_1_pane_4.SetSizer(grid_sizer_5)
        grid_sizer_5.Fit(self.notebook_1_pane_4)
        grid_sizer_5.SetSizeHints(self.notebook_1_pane_4)
        self.notebook_1.AddPage(self.notebook_1_pane_1, "MapDisplay")
        self.notebook_1.AddPage(self.notebook_1_pane_2, "Targets")
        self.notebook_1.AddPage(self.notebook_1_pane_3, "Planning")
        self.notebook_1.AddPage(self.notebook_1_pane_4, "Configuration")
        sizer_2.Add(self.notebook_1, 1, wx.ALL|wx.EXPAND, 2)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_2)
        sizer_2.AddGrowableRow(0)
        sizer_2.AddGrowableCol(1)
        self.Layout()
        self.Centre()
        # end wxGlade

# end of class MyFrame


class MyFrame1(wx.Frame):
    def __init__(self, *args, **kwds):
        # content of this block not found: did you rename this class?
        pass

    def __set_properties(self):
        # content of this block not found: did you rename this class?
        pass

    def __do_layout(self):
        # content of this block not found: did you rename this class?
        pass

# end of class MyFrame1

