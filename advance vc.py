import pyaudio
import numpy as np
from scipy import signal
import threading
import queue
import time

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

    def pitch_shift(self, audio_data, pitch_factor):
        return signal.resample(audio_data, int(len(audio_data) / pitch_factor))

    def voice_transform(self, audio_data, voice_profile):
        profile = self.voice_profiles[voice_profile]
        pitch_factor = np.random.uniform(profile['pitch_ranges'][0][0], profile['pitch_ranges'][0][1])
        return self.pitch_shift(audio_data, pitch_factor)

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

def interactive_voice_changer():
    print("\nVoice Selection Menu:")
    print("\nFemale Voices:")
    print("1. Sophia   2. Emma    3. Olivia")
    print("4. Isabella 5. Victoria 6. Elena")
    
    print("\nMale Voices:")
    print("7. Ethan    8. Noah    9. Liam")
    print("10. Mason   11. Jacob  12. Oliver")
    
    print("\nSpecial Voices:")
    print("13. Grandpa Henry  14. Tommy  15. Lily")
    print("16. Exit")

    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    input_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    output_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    modulator = VoiceModulator(sample_rate=RATE)
    voice_queue = queue.Queue()

    voice_thread = threading.Thread(
        target=audio_processing_thread, 
        args=(modulator, input_stream, output_stream, voice_queue)
    )
    voice_thread.daemon = True
    voice_thread.start()

    voice_mapping = {
        1: 'sophia', 2: 'emma', 3: 'olivia', 4: 'isabella', 
        5: 'victoria', 6: 'elena',
        7: 'ethan', 8: 'noah', 9: 'liam', 10: 'mason', 
        11: 'jacob', 12: 'oliver',
        13: 'grandpa_henry', 14: 'tommy', 15: 'lily'
    }

    while True:
        try:
            choice = input("\nSelect voice type (1-16): ")
            
            if choice == '16':
                break
            
            voice_choice = int(choice)
            if voice_choice not in voice_mapping:
                print("Invalid choice. Please select 1-16.")
                continue
            
            selected_voice = voice_mapping[voice_choice]
            voice_queue.put(selected_voice)
            print(f"Changed to voice: {selected_voice}")
            
        except ValueError:
            print("Please enter a valid number between 1 and 16.")

    # Cleanup
    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()

if __name__ == "__main__":
    interactive_voice_changer()
