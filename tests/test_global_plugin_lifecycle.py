import ast
import unittest
from pathlib import Path


SOURCE_PATH = (
	Path(__file__).resolve().parents[1]
	/ "globalPlugins"
	/ "vocalizer_automotive_globalPlugin"
	/ "__init__.py"
)


def _load_function(name):
	tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))
	for node in tree.body:
		if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin":
			for child in node.body:
				if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
					if child.name == name:
						return child
	raise AssertionError(f"Function not found: {name}")


def _call_path(node):
	if isinstance(node, ast.Name):
		return node.id
	if isinstance(node, ast.Attribute):
		parent = _call_path(node.value)
		return f"{parent}.{node.attr}" if parent else node.attr
	return None


def _calls(node):
	return {
		path
		for call in ast.walk(node)
		if isinstance(call, ast.Call)
		for path in [_call_path(call.func)]
		if path is not None
	}


class GlobalPluginLifecycleTests(unittest.TestCase):
	def test_license_import_does_not_restart_or_destroy_menu(self):
		calls = _calls(_load_function("onVocalizerLicenseMenu"))
		self.assertNotIn("core.restart", calls)
		self.assertNotIn("self.createMenu", calls)
		self.assertIn("wx.CallAfter", calls)

	def test_license_removal_does_not_rebuild_menu_from_event_handler(self):
		calls = _calls(_load_function("onVocalizerLicenseRemoveMenu"))
		self.assertNotIn("self.createMenu", calls)
		self.assertIn("wx.CallAfter", calls)

	def test_menu_uses_main_nvda_menu_and_does_not_destroy_submenu(self):
		createCalls = _calls(_load_function("createMenu"))
		removeCalls = _calls(_load_function("removeMenu"))
		self.assertIn("self.menu.Insert", createCalls)
		self.assertNotIn("self.removeMenu", createCalls)
		self.assertNotIn("self.submenu_vocalizer.Destroy", createCalls | removeCalls)
		self.assertIn("self.menu.Remove", removeCalls)

	def test_reinitialize_menu_is_blocked_during_termination(self):
		calls = _calls(_load_function("reinitializeMenu"))
		self.assertIn("self.removeMenu", calls)
		self.assertIn("self.createMenu", calls)

	def test_terminate_does_not_destroy_wx_menu_objects(self):
		calls = _calls(_load_function("terminate"))
		self.assertNotIn("self.removeMenu", calls)


if __name__ == "__main__":
	unittest.main()
