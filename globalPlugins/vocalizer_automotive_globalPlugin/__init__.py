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
import core
import globalPluginHandler
import globalVars
import gui
import languageHandler
from logHandler import log

addonHandler.initTranslation()

from .dialogs import VocalizerLanguageSettingsDialog, getInstalledVoiceLocaleMap


BRIDGE_SYNTH_NAME = "vocalizerAutomotive32"
URL = "http://vocalizer-nvda.com"
VOICE_DOWNLOADS_URL_TEMPLATE = (
	"http://www.vocalizer-nvda.com/downloads_redirect.php?lang={lang}"
)
CONTRIBUTORS = "NV Access ltd, Ângelo Abrantes, Diogo Costa, Mesar Hameed, Babbage B.V.."

ABOUT_MESSAGE = _("""
 URL: {url}
\x20
This product is composed of two independent components:
- Nuance Vocalizer speech synthesizer.
- NVDA speech driver and interface for Nuance Vocalizer.
Licenses and conditions for these components are as follows:

Nuance Vocalizer speech synthesizer:

Copyright (C) 2011 Nuance Communications, Inc. All rights reserved.

Synthesizer Version: {synthVersion}
This copy of the Nuance Vocalizer synthesizer is licensed to be used exclusively with the NVDA screen reader (Non Visual Desktop Access).

License information:
{licenseInfo}

License management components are property of Tiflotecnia, LDA.
Copyright (C) 2012 Tiflotecnia, LDA. All rights reserved.


NVDA speech driver and interface for Nuance Vocalizer:

Copyright (C) 2012 Tiflotecnia, LDA.
Copyright (C) 2012 Rui Batista.
Copyright (C) 2019 Babbage B.V.

 Version: {driverVersion}
\x20
 NVDA speech driver and interface for Nuance Vocalizer is covered by the GNU General Public License (Version 2). You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it. This applies to both original and modified copies of this software, plus any derivative works.
For further details, you can view the license from the NVDA Help menu.
It can also be viewed online at: http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

This component was developed by Tiflotecnia, LDA and Rui Batista, with contributions from many others. Special thanks goes to:
{contributors}
""")

LICENSE_IMPORT_WARNING = _(
	"Use your own Vocalizer license file. The selected file will be copied "
	"to your NVDA configuration.\n\n"
	"The Automotive engine will check the license after NVDA is restarted. "
	"Due to limitations of communication between 64-bit NVDA and the 32-bit "
	"host, a detailed reason for rejecting the license may not be displayed. "
	"If the engine rejects the license, the synthesizer may simply fail to "
	"load.\n\n"
	"Do you want to continue?"
)


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
		addon = addonHandler.getCodeAddon()
		return addon.manifest["version"]
	except Exception:
		log.debugWarning("Unable to read Automotive driver version.", exc_info=True)
		return _("Unknown")


def _getLicenseSummary():
	licenseInfo = getLicenseInfo()
	if licenseInfo == "none":
		return _("No License.")
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
					"License validity is checked by the 32-bit Automotive host. "
					"Detailed license errors are not available through the current "
					"64/32-bit bridge."
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
		self.menu = None
		self.submenu_vocalizer = None
		self.menuItem = None
		self._terminating = False
		self._noVoicesWarning = None
		if globalVars.appArgs.secure:
			return
		try:
			self.createMenu()
		except Exception:
			log.error("Unable to create Vocalizer Automotive menu.", exc_info=True)
		try:
			if not getInstalledVoiceLocaleMap():
				self._noVoicesWarning = wx.CallLater(
					2000,
					self.onNoVoicesInstalled,
				)
		except Exception:
			log.debugWarning("Unable to check for Automotive voices.", exc_info=True)

	def createMenu(self):
		self.submenu_vocalizer = wx.Menu()
		sysTrayIcon = gui.mainFrame.sysTrayIcon
		self.menu = sysTrayIcon.menu

		item = self.submenu_vocalizer.Append(
			wx.ID_ANY,
			_("Automatic &Language Switching Settings"),
			_("Configure which voice is to be used for each language."),
		)
		sysTrayIcon.Bind(wx.EVT_MENU, self.onLanguageSettings, item)

		licenseInfo = getLicenseInfo()
		if licenseInfo.startswith("licensed:") or licenseInfo == "invalid":
			item = self.submenu_vocalizer.Append(
				wx.ID_ANY,
				_("Remove License"),
				_("Remove your license from this NVDA copy"),
			)
			sysTrayIcon.Bind(wx.EVT_MENU, self.onVocalizerLicenseRemoveMenu, item)
		else:
			item = self.submenu_vocalizer.Append(
				wx.ID_ANY,
				_("Enter License"),
				_("Enter your license data for this computer."),
			)
			sysTrayIcon.Bind(wx.EVT_MENU, self.onVocalizerLicenseMenu, item)

		item = self.submenu_vocalizer.Append(
			wx.ID_ANY,
			_("Download More Voices"),
			_("Open the vocalizer voices download page."),
		)
		sysTrayIcon.Bind(wx.EVT_MENU, self.onVoicesDownload, item)

		item = self.submenu_vocalizer.Append(
			wx.ID_ANY,
			_("About Nuance Vocalizer for NVDA"),
		)
		sysTrayIcon.Bind(wx.EVT_MENU, self.onAbout, item)

		self.menuItem = self.menu.Insert(
			2,
			wx.ID_ANY,
			_("Vocalizer Automotive"),
			self.submenu_vocalizer,
			_("Vocalizer Automotive management options"),
		)

	def removeMenu(self):
		if self.menuItem is None:
			return
		try:
			self.menu.Remove(self.menuItem)
		except Exception:
			log.debugWarning(
				"Unable to remove Vocalizer Automotive menu item.",
				exc_info=True,
			)
		self.menuItem = None
		self.menu = None
		self.submenu_vocalizer = None

	def reinitializeMenu(self):
		if self._terminating:
			return
		try:
			# Follow the current Tiflotecnia menu pattern: remove only the
			# parent item. Destroying the active wx.Menu can terminate NVDA.
			self.removeMenu()
			self.createMenu()
		except Exception:
			log.error("Unable to reinitialize Vocalizer Automotive menu.", exc_info=True)

	def onLanguageSettings(self, event):
		if not getInstalledVoiceLocaleMap():
			gui.messageBox(
				_("No Automotive voice resources were found."),
				_("Vocalizer Automotive"),
				wx.OK | wx.ICON_INFORMATION,
			)
			return
		gui.mainFrame._popupSettingsDialog(VocalizerLanguageSettingsDialog)

	def onNoVoicesInstalled(self):
		self._noVoicesWarning = None
		if self._terminating or getInstalledVoiceLocaleMap():
			return
		if (
			gui.messageBox(
				_(
					"You have no Vocalizer voices installed.\n"
					"You need at least one voice installed to use Vocalizer for NVDA.\n"
					"You can download all Vocalizer voices from the product web page.\n"
					"Would you want to open the vocalizer for NVDA voices download page now?"
				),
				_("No voices installed."),
				wx.YES_NO | wx.ICON_WARNING,
			)
			== wx.YES
		):
			self._openVoicesDownload()

	def onVocalizerLicenseMenu(self, event):
		if (
			gui.messageBox(
				LICENSE_IMPORT_WARNING,
				_("Entering License Data:"),
				wx.YES_NO | wx.ICON_QUESTION,
			)
			!= wx.YES
		):
			return

		licensePath = getDefaultLicensePath()
		fd = wx.FileDialog(
			gui.mainFrame,
			message=_("Choose license file"),
			wildcard=_("Nuance Vocalizer license files") + "|license*.ini",
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
				restart = (
					gui.messageBox(
						_(
							"License entered successfully!\n"
							"For all changes to take effect NVDA must be restarted.\n"
							"Do you want to restart NVDA now?"
						),
						_("Success!"),
						wx.YES_NO,
					)
					== wx.YES
				)
				wx.CallAfter(self.reinitializeMenu)
				if restart:
					core.restart()
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
				_(
					"Are you sure you want to remove your license?\n"
					"This can not be reverted."
				),
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
			wx.CallAfter(self.reinitializeMenu)
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
		self._openVoicesDownload()

	def _openVoicesDownload(self):
		webbrowser.open(
			VOICE_DOWNLOADS_URL_TEMPLATE.format(
				lang=languageHandler.getLanguage()
			)
		)

	def onAbout(self, event):
		message = ABOUT_MESSAGE.format(
			url=URL,
			contributors=CONTRIBUTORS,
			synthVersion="5.5",
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
		self._terminating = True
		if self._noVoicesWarning is not None:
			self._noVoicesWarning.Stop()
			self._noVoicesWarning = None
		super(GlobalPlugin, self).terminate()
