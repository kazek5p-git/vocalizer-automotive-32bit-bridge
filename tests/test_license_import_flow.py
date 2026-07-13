import builtins
import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


SOURCE_PATH = (
	Path(__file__).resolve().parents[1]
	/ "globalPlugins"
	/ "vocalizer_automotive_globalPlugin"
	/ "__init__.py"
)


class LicenseImportFlowTests(unittest.TestCase):
	def _load_plugin(self):
		packageName = "vocalizer_automotive_test_plugin"
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
		previousBuiltinTranslation = getattr(builtins, "_", None)

		def initTranslation():
			builtins._ = lambda text: text

		addonHandler.initTranslation = initTranslation
		addonHandler.getRunningAddons = lambda: []

		configobj = types.ModuleType("configobj")
		configobj.ConfigObj = object

		globalPluginHandler = types.ModuleType("globalPluginHandler")
		globalPluginHandler.GlobalPlugin = BaseGlobalPlugin

		globalVars = types.ModuleType("globalVars")
		globalVars.appArgs = types.SimpleNamespace(secure=False, configPath=None)

		gui = types.ModuleType("gui")
		gui.mainFrame = types.SimpleNamespace()

		languageHandler = types.ModuleType("languageHandler")
		logHandler = types.ModuleType("logHandler")
		logHandler.log = FakeLog()

		wx = types.ModuleType("wx")
		wx.ID_ANY = -1
		wx.ID_OK = 1
		wx.OK = 1
		wx.ICON_ERROR = 2
		wx.ICON_INFORMATION = 4
		wx.FD_OPEN = 8
		wx.FD_FILE_MUST_EXIST = 16

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
		return (
			module,
			wx,
			gui,
			previousModules,
			moduleNames,
			previousBuiltinTranslation,
		)

	def test_license_import_copies_file_without_menu_rebuild(self):
		(
			module,
			wx,
			gui,
			previousModules,
			moduleNames,
			previousBuiltinTranslation,
		) = self._load_plugin()
		try:
			with tempfile.TemporaryDirectory() as tempDir:
				sourcePath = Path(tempDir) / "source.ini"
				targetPath = Path(tempDir) / "vocalizer_license.ini"
				sourcePath.write_text("[info]\nusername = Test\n", encoding="utf-8")
				dialogState = {"destroyed": False}

				class FileDialog:
					def __init__(self, *args, **kwargs):
						return None

					def ShowModal(self):
						return wx.ID_OK

					def GetPath(self):
						return str(sourcePath)

					def Destroy(self):
						dialogState["destroyed"] = True

				wx.FileDialog = FileDialog
				gui.messageBox = mock.Mock()
				wx.CallAfter = mock.Mock(
					side_effect=AssertionError("menu rebuild must not be scheduled")
				)

				plugin = module.GlobalPlugin.__new__(module.GlobalPlugin)
				plugin.createMenu = mock.Mock(
					side_effect=AssertionError("menu rebuild must not run")
				)
				module.getDefaultLicensePath = lambda: str(targetPath)
				module.getLicenseInfo = lambda: f"licensed:{targetPath}"

				plugin.onVocalizerLicenseMenu(object())

				self.assertEqual(targetPath.read_bytes(), sourcePath.read_bytes())
				self.assertTrue(dialogState["destroyed"])
				gui.messageBox.assert_called_once()
				wx.CallAfter.assert_not_called()
				plugin.createMenu.assert_not_called()
		finally:
			for name in moduleNames:
				oldModule = previousModules[name]
				if oldModule is None:
					sys.modules.pop(name, None)
				else:
					sys.modules[name] = oldModule
			if previousBuiltinTranslation is None:
				builtins.__dict__.pop("_", None)
			else:
				builtins._ = previousBuiltinTranslation


if __name__ == "__main__":
	unittest.main()
