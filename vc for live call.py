import pyaudio
import numpy as np
from scipy import signal

def pitch_shift(audio_data, pitch_factor):
    """
    Shift the pitch of audio data by the given factor
    pitch_factor > 1 increases pitch
    pitch_factor < 1 decreases pitch
    """
    return signal.resample(audio_data, int(len(audio_data) / pitch_factor))

def voice_changer():
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100
    
    p = pyaudio.PyAudio()
    
    # Open input stream (microphone)
    input_stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    
    # Open output stream (speakers)
    output_stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True,
        frames_per_buffer=CHUNK
    )
    
    print("* Voice changer active. Press Ctrl+C to stop.")
    
    try:
        while True:
            # Read audio data
            data = np.frombuffer(input_stream.read(CHUNK), dtype=np.float32)
            
            # Apply voice changing effects
            # Example: Lower pitch by factor of 0.8
            modified_data = pitch_shift(data, 0.8)
            
            # Play modified audio
            output_stream.write(modified_data.tobytes())
            
    except KeyboardInterrupt:
        print("\n* Stopping voice changer...")
    
    finally:
        # Clean up
        input_stream.stop_stream()
        input_stream.close()
        output_stream.stop_stream()
        output_stream.close()
        p.terminate()

if __name__ == "__main__":
    voice_changer()
