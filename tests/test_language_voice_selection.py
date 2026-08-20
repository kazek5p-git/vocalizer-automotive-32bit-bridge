import ast
import types
import unittest
from pathlib import Path


SOURCE_PATH = (
	Path(__file__).resolve().parents[1]
	/ "addon"
	/ "synthDrivers"
	/ "vocalizerAutomotive"
	/ "_voiceManager.py"
)


def _load_voice_manager(config):
	tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))
	classNode = next(
		node
		for node in tree.body
		if isinstance(node, ast.ClassDef) and node.name == "VoiceManager"
	)
	namespace = {"_config": config}
	exec(
		compile(ast.Module(body=[classNode], type_ignores=[]), str(SOURCE_PATH), "exec"),
		namespace,
	)
	return namespace["VoiceManager"]


class ConfiguredLanguageVoiceTests(unittest.TestCase):
	def _manager(self, mappings):
		config = types.SimpleNamespace(
			vocalizerConfig={"autoLanguageSwitching": mappings},
		)
		managerClass = _load_voice_manager(config)
		return managerClass.__new__(managerClass)

	def test_regional_language_uses_configured_base_language_voice(self):
		manager = self._manager({"en": {"voice": "Daniel"}})
		self.assertEqual(
			manager._getConfiguredVoiceNameForLanguage("en_US"),
			"Daniel",
		)

	def test_exact_regional_setting_takes_priority_over_base_language(self):
		manager = self._manager(
			{
				"en": {"voice": "Daniel"},
				"en_GB": {"voice": "Serena"},
			}
		)
		self.assertEqual(
			manager._getConfiguredVoiceNameForLanguage("en_GB"),
			"Serena",
		)

	def test_unconfigured_language_returns_none(self):
		manager = self._manager({"en": {"voice": "Daniel"}})
		self.assertIsNone(manager._getConfiguredVoiceNameForLanguage("fr_FR"))


if __name__ == "__main__":
	unittest.main()
