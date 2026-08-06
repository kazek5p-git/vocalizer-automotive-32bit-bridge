import builtins
import importlib.util
import sys
import types
import unittest
from pathlib import Path


SOURCE_PATH = (
	Path(__file__).resolve().parents[1]
	/ "globalPlugins"
	/ "vocalizer_automotive_globalPlugin"
	/ "__init__.py"
)


class FakeMenu:
	def __init__(self):
		self.items = []
		self.removed = []
		self.destroyed = False

	def Append(self, *args):
		item = ("append", args)
		self.items.append(item)
		return item

	def Insert(self, position, *args):
		item = ("insert", position, args)
		self.items.insert(position, item)
		return item

	def Remove(self, item):
		self.removed.append(item)
		self.items.remove(item)

	def Destroy(self):
		self.destroyed = True


class MenuRuntimeTests(unittest.TestCase):
	def _load_plugin(self):
		packageName = "vocalizer_automotive_menu_test_plugin"
		moduleNames = [
			packageName,
			f"{packageName}.dialogs",
			"addonHandler",
			"configobj",
			"core",
			"globalPluginHandler",
			"globalVars",
			"gui",
			"languageHandler",
			"logHandler",
			"wx",
		]
		previousModules = {name: sys.modules.get(name) for name in moduleNames}
		previousBuiltinTranslation = getattr(builtins, "_", None)

		class BaseGlobalPlugin:
			def terminate(self):
				return None

		class FakeLog:
			def debugWarning(self, *args, **kwargs):
				return None

			def error(self, *args, **kwargs):
				return None

		dialogs = types.ModuleType(f"{packageName}.dialogs")
		dialogs.VocalizerLanguageSettingsDialog = object
		dialogs.getInstalledVoiceLocaleMap = lambda: {}

		addonHandler = types.ModuleType("addonHandler")
		addonHandler.initTranslation = lambda: setattr(builtins, "_", lambda text: text)
		addonHandler.getRunningAddons = lambda: []

		configobj = types.ModuleType("configobj")
		configobj.ConfigObj = object

		core = types.ModuleType("core")
		core.restart = lambda: None

		globalPluginHandler = types.ModuleType("globalPluginHandler")
		globalPluginHandler.GlobalPlugin = BaseGlobalPlugin

		globalVars = types.ModuleType("globalVars")
		globalVars.appArgs = types.SimpleNamespace(secure=False, configPath=None)

		sysTrayIcon = types.SimpleNamespace(menu=FakeMenu(), Bind=lambda *args: None)
		gui = types.ModuleType("gui")
		gui.mainFrame = types.SimpleNamespace(sysTrayIcon=sysTrayIcon)

		languageHandler = types.ModuleType("languageHandler")
		logHandler = types.ModuleType("logHandler")
		logHandler.log = FakeLog()

		wx = types.ModuleType("wx")
		wx.ID_ANY = -1
		wx.EVT_MENU = object()
		wx.OK = 1
		wx.ICON_ERROR = 2
		wx.ICON_INFORMATION = 4
		wx.ICON_WARNING = 32
		wx.YES = 8
		wx.NO = 16
		wx.YES_NO = wx.YES | wx.NO
		wx.Menu = FakeMenu
		wx.callLaterInstances = []

		class FakeCallLater:
			def __init__(self, delay, callback):
				self.delay = delay
				self.callback = callback
				self.stopped = False
				wx.callLaterInstances.append(self)

			def Stop(self):
				self.stopped = True

		wx.CallLater = FakeCallLater

		package = types.ModuleType(packageName)
		package.__path__ = [str(SOURCE_PATH.parent)]
		sys.modules[packageName] = package
		sys.modules[f"{packageName}.dialogs"] = dialogs
		sys.modules["addonHandler"] = addonHandler
		sys.modules["configobj"] = configobj
		sys.modules["core"] = core
		sys.modules["globalPluginHandler"] = globalPluginHandler
		sys.modules["globalVars"] = globalVars
		sys.modules["gui"] = gui
		sys.modules["languageHandler"] = languageHandler
		sys.modules["logHandler"] = logHandler
		sys.modules["wx"] = wx

		spec = importlib.util.spec_from_file_location(
			packageName,
			SOURCE_PATH,
			submodule_search_locations=[str(SOURCE_PATH.parent)],
		)
		module = importlib.util.module_from_spec(spec)
		sys.modules[packageName] = module
		spec.loader.exec_module(module)
		return module, sysTrayIcon, previousModules, moduleNames, previousBuiltinTranslation

	def test_menu_reinitialization_removes_item_without_destroying_menu(self):
		module, sysTrayIcon, previousModules, moduleNames, previousTranslation = (
			self._load_plugin()
		)
		try:
			module.getLicenseInfo = lambda: "none"
			module.getDefaultLicensePath = lambda: "missing-license.ini"
			plugin = module.GlobalPlugin.__new__(module.GlobalPlugin)
			plugin.menu = None
			plugin.submenu_vocalizer = None
			plugin.menuItem = None
			plugin._terminating = False

			plugin.createMenu()
			oldMenu = plugin.submenu_vocalizer
			oldItem = plugin.menuItem
			self.assertEqual(oldItem[2][1], "Vocalizer Automotive")
			plugin.reinitializeMenu()

			self.assertEqual(sysTrayIcon.menu.removed, [oldItem])
			self.assertFalse(oldMenu.destroyed)
			self.assertIsNot(plugin.submenu_vocalizer, oldMenu)
			self.assertIsNotNone(plugin.menuItem)
		finally:
			for name in moduleNames:
				oldModule = previousModules[name]
				if oldModule is None:
					sys.modules.pop(name, None)
				else:
					sys.modules[name] = oldModule
			if previousTranslation is None:
				builtins.__dict__.pop("_", None)
			else:
				builtins._ = previousTranslation

	def test_missing_voices_warning_keeps_menu_and_offers_download(self):
		module, sysTrayIcon, previousModules, moduleNames, previousTranslation = (
			self._load_plugin()
		)
		try:
			module.getLicenseInfo = lambda: "none"
			module.getDefaultLicensePath = lambda: "missing-license.ini"
			messageBoxes = []
			module.gui.messageBox = lambda *args: messageBoxes.append(args) or module.wx.YES
			openedDownloads = []

			plugin = module.GlobalPlugin()
			plugin._openVoicesDownload = lambda: openedDownloads.append(True)

			self.assertIsNotNone(plugin.menuItem)
			self.assertEqual(len(module.wx.callLaterInstances), 1)
			warning = module.wx.callLaterInstances[0]
			self.assertEqual(warning.delay, 2000)
			self.assertIs(plugin._noVoicesWarning, warning)

			warning.callback()

			self.assertIsNone(plugin._noVoicesWarning)
			self.assertEqual(len(messageBoxes), 1)
			self.assertEqual(openedDownloads, [True])
		finally:
			for name in moduleNames:
				oldModule = previousModules[name]
				if oldModule is None:
					sys.modules.pop(name, None)
				else:
					sys.modules[name] = oldModule
			if previousTranslation is None:
				builtins.__dict__.pop("_", None)
			else:
				builtins._ = previousTranslation

	def test_missing_voices_warning_is_cancelled_during_termination(self):
		module, sysTrayIcon, previousModules, moduleNames, previousTranslation = (
			self._load_plugin()
		)
		try:
			module.getLicenseInfo = lambda: "none"
			module.getDefaultLicensePath = lambda: "missing-license.ini"
			plugin = module.GlobalPlugin()
			warning = plugin._noVoicesWarning

			plugin.terminate()

			self.assertTrue(plugin._terminating)
			self.assertTrue(warning.stopped)
			self.assertIsNone(plugin._noVoicesWarning)
		finally:
			for name in moduleNames:
				oldModule = previousModules[name]
				if oldModule is None:
					sys.modules.pop(name, None)
				else:
					sys.modules[name] = oldModule
			if previousTranslation is None:
				builtins.__dict__.pop("_", None)
			else:
				builtins._ = previousTranslation


if __name__ == "__main__":
	unittest.main()
