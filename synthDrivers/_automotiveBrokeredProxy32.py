#Copyright (C) 2026 DJ Graco and Kazek5p.
#This file is covered by the GNU General Public License.
#See the file GPL.txt for more details.
#"""Run the legacy 32-bit driver through NVDA's main audio pipeline.
#This bridge combines two lifecycle fixes:
#* The synth bridge is closed by the standard ``Proxy.__del__`` lifecycle,
  #after ``AudioPanel.onSave`` releases its reference to the previous synth.
#* File-backed Windows RPyC pipe streams close their owning ``FileIO`` objects
  #rather than closing the underlying Windows handles behind those objects.
#"""

import subprocess

import rpyc
from rpyc.core.stream import ClosedFile, PipeStream

from _bridge.base import Connection, Service
from _bridge.clients.synthDriverHost32 import launcher
from _bridge.clients.synthDriverHost32.synthDriver import SynthDriverProxy32
from _bridge.components.proxies.synthDriver import SynthDriverProxy
from _bridge.components.services.nvwave import WavePlayerService
from logHandler import log


class _FileOwningPipeStream(PipeStream):
	"""A Windows PipeStream which owns and closes its FileIO wrappers.

	RPyC's Windows PipeStream keeps FileIO objects alive, but its close method
	closes their raw Windows handles directly.  When the FileIO objects are later
	destroyed, they attempt to close the same handles and raise EBADF.  This
	variant closes the FileIO objects themselves, exactly once.
	"""

	def __init__(self, incoming, outgoing):
		if not hasattr(incoming, "close") or not hasattr(outgoing, "close"):
			raise TypeError("_FileOwningPipeStream requires closeable file objects")
		super().__init__(incoming, outgoing)

	def close(self):
		if self.closed:
			return

		ownedFiles = self._keepalive
		# Mark the stream closed before closing the files.  A concurrent poll
		# will then follow RPyC's normal closed-stream path.
		self.incoming = ClosedFile
		self.outgoing = ClosedFile
		self._keepalive = ()

		firstError = None
		for fileObject in ownedFiles:
			try:
				fileObject.close()
			except Exception as error:
				if firstError is None:
					firstError = error
		if firstError is not None:
			raise firstError


class _BrokeredWavePlayerService(WavePlayerService):
	"""WavePlayer service whose parent-side feeder stream owns its files."""

	def _createDependentConnection(self, localService, name=None):
		if not name:
			name = (
				f"Dependent service '{localService.__class__.__name__}' "
				f"of '{self.__class__.__name__}'"
			)
		log.debug(
			f"Creating file-owning dependent connection: {name} "
			f"on Service {self}, using service {localService} as root"
		)
		if not self._childProcess:
			raise RuntimeError("This service is not associated with a child process.")

		incomingFile = None
		outgoingFile = None
		stream = None
		try:
			# The child-side handles are duplicated into the 32-bit host by the
			# standard NVDA helper.  The parent-side file objects are owned by our
			# stream and will be closed through FileIO.close().
			outgoingFile, childReadHandle = self._createPipe(
				push=True,
				duplicateIntoProcess=True,
			)
			incomingFile, childWriteHandle = self._createPipe(
				push=False,
				duplicateIntoProcess=True,
			)
			stream = _FileOwningPipeStream(incomingFile, outgoingFile)
			conn = Connection(stream, localService, name=name)
			self._dependentConnections.append(conn)
			conn.bgEventLoop(daemon=True)
			return childReadHandle.value, childWriteHandle.value
		except Exception:
			if stream is not None:
				stream.close()
			else:
				for fileObject in (incomingFile, outgoingFile):
					if fileObject is not None:
						fileObject.close()
			raise


@rpyc.service
class _BrokeredNVDAService(launcher.NVDAService):
	"""NVDA service which creates file-owning brokered WavePlayer pipes."""

	@Service.exposed
	def WavePlayer(
		self,
		channels,
		samplesPerSec,
		bitsPerSample,
		outputDevice,
		wantDucking=True,
	):
		return _BrokeredWavePlayerService(
			self._childProcess,
			channels=channels,
			samplesPerSec=samplesPerSec,
			bitsPerSample=bitsPerSample,
			outputDevice=outputDevice,
			wantDucking=wantDucking,
		)


# RPyC resolves a remote call to ``WavePlayer`` through ``exposed_WavePlayer``.
# NVDAService already has that alias, and subclassing it does not replace the
# inherited alias automatically.  Point it explicitly at our wrapped method.
_BrokeredNVDAService.exposed_WavePlayer = _BrokeredNVDAService.WavePlayer


def _stopPartiallyStartedHost(hostProcess, job, assignedToJob):
	"""Stop a host whose bridge initialization did not complete."""
	if hostProcess is None:
		return
	if assignedToJob:
		if getattr(hostProcess, "_job", None) is job:
			hostProcess._job = None
		return
	try:
		hostProcess.terminate()
	except (OSError, ValueError):
		log.debugWarning(
			"Unable to terminate a partially started brokered Automotive host.",
			exc_info=True,
		)


def createBrokeredSynthDriver(name, synthDriversPath):
	job = launcher.jobObject.Job()
	job.setBasicLimits(launcher.JOB_OBJECT_LIMIT.KILL_ON_JOB_CLOSE)
	hostProcess = None
	stream = None
	conn = None
	assignedToJob = False
	try:
		hostProcess = subprocess.Popen(
			[launcher._hostExe],
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			creationflags=subprocess.CREATE_NO_WINDOW,
		)
		job.assignProcess(hostProcess._handle)
		assignedToJob = True
		hostProcess._job = job

		stream = _FileOwningPipeStream(hostProcess.stdout, hostProcess.stdin)
		service = _BrokeredNVDAService(hostProcess)
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
				log.debugWarning(
					"Unable to close a partially initialized brokered Automotive connection.",
					exc_info=True,
				)
		elif stream is not None:
			try:
				stream.close()
			except Exception:
				log.debugWarning(
					"Unable to close a partially initialized brokered Automotive pipe stream.",
					exc_info=True,
				)
		_stopPartiallyStartedHost(hostProcess, job, assignedToJob)
		job = None
		raise


class BrokeredSynthDriverProxy32(SynthDriverProxy32):
	def _releaseAudioDuckingSuspender(self):
		"""Allow NVDA's brokered WavePlayer to manage native audio ducking."""
		suspender = getattr(self, "_audioDuckingSuspender", None)
		if suspender is None:
			return
		self._audioDuckingSuspender = None
		log.debug("Released NVDA audio ducking suspender for brokered Automotive audio.")

	def __init__(self):
		# Proxy.__del__ can run after any exception in initialization.
		self._heldConnections = []
		conn = None
		try:
			conn, remoteDriver = createBrokeredSynthDriver(
				self.synthDriver32Name,
				self.synthDriver32Path,
			)
			SynthDriverProxy.__init__(self, remoteDriver)
			self._releaseAudioDuckingSuspender()
			self.holdConnection(conn)
			log.debug("Brokered Automotive bridge active.")
		except Exception:
			if conn is not None:
				try:
					conn.close()
				except Exception:
					log.debugWarning(
						"Unable to close the brokered Automotive connection after proxy initialization failed.",
						exc_info=True,
					)
			raise
