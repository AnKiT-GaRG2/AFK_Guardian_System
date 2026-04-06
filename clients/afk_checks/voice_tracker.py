try:
    import pyaudio
except Exception:
    pyaudio = None

try:
    import sounddevice as sd
except Exception:
    sd = None

try:
    import numpy as np
except ImportError:
    np = None
import subprocess
import shutil
import os
import time
import datetime
import collections


class VoiceTracker:
    def __init__(self):
        self.has_arecord = shutil.which("arecord") is not None
        self.available = np is not None and (pyaudio is not None or sd is not None or self.has_arecord)
        self.mode = "pyaudio" if pyaudio is not None else ("sounddevice" if sd is not None else ("arecord" if self.has_arecord else "none"))

        # Audio parameters
        self.FORMAT = pyaudio.paInt16 if pyaudio is not None else None
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.THRESHOLD = float(os.getenv("VOICE_BASE_THRESHOLD", "8"))
        self.NOISE_MULTIPLIER = float(os.getenv("VOICE_NOISE_MULTIPLIER", "1.35"))
        self.MIN_DYNAMIC_THRESHOLD = float(os.getenv("VOICE_MIN_DYNAMIC_THRESHOLD", "6"))
        self.SILENCE_LIMIT = 2  # Seconds of silence to reset speaking status
        self.BACKGROUND_NOISE_WINDOW = 30  # Number of samples for noise adaptation

        # State tracking
        self.is_speaking = False
        self.silence_start = None
        self.background_noise_levels = collections.deque(maxlen=self.BACKGROUND_NOISE_WINDOW)

        if not self.available:
            self.audio = None
            self.stream = None
            return

        if self.mode == "pyaudio":
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
        else:
            self.audio = None
            self.stream = True

    def _capture_with_arecord(self):
        try:
            result = subprocess.run(
                [
                    "arecord",
                    "-q",
                    "-f",
                    "S16_LE",
                    "-c",
                    "1",
                    "-r",
                    str(self.RATE),
                    "-t",
                    "raw",
                    "--samples",
                    str(self.CHUNK),
                ],
                capture_output=True,
                check=False,
                timeout=2,
            )
            if result.returncode != 0 or not result.stdout:
                return None
            return result.stdout
        except Exception:
            return None

    def _calculate_energy(self, data):
        """Calculate audio energy (volume) from the audio chunk"""
        if np is None:
            return 0
        data_np = np.frombuffer(data, dtype=np.int16)
        mean_square = np.mean(np.square(data_np))
        return np.sqrt(max(mean_square, 0))

    def _adapt_threshold(self):
        """Dynamically adjust the threshold based on background noise levels"""
        if self.background_noise_levels:
            avg_noise = np.mean(self.background_noise_levels)
            return max(avg_noise * self.NOISE_MULTIPLIER, self.MIN_DYNAMIC_THRESHOLD)
        return self.THRESHOLD  # Default threshold if no data

    def get_speaking_status(self):
        """Returns 0 if speaking, -1 if not speaking, None if unavailable"""
        if not self.available or self.stream is None:
            return None

        if self.mode == "pyaudio":
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            energy = self._calculate_energy(data)
        elif self.mode == "sounddevice":
            try:
                recording = sd.rec(self.CHUNK, samplerate=self.RATE, channels=1, dtype='int16', blocking=True)
                energy = float(np.sqrt(np.mean(np.square(recording.astype(np.float32)))))
            except Exception:
                return None
        else:
            data = self._capture_with_arecord()
            if data is None:
                return None
            energy = self._calculate_energy(data)

        # Update background noise level
        self.background_noise_levels.append(energy)
        dynamic_threshold = self._adapt_threshold()

        # Voice detected
        if energy > dynamic_threshold:
            self.is_speaking = True
            self.silence_start = None  # Reset silence timer
            return 0  # Talking
        else:
            # Start silence timer if not already set
            if self.is_speaking and self.silence_start is None:
                self.silence_start = time.time()

            # If silence persists, mark as not speaking
            if self.silence_start and time.time() - self.silence_start > self.SILENCE_LIMIT:
                self.is_speaking = False

            return -1  # Not talking

    def close(self):
        """Closes the audio stream"""
        if self.mode != "pyaudio":
            return

        if self.stream is None or self.audio is None:
            return
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
