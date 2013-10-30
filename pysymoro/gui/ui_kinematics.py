__author__ = 'Izzat'
import wx

class DialogJacobian(wx.Dialog):
    def __init__(self, prefix, robo, parent=None):
        super(DialogJacobian, self).__init__(parent, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.robo = robo
        self.InitUI()
        self.SetTitle(prefix + ": Jacobian matrix (jac)")

    def InitUI(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        #title
        label_main = wx.StaticText(self, label="Calculation of i Jr j")
        mainSizer.Add(label_main, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 25)

        #input
        choices = [str(i) for i in range(self.robo.NF)]
        label = wx.StaticText(self, label='Frame number ( r )')
        mainSizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.cmb_frame = wx.ComboBox(self, size=(50, -1), choices=choices, style=wx.CB_READONLY)
        self.cmb_frame.SetSelection(len(choices)-1)
        self.cmb_frame.Bind(wx.EVT_COMBOBOX, self.OnFrameChanged)
        mainSizer.Add(self.cmb_frame, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)

        chain = self.robo.chain(int(self.cmb_frame.Value))
        choices = [str(i) for i in reversed(chain + [0])]
        label = wx.StaticText(self, label='Projection frame ( i )')
        mainSizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.cmb_inter = wx.ComboBox(self, size=(50, -1), choices=choices, style=wx.CB_READONLY)
        self.cmb_inter.SetSelection(0)
        mainSizer.Add(self.cmb_inter, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)

        label = wx.StaticText(self, label='Intermediate frame ( j )')
        mainSizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.cmb_proj = wx.ComboBox(self, size=(50, -1), choices=choices, style=wx.CB_READONLY)
        self.cmb_proj.SetSelection(len(choices)-1)
        self.cmb_proj.SetSelection(0)
        mainSizer.Add(self.cmb_proj, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)

        horSizer = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "OK")
        okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel")
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        horSizer.Add(okButton, 0, wx.ALL, 25)
        horSizer.Add(cancelButton, 0, wx.ALL, 25)
        mainSizer.Add(horSizer)

        self.SetSizerAndFit(mainSizer)

    def OnFrameChanged(self, evt):
        chain = self.robo.chain(int(self.cmb_frame.Value))
        choices = [str(i) for i in reversed(chain + [0])]
        self.cmb_inter.SetItems(choices)
        self.cmb_inter.SetSelection(0)
        self.cmb_proj.SetItems(choices)
        self.cmb_proj.SetSelection(0)

    def OnOK(self, e):
        self.EndModal(wx.ID_OK)

    def OnCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def GetValues(self):
        return int(self.cmb_frame.Value), int(self.cmb_proj.Value), int(self.cmb_inter.Value)

class DialogDeterminant(wx.Dialog):
    def __init__(self, prefix, robo, parent=None):
        super(DialogDeterminant, self).__init__(parent, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.robo = robo
        self.InitUI()
        self.SetTitle(prefix + ": Determinant of a jacobian matrix (det)")

    def InitUI(self):
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        #title
        mainSizer.AddSpacer(10)
        grid = wx.GridBagSizer(5, 15)

        choices = [str(i) for i in range(self.robo.NF)]
        label = wx.StaticText(self, label='Frame number ( r )')
        grid.Add(label, pos=(0, 0), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        self.cmb_frame = wx.ComboBox(self, size=(50, -1), choices=choices, style=wx.CB_READONLY)
        self.cmb_frame.SetSelection(len(choices)-1)
        self.cmb_frame.Bind(wx.EVT_COMBOBOX, self.OnFrameChanged)
        grid.Add(self.cmb_frame, pos=(1, 0), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=15)

        chain = self.robo.chain(int(self.cmb_frame.Value))
        choices = [str(i) for i in reversed(chain + [0])]
        label = wx.StaticText(self, label='Projection frame ( i )')
        grid.Add(label, pos=(2, 0), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        self.cmb_inter = wx.ComboBox(self, size=(50, -1), choices=choices, style=wx.CB_READONLY)
        self.cmb_inter.SetSelection(0)
        grid.Add(self.cmb_inter, pos=(3, 0), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=15)

        label = wx.StaticText(self, label='Intermediate frame ( j )')
        grid.Add(label, pos=(4, 0), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        self.cmb_proj = wx.ComboBox(self, size=(50, -1), choices=choices, style=wx.CB_READONLY)
        self.cmb_proj.SetSelection(len(choices)-1)
        self.cmb_proj.SetSelection(0)
        grid.Add(self.cmb_proj, pos=(5, 0), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=15)

        label_main = wx.StaticText(self, label="Definition of sub-matrix")
        grid.Add(label_main, pos=(6, 0), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        label_main = wx.StaticText(self, label="(Select rows and columns to be deleted)")
        grid.Add(label_main, pos=(7, 0), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=5)

        #input
        label_row = wx.StaticText(self, label="Rows:")
        label_col = wx.StaticText(self, label="Columns:")
        self.box_row = wx.CheckListBox(self, size=(100, 100), choices=['VX', 'VY', 'VZ', 'WX', 'WY', 'WZ'])
        self.box_col = wx.CheckListBox(self, size=(100, 100), choices=[str(i) for i in self.robo.q_vec])
        grid.Add(label_row, pos=(8, 0))
        grid.Add(label_col, pos=(8, 1))
        grid.Add(self.box_row, pos=(9, 0))
        grid.Add(self.box_col, pos=(9, 1))
        okButton = wx.Button(self, wx.ID_OK, "OK")
        okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel")
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        grid.Add(okButton, pos=(10, 0), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        grid.Add(cancelButton, pos=(10, 1), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)

        mainSizer.Add(grid, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        self.SetSizerAndFit(mainSizer)
        self.OnFrameChanged(None)

    def OnFrameChanged(self, evt):
        chain = self.robo.chain(int(self.cmb_frame.Value))
        choices = [str(i) for i in reversed(chain + [0])]
        self.cmb_inter.SetItems(choices)
        self.cmb_inter.SetSelection(0)
        self.cmb_proj.SetItems(choices)
        self.cmb_proj.SetSelection(0)
        choices_list = self.robo.get_q_chain(int(self.cmb_frame.Value))
        self.box_col.SetItems([str(i) for i in choices_list])

    def OnOK(self, e):
        self.EndModal(wx.ID_OK)

    def OnCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def GetValues(self):
        row_selected = [i for i in range(len(self.box_row.Items)) if not self.box_row.IsChecked(i)]
        col_selected = [i for i in range(len(self.box_col.Items)) if not self.box_col.IsChecked(i)]
        return int(self.cmb_frame.Value), int(self.cmb_proj.Value), int(self.cmb_inter.Value), row_selected, col_selected