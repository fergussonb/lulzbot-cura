__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"
""""changed (6/21/2016) by Berkeley Fergusson to allow for energy estimation on jobs"""

import wx
import os

from Cura.gui import configWizard
from Cura.gui import configBase
from Cura.util import machineCom
from Cura.util import profile
from Cura.util import pluginInfo
from Cura.util import resources

class preferencesDialog(wx.Dialog):
	def __init__(self, parent):
		super(preferencesDialog, self).__init__(parent, title=_("Preferences"))

		wx.EVT_CLOSE(self, self.OnClose)

		self.parent = parent
		extruderCount = int(profile.getMachineSetting('extruder_amount'))

		self.panel = configBase.configPanelBase(self)

		left, right, main = self.panel.CreateConfigPanel(self)

		configBase.TitleRow(left, _("Colours"))
		configBase.SettingRow(left, 'model_colour', wx.Colour)
		for i in xrange(1, extruderCount):
			configBase.SettingRow(left, 'model_colour%d' % (i+1), wx.Colour)

		if len(resources.getLanguageOptions()) > 1:
			configBase.TitleRow(left, _("Language"))
			configBase.SettingRow(left, 'language', map(lambda n: n[1], resources.getLanguageOptions()))

		configBase.TitleRow(right, _("Filament settings"))
		configBase.SettingRow(right, 'filament_physical_density')
		configBase.SettingRow(right, 'filament_cost_kg')
		configBase.SettingRow(right, 'filament_cost_meter')

		#configBase.TitleRow(right, 'Slicer settings')
		#configBase.SettingRow(right, 'save_profile')

		configBase.TitleRow(right, 'SD Card settings')
		configBase.SettingRow(right, 'auto_detect_sd')
		configBase.SettingRow(right, 'sdcard_rootfolder')
		#same as the expert settings button.
		self.browseButton = wx.Button(right, -1, '...', style=wx.BU_EXACTFIT)
		self.browseButton.SetFont(wx.Font(wx.SystemSettings.GetFont(wx.SYS_ANSI_VAR_FONT).GetPointSize() * 0.8, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_NORMAL))
		self.browseButton.Bind(wx.EVT_BUTTON, self.OnBrowseSDRootFolder)
		right.GetSizer().Add(self.browseButton, (right.GetSizer().GetRows()-1, 2), flag=wx.ALIGN_CENTER_VERTICAL)

		configBase.TitleRow(right, _("Cura settings"))
		configBase.SettingRow(right, 'check_for_updates')
		#configBase.SettingRow(right, 'submit_slice_information')

		self.okButton = wx.Button(right, -1, _('Ok'))
		right.GetSizer().Add(self.okButton, (right.GetSizer().GetRows(), 0), flag=wx.BOTTOM, border=5)
		self.okButton.Bind(wx.EVT_BUTTON, lambda e: self.Close())

		main.Fit()
		self.Fit()

	def OnClose(self, e):
		#self.parent.reloadSettingPanels()
		self.Destroy()

	def OnBrowseSDRootFolder(self, e):
		path = profile.getPreference('sdcard_rootfolder')
		if path == '':
			path = os.path.expanduser('~/Documents')
			if not os.path.exists(path):
				path = ''

		dlg=wx.DirDialog(self, _("Select replication root folder"), path)
		if dlg.ShowModal() != wx.ID_OK:
			dlg.Destroy()
			return

		profile.putPreference('sdcard_rootfolder', dlg.GetPath())
		dlg.Destroy()
		self.Close()
		self.parent.OnPreferences(None)






class machineSettingsDialog(wx.Dialog):
	def __init__(self, parent):
		super(machineSettingsDialog, self).__init__(parent, title=_("Machine settings"))

		wx.EVT_CLOSE(self, self.OnClose)

		self.parent = parent

		self.panel = configBase.configPanelBase(self)
		self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
		self.GetSizer().Add(self.panel, 1, wx.EXPAND)
		self.nb = wx.Notebook(self.panel)
		self.panel.SetSizer(wx.BoxSizer(wx.VERTICAL))
		self.panel.GetSizer().Add(self.nb, 1, wx.EXPAND)

		for idx in xrange(0, profile.getMachineCount()):
			printer_type = profile.getMachineSetting('machine_type', idx)
			extruderCount = int(profile.getMachineSetting('extruder_amount', idx))
			left, right, main = self.panel.CreateConfigPanel(self.nb)
			configBase.TitleRow(left, _("Machine settings"))
			configBase.SettingRow(left, 'steps_per_e', index=idx)
			configBase.SettingRow(left, 'machine_width', index=idx)
			configBase.SettingRow(left, 'machine_depth', index=idx)
			configBase.SettingRow(left, 'machine_height', index=idx)
			if not printer_type.startswith('lulzbot_TAZ_6'): #Disabled for TAZ 6, use LCD controller instead
				configBase.SettingRow(left, 'extruder_z_offset', index=idx)
			configBase.SettingRow(left, 'extruder_amount', index=idx)
			configBase.SettingRow(left, 'has_heated_bed', index=idx)
			configBase.SettingRow(left, 'machine_center_is_zero', index=idx)
			configBase.SettingRow(left, 'machine_shape', index=idx)
			configBase.SettingRow(left, 'gcode_flavor', index=idx)
			configBase.SettingRow(left, 'machine_startup_energy_PLA', index=idx)
			configBase.SettingRow(left, 'machine_run_energy_PLA', index=idx)
			configBase.SettingRow(left, 'machine_startup_energy_ABS', index=idx)
			configBase.SettingRow(left, 'machine_run_energy_ABS', index=idx)
			configBase.SettingRow(left, 'machine_startup_energy_HIPS', index=idx)
			configBase.SettingRow(left, 'machine_run_energy_HIPS', index=idx)
			configBase.SettingRow(left, 'machine_startup_energy_PETT', index=idx)
			configBase.SettingRow(left, 'machine_run_energy_PETT', index=idx)
			configBase.SettingRow(left, 'machine_startup_energy_Nylon', index=idx)
			configBase.SettingRow(left, 'machine_run_energy_Nylon', index=idx)
			configBase.SettingRow(left, 'machine_startup_energy_Other', index=idx)
			configBase.SettingRow(left, 'machine_run_energy_Other', index=idx)

			if printer_type.startswith('lulzbot_'):
				configBase.TitleRow(right, _("Tool Head"))
				row = configBase.ToolHeadRow(right, 'toolhead', index=idx)
				row.button.Bind(wx.EVT_BUTTON, self.OnChangeToolheadButton)

			configBase.TitleRow(right, _("Printer head size"))
			configBase.SettingRow(right, 'extruder_head_size_min_x', index=idx)
			configBase.SettingRow(right, 'extruder_head_size_min_y', index=idx)
			configBase.SettingRow(right, 'extruder_head_size_max_x', index=idx)
			configBase.SettingRow(right, 'extruder_head_size_max_y', index=idx)
			configBase.SettingRow(right, 'extruder_head_size_height', index=idx)

			for i in xrange(1, extruderCount):
				configBase.TitleRow(left, _("Extruder %d") % (i+1))
				configBase.SettingRow(left, 'extruder_offset_x%d' % (i), index=idx)
				configBase.SettingRow(left, 'extruder_offset_y%d' % (i), index=idx)

			configBase.TitleRow(right, _("Communication settings"))
			serial_list = ['AUTO'] + machineCom.serialList()
			serial_list_labels = serial_list[:]
			if profile.getMachineSetting('serial_port') not in serial_list:
				serial_list.append(profile.getMachineSetting('serial_port'))
				serial_list_labels.append(profile.getMachineSetting('serial_port') + _(" (Currently unavailable)"))
			configBase.SettingRow(right, 'serial_port', serial_list, serial_list_labels, index=idx)
			configBase.SettingRow(right, 'serial_baud', ['AUTO'] + map(str, machineCom.baudrateList()), index=idx)

			machine_name = profile.getMachineName(idx)
			machine_title = machine_name.title()			
			machine_title = machine_title.replace('Taz', 'TAZ')
			machine_title = machine_title.replace('Lulzbot', 'LulzBot')
			self.nb.AddPage(main, machine_title)

		self.nb.SetSelection(int(profile.getPreferenceFloat('active_machine')))

		self.buttonPanel = wx.Panel(self.panel)
		self.panel.GetSizer().Add(self.buttonPanel)

		self.buttonPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
		self.okButton = wx.Button(self.buttonPanel, -1, _('Ok'))
		self.okButton.Bind(wx.EVT_BUTTON, lambda e: self.Close())
		self.buttonPanel.GetSizer().Add(self.okButton, flag=wx.ALL, border=5)

		self.addButton = wx.Button(self.buttonPanel, -1, _('Add new machine'))
		self.addButton.Bind(wx.EVT_BUTTON, self.OnAddMachine)
		self.buttonPanel.GetSizer().Add(self.addButton, flag=wx.ALL, border=5)

		self.remButton = wx.Button(self.buttonPanel, -1, _('Remove machine'))
		self.remButton.Bind(wx.EVT_BUTTON, self.OnRemoveMachine)
		self.buttonPanel.GetSizer().Add(self.remButton, flag=wx.ALL, border=5)

		self.renButton = wx.Button(self.buttonPanel, -1, _('Change machine name'))
		self.renButton.Bind(wx.EVT_BUTTON, self.OnRenameMachine)
		self.buttonPanel.GetSizer().Add(self.renButton, flag=wx.ALL, border=5)

		main.Fit()
		self.Fit()

	def OnChangeToolheadButton(self, e):
		self.Hide()
		self.parent.Hide()
		old_active = int(profile.getPreferenceFloat('active_machine'))
		profile.setActiveMachine(self.nb.GetSelection())
		configWizard.LulzbotChangeToolheadWizard()
		profile.setActiveMachine(old_active)
		self.parent.Show()
		self.parent.reloadSettingPanels()
		self.parent.updateMachineMenu()

		prefDialog = machineSettingsDialog(self.parent)
		prefDialog.Centre()
		prefDialog.Show()
		wx.CallAfter(self.Close)

	def OnAddMachine(self, e):
		self.Hide()
		self.parent.Hide()
		configWizard.ConfigWizard(True)
		self.parent.Show()
		self.parent.reloadSettingPanels()
		self.parent.updateMachineMenu()

		prefDialog = machineSettingsDialog(self.parent)
		prefDialog.Centre()
		prefDialog.Show()
		wx.CallAfter(self.Close)

	def OnRemoveMachine(self, e):
		if profile.getMachineCount() < 2:
			wx.MessageBox(_("Cannot remove the last machine configuration in Cura"), _("Machine remove error"), wx.OK | wx.ICON_ERROR)
			return

		dlg = wx.MessageDialog(self,
			_("Are you sure you want to remove the selected machine?"),
			_('Remove machine?'),
			wx.YES_NO | wx.ICON_EXCLAMATION)
		remove = dlg.ShowModal() == wx.ID_YES
		dlg.Destroy()
		if remove:
			self.Hide()
			profile.removeMachine(self.nb.GetSelection())
			self.parent.reloadSettingPanels()
			self.parent.updateMachineMenu()

			prefDialog = machineSettingsDialog(self.parent)
			prefDialog.Centre()
			prefDialog.Show()
			wx.CallAfter(self.Close)

	def OnRenameMachine(self, e):
		dialog = wx.TextEntryDialog(self, _("Enter the new name:"), _("Change machine name"),
									profile.getMachineSetting('machine_name', self.nb.GetSelection()))
		if dialog.ShowModal() != wx.ID_OK:
			return
		profile.putMachineSetting('machine_name', dialog.GetValue(), self.nb.GetSelection())
		self.nb.SetPageText(self.nb.GetSelection(), profile.getMachineName(self.nb.GetSelection()))
		self.parent.updateMachineMenu()

	def OnClose(self, e):
		self.parent.reloadSettingPanels()
		self.Destroy()
