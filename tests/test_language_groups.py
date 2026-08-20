import ast
import unittest
from collections import OrderedDict
from pathlib import Path


SOURCE_PATH = (
	Path(__file__).resolve().parents[1]
	/ "addon"
	/ "globalPlugins"
	/ "vocalizer_automotive_globalPlugin"
	/ "dialogs.py"
)


def _load_grouping_function():
	tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))
	function = next(
		node
		for node in tree.body
		if isinstance(node, ast.FunctionDef) and node.name == "_addBaseLanguageGroups"
	)
	namespace = {"OrderedDict": OrderedDict}
	exec(
		compile(ast.Module(body=[function], type_ignores=[]), str(SOURCE_PATH), "exec"),
		namespace,
	)
	return namespace["_addBaseLanguageGroups"]


class LanguageGroupTests(unittest.TestCase):
	def setUp(self):
		self.addGroups = _load_grouping_function()

	def test_regional_english_voices_are_available_in_general_english_group(self):
		result = self.addGroups(
			{
				"en_AU": {"Karen"},
				"en_GB": {"Daniel"},
				"en_US": {"Samantha"},
			}
		)
		self.assertEqual(result["en"], ["Daniel", "Karen", "Samantha"])
		self.assertEqual(result["en_AU"], ["Karen"])
		self.assertEqual(result["en_GB"], ["Daniel"])
		self.assertEqual(result["en_US"], ["Samantha"])

	def test_single_voice_regional_language_does_not_get_redundant_base_entry(self):
		result = self.addGroups({"pl_PL": {"Zosia"}})
		self.assertEqual(result, OrderedDict((("pl_PL", ["Zosia"]),)))

	def test_multiple_voices_for_one_region_get_configurable_base_entry(self):
		result = self.addGroups({"cs_CZ": {"Iveta", "Zuzana"}})
		self.assertEqual(result["cs"], ["Iveta", "Zuzana"])
		self.assertEqual(result["cs_CZ"], ["Iveta", "Zuzana"])

	def test_existing_base_entry_is_merged_with_regional_voices(self):
		result = self.addGroups(
			{
				"pt": {"Generic"},
				"pt_BR": {"Luciana"},
				"pt_PT": {"Joana"},
			}
		)
		self.assertEqual(result["pt"], ["Generic", "Joana", "Luciana"])


if __name__ == "__main__":
	unittest.main()
