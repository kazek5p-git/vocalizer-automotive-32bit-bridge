#A 64-bit NVDA proxy for the original 32-bit Vocalizer Automotive driver.
#Copyright (C) 2026 DJ Graco and Kazek5p.
#This file is covered by the GNU General Public License.
#See the file GPL.txt for more details.

import os

import globalVars

from ._automotiveBrokeredProxy32 import BrokeredSynthDriverProxy32


class SynthDriver(BrokeredSynthDriverProxy32):
	name = "vocalizerAutomotive32"
	description = "Nuance Vocalizer 5.5"
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
