import pyaudio
import numpy as np
from scipy import signal
import threading
import queue

class VoiceModulator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.voice_profiles = {
            'sophia': {'pitch_ranges': [(1.2, 1.4)], 'formant_shifts': [(1.2, 1.3)]},
            'emma': {'pitch_ranges': [(1.3, 1.5)], 'formant_shifts': [(1.3, 1.4)]},
            'olivia': {'pitch_ranges': [(1.4, 1.6)], 'formant_shifts': [(1.4, 1.5)]},
            'isabella': {'pitch_ranges': [(1.5, 1.7)], 'formant_shifts': [(1.5, 1.6)]},
            'victoria': {'pitch_ranges': [(1.6, 1.8)], 'formant_shifts': [(1.6, 1.7)]},
            'elena': {'pitch_ranges': [(1.7, 1.9)], 'formant_shifts': [(1.7, 1.8)]},
            'ethan': {'pitch_ranges': [(0.6, 0.8)], 'formant_shifts': [(0.7, 0.9)]},
            'noah': {'pitch_ranges': [(0.7, 0.9)], 'formant_shifts': [(0.8, 1.0)]},
            'liam': {'pitch_ranges': [(0.5, 0.7)], 'formant_shifts': [(0.6, 0.8)]},
            'mason': {'pitch_ranges': [(0.8, 1.0)], 'formant_shifts': [(0.9, 1.1)]},
            'jacob': {'pitch_ranges': [(0.4, 0.6)], 'formant_shifts': [(0.5, 0.7)]},
            'oliver': {'pitch_ranges': [(0.9, 1.1)], 'formant_shifts': [(1.0, 1.2)]},
            'grandpa_henry': {'pitch_ranges': [(0.4, 0.6)], 'formant_shifts': [(0.5, 0.7)]},
            'tommy': {'pitch_ranges': [(0.9, 1.1)], 'formant_shifts': [(0.8, 1.0)]},
            'lily': {'pitch_ranges': [(1.6, 1.8)], 'formant_shifts': [(1.5, 1.7)]}
        }

    def apply_noise_reduction(self, audio_data):
        # Advanced noise reduction using spectral gating
        spectrogram = np.abs(signal.stft(audio_data)[2])
        noise_threshold = np.mean(spectrogram, axis=1) * 0.5
        
        # Soft thresholding to preserve voice characteristics
        mask = spectrogram > noise_threshold[:, np.newaxis]
        cleaned_spectrogram = spectrogram * mask
        
        # Reconstruct audio
        _, cleaned_audio = signal.istft(cleaned_spectrogram)
        return cleaned_audio

    def formant_preserving_pitch_shift(self, audio_data, pitch_factor, formant_factor):
        # Advanced pitch and formant manipulation
        # Resample for pitch shift
        pitch_shifted = signal.resample(audio_data, int(len(audio_data) / pitch_factor))
        
        # Formant shift using resampling
        formant_shifted = signal.resample(pitch_shifted, int(len(pitch_shifted) / formant_factor))
        
        # Apply window to reduce artifacts
        window = signal.hann(len(formant_shifted))
        return formant_shifted * window

    def voice_transform(self, audio_data, voice_profile):
        profile = self.voice_profiles[voice_profile]
        
        # Random pitch and formant factors
        pitch_factor = np.random.uniform(profile['pitch_ranges'][0][0], profile['pitch_ranges'][0][1])
        formant_factor = np.random.uniform(profile['formant_shifts'][0][0], profile['formant_shifts'][0][1])
        
        # Noise reduction
        noise_reduced = self.apply_noise_reduction(audio_data)
        
        # Pitch and formant transformation
        transformed = self.formant_preserving_pitch_shift(noise_reduced, pitch_factor, formant_factor)
        
        return transformed

# The rest of the script remains the same as in the original code
def audio_processing_thread(modulator, input_stream, output_stream, voice_queue):
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32

    current_voice = 'sophia'  # Default voice
    voice_queue.put(current_voice)

    try:
        while True:
            if not voice_queue.empty():
                current_voice = voice_queue.get()
            
            data = np.frombuffer(input_stream.read(CHUNK), dtype=np.float32)
            modified_data = modulator.voice_transform(data, current_voice)
            output_stream.write(modified_data.tobytes())
    except Exception as e:
        print(f"Audio processing error: {e}")
