"""Run the legacy 32-bit driver through NVDA's main audio pipeline."""

import subprocess

from rpyc.core.stream import PipeStream

from _bridge.base import Connection
from _bridge.clients.synthDriverHost32 import launcher
from _bridge.clients.synthDriverHost32.synthDriver import SynthDriverProxy32
from _bridge.components.proxies.synthDriver import SynthDriverProxy


def createBrokeredSynthDriver(name, synthDriversPath):
	job = launcher.jobObject.Job()
	job.setBasicLimits(launcher.JOB_OBJECT_LIMIT.KILL_ON_JOB_CLOSE)
	hostProcess = None
	conn = None
	try:
		hostProcess = subprocess.Popen(
			[launcher._hostExe],
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			creationflags=subprocess.CREATE_NO_WINDOW,
		)
		job.assignProcess(hostProcess._handle)
		hostProcess._job = job

		stream = PipeStream(hostProcess.stdout, hostProcess.stdin)
		service = launcher.NVDAService(hostProcess)
		conn = Connection(stream, service, name="synthDriverHost32")
		conn.bgEventLoop(daemon=True)
		conn.remoteService.installProxies(service, brokerAudio=True)
		conn.remoteService.registerSynthDriversPath(synthDriversPath)
		remoteDriver = conn.remoteService.SynthDriver(name)
		return conn, remoteDriver
	except Exception:
		if conn is not None:
			try:
				conn.close()
			except Exception:
				pass
		if hostProcess is not None and hostProcess.poll() is None:
			hostProcess.terminate()
		raise


class BrokeredSynthDriverProxy32(SynthDriverProxy32):
	def __init__(self):
		conn, remoteDriver = createBrokeredSynthDriver(
			self.synthDriver32Name,
			self.synthDriver32Path,
		)
		try:
			SynthDriverProxy.__init__(self, remoteDriver)
			self.holdConnection(conn)
		except Exception:
			conn.close()
			raise
