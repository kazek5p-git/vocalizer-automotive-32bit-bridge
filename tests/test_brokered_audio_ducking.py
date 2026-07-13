import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BROKERED_PROXY = ROOT / "synthDrivers" / "_automotiveBrokeredProxy32.py"
VOCALIZER = ROOT / "synthDrivers" / "vocalizerAutomotive" / "_vocalizer.py"


def _load_method(path, class_name, method_name):
	tree = ast.parse(path.read_text(encoding="utf-8"))
	for node in ast.walk(tree):
		if isinstance(node, ast.ClassDef) and node.name == class_name:
			for child in node.body:
				if isinstance(child, ast.FunctionDef) and child.name == method_name:
					return child
	raise AssertionError(f"Method not found: {class_name}.{method_name}")


def _call_path(node):
	if isinstance(node, ast.Name):
		return node.id
	if isinstance(node, ast.Attribute):
		parent = _call_path(node.value)
		return f"{parent}.{node.attr}" if parent else node.attr
	return None


class BrokeredAudioDuckingTests(unittest.TestCase):
	def test_brokered_proxy_releases_nvda_suspender(self):
		init = _load_method(
			BROKERED_PROXY,
			"BrokeredSynthDriverProxy32",
			"__init__",
		)
		release = _load_method(
			BROKERED_PROXY,
			"BrokeredSynthDriverProxy32",
			"_releaseAudioDuckingSuspender",
		)
		initCalls = {
			_call_path(call.func)
			for call in ast.walk(init)
			if isinstance(call, ast.Call)
		}
		self.assertIn("self._releaseAudioDuckingSuspender", initCalls)
		self.assertTrue(
			any(
				isinstance(node, ast.Assign)
				and isinstance(node.targets[0], ast.Attribute)
				and node.targets[0].attr == "_audioDuckingSuspender"
				and isinstance(node.value, ast.Constant)
				and node.value.value is None
				for node in ast.walk(release)
			)
		)

	def test_brokered_proxy_uses_nvda_audio_broker(self):
		source = BROKERED_PROXY.read_text(encoding="utf-8")
		self.assertIn("installProxies(service, brokerAudio=True)", source)

	def test_vocalizer_wave_player_keeps_ducking_enabled(self):
		tree = ast.parse(VOCALIZER.read_text(encoding="utf-8"))
		waveCalls = [
			node
			for node in ast.walk(tree)
			if isinstance(node, ast.Call)
			and _call_path(node.func) == "nvwave.WavePlayer"
		]
		self.assertEqual(len(waveCalls), 1)
		wantDucking = [
			keyword
			for keyword in waveCalls[0].keywords
			if keyword.arg == "wantDucking"
		]
		self.assertFalse(
			wantDucking
			and isinstance(wantDucking[0].value, ast.Constant)
			and wantDucking[0].value.value is False
		)


if __name__ == "__main__":
	unittest.main()
