import ast
import os
import types
import unittest
from pathlib import Path


SOURCE_PATH = (
	Path(__file__).resolve().parents[1]
	/ "addon"
	/ "synthDrivers"
	/ "vocalizerAutomotive"
	/ "__init__.py"
)
MANIFEST_PATH = SOURCE_PATH.parents[2] / "manifest.ini"


def _load_version_function(addonHandler, sourcePath=SOURCE_PATH):
	tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))
	function = next(
		node
		for node in tree.body
		if isinstance(node, ast.FunctionDef) and node.name == "_getDriverVersion"
	)
	namespace = {
		"__file__": str(sourcePath),
		"addonHandler": addonHandler,
		"os": os,
	}
	exec(compile(ast.Module(body=[function], type_ignores=[]), str(SOURCE_PATH), "exec"), namespace)
	return namespace["_getDriverVersion"]


def _manifest_version():
	for line in MANIFEST_PATH.read_text(encoding="utf-8-sig").splitlines():
		key, separator, value = line.partition("=")
		if separator and key.strip().lower() == "version":
			return value.strip().strip('"\'')
	raise AssertionError("Version not found in manifest.ini")


class DriverVersionTests(unittest.TestCase):
	def test_addon_manifest_api_takes_priority(self):
		addon = types.SimpleNamespace(manifest={"version": "api-version"})
		addonHandler = types.SimpleNamespace(getCodeAddon=lambda: addon)
		self.assertEqual(_load_version_function(addonHandler)(), "api-version")

	def test_installed_manifest_is_used_when_addon_api_is_unavailable(self):
		self.assertEqual(_load_version_function(None)(), _manifest_version())

	def test_unknown_is_used_instead_of_a_hard_coded_historical_version(self):
		missingSource = (
			SOURCE_PATH.parents[3] / "tests" / "missing" / "deeper" / "driver.py"
		)
		self.assertEqual(_load_version_function(None, missingSource)(), "unknown")
		self.assertNotIn("2.1.6-2025.05.12", SOURCE_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
	unittest.main()
