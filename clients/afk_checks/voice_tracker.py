import pyaudio
import numpy as np
import time
import datetime
import collections


class VoiceTracker:
    def __init__(self):
        # Audio parameters
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.THRESHOLD = 20  # Adjust dynamically later
        self.SILENCE_LIMIT = 2  # Seconds of silence to reset speaking status
        self.BACKGROUND_NOISE_WINDOW = 30  # Number of samples for noise adaptation

        # State tracking
        self.is_speaking = False
        self.silence_start = None
        self.background_noise_levels = collections.deque(maxlen=self.BACKGROUND_NOISE_WINDOW)

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

    def _calculate_energy(self, data):
        """Calculate audio energy (volume) from the audio chunk"""
        data_np = np.frombuffer(data, dtype=np.int16)
        mean_square = np.mean(np.square(data_np))
        return np.sqrt(max(mean_square, 0))

    def _adapt_threshold(self):
        """Dynamically adjust the threshold based on background noise levels"""
        if self.background_noise_levels:
            avg_noise = np.mean(self.background_noise_levels)
            return max(avg_noise * 2, 10)  # Ensure a minimum threshold
        return self.THRESHOLD  # Default threshold if no data

    def get_speaking_status(self):
        """Returns 0 if speaking, -1 if not speaking"""
        data = self.stream.read(self.CHUNK, exception_on_overflow=False)
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
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
