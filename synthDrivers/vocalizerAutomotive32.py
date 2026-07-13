# A 64-bit NVDA proxy for the original 32-bit Vocalizer Automotive driver.

import os

import globalVars
from _bridge.clients.synthDriverHost32.synthDriver import SynthDriverProxy32


class SynthDriver(SynthDriverProxy32):
	name = "vocalizerAutomotive32"
	description = "Nuance Vocalizer 5.5 Automotive (32-bit bridge)"
	synthDriver32Path = os.path.join(
		globalVars.appArgs.configPath,
		"addons",
		"vocalizer_automotive_driver",
		"synthDrivers",
	)
	synthDriver32Name = "vocalizerAutomotive"

	@classmethod
	def check(cls):
		if not os.path.isdir(cls.synthDriver32Path):
			return False
		return super().check()
