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
		wx.YES = 8
		wx.NO = 16
		wx.YES_NO = wx.YES | wx.NO
		wx.Menu = FakeMenu

		package = types.ModuleType(packageName)
		package.__path__ = [str(SOURCE_PATH.parent)]
		sys.modules[packageName] = package
		sys.modules[f"{packageName}.dialogs"] = dialogs
		sys.modules["addonHandler"] = addonHandler
		sys.modules["configobj"] = configobj
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


if __name__ == "__main__":
	unittest.main()
