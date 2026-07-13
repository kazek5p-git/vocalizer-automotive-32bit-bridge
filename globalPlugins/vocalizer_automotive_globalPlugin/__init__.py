#vocalizer_globalPlugin/__init__.py
#A part of the vocalizer driver for NVDA (Non Visual Desktop Access)
#Copyright (C) 2012 Rui Batista <ruiandrebatista@gmail.com>
#Copyright (C) 2012 - 2023 Tiflotecnia, lda. <www.tiflotecnia.net>
#This file is covered by the GNU General Public License.
#See the file GPL.txt for more details.

import os
import shutil
import webbrowser

import configobj
import wx
import addonHandler
import globalPluginHandler
import globalVars
import gui
import languageHandler
from logHandler import log

addonHandler.initTranslation()

from .dialogs import VocalizerLanguageSettingsDialog, getInstalledVoiceLocaleMap


BRIDGE_SYNTH_NAME = "vocalizerAutomotive32"
VOICE_DOWNLOADS_URL = "https://tiflotecnia.net/downloads.htm"
DRIVER_VERSION_FALLBACK = "2.1.7-2026.07.13"


def getDefaultLicensePath():
	appArgs = getattr(globalVars, "appArgs", None)
	configPath = getattr(appArgs, "configPath", None)
	if not configPath:
		configPath = os.path.join(os.environ.get("APPDATA", ""), "nvda")
	return os.path.join(configPath, "vocalizer_license.ini")


def getLicenseInfo():
	path = getDefaultLicensePath()
	if not os.path.isfile(path):
		return "none"
	try:
		licenseData = configobj.ConfigObj(
			path,
			default_encoding="utf-8",
			encoding="utf-8",
		)
		info = licenseData.get("info", {})
		requiredFields = ("username", "userid", "licenseid", "distributor")
		if all(info.get(field) for field in requiredFields):
			return "licensed:" + path
	except Exception:
		log.debugWarning("Unable to read Vocalizer license file.", exc_info=True)
	return "invalid"


def _getDriverVersion():
	try:
		for addon in addonHandler.getRunningAddons():
			if getattr(addon, "name", "") == "vocalizer_automotive_driver":
				return addon.manifest.get("version", DRIVER_VERSION_FALLBACK)
	except Exception:
		log.debugWarning("Unable to read Automotive driver version.", exc_info=True)
	return DRIVER_VERSION_FALLBACK


def _getLicenseSummary():
	licenseInfo = getLicenseInfo()
	if licenseInfo == "none":
		return _("No license file found.")
	if licenseInfo == "invalid":
		return _("The license file exists but could not be read.")

	path = licenseInfo.split(":", 1)[1]
	try:
		licenseData = configobj.ConfigObj(
			path,
			default_encoding="utf-8",
			encoding="utf-8",
		)
		info = licenseData["info"]
		return "\n".join(
			(
				_("User Name: ") + info.get("username", ""),
				_("User Identification: ") + info.get("userid", ""),
				_("License Number: ") + info.get("licenseid", ""),
				_("Distributor: ") + info.get("distributor", ""),
				_(
					"License validation is performed by the 32-bit Automotive host."
				),
			)
		)
	except Exception:
		log.debugWarning("Unable to format Vocalizer license information.", exc_info=True)
		return _("License file found, but detailed information is unavailable.")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Vocalizer Automotive")

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.submenu_vocalizer = None
		self.menuItem = None
		if globalVars.appArgs.secure:
			return
		try:
			self.createMenu()
		except Exception:
			log.error("Unable to create Vocalizer Automotive menu.", exc_info=True)

	def createMenu(self):
		self.removeMenu()
		self.submenu_vocalizer = wx.Menu()
		sysTrayIcon = gui.mainFrame.sysTrayIcon

		item = self.submenu_vocalizer.Append(
			wx.ID_ANY,
			_("Automatic &Language Switching Settings"),
			_("Configure which voice is used for each language."),
		)
		sysTrayIcon.Bind(wx.EVT_MENU, self.onLanguageSettings, item)

		if getLicenseInfo() in ("licensed", "invalid") or os.path.isfile(
			getDefaultLicensePath()
		):
			item = self.submenu_vocalizer.Append(
				wx.ID_ANY,
				_("Remove License"),
				_("Remove the Automotive license from this NVDA copy."),
			)
			sysTrayIcon.Bind(wx.EVT_MENU, self.onVocalizerLicenseRemoveMenu, item)
		else:
			item = self.submenu_vocalizer.Append(
				wx.ID_ANY,
				_("Enter License"),
				_("Enter your Automotive license data for this computer."),
			)
			sysTrayIcon.Bind(wx.EVT_MENU, self.onVocalizerLicenseMenu, item)

		item = self.submenu_vocalizer.Append(
			wx.ID_ANY,
			_("Download More Voices"),
			_("Open the Vocalizer voices download page."),
		)
		sysTrayIcon.Bind(wx.EVT_MENU, self.onVoicesDownload, item)

		item = self.submenu_vocalizer.Append(
			wx.ID_ANY,
			_("About Nuance Vocalizer for NVDA"),
		)
		sysTrayIcon.Bind(wx.EVT_MENU, self.onAbout, item)

		try:
			self.menuItem = sysTrayIcon.preferencesMenu.AppendSubMenu(
				self.submenu_vocalizer,
				_("Vocalizer Automotive"),
			)
		except AttributeError:
			self.menuItem = sysTrayIcon.menu.AppendSubMenu(
				self.submenu_vocalizer,
				_("Vocalizer Automotive"),
			)

	def removeMenu(self):
		if self.menuItem is None:
			return
		try:
			preferencesMenu = gui.mainFrame.sysTrayIcon.preferencesMenu
			preferencesMenu.Remove(self.menuItem)
		except Exception:
			try:
				gui.mainFrame.sysTrayIcon.menu.Remove(self.menuItem)
			except Exception:
				pass
		try:
			self.submenu_vocalizer.Destroy()
		except Exception:
			pass
		self.menuItem = None
		self.submenu_vocalizer = None

	def onLanguageSettings(self, event):
		if not getInstalledVoiceLocaleMap():
			gui.messageBox(
				_("No Automotive voice resources were found."),
				_("Vocalizer Automotive"),
				wx.OK | wx.ICON_INFORMATION,
			)
			return
		gui.mainFrame._popupSettingsDialog(VocalizerLanguageSettingsDialog)

	def onVocalizerLicenseMenu(self, event):
		licensePath = getDefaultLicensePath()
		fd = wx.FileDialog(
			gui.mainFrame,
			message=_("Choose your Vocalizer license file"),
			wildcard=_("License files (*.ini)|*.ini|All files (*.*)|*.*"),
			defaultDir=os.path.dirname(licensePath),
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
		)
		try:
			if fd.ShowModal() != wx.ID_OK:
				return
			sourcePath = fd.GetPath()
		finally:
			fd.Destroy()

		try:
			if os.path.abspath(sourcePath) != os.path.abspath(licensePath):
				shutil.copyfile(sourcePath, licensePath)
			if getLicenseInfo().startswith("licensed:"):
				gui.messageBox(
					_(
						"License entered successfully!\n"
						"Restart NVDA manually for the Automotive host to validate it."
					),
					_("Success!"),
					wx.OK | wx.ICON_INFORMATION,
				)
			else:
				gui.messageBox(
					_("The license file was copied, but its data could not be read."),
					_("Error"),
					wx.OK | wx.ICON_ERROR,
				)
		except Exception as error:
			log.error("Error entering Vocalizer license.", exc_info=True)
			gui.messageBox(
				_("Error copying license data: {error}").format(error=error),
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)
	def onVocalizerLicenseRemoveMenu(self, event):
		if (
			gui.messageBox(
				_("Are you sure you want to remove your Automotive license?"),
				_("Remove License?"),
				wx.YES_NO | wx.ICON_WARNING,
			)
			!= wx.YES
		):
			return
		try:
			os.remove(getDefaultLicensePath())
			gui.messageBox(
				_("License removed. Restart NVDA for the change to take effect."),
				_("Vocalizer Automotive"),
				wx.OK | wx.ICON_INFORMATION,
			)
		except FileNotFoundError:
			pass
		except (OSError, IOError) as error:
			log.error("Error removing Vocalizer license.", exc_info=True)
			gui.messageBox(
				_("Error removing license: {error}").format(error=error),
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)

	def onVoicesDownload(self, event):
		webbrowser.open(VOICE_DOWNLOADS_URL)

	def onAbout(self, event):
		message = _(
			"Nuance Vocalizer for NVDA\n\n"
			"Automotive synthesizer version: 5.5\n"
			"NVDA driver version: {driverVersion}\n\n"
			"{licenseInfo}\n\n"
			"The synthesizer runs in a dedicated 32-bit NVDA host so it can "
			"work with 64-bit NVDA."
		).format(
			driverVersion=_getDriverVersion(),
			licenseInfo=_getLicenseSummary(),
		)
		gui.messageBox(
			message,
			_("About Nuance Vocalizer for NVDA"),
			wx.OK | wx.ICON_INFORMATION,
		)

	def terminate(self):
		# NVDA is tearing down the wx main frame here. Explicitly removing or
		# destroying menus can interrupt shutdown and prevent a restart.
		super(GlobalPlugin, self).terminate()
