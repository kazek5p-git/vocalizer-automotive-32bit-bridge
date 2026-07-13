#vocalizer/_config.py
#A part of the vocalizer driver for NVDA (Non Visual Desktop Access)
#Copyright (C) 2012 Rui Batista <ruiandrebatista@gmail.com>
#Copyright (C) 2012 - 2023 Tiflotecnia, lda. <www.tiflotecnia.net>
#This file is covered by the GNU General Public License.
#See the file GPL.txt for more details.

# Import the necessary modules
from io import StringIO
import os.path
try:
	import configobj
	from configobj.validate import Validator
except ImportError:
	# The NVDA 32-bit synth host does not include configobj.
	configobj = None
	Validator = None
import globalVars
from logHandler import log

VOCALIZER_CONFIG_FILENAME = "vocalizer.ini"

vocalizerConfig = None

_configSpec = """
demo_expired_reported_time = float(default=0)
demo_license_reported_time = float(default=0)
[voices]
[[__many__]]
variant = string(default=None)

[autoLanguageSwitching]
[[__many__]]
voice = string(default=None)
"""

def _getConfigPath():
	appArgs = getattr(globalVars, "appArgs", None)
	configPath = getattr(appArgs, "configPath", None)
	if configPath and os.path.isabs(configPath):
		return configPath
	return os.path.join(os.environ.get("APPDATA", ""), "nvda")

def _newFallbackConfig():
	return {
		"demo_expired_reported_time": 0.0,
		"demo_license_reported_time": 0.0,
		"voices": {},
		"autoLanguageSwitching": {},
	}

def _parseFallbackValue(value):
	value = value.strip()
	if value.startswith('"') and value.endswith('"'):
		return value[1:-1]
	try:
		return float(value)
	except ValueError:
		return value

def _loadFallback(path):
	config = _newFallbackConfig()
	if not os.path.isfile(path):
		return config
	section = None
	subsection = None
	try:
		with open(path, "r", encoding="utf-8") as f:
			for rawLine in f:
				line = rawLine.strip()
				if not line or line.startswith("#"):
					continue
				if line.startswith("[[") and line.endswith("]]"):
					subsection = line[2:-2].strip()
					if section in ("voices", "autoLanguageSwitching"):
						config[section].setdefault(subsection, {})
					continue
				if line.startswith("[") and line.endswith("]"):
					section = line[1:-1].strip()
					subsection = None
					config.setdefault(section, {})
					continue
				if "=" not in line:
					continue
				key, value = line.split("=", 1)
				value = _parseFallbackValue(value)
				if section in ("voices", "autoLanguageSwitching") and subsection:
					config[section][subsection][key.strip()] = value
				elif section is None:
					config[key.strip()] = value
	except Exception:
		log.debugWarning("Unable to read Vocalizer configuration.", exc_info=True)
	return config

def _saveFallback(path):
	lines = [
		"demo_expired_reported_time = %s" % vocalizerConfig["demo_expired_reported_time"],
		"demo_license_reported_time = %s" % vocalizerConfig["demo_license_reported_time"],
	]
	for section in ("voices", "autoLanguageSwitching"):
		lines.append("[%s]" % section)
		for name, values in vocalizerConfig.get(section, {}).items():
			lines.append("[[%s]]" % name)
			for key, value in values.items():
				lines.append("%s = %s" % (key, value))
	os.makedirs(_getConfigPath(), exist_ok=True)
	with open(path, "w", encoding="utf-8", newline="") as f:
		f.write("\r\n".join(lines) + "\r\n")

def load():
	global vocalizerConfig
	if not vocalizerConfig:
		path = os.path.join(_getConfigPath(), VOCALIZER_CONFIG_FILENAME)
		if configobj is None:
			vocalizerConfig = _loadFallback(path)
			return
		vocalizerConfig = configobj.ConfigObj(path, configspec=StringIO(_configSpec), encoding="utf-8")
		vocalizerConfig.newlines = "\r\n"
		vocalizerConfig.stringify = True
		val = Validator()
		ret = vocalizerConfig.validate(val, preserve_errors=True, copy=True)
		if ret != True:
			log.warning("Vocalizer configuration is invalid: %s", ret)

def save():
	global vocalizerConfig
	if not vocalizerConfig:
		raise RuntimeError("Vocalizer config is not loaded.")
	if configobj is None:
		_saveFallback(os.path.join(_getConfigPath(), VOCALIZER_CONFIG_FILENAME))
		return
	val = Validator()
	vocalizerConfig.validate(val, copy=True)
	vocalizerConfig.write()
