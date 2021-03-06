__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import wx
from Cura.util import version

class newVersionDialog(wx.Dialog):
	url = "code.alephobjects.com/w/cura/release-notes/"

	def __init__(self):
		super(newVersionDialog, self).__init__(None, title="Welcome to the new version!")

		wx.EVT_CLOSE(self, self.OnClose)

		p = wx.Panel(self)
		self.panel = p
		s = wx.BoxSizer()
		self.SetSizer(s)
		s.Add(p, flag=wx.ALL, border=15)
		s = wx.BoxSizer(wx.VERTICAL)
		p.SetSizer(s)

		title_text = 'Cura - ' + version.getVersion()
		title = wx.StaticText(p, -1, title_text)
		font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
		title.SetFont(font)
		dc = wx.ScreenDC()
		dc.SetFont(font)
		title.SetMinSize(dc.GetTextExtent(title_text))
		s.Add(title, flag=wx.ALIGN_CENTRE|wx.EXPAND|wx.BOTTOM, border=5)
		s.Add(wx.StaticText(p, -1, _('Welcome to the new release of Cura LulzBot Edition!')))
		s.Add(wx.StaticText(p, -1, _('(This dialog is only shown once)')))
		s.Add(wx.StaticLine(p), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=10)
		s.Add(wx.StaticText(p, -1, _('Want to know what is new and cool in this version?')))
		s.Add(wx.StaticText(p, -1, _('Click here for a list of changes:')))
		s.Add(wx.HyperlinkCtrl(p, -1, newVersionDialog.url, newVersionDialog.url))

		s.Add(wx.StaticLine(p), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=10)
		button = wx.Button(p, -1, _('OK'))
		self.Bind(wx.EVT_BUTTON, self.OnOk, button)
		s.Add(button, flag=wx.TOP|wx.ALIGN_RIGHT, border=5)

		self.Fit()
		self.Centre()
		self.Layout()

	def OnOk(self, e):
		self.Close()

	def OnClose(self, e):
		self.Destroy()
