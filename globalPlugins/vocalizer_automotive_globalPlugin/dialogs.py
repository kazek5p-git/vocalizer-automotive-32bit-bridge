#vocalizer_globalPlugin/dialogs.py
#A part of the vocalizer driver for NVDA (Non Visual Desktop Access)
#Copyright (C) 2012 Rui Batista <ruiandrebatista@gmail.com>
#Copyright (C) 2012 - 2023 Tiflotecnia, lda. <www.tiflotecnia.net>
#This file is covered by the GNU General Public License.
#See the file GPL.txt for more details.

from collections import OrderedDict
from pathlib import Path
from xml.etree import ElementTree

import addonHandler
import globalVars
import gui
from gui import guiHelper
import languageHandler
import wx

from synthDrivers.vocalizerAutomotive import _config, _languages


addonHandler.initTranslation()


def _getVoiceAddonPaths():
	paths = []
	seen = set()
	try:
		addons = addonHandler.getRunningAddons()
	except Exception:
		addons = []
	for addon in addons:
		name = getattr(addon, "name", "")
		path = getattr(addon, "path", "")
		if not name.startswith("vocalizer-voice") or not path:
			continue
		path = str(Path(path))
		if path not in seen and Path(path).is_dir():
			seen.add(path)
			paths.append(path)

	if paths:
		return paths

	appArgs = getattr(globalVars, "appArgs", None)
	configPath = getattr(appArgs, "configPath", None)
	if not configPath:
		return paths
	addonsPath = Path(configPath) / "addons"
	if not addonsPath.is_dir():
		return paths
	for path in addonsPath.iterdir():
		if path.is_dir() and path.name.startswith("vocalizer-voice"):
			paths.append(str(path))
	return paths


def _languageToLocale(language, tlw):
	locale = _languages.getLocaleNameFromTLW(tlw)
	if locale:
		return locale
	fallbacks = {
		"Polish": "pl_PL",
		"British English": "en_GB",
		"American English": "en_US",
		"Portuguese": "pt_PT",
		"Brazilian Portuguese": "pt_BR",
	}
	return fallbacks.get(language)


def _readVoiceHeader(path):
	try:
		root = ElementTree.parse(path).getroot()
		parameters = root.find("./HEADER/PARAMETERS")
		if parameters is None:
			return None
		voice = (parameters.findtext("voice") or "").strip()
		language = (parameters.findtext("language") or "").strip()
		tlw = (parameters.findtext("langcode") or "").strip()
		locale = _languageToLocale(language, tlw)
		if voice and locale:
			return locale, voice
	except Exception:
		return None
	return None


def getInstalledVoiceLocaleMap():
	voices = {}
	for addonPath in _getVoiceAddonPaths():
		for header in Path(addonPath).rglob("*.hdr"):
			result = _readVoiceHeader(str(header))
			if result is None:
				continue
			locale, voice = result
			voices.setdefault(locale, set()).add(voice)
	return OrderedDict((locale, sorted(names)) for locale, names in sorted(voices.items()))


class VocalizerLanguageSettingsDialog(gui.SettingsDialog):
	title = _("Vocalizer Automatic Language Switching Settings")

	def __init__(self, parent):
		_config.load()
		self._localeToVoices = getInstalledVoiceLocaleMap()
		self._dataToPersist = {}
		self._locales = list(self._localeToVoices)
		super(VocalizerLanguageSettingsDialog, self).__init__(parent)

	def makeSettings(self, sizer):
		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=sizer)

		helpLabel = wx.StaticText(
			self,
			label=_("Select a language, and then configure the voice to be used:"),
		)
		helpLabel.Wrap(self.GetSize()[0])
		settingsSizerHelper.addItem(helpLabel)

		localeNames = [self._getLocaleReadableName(locale) for locale in self._locales]
		self._localesChoice = settingsSizerHelper.addLabeledControl(
			_("Locale Name:"),
			wx.Choice,
			choices=localeNames,
		)
		self.Bind(wx.EVT_CHOICE, self.onLocaleChanged, self._localesChoice)

		self._voicesChoice = settingsSizerHelper.addLabeledControl(
			_("Voice Name:"),
			wx.Choice,
			choices=[],
		)
		self.Bind(wx.EVT_CHOICE, self.onVoiceChange, self._voicesChoice)

		if not self._locales:
			self._localesChoice.Disable()
			self._voicesChoice.Disable()

	def postInit(self):
		if self._locales:
			self._localesChoice.SetSelection(0)
			self._updateVoicesSelection()
			self._localesChoice.SetFocus()

	def _updateVoicesSelection(self):
		localeIndex = self._localesChoice.GetCurrentSelection()
		if localeIndex < 0:
			self._voicesChoice.SetItems([])
			return

		locale = self._locales[localeIndex]
		voices = self._localeToVoices[locale]
		self._voicesChoice.SetItems(voices)
		configured = _config.vocalizerConfig["autoLanguageSwitching"].get(locale, {})
		voice = configured.get("voice")
		if voice in voices:
			self._voicesChoice.SetStringSelection(voice)
		elif voices:
			self._voicesChoice.SetSelection(0)

	def onLocaleChanged(self, event):
		self._updateVoicesSelection()
		event.Skip()

	def onVoiceChange(self, event):
		localeIndex = self._localesChoice.GetCurrentSelection()
		if localeIndex >= 0:
			locale = self._locales[localeIndex]
			self._dataToPersist[locale] = {
				"voice": self._voicesChoice.GetStringSelection() or None,
			}
		event.Skip()

	def onOk(self, event):
		autoSwitching = _config.vocalizerConfig["autoLanguageSwitching"]
		for locale, values in self._dataToPersist.items():
			if values.get("voice"):
				autoSwitching[locale] = values
			elif locale in autoSwitching:
				del autoSwitching[locale]
		_config.save()
		return super(VocalizerLanguageSettingsDialog, self).onOk(event)

	def _getLocaleReadableName(self, locale):
		description = languageHandler.getLanguageDescription(locale)
		return "%s - %s" % (description, locale) if description else locale
